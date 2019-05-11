from datetime import datetime
from uuid import uuid4
import json
import hashlib
from Transaction import Transaction

from Block import Block

class Blockchain:

    def __init__(self):
        self.chain = []
        self.pendingTransaction = []
        self.networkNodes = []
        self.createBlock(1, '0', '0')

    def createBlock(self, nonce , prevHash, blockHash):
        block = Block(nonce, prevHash, blockHash, len(self.chain)+1, self.pendingTransaction)
        self.pendingTransaction = []

        self.chain.append(block)

        return block

    def getLastBlock(self):
        return self.chain[-1]

    def createNewTransaction(self, amount, from_address, to_address):
        newTransaction= Transaction(from_address, to_address, amount)
        return newTransaction

    def addToPendingTransaction(self, transaction):
        if(not transaction.is_valid()):
            raise Exception('Inavlid Transaction')
        self.pendingTransaction.append(transaction)
        return self.getLastBlock().index + 1

    def hashBlock(self, blockData, nonce ):
        blockData['nonce'] = nonce
        encoded_block = json.dumps(blockData, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def proofOfWork(self, blockData ):
        nonce = 0
        hash =  self.hashBlock(blockData, nonce)
        while hash[:4]!='0000':
            nonce+=1
            hash =  self.hashBlock(blockData, nonce)

        return nonce
    
    def isChainValid(self, blockchain):
        for i in range(1, len(blockchain)):
            currentBlock = blockchain[i]
            prevBlock = blockchain[i-1]
            if(not self.has_valid_transaction(currentBlock)):
                return False
            blockData = {
                'transactions' : currentBlock.transaction,
                'index'        : prevBlock.index + 1
                }
            blockHash = self.hashBlock(blockData, currentBlock.nonce)
            if(blockHash[:4] != '0000'):
                return False
            if (currentBlock.previousBlockHash!= prevBlock.hash):
                return False
        return True

    def has_valid_transaction(self, block):
        if(block.isBlockValid()):
            return True
        else :
            return False

    def addNode(self, address):
        self.networkNodes.append(address)
    
    def serialize_chain(self):
        display  = []
        for block in self.chain:
            display.append(block.serialize())

        return display
            
