#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def check_validity():
    """
    when a node first enters a network and downloads the block chain
    it must confirm the validity of the blocks since some nodes can 
    be malicious
        1. connect several RANDOM nodes and request the hash of the entire chain
        2. compare hashes and download from a node whose hash is in the majority
    """
