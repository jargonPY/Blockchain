# Blockchain



A short intro to cryptocurrencies:
- Digital Signatures allow for confirmation of ownership
- An immutable public ledger ensures transparency of all transactions, this is the mechanism by which double spending is avoided
- Proof of work facilitates consensus amongst peers in a decentralized network

Given the distributed nature of the network and the random topology, different nodes will recieve transactions in different order. However to verify the validity of transactions there is a need for an agreed upon ledger that nodes can reference. Therefore at some point a node needs to propose a set of transactions that will be appended to the ledger and ensure all nodes are in agreeement of the current state of verified transactions. Since we have a distributed and anonymous network, there is a need to ensure that the porposed block was not produced by a malicious node, this is where the proof-of-work algorithm comes in, nodes compete based on CPU power, and are incentivized by transaction fees. As long as more than 50% of the network's nodes (by CPU power) are honest, the malicious nodes will not be able to outpace and cheat the system.
  - decentralized consensus
  - nodes compete based on CPU power (difficult to monopolize)
      
Data Structures:
  - Block: 
          {'header': dict with header details,
           'transactions': list of transaction}
  - Transaction:
          {'txid': hash of current transaction
           'vin' : list of input transaction
           'vout': output transactions (max. 2 output transactions)}
  - Blockdb:
          An SQL database containing three fields (id (primary key), hash (of the block), filename). 
      - This database is used to query blocks by their hash and find corresponding files.
          
  - UTXO (Unspent Transaction Output) database:
           An SQL database containing all unspent transaction outputs.
           Contains six fields (id (primary key), txid, address (public key of output), change (0 or 1), amount, block (the hash of the block that contains the transaction)).
      - This allows a node to quickly verify inputs of incoming transactions. Wallets also use the database to find outputs belonging to their public key (and thus can show the            'balance' of the account to the user), and to find output transactions to be used as inputs for new transactions.
      
      - transactions are only added to the UTXO database once they are confirmed and are part of the blockchain

On startup of server:
  1. Empty transaction pool
  2. Get latest block from peers
      - request hash of chain, if doesn't match to local hash then request missing blocks
