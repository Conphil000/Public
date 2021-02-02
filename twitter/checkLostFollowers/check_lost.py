# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 20:44:44 2020

@author: Conor
"""

import os

import pickle
cwd = os.getcwd()
import tweepy

os.chdir('C:/Users/Conor/Desktop')
from importlib import reload
import API_Explore
reload(API_Explore)
from API_Explore import keys
os.chdir(cwd)

CK = keys['APIK']
CS = keys['APISK']

AT = keys['AT']
ATS = keys['ATS']

auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)

api = tweepy.API(auth,wait_on_rate_limit =True,wait_on_rate_limit_notify=(True))


shae = api.get_user('shaejwhite').id

from datetime import datetime, timedelta
import time


os.chdir('C:/Users/Conor/Desktop/public/twitter')
while True:
    x = []
    list1 = api.followers_ids(api.me().id)
    with open('followers.pickle', 'rb') as handle:
        list2 = pickle.load(handle)
    with open('followers.pickle', 'wb') as handle:
        pickle.dump(list1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    unfollowed = list(set(list2) - set(list1))
    
    for i in unfollowed:
        x.append( api.get_user(id=i).screen_name)
        api.destroy_friendship(i)
    if len(x) == 0:
        api.send_direct_message(shae, 'No one Unfollowed me! Thanks for Following me! Black SUS n THIKKKK!!')
    else:
        api.send_direct_message(shae,f"I have been unfollowed by: {','.join([f'@{i}' for i in x])}. Automated message and i love u!")

    now = datetime.now()
    next = now + timedelta(hours=24)
    wait = (next - now).total_seconds()
    break
    time.sleep(wait)
    
    
    
    
    
    
    
    