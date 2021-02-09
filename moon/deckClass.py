# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:16:54 2021

@author: ConorPhillips
"""
import random

from dominoClass import domino

class deck:
    def __init__(self):
        self.__resetDeck()
    def __resetDeck(self,):
        # Use this function to reset the deck.
        self.__deck = []
    def newDeck(self,):
        # Use this function to create a new deck.
        self.__resetDeck()
        for i in range(1,7):
            for j in range(i,7):
                self.__deck.append(domino(i,j))
        self.__deck.append(domino(0,0))
        random.shuffle(self.__deck)
    def showDeck(self):
        # Use this function to show the current deck.
        show = []
        for i in self.__deck:
            show.append(i.showDomino())
        return show
    def sizeDeck(self):
        # Use this function to show how many cards are left in the deck.
        return len(self.__deck)
    def pullHand(self,):
        # Use this function to pull 7 random cards into a list
        hand = []
        for i in range(7):
            domino = random.choice(self.__deck)
            hand.append(domino)
            self.__deck.remove(domino)
        return hand
    def showBone(self):
        # Use this function to show the last domino available.
        if self.sizeDeck() == 1:
            return self.__deck[-1]
        else:
            print('Finish dealing before showing the final domino.')