#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

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
        
        self.conn = sqlite3.connect("utxo.db")
        self.c = self.conn.cursor()
    
    def get_by_txid(self, txid):
        """ query database by transaction id """
        
        self.c.execute("SELECT * FROM utxo WHERE txid=:txid", {'txid':txid})
        return self.c.fetchone() # fetchone since txid should be unique
    
    def get_by_pk(self, pk):
        """ query database by public key address """
        
        self.c.execute("SELECT * FROM utxo WHERE address=:address", {'address':pk})
        return self.c.fetchall()
    
    def add_trans(self, trans):
        """
        trans : list
            a list of transactions
            
        once a block is confirmed all of its transactions are added to the utxo
        database
        """
        
        with open(os.getcwd() + "/blocks" + "/counter.txt") as f:
            block_num = int(f.read())
        
        for t in trans:
            if len(t['vout']) == 2: # t['vout'] is a list of outputs
                self.c.execute("INSERT INTO utxo VALUES (:txid, :address, :amount, :block)",
                                                    {'id':'NULL', # inserting NULL to pk will auto-increment
                                                     'txid': trans['txid'],
                                                     'address': t['vout'][1]['address'],
                                                     'change': 1,
                                                     'amount': t['vout'][1]['amount'],
                                                     'block': block_num})
                self.conn.commit()
                
            self.c.execute("INSERT INTO utxo VALUES (:txid, :address, :amount, :block)",
                                                    {'id':'NULL', # inserting NULL to pk will auto-increment
                                                     'txid': trans['txid'],
                                                     'address': t['vout'][0]['address'],
                                                     'change': 0,
                                                     'amount': t['vout'][0]['amount'],
                                                     'block': block_num})
            self.conn.commit()
        
    def remove_trans(self, txid):
        """ removes transaction from utxo by it's id (transaction hash) """
        
        with self.conn:
            self.c.execute("DELETE from utxo WHERE txid = :txid", {'txid': txid})
    
    def update(self):
        """ 
        if the computer was disconnected from the network it should update by querying
        other nodes in the network 
        """
            
        pass
    
    def close(self):
        
        self.conn.close()
        
        
    
