#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import os
import sys

def miller_test(n, k):
    """
    n : an odd integer
        the number to be tested for primality
    k : integer
        the number of times to run the test
    """
    
    # r = 1
    # while ((n-1)/(2**r)).is_integer():
    #     r += 1
    # r -= 1
    # m = int((n-1) / (2**r))
    
    m = n - 1
    r = 0
    while m % 2 == 0:
        m = m/2
        r += 1
        
    for i in range(k):
        a = random.randint(2, n-1)
        # a**m % n
        x = pow(a, int(m), n)
    
        if x == (n-1) or x == 1:
            continue
        for j in range(1, r):
            x = (x**2) % n
            if x == (n-1):
                break
            if x == 1:
                return False
            if j == (r-1):
                return False
    return True

def low_prime(n):
    
    low = [3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97
                   ,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179
                   ,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269
                   ,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367
                   ,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461
                   ,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571
                   ,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661
                   ,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773
                   ,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883
                   ,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997]
    
    for i in low:
        if n % i == 0:
            return False
    return True

def generate_prime(bits=1024, k=1):
    """
    b : integer that is a multiple of 8
        the number of bits of the prime number
    k : integer
        number of testing rounds
    """
    trials = 0
    byte = int(bits / 8)
    n = int.from_bytes(os.urandom(byte), byteorder=sys.byteorder) | 1
    
    prime = miller_test(n, k)
    while not prime:
        n += 2
        check_low = low_prime(n)
        if not check_low:
            n += 2
        prime = miller_test(n, k)
        trials += 1
    print("Trials: ", trials)
    return n
        
if __name__ == "__main__":
    start = time.time()
    n = generate_prime(bits=80)
    end = time.time()
    print("Ellapsed time: ", end - start)
    
    
    
    
    
    
    
    


        
    