# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:06:07 2021

@author: ConorPhillips
"""


class player:
    def __init__(self,name,nameid):
        # When someone responds to the initial tweet we want to create a player:
            # A player has an @ name and an id associated with their twitter account.
            # You will only ever want one player per person.
        # When someone replies we will store their name and id
        self.__name = name
        self.__nameid = nameid
        self.__status = 'wait'
        
        # When someone creates a character we will start counting win/loss/number of games:
        self.__numGames = 0
        self.__numWins = 0
        self.__numLoss = 0
        
        # Let's set the normal favor to be 0.4,
            # Favor indicates how difficult the game will be for the player.
            # If someone has a favor of 0 the computer will always play the best move,
            # if someon has a favor of .5 the computer will play the best move 50% of the time.
        self.changeFavor(0.4)
    def getName(self):
        # If you want to identify the player you should call this function.
        return self.__name
    def getNameID(self):
        # If you want to identify the player id you should call this function.
        return self.__nameid
    def getStatus(self,):
        # If you want to know the current status of a player you should call this function.
        return self.__status
    def getWins(self,):
        # If you want to know how many games someone has won call this function.
        return self.__numWins
    def getLosses(self,):
        # if you want to know how many games someone has lost call this function.
        return self.___numLoss
    def getNumGames(self,):
        # If you want to know how many games someone has attempted call this fucntion.
        return self.__numGames
    def changeFavor(self,n):
        # If you want to change the current favor of a player you should call this function with a value between 1 and 0.
        if n <= 1 and n > 0:
            self.__favor = n
    def changeStatus(self,status):
        # If you want to change the current status of a player you should call this function with a new status as an input.
        self.__status = status
    def addGame(self,):
        # If you want to increase the game count by 1 call this function.
        self.__numGames += 1
    def addWin(self,):
        # If you want to increase the win count by 1 call this function.
        self.__numWins += 1
    def addLoss(self,):
        # If you want to increase the loss count by 1 call this function.
        self.__numLoss += 1
