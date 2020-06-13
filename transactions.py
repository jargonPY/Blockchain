#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from rsa import RSA

class NewTransaction():
    
    def __init__(self, amount, recepient):
        
        self.amount = amount
        self.recep = recepient
        
    def check_wallet(self):
        """ ensures sufficient funds are available """
        
        pass
    
    def sign_trans(self, trans_hash):
        
        sig = RSA.sign(trans_hash, hashed=True)
        return sig
    
    def get_trans(self):
        
        pass
    
    def create_trans(self):
        """
        inputs : dictionary
            value - previous transaction hash , key - the output number
        outputs : dictionary
            value - value , key - destination public key hash
        """
        
        data = {
                "vin": [ ]
            }