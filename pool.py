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
        
        del self.pool[txid]
        
    def check_new_block(self, block):
        
        trans = block['transactions']
        for t in trans:
            self.remove(t['txid'])