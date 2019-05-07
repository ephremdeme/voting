from datetime import datetime
from uuid import uuid4
import json
from urlparse import urlparse
import hashlib

class Blockchain:

    def __init__(self):
        self.chain = []
        self.pendingTransaction = []
        self.networkNodes = []
        self.createBlock(1, '0', '0')

    def createBlock(self, nonce , prevHash, blockHash):
        block = {
            'index'             : len(self.chain) + 1,
            'timestamp'         : str(datetime.now()),
            'transactions'      : self.pendingTransaction,
            'nonce'             : nonce,
            'hash'              : blockHash,
            'previousBlockHash' : prevHash
        }

        self.pendingTransaction = []

        self.chain.append(block)

        return block

    def getLastBlock(self):
        return self.chain[-1]

    def createNewTransaction(self, amount, sender, receiver):
        newTransaction={
            'transactionID' : str(uuid4()).replace('-', ''),
            'sender'   : sender,
            'receiver' : receiver,
            'amount'   : amount
        }
        return newTransaction

    def addToPendingTransaction(self, transaction):
        self.pendingTransaction.append(transaction)
        print 11
        return self.getLastBlock()['index'] + 1

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
            blockData = {
                'transactions' : currentBlock['transactions'],
                'index'        : prevBlock['index'] + 1
                }
            blockHash = self.hashBlock(blockData, currentBlock['nonce'])
            if(blockHash[:4] != '0000'):
                print blockHash 
                print currentBlock['hash']
                return False
            if (currentBlock['previousBlockHash']!= prevBlock['hash']):
                return False
        return True

    def addNode(self, address):
        self.networkNodes.append(address)

    
# blockchain = Blockchain()
# block = blockchain.createBlock(12, '0', '0')
# test = {
#     'index' : len(blockchain.chain) +1,
#     'timestamp' : str(datetime.now()),
#     'transaction' : blockchain.pendingTransaction
# }
# nonce=blockchain.proofOfWork(test)
# prevHash= blockchain.getLastBlock()['previousBlockHash']
# blockhash = blockchain.hashBlock(test, nonce)
# block = blockchain.createBlock(nonce, prevHash, blockhash)
# print block
# test = {
#     'index' : len(blockchain.chain) +1,
#     'timestamp' : str(datetime.now()),
#     'transaction' : blockchain.pendingTransaction
# }
# nonce=blockchain.proofOfWork(test)
# prevHash= blockchain.getLastBlock()['hash']
# blockhash = blockchain.hashBlock(test, nonce)
# block = blockchain.createBlock(nonce, prevHash, blockhash)
# print block
# print blockchain.chain