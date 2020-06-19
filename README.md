# Blockchain

- Digital Signatures allow for confirmation of ownership
- An immutable public ledger ensures transparency of all transactions, this is the mechanism by which double spending is avoided
- proof of work allows for distributed consensus

The need for a proof-of-work algorithm:
Given the distributed nature of the network and the random topology, different nodes will recieve transactions in different order. However to verify the validity of transactions there is a need for an agreed upon ledger that nodes can reference. Therefore at some point a node needs to propose a set of transactions that will be appended to the ledger and ensure all nodes are in agreeement of the current state of verified transactions. Since we have a distributed and anonymous network, there is a need to ensure that the porposed block was not produced by a malicious node, this is where the proof-of-work algorithm comes in, nodes compete based on CPU power, and are incentivized by transaction fees. As long as more than 50% of the network's nodes (by CPU power) are honest, the malicious nodes will not be able to outpace and cheat the system.
  - decentralized consensus
  - nodes compete based on CPU power (difficult to monopolize)

- transactions are only added to the UTXO database once they are confirmed (they are part of the blockchain)

On startup:
  1. Empty transaction pool
  2. Get latest block
      - request hash of chain, if doesn't match then request missing blocks
