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
        if self.hash[:4] == '0000':
            return True
        return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.nonce == other.nonce:
                if self.previousBlockHash == other.previousBlockHash:
                    if self.hash == other.hash:
                        if self.timestamp == other.timestamp:
                            if self.index == other.index:
                                return True
        return False

    def __ne__(self, other):
        return self.hash != other.hash \
               and self.previousBlockHash != other.previousBlockHash \
               and not isinstance(other, self.__class__)

    def serialize(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [e.serialize() for e in self.transaction],
            'nonce': self.nonce,
            'hash': self.hash,
            'previousBlockHash': self.previousBlockHash
        }
