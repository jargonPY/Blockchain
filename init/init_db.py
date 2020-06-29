#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3 

currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)

def init_utxo():
    
    conn = sqlite3.connect(parentdir + "/databases" + "/utxo.db")
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
    
def init_blocks():
    
    conn = sqlite3.connect(parentdir + "/databases" + "/blocks.db")
    c = conn.cursor()
    
    c.execute("""CREATE TABLE blocks (
                id INTEGER PRIMARY KEY,
                hash TEXT,
                file TEXT
                )""")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_utxo()
    init_blocks()