#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
from rsa import RSA
from utxo import UTXO

class Wallet():
    
    def __init__(self, load="Auto"):
        
        if load == "Auto":
            # self.sk = load file --> tuple (n, d)
            # self.pk = load file --> tuple (n, e)
            pass
        else:
            # load keys specified by user --> allows for usage of multiple keys
            pass
        
        self.balance()
    
    def balance(self):
        
        trans = UTXO.get_by_pk(self.pk)
        self.balance = 0
        for t in trans:
            self.balance += t[4]
        
    def pay(self, amount, recepient):
        """ checks for sufficient funds, creates transaction """
        
        if amount > self.balance:
            print("Insufficient Funds")
        else:
            self.new_trans(amount, recepient)
    
    def check_received(self):
        """ confirms transaction is sent and valid by looking in the 
            transaction pool
        """
        
        pass
    
    def get_trans(self):
        
        pass
    
    def sign(self, txid):
        """
        tx_id : string
            transaction hash which is a unique identifier for the tranaction
        
        returns : signature
            the signature varifies that the input coins are valid and owned
            by this private key
        """
        
        sig = RSA.sign(txid, hashed=True)
        return sig
    
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
                    "address":self.pk
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
        
        trans = UTXO.get_by_pk(self.pk)
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
        return hashed
    
        
        
        
        
        
        
        
        
        

