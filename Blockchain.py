from datetime import datetime
from uuid import uuid4
import json
import jsonpickle
import hashlib
from Transaction import Transaction
from FileUtil import FileUtil
from Block import Block

class Blockchain:

    def __init__(self, PORT):
        self.chain = []
        self.pendingTransaction = []
        self.networkNodes = []
        self.file = FileUtil('json/' +str(PORT) +'.json')
        self.file.storeGenesisBlock(self.createBlock(1, '0', '0'))

    def createBlock(self, nonce , prevHash, blockHash):
        block = Block(nonce, prevHash, blockHash, len(self.chain)+1, self.pendingTransaction)
        self.pendingTransaction = []

        self.chain.append(block)

        return block

    def getLastBlock(self):
        return self.chain[-1]
    
    def storeBlock(self, block):
        self.file.write(block)
    
    def readChain(self):
        self.chain = self.file.read()

    def replace(self, bestChain):
        self.file.replace(bestChain)

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
                'transactions' : jsonpickle.encode(currentBlock.transaction),
                'index'        : prevBlock.index + 1
                }
            blockHash = self.hashBlock(blockData, currentBlock.nonce)
            if(blockHash[:4] != '0000'):
                return False
            correctHash = currentBlock.previousBlockHash == prevBlock.hash
            correctIndex = currentBlock.index == prevBlock.index+1
            if (not(correctHash and correctIndex)):
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
            
