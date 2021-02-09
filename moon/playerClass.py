# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:17:23 2021

@author: ConorPhillips
"""
import random
class player:
    def __init__(self,):   
        self.__score = 0
        self.__win = 0 
        self.__deck = []
        self.__deckDict = {}
    def setDeck(self,deck):
        # Use this function to assign a list to the deck variable.
        self.__deck = deck
        for i in self.__deck:
            self.__deckDict[i.showDomino()] = i
    def showDeck(self,):
        # Use this function to show the current deck values.
        return self.__deck
    def showScore(self,):
        # Use this function to show the current score.
        return self.__score
    def showWins(self,):
        # Use this function to show the number of wins.
        return self.__wins
    def showName(self,):
        # Use this function to show the name of player.
        return self.__name
    def addWin(self,):
        # Use this function to add a win to the player
        self.__win += 1
    def addScore(self,n):
        # Use this function to add an integer to the players score.
        self.__score += n
    def resetScore(self,):
        # Use this function to change the score to 0.
        self.__score = 0
    def resetWin(self,):
        # Use this function to change the number of wins to 0
        self.__win = 0
    def clearDeck(self,):
        # Use this function to reset the players deck.
        self.__deck = []
        self.__deckDict = {}
    def removeDomino(self,domino):
        # Use this function to remove a specific domino from the players deck.
        try:
            self.__deck.remove(domino)
        except:
            print(f"Can't find Mr. Domino: {domino}!")
    def playRandom(self,):
        play = random.choice(self.__deck)
        self.removeDomino(play)
        return play        
        
        
        
        