# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 22:44:38 2020

@author: Conor
"""

import tweepy
import datetime
import threading
import time
import re
import random

class tweeter:
    def __init__(self,K):
        self.__keys = K
        self.__known = {}
        self.__tlog = {}
        self.__dif = .75
        self.__c = 'X'
        self.__p = 'O'
        self.__like = ['shaejwhite','conorphillips42']
        self.__who = {self.__c:'I',self.__p:'You','':'We'}
        self.__scoreminmax = {'I won':-1,'You w':1,'We Ti':0}
        self.__setupAPI()
        self.__active = True
        self.__condition = 'start'
        self.__postGame()
        self.__mon = threading.Thread(target = self.__monitorDM, args=[])
        self.__mon.start()
        self.__m = threading.Thread(target = self.__main,args=[])
        self.__m.start()
    def __setupAPI(self):
        try: #Connect to API
            self.__apik = self.__keys['APIK']
            self.__apisk = self.__keys['APISK']
            self.__bk = self.__keys['BK']
            self.__at = self.__keys['AT']
            self.__ats = self.__keys['ATS']
            auth = tweepy.OAuthHandler(self.__apik, self.__apisk)
            auth.set_access_token(self.__at, self.__ats)
            self.__api = tweepy.API(auth,wait_on_rate_limit =True,wait_on_rate_limit_notify=(True))
            self.__un = self.__api.me().screen_name
            self.__id = self.__api.me().id
            print('API Launching...')
        except:
            print('ERROR IN LAUNCHING API!')
    def __grabLastID(self):
        nJSON = self.__api.user_timeline(screen_name = self.__un,count=1)
        for i in nJSON:
            return i._json['id'] #This is the most recent response
    def __monitorDM(self):
        print('Monitor Launched...')
        dms = self.__api.list_direct_messages(5)
        alive = True
        while alive:
            dms = self.__api.list_direct_messages(1) # Pull one of the new DMs
            for m in dms:
                nc = m.message_create['message_data']['text'].replace(' ','').replace('\n','').lower() # What is the text in the DM? Remove spaces and make all lowercase.
                t = m.message_create['target']['recipient_id']
                s = m.message_create['sender_id']
            if s==t: # Make sure this is a DM to myself. (High Risk for DDOS)
                if nc[:3] == 'sta':
                    if self.__condition == 'start':
                        self.__api.send_direct_message(self.__id, 'Ignored, already started...') 
                    elif self.__condition == 'pause':
                        self.__api.send_direct_message(self.__id, 'Now Paused...') 
                        self.__changeCondition('pause')
                elif nc[:3] == 'pau':
                    if self.__condition == 'pause':
                        self.__api.send_direct_message(self.__id, 'Ignored, already paused...') 
                    elif self.__condition == 'start':
                        self.__api.send_direct_message(self.__id, 'Now Starting...') 
                        self.__changeCondition('start')
                elif nc[:3] == 'res':
                    self.__api.send_direct_message(self.__id, 'Now Restarting...') 
                    self.__active = False
                    time.sleep(30)
                    self.__active = True
                    self.__postGame()
                    self.__m.start()
                    self.__changeCondition('start')
                elif nc[:3] == 'bre':
                    self.__api.send_direct_message(self.__id, 'Now Breaking...') 
                    self.__active = False
                    alive = False
                elif nc[:3] == 'dif':
                    try:
                        new_dif = float(nc.split(':')[1])
                        self.__dif = new_dif
                        self.__api.send_direct_message(self.__id, f'New Difficulty: {self.__dif}')
                    except:
                        self.__api.send_direct_message(self.__id, 'Ignored, bad input...') 
            else:
                self.__api.create_block(s)
            time.sleep(60)
    def __changeCondition(self,nc):
        self.__api.list_direct_messages(1); # I've sent myself a DM so I want to remove it from the queue
        self.__condition = nc
        time.sleep(60)
    def __postGame(self):
        def deleteTID(tid):
            self.__api.destroy_status(tid)
        list(map(lambda x: deleteTID(x._json['id']),tweepy.Cursor(self.__api.user_timeline).items())) #Delete all
        self.__board = '1 |  2  | 3\n- + - + -\n4 |  5  | 6\n- + - + -\n7 |  8  | 9'
        self.__api.update_status(f"To play, respond to this tweet with a number and wait for a response!\n\nYou are {self.__p}'s!\n{self.__board}")
        tweetMain = self.__grabLastID()
        self.__tweetMain = tweetMain
        self.__tweetLast = tweetMain
    def __updateLast(self,nid):
        if nid > self.__tweetLast:
            self.__tweetLast = nid + 1
    def __refreshCursor(self):
        self.__resp = tweepy.Cursor(self.__api.search, q=f'@{self.__un}', since_id=self.__tweetLast, tweet_mode='extended')
    def __trimJSON(self,js):
        return {'un':js['user']['screen_name'],
              'tid':js['id'],
              'rid':js['in_reply_to_status_id'],
              's':js['full_text'].replace(f"@{js['in_reply_to_screen_name']}",'').replace(' ','').replace('\n','')}
    def __main(self):
        self.__queue = []
        t = threading.Thread(target = self.__exectueJobs,args=[])
        t.start()
        while self.__active:
            if self.__condition == 'start':
                
                error = 'Success'
                self.__refreshCursor()
                try:
                    tweets = list(map(lambda x: self.__trimJSON(x._json),self.__resp.items())) #Trim new tweets
                    try:
                        list(map(lambda x: self.__monitorLive(x),self.__known.keys()))
                        try:  
                            list(map(lambda x: self.__createJobs(x),reversed(tweets)))
                        except:
                            error = 'Handle Error'
                            time.sleep(30)
                        time.sleep(5)
                    except:
                        error = 'Monitor Error'
                        time.sleep(30)
                except:
                    error = 'Twitter Error'
                    time.sleep(30)
                dt = datetime.datetime.now()
                print(dt,':',error)
                self.__tlog[str(dt)] = {'error':error,'tweets':tweets}
        print('i stop:self.__main')   
    def __kill(self,key):
        self.__known[key]['status'] = 'dead'
    def __addError(self,key):
        self.__known[key]['count_error']+=1
        if self.__known[key]['count_error'] > 20:
            self.__kill(key)
            self.__api.create_block(key)
    def __reset(self,key):
        self.__known[key]['moves'] = [1,2,3,4,5,6,7,8,9]
        self.__known[key]['board'] = '123456789'
        self.__known[key]['known'] = {}
        self.__known[key]['status'] = 'live'
        self.__known[key]['inactive'] = 0
    def __start(self,t):
        key = t['un']
        if t['s'].isdigit():
            self.__reset(key)
            self.__known[key]['score'] = [0,0,0]
            self.__player(t)
        else:
            self.__kill(key)
            self.__inputError(t)
    def __player(self,t):
        key = t['un']
        if t['s'] in self.__known[key]['board']:
            self.__makeMove(key, t['s'], self.__p)
            self.__known[key]['rid'] = 123
            self.__computer(t)
        else:
            if len(self.__known[key]['moves']) == 9:  
                self.__kill(key)
            self.__moveError(t)
    def __tie(self,key):
        self.__known[key]['score'][1] += 1
        self.__known[key]['score'][2] += 1
    def __removeMove(self,key):
        self.__known[key]['moves'] = list(set(re.sub('\D','',self.__known[key]['board'])))
    def __makeMove(self,key,move,char):
        self.__known[key]['board'] = self.__known[key]['board'].replace(str(move),char)
        self.__removeMove(key)
    def __tweetWin(self,t,w,b):
        key = t['un']
        scores = self.__known[key]['score']
        self.__queue.append({'un':t['un'],'id':t['tid'],'s':f"{b}\n{w}! You have won {scores[0]} out of {scores[2]} game{'s' if scores[2] != 1 else ''}, {scores[1]} tie{'s' if scores[1] != 1 else ''}.",'code':'win'})
    def __computer(self,t):
        key =  t['un']
        w = self.__win(self.__known[key]['board'])
        if w[:5] != '' and w[:5] != 'We Ti':
            self.__known[key]['score'][0] += 1
            self.__known[key]['score'][2] += 1
            self.__tweetWin(t,w,self.__buildBoard(self.__known[key]['board']))
        elif w[:5] == 'We Ti':
            self.__known[key]['score'][1] += 1
            self.__known[key]['score'][2] += 1
            self.__tweetWin(t,w,self.__buildBoard(self.__known[key]['board']))
        else:
            movesAvail = self.__known[key]['moves']
            if key.lower() in self.__like:
                cmin = -999
                moves = []
                for i in movesAvail:
                    newMoves = movesAvail.copy()
                    newMoves.remove(i)
                    b = self.__known[key]['board']
                    b = b.replace(i,self.__c)
                    v = self.__minimax(b,newMoves,True)
                    if v > cmin:
                        moves = []
                        moves.append(i)
                        cmin = v
                    elif cmin == v:
                        moves.append(i)
            elif random.random() < self.__dif:
                cmin = 999
                moves = []
                for i in movesAvail:
                    newMoves = movesAvail.copy()
                    newMoves.remove(i)
                    b = self.__known[key]['board']
                    b = b.replace(i,self.__c)
                    v = self.__minimax(b,newMoves,True)
                    if v < cmin:
                        moves = []
                        moves.append(i)
                        cmin = v
                    elif cmin == v:
                        moves.append(i)
            else:
                moves = movesAvail
            move = random.choice(moves)
            self.__makeMove(key,move,self.__c)
            w = self.__win(self.__known[key]['board'])
            if w != '':
                self.__known[key]['score'][2] += 1
                self.__tweetWin(t,w,self.__buildBoard(self.__known[key]['board']))
            else:
                self.__queue.append({'un':t['un'],'id':t['tid'],'s':f"Respond to this tweet with your next move!\n{self.__buildBoard(self.__known[key]['board'])}",'code':''}) #Game not Finished
    def __minimax(self, board, moves,player):
        w = self.__win(board)
        if w != '':
            return self.__scoreminmax[w[:5]]
        if player == True:
            cmax = -999999
            for i in moves:
                nmoves = moves.copy()
                nmoves.remove(i)
                nb = board.replace(i,self.__p)
                nmax = self.__minimax(nb,nmoves,False)
                cmax = max(nmax,cmax)
            return cmax
        elif player == False:
            cmin = 999999
            for i in moves:
                nmoves = moves.copy()
                nmoves.remove(i)
                nb = board.replace(i,self.__c)
                nmin = self.__minimax(nb,nmoves,True)
                cmin = min(nmin,cmin)
            return cmin
    def __same(self,items):
        return all(x == items[0] for x in items)
    def __win(self,board):
        for i in range(0,3):
            set1 = board[3*i:3*(i+1)]
            if self.__same(set1):
                how = 'won Horizontally'
                who = set1[0]
                return f'{self.__who[who]} {how}'
        for i in range(0,3):
            set1 = board[0+i:1+i]+board[3+i:4+i]+board[6+i:7+i]
            if self.__same(set1):
                how = 'won Vertically'
                who = set1[0]
                return f'{self.__who[who]} {how}'
        di1 = board[0:1]+board[4:5]+board[8:9]
        di2 = board[2:3]+board[4:5]+board[6:7]
        if self.__same(di1) or self.__same(di2):
            how = 'won Diagonally'
            who = board[4:5]
            return f'{self.__who[who]} {how}'
        if len(re.sub('\D','',board)) == 0:
            who = ''
            how = 'Tied'
            return f'{self.__who[who]} {how}'
        return ''
    def __buildBoard(self,b):
        blist = []
        for i in range(0,3):
            blist.append(f'{b[3*i:3*i+1]} |  {b[3*i+1:3*i+2]}  | {b[3*i+2:3*i+3]}')
        return '\n- + - + -\n'.join(blist)
    def __createJobs(self,t):
        key = t['un']
        if key in self.__known.keys():
            if self.__known[key]['status'] == 'live':
                if t['rid'] == self.__known[key]['rid']:
                    self.__player(t) #Try to continue a game
                else:
                    self.__wrongError(t) #Responded to wrong tweet
            elif self.__known[key]['status'] in ['dead','inactive']:
                if t['rid'] == self.__tweetMain:
                    self.__reset(t['un']) #Starting a New Game
                    self.__player(t) 
                elif self.__known[key]['rid'] == t['rid'] and self.__known[key]['status'] == 'inactive':
                    self.__inactiveError(t) #Responded to an inactive game
                    self.__kill(key)
                else:
                    self.__addError(key) #Trolling Ignore
        else:
            self.__known[key] = {'rid':self.__tweetMain,'status':'','count_error':0}
            if t['rid'] == self.__known[key]['rid']:
                self.__start(t) #Try to start a new game
            else:
                self.__addError(key)
                pass #Not someone trying to start a game, Ignore.
        self.__updateLast(t['tid'])
    def __monitorLive(self,key):
        if self.__known[key]['status'] == 'live':
            self.__known[key]['inactive'] += 1
            if self.__known[key]['inactive'] > 120:
                self.__known[key]['status'] = 'inactive'
                self.__known[key]['score'][2] += 1
    def __exectueJobs(self):
        while self.__active:
            if self.__condition == 'start':
                try:
                    copy = self.__queue.copy()
                    for i in copy:
                        key = i['un']
                        tweet = f"@{key} {i['s']}"
                        self.__api.update_status(tweet,in_reply_to_status_id=i['id'])
                        self.__queue.remove(i)
                        if i['code'] == 'error':
                            self.__addError(key)
                        else:
                            if i['code'] == '':
                                self.__known[key]['rid'] = self.__grabLastID()
                                self.__known[key]['inactive'] = 0
                            elif i['code'] == 'win':
                                self.__kill(key)
                            else:
                                print('i cant handle {}'.format(i['code']))
                            time.sleep(.25)
                except:
                    print('Job Error')
                    time.sleep(30)
        print('i stop:self.__handleJobs') 
    #ERROR MESSAGES:
    def __inactiveError(self,t):
        self.__queue.append({'un':t['un'],'id':t['tid'],'s':'Game marked as inactive, start a new game!','code':'error'})
    def __wrongError(self,t):
        self.__queue.append({'un':t['un'],'id':t['tid'],'s':'You responded to the wrong tweet!','code':'error'})
    def __inputError(self,t):
        self.__queue.append({'un':t['un'],'id':t['tid'],'s':'Try using an input I would understand!','code':'error'})
    def __moveError(self,t):
        self.__queue.append({'un':t['un'],'id':t['tid'],'s':'Please select an available move!','code':'error'})
    #LOG
    def export_tlog(self):
        return self.__tlog
    def export_known(self):
        return self.__known
    
engine = tweeter(K)      




















