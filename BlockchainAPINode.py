from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from Blockchain import Blockchain
from sys import argv
import jsonpickle

# Creating a Web App
app = Flask(__name__)
PORT = argv[1]
# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

currentNodeURl = "http://localhost:" + str(PORT)
# Creating a Blockchain
blockchain = Blockchain(PORT)
blockchain.read_chain()

app.debug = True


@app.route("/", methods=['GET'])
def home():
    return jsonify({'chain': blockchain.serialize_chain(),
                    'pendingTransaction': [e.serialize() for e in blockchain.pendingTransaction],
                    'networkNode': blockchain.networkNodes})


@app.route('/get-blockchain', methods=['GET'])
def get_blockchain():
    return jsonify(
        {
            'chain': jsonpickle.encode(blockchain.chain),
            'pendingTransaction': jsonpickle.encode(blockchain.pendingTransaction)
        })


@app.route('/transaction/broadcast', methods=['POST'])
def transaction_broadcast():
    json = request.get_json()
    transaction = jsonpickle.decode(json)
    if blockchain.add_to_pending_transaction(transaction):
        transaction = jsonpickle.encode(transaction)
    else:
        response = {'message': 'This transaction is invalid will not be added to Block '}
        return jsonify(response), 500

    if len(blockchain.networkNodes) is not 0:
        for node in blockchain.networkNodes:
            requests.post(node + '/transaction/broadcast', json=transaction, timeout=2)

    return jsonify({'note': 'Transaction created and broadcast successfully.',
                    'pendingTransaction': [e.serialize() for e in blockchain.pendingTransaction]}), 200


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.get_last_block()
    block_data = {
        'transactions': jsonpickle.encode(blockchain.pendingTransaction),
        'index': last_block.index + 1
    }

    # finding nonce for the block
    nonce = blockchain.proof_of_work(block_data)
    # generating hash for the block and mining
    block_hash = blockchain.hash_block(block_data, nonce)
    block = blockchain.create_block(nonce, last_block.hash, block_hash)
    blockchain.store_block(block)
    block = jsonpickle.encode(block)

    for node in blockchain.networkNodes:
        print(1, "the block is transmitted to" + str(node))
        requests.post(node + '/receive-new-block', json={'new_block': block})

    # print(1, "minning fee is being transmitted")
    # transaction = {
    #     "sender": None,
    #     "receiver": node_address,
    #     "amount": 12.5
    # }
    # transaction = miner_wallet.create_transaction(transaction['receiver'], transaction['amount'])
    #
    # blockchain.add_to_pending_transaction(transaction)
    # transaction = jsonpickle.encode(transaction)
    #
    # for node in blockchain.networkNodes:
    #     requests.post(node + '/transaction', json=transaction)

    # r=requests.post( currentNodeURl + '/transaction/broadcast', json=transaction)
    block = jsonpickle.decode(block)
    response = {'message': 'Congratulations, you just mined a block!',
                'block': block.serialize()}

    print(1, "minning completed successfully")
    return jsonify(response), 200


@app.route('/receive-new-block', methods=['POST'])
def receive_new_block():
    json = request.get_json()
    new_block = json['new_block']
    new_block = jsonpickle.decode(new_block)
    if blockchain.receive_block(new_block):
        new_block = jsonpickle.encode(new_block)
        for node in blockchain.networkNodes:
            print(1, "the block is transmitted to" + str(node))
            requests.post(node + '/receive-new-block', json={'new_block': new_block})
        return jsonify({
            'note': 'New block received and accepted.'
        })
    else:
        return jsonify({
            'note': 'New block received and rejected.'
        })


@app.route('/register-node/broadcast', methods=['POST'])
def register_broadcast_node():
    json = request.get_json()
    new_node = json['new_node']

    if new_node == currentNodeURl:
        return "current node cannot be added"
    if blockchain.networkNodes.__contains__(new_node):
        return "already exist"

    blockchain.add_node(new_node)

    for node in blockchain.networkNodes:
        requests.post(node + '/register-node', json={'new_node': new_node})

    all_network_nodes = blockchain.networkNodes
    all_network_nodes.append(currentNodeURl)
    requests.post(new_node + '/register-bulk-nodes', json={'all_network_nodes': all_network_nodes})

    all_network_nodes.remove(currentNodeURl)

    response = {'message': 'All the nodes are now connected. The Blockchain now contains the following nodes:',
                'total_nodes': list(blockchain.networkNodes)}
    return jsonify(response), 200


@app.route('/register-node', methods=['POST'])
def register_node():
    json = request.get_json()
    node = json['new_node']
    if node == currentNodeURl:
        return "current node cannot be added"
    elif blockchain.networkNodes.__contains__(node):
        return "already exist"
    else:
        blockchain.add_node(node)
        return jsonify({'note': 'New node registered successfully.'})


@app.route('/register-bulk-nodes', methods=['POST'])
def register_bulk_nodes():
    all_nodes = request.get_json()['all_network_nodes']
    for node in all_nodes:
        if not blockchain.networkNodes.__contains__(node):
            if node != currentNodeURl:
                blockchain.add_node(node)

    return jsonify({'note': "bulk registration successfull"}), 200


@app.route('/consensus', methods=['GET'])
def consensus():
    all_blockchain = []
    current_chainlen = len(blockchain.chain)
    max_len = current_chainlen
    best_chain = []
    new_pending_transaction = []
    for node in blockchain.networkNodes:
        r = requests.get(node + '/get-blockchain')
        all_blockchain.append(r.json())

    for block in all_blockchain:
        block['chain'] = jsonpickle.decode(block['chain'])
        block['pendingTransaction'] = jsonpickle.decode(block['pendingTransaction'])
        if True:
            if len(block['chain']) > max_len:
                max_len = len(block['chain'])
                best_chain = block['chain']
                new_pending_transaction = block['pendingTransaction']

    if blockchain.is_chain_valid(best_chain) and len(best_chain):
        blockchain.chain = best_chain
        blockchain.pendingTransaction = new_pending_transaction
        blockchain.replace(best_chain)
        return jsonify({'message': 'This chain has been replaced ', 'chain': [e.serialize() for e in best_chain]})
    else:
        return jsonify({'message': 'this chain is not replaced ', 'best': [e.serialize() for e in best_chain]})


@app.route('/connect-nodes', methods=['GET'])
def connect_node():
    for i in range(5):
        data = {
            "new_node": "http://localhost:500" + str(i + 1)
        }
        requests.post(currentNodeURl + '/register-node/broadcast', json=data)
    return jsonify({'network nodes': blockchain.networkNodes})


@app.route('/vote', methods=['GET'])
def vote():
    return jsonify({'vote count': blockchain.calculate_vote(blockchain.chain)})


app.run(host='0.0.0.0', port=int(PORT))
