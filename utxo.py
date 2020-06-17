#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        
        self.c.execute("SELECT * FROM utxo WHERE address=:address", {'address':address})
        return self.c.fetchall()
    
    def add_trans(self, trans):
        """
        trans : json
            a json object containing the data of the transaction
        """
        
        with self.conn:
            self.c.execute("INSERT INTO utxo VALUES (:txid, :address, :amount, :block)",
                                                {'id':'NULL', # inserting NULL to pk will auto-increment
                                                 'txid':trans['txid'],
                                                 'address':pass,
                                                 'change':pass,
                                                 'amount':pass,
                                                 'block':pass})
    
    def remove_trans(self, txid):
        """ removes transaction from utxo by it's id (transaction hash) """
        
        with conn:
            c.execute("DELETE from utxo WHERE txid = :txid", {'txid': txid})
    
    def update(self):
        """ If the computer was disconnected from the network it should update by querying
            other nodes in the network """
            
        pass
    
    def close(self):
        
        self.conn.close()
        
        
    
