from datetime import datetime


class Block:
    def __init__(self, nonce, prev_hash, block_hash, index, pending_tx):
        self.nonce = nonce
        self.previousBlockHash = prev_hash
        self.hash = block_hash
        self.index = index
        self.timestamp = str(datetime.now())
        self.transaction = pending_tx

    def is_block_valid(self):
        for tx in self.transaction:
            if not tx.is_valid():
                return False
        return True

    def serialize(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [e.serialize() for e in self.transaction],
            'nonce': self.nonce,
            'hash': self.hash,
            'previousBlockHash': self.previousBlockHash
        }
