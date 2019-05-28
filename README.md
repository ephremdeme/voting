#Blockchain Based Voting
It is python based implementation of blockchain technology to used for e-Voting. 
By considering each vote as transaction to be added pending_transaction, which 
is ready to mined and included in **Block**. and then the newly created block is added to blockchain and broadcast
to the all nodes of  the network.
<!Configuration
1. List of Voters: This list contains all eligible voters for the given election. 
2. List of Candidates: This list outlines the individual subjects on which voters
must decide.
3. Election Type: This value determines the concrete voting mechanism, such as majority voting or single transferable voting (STV), and its parameters, e.g., how many options a voter can
select in an STV.
4. Election Start/End Times: These values specify the time frame in which eligible voters are
allowed to cast their vote.!>

#Features
####The blockchain :

* Possibility of adding multiple nodes to the blockchain
* Proof of Work (PoW)
* Simple conflict resolution between nodes
* Transactions with ecdsa signature verification
####The blockchain client has the following features:
* Desktop based GUI app
* Wallets generation using Public/Private key encryption (based on ecdsa)
* Generation of transactions with ecdsa asymmetric encryption
####The blockchain API server for miners
* Block explorer
* Transaction and Block verification & Broadcasting
* Block mining
* p2p communication

# Installation
* first clone the repository
```text
git clone https://github.com/ephremdeme/voting.git
```
* simply `cd voting` and install all the dependencies from requirement.txt
```text
pip install -r requirements.txt 
```
* on linux terminal run `./run.sh`, this will apen a 6 tab terminal for 6 network nodes 

* or add each node like `python BlockchainAPINode.py 5000`
* to start the blockchain client, go to `cd client` and execute: `python clientGUI.py`
* finally open your browser and go to `localhost:5000` 


# Contribution 
Any suggestion or contribution is welcome.


