# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:48:34 2021

@author: ConorPhillips
"""

from apiClass import API
from playerClass import player
import threading
import time

import json

class game:
    def __init__(self):
        # Start the API, create lists to hold everyone who has played and is currently playing.
        with open('keys.json','r') as fp:
            keys = json.load(fp)
        self.__api = API(keys['APIK'],keys['APISK'],keys['BK'],keys['AT'],keys['ATS'])
        self.__p = 'O'
        self.__c = 'X'
        
        self.__players = {}
        self.__active = []
        self.__alive = True
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
    def __heartBeat(self,):
        print('boink')
    def __updateLast(self,last):
        if last > self.__last:    
            self.__last = last + 1
    def __reduceJson(self,json):
        # The twitter cursor returns a bunch of junk we don't need,
            # Let's just create a smaller dictionary of things we might find usefull...
        returnDict = {}
        returnDict['user'] = json['user']['screen_name']
        returnDict['userid'] = json['user']['id']
        returnDict['tid'] = json['id']
        returnDict['irid'] = json['in_reply_to_status_id_str']
        returnDict['iruid'] = json['in_reply_to_user_id']
        returnDict['str'] = json['full_text'].replace(f'@{json["in_reply_to_screen_name"]}','').replace(' ','').replace('\n','')
        return returnDict
    def __listen(self,):
        while self.__alive:
            tweets = self.__api.refreshCursor(self.__api.getName(),self.__last).items()
            list(map(lambda x: self.__handle(x._json),tweets))
            self.__heartBeat()
            time.sleep(15)
    def __handle(self,item):
        item = self.__reduceJson(item)
        
        if item['user'] in self.__players.keys():
            print(f'Known Player: {item["user"]}')
        else:
            print(f'Unknown Player: {item["user"]}')
            if item['irid'] == self.__gameTweet:
                if len(item['str']) == 1:
                    try:
                        move = int(item['str'])
                    except:
                        print(f'{item["str"]} can no be an integer...')
                else:
                    print(f'{item["str"]} is not a valid input...')
                    
                self.__players[item['user']] = player(item['user'],item['userid'])
        self.__updateLast(item['tid'])
    def startListen(self,):
        t1 = threading.Thread(target = self.__listen,args = [])
        t1.start()
    def killAll(self):
        self.__alive = False
    def CPR(self):
        self.__alive = True
test = game()
test.startGame()

test.startListen()

# for thread in threading.enumerate():
#     print(thread)
if 1 == 2:
    test.killAll()
    test.deleteGame()