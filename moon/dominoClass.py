# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 19:16:09 2021

@author: ConorPhillips
"""

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
