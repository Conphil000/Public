# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 22:06:29 2021

@author: Conor
"""

import os
import json

# Pull the Twitter API keys associated with my account from a hidden json file.

with open('C:\\Users\\Conor\\Desktop\\r1\\twitter\\tictactoe\\keys.json') as f:
    keys = json.load(f)
    
# Now we have a dictionary of keys needed to access my accounts, this can be passed to the class.


class player:
    def __init__(self,author_id,move):
        print(f'{author_id} has responded to the tweet...')
        print('tweet created...')
        pass









