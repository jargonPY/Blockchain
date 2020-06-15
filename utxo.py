#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class UTXO():
    """
    A database that stores all unspent transactions.
    
    All new transactions must be checked to ensure they are in
    the UTXO database.
    
    A wallet looks for transactions that belong to its key
    by checking the UTXO database.
    
    How to synchronize? 
    """
    
    def __init__(self):
        
        pass
    
    def get_by_txid(self, tx_id):
        
        pass
    
    def get_by_pk(self, pk):
        
        pass
    
    def add_trans(self):
        
        pass
    
    def remove_trans(self):
        
        pass
    
    def update(self):
        
        pass
    

