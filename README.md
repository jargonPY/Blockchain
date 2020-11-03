# Blockchain

A prototype of a cryptocurrency meant as a learning project to understand the inner wokrings of the many concepts involved with building a working cryptocurrency. This code can facilitate the creation, propogation, verification of transactions and blocks between nodes on a local network.

## Instructions:
    Initialization:
    1. Clone the repo
    2. Open repo in the terminal and run `python ./init/genesis_block.py`
      - This will create a private and public key for you and generate the first block which an initial transaction to your public key. Anyone joining your network will now be             able to recieve and verify your payments
    3. Run the server `python ./network/server.py`
      - This will open up a port for others on the network to connect to and communicate with your node
      
    Connecting more computers to the network:
    1. Clone the repo on the new computer
    2. Enter the local IP address of the original computer into `./network/addr.json`
    3. Run the server on the new computer
    4. Now the two computers can communicate and propagate transactions
  
## Data structures used:
  - Block: 
          {'header': dict with header details,
           'transactions': list of transaction}
  - Transaction:
          {'txid': hash of current transaction
           'vin' : list of input transaction
           'vout': output transactions (max. 2 output transactions)}
## Databases used:
  - Blockdb:
          An SQL database containing three fields (id (primary key), hash (of the block), filename). 
      - This database is used to query blocks by their hash and find corresponding files.
          
  - UTXO (Unspent Transaction Output) database:
           An SQL database containing all unspent transaction outputs.
           Contains six fields (id (primary key), txid, address (public key of output), change (0 or 1), amount, block (the hash of the block that contains the transaction)).
      - This allows a node to quickly verify inputs of incoming transactions. Wallets also use the database to find outputs belonging to their public key (and thus can show the            'balance' of the account to the user), and to find output transactions to be used as inputs for new transactions.
      
      - transactions are only added to the UTXO database once they are confirmed and are part of the blockchain





## How mining nodes help achieve decentralized consensus:
Given the distributed nature of the network and the random topology, different nodes will recieve transactions in different order. However to verify the validity of transactions there is a need for an agreed upon ledger that nodes can reference. Therefore at some point a node needs to propose a set of transactions that will be appended to the ledger and ensure all nodes are in agreeement of the current state of verified transactions. Since we have a distributed and anonymous network, there is a need to ensure that the porposed block was not produced by a malicious node, this is where the proof-of-work algorithm comes in, nodes compete based on CPU power, and are incentivized by transaction fees. As long as more than ~50% of the network's nodes (by CPU power) are honest, the malicious nodes will not be able to outpace and cheat the system. Hence mining nodes, which are difficult to monopolize (on a large network), are the mechanism used to achieve decentralized consensus.
