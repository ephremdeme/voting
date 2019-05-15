from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from Blockchain import Blockchain
from sys import argv
from logging import log
from fastecdsa import keys, curve
import jsonpickle
from wallet import Wallet

private_key = keys.gen_private_key(curve.P256)
public_key = keys.get_public_key(private_key, curve.P256)


# Creating a Web App
app = Flask(__name__)
PORT = argv[1]
# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

currentNodeURl = "http://localhost:" + str(PORT)
# Creating a Blockchain
blockchain = Blockchain(PORT)
blockchain.readChain()
wallet = Wallet()
minnerWallet = Wallet()
@app.route("/", methods = ['GET'])
def home():
    return jsonify({'chain' : blockchain.serialize_chain(), 
    'pendingTransaction':  [e.serialize() for e in blockchain.pendingTransaction],
    'networkNode' : blockchain.networkNodes})
    # return jsonify({'chain':blockchain.chain, 'networkNodes' : blockchain.networkNodes, 'pendingtransaction' : blockchain.pendingTransaction}), 200

@app.route('/get-blockchain', methods = ['GET'])
def test():
    return jsonify(
        {
            'chain' : jsonpickle.encode(blockchain.chain), 
            'pendingTransaction':  jsonpickle.encode(blockchain.pendingTransaction)
        })

@app.route('/transaction', methods = ['POST'])
def addTransaction():
    json = request.get_json()
    try:
        json = jsonpickle.decode(json)
        index = blockchain.addToPendingTransaction(json)
        
    except Exception:
        response = {'message': 'This transaction is invalid will not be added to Block '}
        return response, 200

    
    response = {'message': 'This transaction will be added to Block '+str(index)}
    return jsonify(response), 201

@app.route('/transaction/broadcast', methods = ['POST'] )
def transactionBroadcast():
    json = request.get_json()
    transaction = wallet.createTransaction( json['receiver'], json['amount'])
    try:
        blockchain.addToPendingTransaction(transaction)
    except Exception:
        response = {'message': 'This transaction is invalid will not be added to Block '}
        return jsonify(response), 500
    
    if(len(blockchain.networkNodes)==0):
        return 'empty'
    transaction = jsonpickle.encode(transaction)
    for node in blockchain.networkNodes:
        requests.post(node + '/transaction', json = transaction, timeout=2 )
    
    return jsonify({'note': 'Transaction created and broadcast successfully.', 
    'pendingTransaction': [e.serialize() for e in blockchain.pendingTransaction]})

@app.route('/mine', methods = ['GET'])
def mine():
    lastBlock = blockchain.getLastBlock()
    blockData = {
        'transactions' : jsonpickle.encode(blockchain.pendingTransaction),
        'index'        : lastBlock.index+1
        }
    
    # finding nonce for the block
    nonce = blockchain.proofOfWork(blockData)
    # generating hash for the block and mining
    blockHash = blockchain.hashBlock(blockData, nonce)
    block = blockchain.createBlock(nonce, lastBlock.hash, blockHash )
    blockchain.storeBlock(block)
    block = jsonpickle.encode(block)
    

    for node in blockchain.networkNodes:
        log(1, "the block is transmitted to" + str(node))
        requests.post(node + '/receive-new-block', json={'newBlock' : block})
    

    log(1, "minning fee is being transmitted")
    transaction = {
	    "sender" : None,
	    "receiver" : minnerWallet.address, 
	    "amount" : 12.5
    }
    transaction = wallet.createTransaction( transaction['receiver'], transaction['amount'])
    
    blockchain.addToPendingTransaction(transaction)
    transaction = jsonpickle.encode(transaction)

    for node in blockchain.networkNodes:
        requests.post( node + '/transaction', json=transaction)

    
    # r=requests.post( currentNodeURl + '/transaction/broadcast', json=transaction)
    block = jsonpickle.decode(block)
    response = {'message': 'Congratulations, you just mined a block!',
                'block': block.serialize()}


    log(1, "minning completed successfully")
    return jsonify(response), 200

@app.route('/receive-new-block', methods = ['POST'] )
def receiveNewBlock():
    json = request.get_json()
    newBlock = json['newBlock']
    newBlock = jsonpickle.decode(newBlock)
    lastBlock = blockchain.getLastBlock()

    # checking weather hash is maching and has valid transaction
    # befor accepting a new block

    correctHash = lastBlock.hash==newBlock.previousBlockHash
    correctIndex = lastBlock.index+1 ==newBlock.index
    has_valid_tx = blockchain.has_valid_transaction(newBlock)
    if(correctHash and correctIndex and has_valid_tx):
        blockchain.chain.append(newBlock)
        blockchain.pendingTransaction = []
        blockchain.storeBlock(newBlock)
        return jsonify({
			'note': 'New block received and accepted.',
			'newBlock': [e.serialize() for e in newBlock.transaction]
		})
    else:
        return jsonify({
			'note': 'New block received and rejected.',
			'newBlock': [e.serialize() for e in newBlock.transaction]
		})



@app.route('/register-node/broadcast', methods = ['POST'])
def registerBroadcastNode():
    json = request.get_json()
    newNode = json['newNode']
    
    if(newNode==currentNodeURl):
        return "current node cannot be added"
    if(blockchain.networkNodes.__contains__(newNode)):
        return "already exist"
    
    blockchain.addNode(newNode)

    for node in blockchain.networkNodes:
        requests.post(node + '/register-node', json={'newNode' : newNode})
      
    allNetworkNodes = blockchain.networkNodes
    allNetworkNodes.append(currentNodeURl)
    requests.post(newNode + '/register-bulk-nodes', json={'allNetworkNodes' : allNetworkNodes })

    allNetworkNodes.remove(currentNodeURl)
    
    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
               'total_nodes': list(blockchain.networkNodes)}
    return jsonify(response), 201

@app.route('/register-node', methods = ['POST'])
def registerNode():
    json = request.get_json()
    node = json['newNode']
    if(node==currentNodeURl):
        return "current node cannot be added"
    elif(blockchain.networkNodes.__contains__(node)):
        return "already exist"
    else:
        blockchain.addNode(node)
        return jsonify({ 'note': 'New node registered successfully.' })

    
@app.route('/register-bulk-nodes', methods = ['POST'])
def registerBulkNodes():
    allNodes = request.get_json()['allNetworkNodes']
    for node in allNodes:
        if( not blockchain.networkNodes.__contains__(node) ):
            if(node!=currentNodeURl):
                blockchain.addNode(node)
    
    return jsonify({'note' : "bulk registration successfull"}), 200

@app.route('/consensus', methods = ['GET'])
def consensus():
    allBlcockchain = []
    currentChainlen=len(blockchain.chain)
    maxLen  = currentChainlen
    bestChain = []
    newPendingTransaction = []
    for node in blockchain.networkNodes:
        r= requests.get(node + '/get-blockchain')
        allBlcockchain.append(r.json())
    for block in allBlcockchain:
        block['chain'] = jsonpickle.decode(block['chain'])
        block['pendingTransaction'] = jsonpickle.decode(block['pendingTransaction'])
        if True:
            if(len(block['chain'])>maxLen):
                maxLen = len(block['chain'])
                bestChain = block['chain']
                newPendingTransaction = block['pendingTransaction']
    
    if  blockchain.isChainValid(bestChain) and len(bestChain):
        blockchain.chain = bestChain
        blockchain.pendingTransaction = newPendingTransaction
        blockchain.replace(bestChain)
        return jsonify({'message' : 'This chain has been replaced ','chain' :[e.serialize() for e in bestChain]})
    else:
        return jsonify({'message' : 'this chain is not replaced ', 'best': [e.serialize() for e in bestChain]})    


@app.route('/connect-nodes', methods = ['GET'])
def connectNode():
    for i in range(5):
        data = {
            "newNode":  "http://localhost:500" + str(i+1) 
        }
        requests.post(currentNodeURl +'/register-node/broadcast', json=data)
    return jsonify({'network nodes' :blockchain.networkNodes}) 
    

@app.route('/vote', methods = ['GET'])
def vote():
    return jsonify({'vote counte': wallet.calculateVote(blockchain.chain)})

app.run(host = '0.0.0.0', port = int(PORT))