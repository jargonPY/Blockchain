#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3 

def init_utxo():
    
    conn = sqlite3.connect("utxo.db")
    c = conn.cursor()
    
    c.execute("""CREATE TABLE utxo (
                id INTEGER PRIMARY KEY,
                txid TEXT,
                address TEXT,
                change INTEGER,
                amount REAL,
                block INTEGER
                )""")
    
    conn.commit()
    conn.close()
    
""" TRANSACTION FORMAT """

""" {txid : sdf234
    vin : asdf
        prev_hash: sadf
    vout : asdf} """
    
#conn = sqlite3.connect(":memory:") # creates a new table on every run
#c = conn.cursor()
    
#c.execute("INSERT INTO utxo VALUES ('h2214', 'asdf34', 432.32, 540)")
#c.commit()
#c.execute("SELETCT * FROM utxo WHERE address='asdf34'")
#c.fetchall() # returns a list of all results, returns None/[] if there are no results
#
#c.execute("INSERT INTO utxo VALUES (:txid, :address, :amount, :block)", {'txid':var,
#                                                                             etc.})
#with conn:
#   c.execute("SELETCT * FROM utxo WHERE address=:address, {'address':address}")

""" To Remove """
#with conn:
#    c.execute("DELETE from utxo WHERE txid = :txid AND block = :block", {'txid': txid, etc.})

""" Bulk INSERTS ??? """

if __name__ == "__main__":
    init_utxo()