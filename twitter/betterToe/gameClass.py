# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:48:34 2021

@author: ConorPhillips
"""

from apiClass import API
from playerClass import player

import json

class game:
    def __init__(self):
        # Start the API, create lists to hold everyone who has played and is currently playing.
        with open('keys.json','r') as fp:
            keys = json.load(fp)
        self.__api = API(keys['APIK'],keys['APISK'],keys['BK'],keys['AT'],keys['ATS'])
        self.__p = 'O'
        self.__c = 'X'
        
        self.__players = []
        self.__active = []
        
    def __gameTweet(self):
        self.__board = '1 |  2  | 3\n- + - + -\n4 |  5  | 6\n- + - + -\n7 |  8  | 9'
        string = f"To play, respond to this tweet with a number and wait for a response!\n\nYou are {self.__p}'s!\n{self.__board}"
        self.__api.publishTweet(string)
        last = self.__api.grabLastTID()
        self.__last = last
        self.__gameTweet = last
    def deleteGame(self):
        self.__api.deleteTweet(self.__gameTweet)
    def startGame(self,):
        self.__gameTweet()
test = game()
test.startGame()

#test.deleteGame()