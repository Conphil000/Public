# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:24:24 2021

@author: Conor
"""

from deckClass import deck
from playerClass import player

newDeck = deck()

newDeck.newDeck()


p1 = player('1234')
p2 = player('1432')
p3 = player('4321')

p1.setDeck(newDeck.pullHand())
p2.setDeck(newDeck.pullHand())
p3.setDeck(newDeck.pullHand())
print(p1.showDeck())
print(p1.playRandom().showDomino())
print(p1.showDeck())



