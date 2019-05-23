import json
import jsonpickle
import hashlib
from FileUtil import FileUtil
from Block import Block


class Blockchain:

    def __init__(self, PORT):
        self.chain = []
        self.pendingTransaction = []
        self.networkNodes = []
        self.file = FileUtil('json/' + str(PORT) + '.json')
        self.file.store_genesis_block(Block(1, '0000x', '0000x', 1, []))

    def create_block(self, nonce, prev_hash, block_hash):
        block = Block(nonce, prev_hash, block_hash, len(self.chain) + 1, self.pendingTransaction)
        if block.is_block_valid():
            self.chain.append(block)
            self.pendingTransaction = []
            return block
        return False

    def get_last_block(self):
        return self.chain[-1]

    def receive_block(self, other):
        if type(other) == str:
            other = jsonpickle.decode(other)

        last_block = self.get_last_block()
        print(other)
        if last_block == other:
            return False

        block_data = {
            'transactions': jsonpickle.encode(other.transaction),
            'index': last_block.index + 1
        }
        block_hash = self.hash_block(block_data, other.nonce)
        if block_hash != other.hash:
            return False

        if other.is_block_valid():
            if last_block.index + 1 == other.index:
                if last_block.hash == other.previousBlockHash:
                    self.chain.append(other)
                    self.pendingTransaction = []
                    self.store_block(other)
                    return True
        return False

    def store_block(self, block):
        self.file.write(block)

    def read_chain(self):
        self.chain = self.file.read()

    def replace(self, best_chain):
        self.file.replace(best_chain)

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
