#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import gcd
import hashlib
import random
from Crypto.Util import number

class RSA():
    """
    public key pair : (n, e)
    private key pair: (n, d)
    """
    
    def __init__(self, get_new=False):
        
        if get_new:
            self.n, self.p, self.q = self.get_primes()
            self.e = self.generate_public_key()
            self.d = self.generate_private_key()
            
    def get_primes(self):
        
        p = number.getPrime(1024)
        q = number.getPrime(1024)
        if p == q:
            self.get_primes()
        n = p * q
        return n, p, q
    
    def generate_public_key(self):
        
        phi = (self.p - 1) * (self.q - 1)
        e = random.randrange(2,(phi-1))
        while gcd(phi, e) != 1:
            e = random.randrange(2,(phi-1))
        return e
    
    # def generate_private_key(self):
        
    #     phi = (self.p - 1) * (self.q - 1)
    #     for i in range(phi):
    #         x = (i * phi) + 1
    #         if x % self.e == 0:
    #             d = int(x/self.e)
    #             return d
    #     print("DIDNT WORK")
    
    def generate_private_key(self):
        
        phi = (self.p - 1) * (self.q - 1)
        d = random.randrange(2,(phi-1))
        check = (d * self.e) % phi
        while check != 1:
            d = random.randrange(2,(phi-1))
            check = (d * self.e) % phi
        print((d * self.e) % phi)
        return int(d)
                
    def sign(self, data, hashed=False):
        
        if not hashed:
            #hashed = hashlib.sha256(data.encode()).hexdigest()
            #hashed = int(hashed, 16)
            hashed = ord(data)
        signed = pow(hashed, self.d, self.n)
        return signed
    
    def verify(self, data, signature, hashed=False):
        
        if not hashed:
           # hashed = hashlib.sha256(data.encode()).hexdigest()
           # hashed = int(hashed, 16)
            hashed = ord(data)
        check = pow(signature, self.e, self.n)
        print("ORIGINAL HASH: ", hashed)
        print("CHECKED: ", check)
        if check == hashed:
            return True
        else:
            return False
    
        
x = RSA(get_new=True)
data = "H"
sig = x.sign(data)
print(x.verify(data, sig))

h = 14413
s = pow(h, x.d, x.n)
hprime = pow(s, x.e, x.n)










