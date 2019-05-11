from datetime import datetime



class Block:
    def __init__(self,  nonce , prevHash, blockHash, index, pendingTx):
        self.nonce = nonce
        self.previousBlockHash = prevHash
        self.hash = blockHash
        self.index = index
        self.timestamp = str(datetime.now())
        self.transaction = pendingTx
    
    def isBlockValid(self):
        for tx in self.transaction :
            if(not tx.is_valid()): 
                return False
        return True
    
    def serialize(self):
        return {
            'index'             : self.index,
            'timestamp'         : self.timestamp,
            'transactions'      : [e.serialize() for e in self.transaction],
            'nonce'             : self.nonce,
            'hash'              : self.hash,
            'previousBlockHash' : self.previousBlockHash
        }