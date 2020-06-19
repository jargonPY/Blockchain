#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TransactionPool():
    """
    Should it hold all transactions in memory?
        - if a block is built every 10 min then most transactions will be removed
        - how many bytes is one transaction?
        
    Create a queue if multiple transactions arrive almost instantenously
    """
    
    def __init__(self):
        
        self.pool = { }
        
    def insert(self, trans):
        
        self.pool[trans['txid']] = trans
    
    def propogate(self):
        
        pass
    
    def remove(self, txid):
        
        if txid in self.pool.keys():
            del self.pool[txid]
            
    def check_in_pool(self, txid):
        """ check if a transaction is in the transaction pool """
        
        if txid in self.pool.keys():
            return True
        else:
            return False
        
    def check_new_block(self, block):
        """
        once new block is confirmed this method removes the corresponding 
        transactions from the pool
        """
        
        trans = block['transactions']
        for t in trans:
            self.remove(t['txid'])


