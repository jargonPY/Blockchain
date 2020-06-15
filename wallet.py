#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rsa import RSA
from utxo import UTXO

class Wallet():
    
    def __init__(self, load="Auto"):
        
        if load == "Auto":
            # self.sk = load file
            # self.pk = load file
            pass
        else:
            # load keys specified by user --> allows for usage of multiple keys
            pass
    
    def balance(self):
        
        trans = UTXO.get_by_pk(self.pk)
    
    def pay_to(self):
        
        pass
    
    def check_received(self):
        
        pass
    
    def get_trans(self):
        
        pass
    
    def sign(self, tx_id):
        """
        tx_id : string
            transaction hash which is a unique identifier for the tranaction
        
        returns : signature
            the signature varifies that the input coins are valid and owned
            by this private key
        """
        
        sig = RSA.sign(tx_id, hashed=True)
        return sig
    
    def new_trans(self, amount, recepient):
        """
        amount : float
            the total payment to the recepient
        recepient : string
            the public key address of the receiving party
            
        returns: json
            a json data structure with input/output information of the transaction
        """
        
        data = {
                "vin": [ ]
            }
        
    def _get_unspent(self, amount):
        """ 
        returns: list
            a list of transaction ids
        
        Helper function that gets enough unspent transaction to cover the current
        transaction amount
        """
        trans = UTXO.get_by_pk(self.pk)
        cash = 0
        while cash < amount:
            
            pass        
        
        
        
        
        
        
        

