#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from Crypto.PublicKey import RSA


currentdir = os.path.dirname(__file__)
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from core.sha import sha
from core.pool import TransactionPool
from core.utxo import UTXO
from network.client import Client

class Wallet():
    
    def __init__(self):
        
        self.pool = TransactionPool()
        self.utxo = UTXO()
        self.key = self.load_key()
        self.balance = self.balance()
        
    def load_key(self):
        
        if "key.pem" in os.listdir():
            with open(os.getcwd() + "/key.pem") as f:
                key = RSA.importKey(f.read())
        else:
            key = self.generate_key()
        return key
        
    def generate_key(self):
        
        key = RSA.generate(1024)
        with open(os.getcwd() + "/key.pem", "wb") as f:
            f.write(key.exportKey("PEM"))
        return key
        
    def sign(self, txid):
        """
        txid : hex string
            the hex of the hash object of the transaction id
        
        returns : signature
            the signature varifies that the input coins are valid and owned
            by this private key
        """
        
        byte_id = bytes.fromhex(txid)
        sig = self.key.sign(byte_id, 32)
        return sig
    
    def balance(self):
                
        trans = self.utxo.get_by_pk(self.key.publickey().exportKey().decode())
        balance = 0
        for t in trans:
            balance += t[4]
        return balance
        
    def pay(self, amount, recepient):
        """ 
        amount : int
            the amount of money to transfer
        recepient : str
            the public key address of receiving party
        """
        
        if amount > self.balance:
            return "Insufficient Funds"
        else:
            self.new_trans(amount, recepient)
    
    def new_trans(self, amount, recepient):
        """
        amount : float
            the total payment to the recepient
        recepient : str
            the public key address of the receiving party
            
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
                    "address":self.key.publickey().exportKey().decode()
                    })
        
        data = {
                "vin": vin,
                "vout": vout
            }
        
        data['txid'] = sha(json.dumps(data)) # hashes the transaction
        self.broadcast(data)
        
    def _get_unspent(self, amount):
        """ 
        returns: list, float
            a list of transaction ids, 
            float with the change amount
        
        Helper function that gets enough unspent transaction to cover the current
        transaction amount
        """
        
        trans = self.utxo.get_by_pk(self.key.publickey().exportKey().decode())
        cash = 0
        count = 0
        
        while cash < amount:
            cash += trans[count][4] #(id, txid, address, change, amount, block)
            count += 1
            
        change = cash - amount
        return trans[:count], change
    
    def broadcast(self, trans):
        
        self.pool.insert(trans)
        client = Client()
        client.prop_trans(trans)
        client.close()
        
if __name__ == "__main__":
    wallet = Wallet()
    exit_wallet = False
    
    while not exit_wallet:
        command = input("To check balance type 'balance' | To make payment type 'pay' | To exit type 'exit': ")
        
        if command == "balance":
            print("Balance: ", wallet.balance)
        elif command == "pay":
            amount = input("Amount: ")
            address = input("Address: ")
            payment = wallet.pay(float(amount), address)
            if payment == None:
                print("Payment successful")
            else:
                print(payment)
        elif command == "exit":
            exit_wallet = True
        else:
            print("Invalid command")
            
        


        

