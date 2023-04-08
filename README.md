# Blockchain Based Voting

It is python based implementation of blockchain technology to be used for e-Voting.
By considering each vote as transaction to be added to pending_transaction, which
is ready to be mined and included in a **Block**. And then the newly created block is added to the blockchain and broadcast
to all the nodes.


# Features

#### The blockchain :

- Possibility of adding multiple nodes to the blockchain
- Proof of Work (PoW)
- Simple conflict resolution between nodes
- Transactions with ecdsa signature verification

#### The blockchain client has the following features:

- React based Web App
- Here is Client [README.md](/web_client/README.md)

#### The blockchain API server for miners

- Block explorer
- Transaction and Block verification & Broadcasting
- Block mining
- p2p communication

# Installation

- first clone the repository by typing this code into your terminal.

```text
git clone https://github.com/ephremdeme/voting.git
```

- simply ` cd voting` and install all the dependencies from requirement.txt by typing this code

```text
pip install -r requirements.txt
```
Note: if fastecdsa gives "gmp.h" error with above command, use the command ```sudo apt-get install libgmp-dev```, then again try the above command.

- First export Flask api app using `export FLASK_APP=api`
- on linux terminal run `./run.sh`, this will apen a 6 tab terminal for 6 network nodes
- or add each node like `python BlockchainAPINode.py 5000`
- to add peer node to the blockchain, open postman POST request `localhost:5000/register-node/broadcast`
  and send json `{ "new_node": "http://localhost:5002"}`
- to start the blockchain client, go to `cd client` and execute: ` python clientGUI.py`
- finally open your browser and go to `localhost:5000`

# Contribution

Any suggestion or contribution is welcome.
