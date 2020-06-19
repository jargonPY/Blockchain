#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import os
from rsa import RSA
from utxo import UTXO
from Crypto.PublicKey import RSA

class Wallet():
    
    def __init__(self, pool, utxo):
        
        self.pool = pool
        self.utxo = utxo
        self.key = self.load_key()
        self.balance = self.balance()
        
    def load_key(self):
        
        if "key.pem" in os.lsdir():
            with open(os.getcwd() + "/key.pem") as f:
                key = RSA.importKey(f.read())
        else:
            key = self.generate_key()
        return key
        
    def generate_key(self):
        
        key = RSA.generate(1024)
        with open(os.getcwd() + "/key.pem", "w") as f:
            f.write(RSA.exportKey("PEM"))
        return key
        
    def sign(self, txid):
        """
        txid : hex string
            the hex of the hash object of the transaction id
        
        returns : signature
            the signature varifies that the input coins are valid and owned
            by this private key
        """
        
        byte_id = bytes.fromhex(txid.hexdigest())
        sig = self.key.sign(byte_id, 32)
        return sig
    
    def balance(self):
        
        trans = UTXO.get_by_pk(self.pk)
        balance = 0
        for t in trans:
            balance += t[4]
        return balance
        
    def pay(self, amount, recepient):
        """ checks for sufficient funds, creates transaction """
        
        if amount > self.balance:
            print("Insufficient Funds")
        else:
            self.new_trans(amount, recepient)
    
    def check_received(self):
        """ 
        confirms transaction is sent and valid by looking in the 
        transaction pool
        """
        
        pass
    
    def get_trans(self):
        
        pass
    
    def new_trans(self, amount, recepient):
        """
        amount : float
            the total payment to the recepient
        recepient : tuple
            the public key address of the receiving party (n, e)
            
        returns: json
            a json data structure with input/output information of the transaction
        """
        
        trans, change = self._get_unspent(amount)

        vin = [ ]
        for t in trans:
            sig = self.sign(t[1]) # sign transaction id
            vin.append({
                        'txid':t[1], # (id, txid, address, change, amount, block)
                        'change':t[3], # boolean 0 or 1
                        'sig':sig,
                        })
        
        vout = [{
                    "amount":amount,
                    "address":recepient
                }]
        
        if change > 0:
            vout.append({
                    "amount":change,
                    "address":self.key.publickey().exportKey()
                    })
        
        data = {
                "vin": vin,
                "vout": vout
            }
        
        data['txid'] = Wallet.sha(data) # hashes the transaction
        
    def _get_unspent(self, amount):
        """ 
        returns: list, float
            a list of transaction ids, 
            float with the change amount
        
        Helper function that gets enough unspent transaction to cover the current
        transaction amount
        """
        
        trans = self.utxo.get_by_pk(self.pk)
        cash = 0
        count = 0
        
        while cash < amount:
            cash += trans[count][4] #(id, txid, address, change, amount, block)
            count += 1
            
        change = cash - amount
        return trans[:count()], change
    
    @staticmethod
    def sha(data):
        
        hashed = hashlib.sha256(data.encode())
        return hashed.hexdigest()
    
        
        
        
# hashed = hashlib.sha256("Hello!".encode()).digest()
# sig = key.sign(hashed, 32)        
# pk = key.publickey().exportKey()
# pubKeyObj =  RSA.importKey(pk)
# pubKeyObj.verify(hashed, sig)

        

