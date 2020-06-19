#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import socket
import threading
import os
from server import Server
from client import Client

"""
Node A --> (client A, server A)
When client A connects to server B, node B tells client B to connect to server A
"""

class Node():
    
    def __init__(self):
        
        self.server = Server(self)
        self.client = Client(self)
        
    def add_client(self, addr):
        """
        Called by the Server class to establish a two-way connection 
        """
        
        self.client.connect_from_server(addr)
        
        
            

