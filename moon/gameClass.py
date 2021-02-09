# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:24:24 2021

@author: Conor
"""

from deckClass import deck
from playerClass import player
import random
newDeck = deck()

newDeck.newDeck()


p1 = player()
p2 = player()
p3 = player()

p1.setDeck(newDeck.pullHand())
p2.setDeck(newDeck.pullHand())
p3.setDeck(newDeck.pullHand())
print([i.showDomino() for i in p1.showDeck()])
print(p1.playRandom().showDomino())
print([i.showDomino() for i in p1.showDeck()])



class game:
    def __init__(self,):
        self.__players = {}
        self.__turn = 0
        self.__startGame()
        print('Game Started')
    def __startGame(self):
        self.__turn = random.randint(0,2)
        print(f'Player {self.__turn} will start the bidding... dealing the first hand!')
        self.__deck = deck()
        self.__deck.newDeck()
        for i in range(0,3):
            self.__players[i] = player()
        self.__dealDeck()
    def __dealDeck(self):
        first = self.__turn
        for i in range(0,3):
            self.__players[first].setDeck(self.__deck.pullHand())
            first = self.__rotateItem(first)
    def showHands(self):
        for i,j in self.__players.items():
            print([i.showDomino() for i in j.showDeck()])
    def __rotateItem(self,n):
        if n == 2 :
            n = 0
        else:
            n += 1
        return n
    def setTrump(self,trump):
        for i,j in self.__players.items():
            for k in j.showDeck():
                k.declareTrump(trump)
    def showTurn(self,):
        return self.__turn
    
test = game()

test.showHands()

