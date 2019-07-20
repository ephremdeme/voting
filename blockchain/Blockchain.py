import json
import jsonpickle
import hashlib

from util.DBUtil import DBUtil
from blockchain.Block import Block


class Blockchain:

    def __init__(self, PORT):
        self.chain = []
        self.pendingTransaction = []
        self.db = DBUtil('db/' + str(PORT))
        self.networkNodes = self.db.get_network_node()
        self.db.store_genesis_block(Block(1, ' ', '00000', 1, []))

    def create_block(self, nonce, prev_hash, block_hash):
        block = Block(nonce, prev_hash, block_hash, self.count() + 1, self.pendingTransaction)
        print(self.count(), "count")
        if block.is_block_valid():
            self.chain.append(block)
            self.pendingTransaction = []
            return block
        return False

    def get_last_block(self):
        return self.chain[-1]

    def get_all_block(self):
        return self.db.get_all_block()

    def find_block_by_hash(self, block_hash):
        return self.db.get_block_index(block_hash)

    def find_block_by_index(self, index):
        return self.db.getblock(index)

    def receive_block(self, other):
        last_block = self.get_last_block()

        if last_block.__eq__(other):
            return False

        block_data = {
            'transactions': jsonpickle.encode(other.transaction),
            'index': last_block.index + 1
        }
        if block_data['transactions'] is None:
            return False
        block_hash = self.hash_block(block_data, other.nonce)
        if block_hash != other.hash:
            return False
        if other.is_block_valid():
            if last_block.index + 1 == other.index:
                if last_block.hash == other.previousBlockHash:
                    self.chain.pop(0)
                    self.chain.append(other)
                    self.pendingTransaction = []
                    self.store_block(other)
                    return True
        return False

    def store_block(self, block):
        self.chain.pop(0)
        self.db.store_block(block.index, block)

    def read_chain(self):
        chain = self.db.get_block_range(self.count() - 10, self.count() + 1)
        if self.range_blockchain_check():
            self.chain = chain

    def range_blockchain_check(self):
        i = 10
        count = self.count()
        valid = True
        for i in range(i, count, 10):
            chain = self.db.get_block_range(i - 10, i)
            valid = valid and self.is_chain_valid(chain)
            if not valid: return False
        if i < count:
            chain = self.db.get_block_range(i, count)
            valid = valid and self.is_chain_valid(chain)
            if not valid: return False
        return True

    def replace(self, best_chain):
        self.db.replace_chain(best_chain)

    def add_to_pending_transaction(self, transaction):
        if not transaction.is_valid():
            return False
        if self.transaction_exist(transaction.id):
            return False
        self.pendingTransaction.append(transaction)
        return True

    @staticmethod
    def hash_block(block_data, nonce):
        block_data['nonce'] = nonce
        encoded_block = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, block_data):
        nonce = 0
        block_hash = self.hash_block(block_data, nonce)
        while block_hash[:4] != '0000':
            nonce += 1
            block_hash = self.hash_block(block_data, nonce)

        return nonce

    def is_chain_valid(self, blockchain):
        for i in range(1, len(blockchain)):
            current_block = blockchain[i]
            prev_block = blockchain[i - 1]
            if not self.has_valid_transaction(current_block):
                return False

            block_data = {
                'transactions': jsonpickle.encode(current_block.transaction),
                'index': prev_block.index + 1
            }
            block_hash = self.hash_block(block_data, current_block.nonce)
            if block_hash[:4] != '0000':
                return False
            correct_hash = current_block.previousBlockHash == prev_block.hash
            correct_index = current_block.index == prev_block.index + 1
            if not (correct_hash and correct_index):
                return False
        return True

    def add_node(self, address):
        self.networkNodes.append(address)
        self.db.store_network_node(self.networkNodes)

    def serialize_chain(self):
        if len(self.chain) == 0:
            return
        display = []
        for block in self.chain:
            display.append(block.serialize())
        return display

    @staticmethod
    def calculate_vote(chain):
        vote = 0
        for block in chain:
            for tx in block.transaction:
                if tx.to_address == '00f23132c7bc626122a6878bbb0b916e5a2bbc26':
                    vote += 1
        return vote

    def count(self):
        return self.db.count()

    @staticmethod
    def has_valid_transaction(block):
        if block.is_block_valid():
            return True
        else:
            return False

    def transaction_exist(self, tx_id):
        for tx in self.pendingTransaction:
            if tx.id == tx_id:
                return True

        for block in self.chain:
            for tx in block.transaction:
                if tx.id == tx_id:
                    return True

        return False

    def find_vote_by_id(self, tx_id):
        for tx in self.pendingTransaction:
            if tx.id == tx_id:
                return tx.serialize(), None
        i = 10
        count = self.count()
        for i in range(i, count, 10):
            chain = self.db.get_block_range(i - 10, i)
            if self.get_transaction(chain, tx_id, "ID"):
                return self.get_transaction(chain, tx_id, "ID")

        if i < count:
            chain = self.db.get_block_range(i, count)
            if self.get_transaction(chain, tx_id, "ID"):
                return self.get_transaction(chain, tx_id, "ID")
        return str(tx_id) + "not found"

    def find_candidate_vote(self, cand):
        vote_list = []
        i = 10
        count = self.count() + 1
        for i in range(i, count, 10):
            chain = self.db.get_block_range(i - 10, i)
            vote_list.extend(self.collect_vote(chain, to_address=cand))

        if i < count:
            chain = self.db.get_block_range(i, count)
            vote_list.extend(self.collect_vote(chain, to_address=cand))
        return vote_list

    def vote_result(self, sec_hash):
        candidates = self.db.get_sec_candidate(sec_hash)
        result = []
        total = 0
        for (key, cand) in candidates:
            c = len(self.find_candidate_vote(key))
            result.append((cand, c))
            total += c
        return result, total

    @staticmethod
    def collect_vote(chain, to_address):
        vote = []
        for block in chain:
            for tx in block.transaction:
                if tx.to_address == to_address:
                    vote.append(tx.serialize())
        return vote

    @staticmethod
    def get_transaction(chain, tx_id, by):
        for block in chain:
            for tx in block.transaction:
                if by == "ID":
                    if tx.id == tx_id:
                        return tx, block
                else:
                    if tx.to_address == tx_id:
                        return tx, block
        return False
