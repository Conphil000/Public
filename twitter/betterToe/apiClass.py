# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:25:51 2021

@author: ConorPhillips
"""
import tweepy
import json

with open('keys.json','r') as fp:
    keys = json.load(fp)
    
class API():
    def __init__(self,apik,apisk,bt,at,ats):
        # You need to provide this object with the keys you got from twitter;
            # You need to ask twitter for permission to tweet from you api and get those extra keys:
                # apik:  api key provided in twitter developer portal
                # apisk: api secret key provided in twitter developer portal
                # bt:
                # at: access token provided from getting read,write, and DM access in twitter dev portal.
                # ats: access secret toke provided from *
                
            
        self.__apik = apik
        self.__apisk = apisk
        self.__bt = bt
        self.__at = at
        self.__ats = ats
        try:
            self.__connectAPI()
        except:
            print('Unable to establish API Feed.')
    def __connectAPI(self,):
        # establish a connection to your twitter API using the keys provided to the object.
        
        auth = tweepy.OAuthHandler(self.__apik, self.__apisk)
        auth.set_access_token(self.__at, self.__ats)
        self.__api = tweepy.API(auth,wait_on_rate_limit =True,wait_on_rate_limit_notify=(True))
        
        # Record the name of the twitter being used and the ID as well.
        self.__un = self.__api.me().screen_name
        self.__id = self.__api.me().id
        
    def publishTweet(self,text):
        # Use this function to tweet a message given to the function as text
        self.__api.update_status(text)
    def deleteTweet(self,tid):
        # Use this function to destroy a status id.
        self.__api.destroy_status(tid)
    def grabLastTID(self):
        # use this function to grab the tweet id of the last message sent.
        nJSON = self.__api.user_timeline(screen_name = self.__un,count=1)
        for i in nJSON:
            return i._json['id']
    def grabDM(self,n):
        # use this function to grab n messages from you Direct Messages, returns a list of size n
        return self.__api.list_direct_messages(n)
    def sendDM(self,tid,text):
        # use this function to send a DM to someone, provide it with the persons id and the text
        self.__api.send_direct_message(tid, text) 
    def refreshCursor(self,un,lastID):
        # use this function to grab all responses to a person since a given id.
        return tweepy.Cursor(self.__api.search, q=f'@{un}', since_id=lastID, tweet_mode='extended')
    def getName(self,):
        # Get the name of the API account.
        return self.__un
    def getNameID(self,):
        # Get the id of the API account.
        return self.__id
    

test = API(keys['APIK'],keys['APISK'],keys['BK'],keys['AT'],keys['ATS'])

test.publishTweet('test#1')
print(test.getName(),test.getNameID())
testid = test.grabLastTID()
if 1 == 0:    
    test.deleteTweet(testid)
                  
                  
                  
                  
                  
                  