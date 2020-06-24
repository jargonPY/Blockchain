#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib

def sha(data):
        
    hashed = hashlib.sha256(data.encode()).hexdigest()
    return hashed
