#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import gcd
import hashlib
import random
from prime_generator import generate_prime

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
        
        p = generate_prime(bits=10)
        q = generate_prime(bits=10)
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
    
    def generate_private_key(self):
        
        phi = (self.p - 1) * (self.q - 1)
        for i in range(phi):
            x = (i * phi) + 1
            if x % self.e == 0:
                d = int(x/self.e)
                return d
        print("DIDNT WORK")
                
    def sign(self, data, hashed=False):
        
        if not hashed:
            hashed = hashlib.sha256(data.encode()).hexdigest()
            hashed = int(hashed, 16)
        signed = pow(hashed, self.d, self.n)
        return signed
    
    def verify(self, data, signature):
        
        hashed = hashlib.sha256(data.encode()).hexdigest()
        hashed = int(hashed, 16)
        check = pow(signature, self.e, self.n)
        print(hashed)
        print(check)
        if check == hashed:
            return True
        else:
            return False
    
        
x = RSA(get_new=True)
data = "Hello"
sig = x.sign(data)
print(x.verify(data, sig))