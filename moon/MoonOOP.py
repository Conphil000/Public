# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 11:24:24 2021

@author: Conor
"""
import random


class domino:
    def __init__(self,s1,s2):
        # When a domino is created it needs two numbers.
        # These numbers represent the two sides of a domino.
        self.__trump = -1
        self.__s1 = s1
        self.__s2 = s2
    def declareTrump(self,trump):
        # At some point we will need to be able to declare the trump suit chosen.
        self.__trump = trump
    def isTrump(self,):
        # Check if a trump suit has been set, if it has check if either suit is that trump.
        if self.__trump != -1:
            if self.__s1 == self.__trump or self.__s2 == self.__trump:
                return True
            else:
                return False
        else:
            print('The trump suit has not been declared.')
    def isAce(self,):
        # Check if the domino is the ace
        if self.__s1 != - 1 and self.__s2 != -1:
            if self.__s1 == self.__s2:
                return True
            else:
                return False
        else:
            print('The suits have not been set properly.')
    def flip(self,):
        temp = self.__s1
        self.__s1 = self.__s2
        self.__s2 = temp
    def showDomino(self,):
        domino = f'{self.__s1}{self.__s2}'
        return domino

class deck:
    def __init__(self):
        self.newDeck()
    def __resetDeck(self,):
        self.__deck = []
    def newDeck(self,):
        self.__resetDeck()
        for i in range(1,7):
            for j in range(i,7):
                self.__deck.append(domino(i,j))
        self.__deck.append(domino(0,0))
        random.shuffle(self.__deck)
    def showDeck(self):
        show = []
        for i in self.__deck:
            show.append(i.showDomino())
        return show
    def sizeDeck(self):
        return len(self.__deck)
    def pullHand(self,):
        hand = []
        for i in range(7):
            domino = random.choice(self.__deck)
            hand.append(domino)
            self.__deck.remove(domino)
        return hand
    def showBone(self):
        if self.sizeDeck() == 1:
            return self.__deck[-1]
        else:
            print('Finish dealing before showing the final domino.')
class player:
    def __init__(self,un):   
        self.__name = un
class game:
    def __init__(self):
        pass



test = deck()
h1 = test.pullHand()
h2 = test.pullHand()
h3 = test.pullHand()