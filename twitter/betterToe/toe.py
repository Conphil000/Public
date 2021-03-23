
# Minimum Viable Product: Toe

import tweepy
import os
import time
import json
import random
from datetime import datetime
import itertools
import sys

def heartbeat():
    print('badunka')

""" Change working directory """
cwd = os.getcwd()
os.chdir(f'{cwd}//twitter//betterToe')

""" Import my Twitter development keys from the file keys.json; you can create this file for your own application """

with open('keys.json') as json_file:
    keyPayload = json.load(json_file)

""" Class Development """
class aAPI:
    """ Handle all API related tasks"""

    def __init__(self,keyPayload):
        """
        Define key parameters from keyPayload

        :keyPayload: The keys associated with twitter authentication.
                        {"APIK": "API Key"
                        "SAPIK": "API Secret Key", 
                        "BT": "Bearer Token", 
                        "AT": "Access Token", 
                        "SAT": "Access Token Secret"}
        """
        try:
            self.__apik = keyPayload['APIK']
            self.__sapik = keyPayload['SAPIK']
            self.__at = keyPayload['AT']
            self.__sat = keyPayload['SAT']
            self.__bt = keyPayload['BT']
            try:
                self.__launchAPI()
            except:
                # If Tweepy is unable to connect to your account,
                # throw an error.
                print('Unable to connect to API.')
                return
        except:
            # If all keys are not provided in the keyPayLoad,
            # throw an error.
            print('Unable to unpack Payload.')
            return 

        # Store some items from the me() method
        # https://docs.tweepy.org/en/latest/api.html

        self.__user = self.API.me().screen_name
        self.__userID = self.API.me().id

    def __launchAPI(self,):
        """
        Connect to Twitter API using Tweepy
        """
        # Use Tweepy documentation to handle authentication
        # https://docs.tweepy.org/en/latest/getting_started.html
        
        auth = tweepy.OAuthHandler(self.__apik, self.__sapik)
        auth.set_access_token(self.__at, self.__sat)

        self.API = tweepy.API(auth,wait_on_rate_limit =True,wait_on_rate_limit_notify=(True))

    def getRecentPost(self,):
        """
        Get the last tweet sent by the API user
        """
        latest = self.API.user_timeline(user_id = self.__userID,count=1)
        return latest[0].id
    def getRecentMention(self,sinceID = 1, nTweets = 25):
        """
        Get recent tweets sent to the API user

        :sinceID: The earliest tweet you would want to include,
                    normally this is that last handled ID + 1
        :nTweets: This is the number of tweets the method will pull, 
                    balance this number with frequency to satisfy rate limits
        """
        # Rate Limits are a pain in the ASS; most of this project is hacking these limits haha
        # https://developer.twitter.com/en/docs/twitter-api/v1/rate-limits

        responses = self.API.mentions_timeline(since_id = sinceID, count = 25)
        return responses
    def sendTweet(self,message,payload = {}):
        """
        Send a response
        
        :message: What do i want to say?
        :payload: if you want to respond to a tweet you should provide the payload for the tweet, if not it posts to timeline
        """
        if payload == {}:
            # Post a tweet to your timeline
            self.API.update_status(message)
        else:
            # Post a tweet in response to someone
            try:
                self.API.update_status(f"@{payload._json['user']['screen_name']}\n {message}",in_reply_to_status_id = payload._json['id'])
            except:
                print(sys.exc_info()[0])
                file_object = open(r'response_exceptions.txt','a')
                file_object.write(f"{datetime.now().strftime('%c')}: @{payload._json['user']['screen_name']} {message}\n")
                file_object.close()


        
class aPlayer:
    """ Handle all Player related tasks """
    player = 'X'
    computer = 'O'
    board = '1 |  2  | 3\n- + - + -\n4 |  5  | 6\n- + - + -\n7 |  8  | 9'
    def __init__(self,payload):
        """
        Each instance of this class belongs to an individual twitter account playing

        :payload: The original tweet used to create a player instance.
        """

        # Store current in_reply_to_status_id and create a board + stats
        self.RID = payload._json['in_reply_to_status_id']

        self.score = [0,0,0]
        self.inactive = 0
        self.error = 0

        self.resetGame()

    def resetGame(self,):
        """
        Reset the game board
        """
        self.availableMoves = [ 1,2,3,
                                4,5,6,
                                7,8,9]
        self.playerMoves = []
        self.computerMoves = []
        
        def newDifficulty(score):
            if score[0] == score[1]:
                diff = 0.3
            if score[0] > score[1]:
                diff = 0.6
            if score[0] > 2 * score[1]:
                diff = 1
            if score[1] > score[0]:
                diff = 0.1
            return diff

        self.diff = newDifficulty(self.score)

    def checkWin(self,moves):
        """
        Check to see if someone has a winning hand

        :moves: What moves has the player made in the current game
        """

        wins = ['123','456','789','147','258','369','159','357']
        winDef = {'123':'horizontal','456':'horizontal','789':'horizontal','147':'vertical','258':'vertical','369':'vertical','159':'diagnonal','357':'diagnonal'}
        # See if any combination of the moves provided matches a win.
        ordered_moves = [i for i in ['1','2','3','4','5','6','7','8','9'] if i in moves]
        for i in itertools.combinations(ordered_moves,3):
            if ''.join(i) in wins:
                return [True,winDef[''.join(i)]]

        # If no winner and no moves left then tie
        if len(self.availableMoves) == 0:
            return [True,'tie']

        # No winner
        return [False,None]

    def cleanText(self,payload):
        """
        Remove @{Mention} and empty spaces from the tweet, this will hopefully leave only the move.

        :payload: This is the data associated with the recent mention
        """
        string = payload._json['text'].replace(f"@{payload._json['entities']['user_mentions'][0]['screen_name']}",'')
        string = string.replace(' ','')
        return string 
    def updatePayload(self,payload):
        """
        Update the instance payload to the most recent mention

        :payload: This is the data associated with the recent mention
        """
        self.payload = payload
    def validMove(self,):
        """
        See if the move provided by the player is valid

        """

        move = self.cleanText(self.payload)
        
        try:
            # Check if the move is a single digit
            if len(move) == 1:
                # Check if the move is an integer
                move = int(move)
                if move in self.availableMoves:
                    self.availableMoves.remove(move)
                    self.playerMoves.append(str(move))
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False
    def currentBoard(self,):
        '''
        Return a string of the current board
        '''
        # Replace all the current moves with the its respected character
        cBoard = self.board
        for i in self.playerMoves:
            cBoard = cBoard.replace(str(i),self.player)
        for i in self.computerMoves:
            cBoard = cBoard.replace(str(i),self.computer)
        return cBoard
    def minimax(self, moves, pmoves, cmoves, player):
        """
        Good ol MiniMax

        :moves: The moves that are available
        :pmoves: The moves the player has already made
        :cmoves: The moves the computer has alread made
        :player: Whose turn is it? (False if Computer, True if player)
        """
        ### Close Recursion ###
        wp = self.checkWin(pmoves)
        wc = self.checkWin(cmoves)

        if wp != None or wc != None:
            if wp[1] == 'tie' and wc[1] == 'tie':
                return 0
            elif wp[1] != None:
                return 1
            elif wc[1] != None:
                return -1

        ### Start Recursion ###
        if player == True:
            cmax = -999999
            for i in moves:
                nmoves = moves.copy()
                nmoves.remove(i)
                nb = pmoves.copy()
                nb.append(str(i))
                nmax = self.minimax(nmoves,nb,cmoves,False)
                cmax = max(nmax,cmax)
            return cmax
        elif player == False:
            cmin = 999999
            for i in moves:
                nmoves = moves.copy()
                nmoves.remove(i)
                nb = cmoves.copy()
                nb.append(str(i))
                nmin = self.minimax(nmoves,pmoves,nb,True)
                cmin = min(nmin,cmin)
            return cmin

    def computerMove(self,):
        """
        The computer will use the available moves to make a decision
        """
        guess = random.random()
        if guess > self.diff:
            # Random choice from available
            move = random.choice(self.availableMoves)
        else:
            # Use minimax to select the best possible move from available
            best = 99999999
            for i in random.sample(self.availableMoves,len(self.availableMoves)):
                
                nam = self.availableMoves.copy()
                nam.remove(i)
                pm = self.playerMoves.copy()
                cm = self.computerMoves.copy()
                cm.append(str(i))
                out = self.minimax(nam,pm,cm,True)
                if out < best:
                    best = out
                    move = i

        # Add the move to computers list and remove the move from available
        self.computerMoves.append(str(move))
        self.availableMoves.remove(move)

    def getRID(self,):
        """
        Return the ID that the player needs to respond to.
        """
        return self.RID

class aGame:
    """ The MainLoop for Toe"""
    def __init__(self,keyPayload):
        """
        Define key parameters from keyPayload

        :keyPayload: The keys associated with twitter authentication.
                        {"APIK": "API Key"
                        "SAPIK": "API Secret Key", 
                        "BT": "Bearer Token", 
                        "AT": "Access Token", 
                        "SAT": "Access Token Secret"}
        """
        self.__intMain = 15
        self.__active = True
        self.__currentID = 0

        # Keep track of known games
        self.known = {}   


        # Initialize the API associated with the keyPayload
        self.API = aAPI(keyPayload)
        try:
            # Check if I am able to use the API
            self.API.API.me()
        except:
            # If code fails to create an API Instance there is no reason
            # to continue.
            print('Failed to launch API')
            return
        # Post a Game tweet
        self.API.sendTweet('Respond to this tweet with a number 1-9 to play, you are X.')

        # Check if there is an existing game tweet
        self.gameID = self.API.getRecentPost()

        # There needs to be a way to store latest tweet id to look for
        self.lastID = self.gameID + 1

        # Initialize the Main Loop for the Twitter Application
        self.startMain()
    def handle(self,payload):
        """ 
        Decide what to do with tweets that are in response to API user
        
        :payload: All the data associated with a single tweet
        """
        # Keep track of what tweets have been handled.
        if payload._json['id'] > self.lastID:
            self.lastID = payload._json['id']

        # This is the player id to check against known
        gid = payload._json['user']['id']

        try:
            if gid not in self.known.keys():
                # New Player 

                # Mark this player as Known
                self.known[gid] = aPlayer(payload)

                if payload._json['user']['followers_count'] >= 50:
                    # New Player is Active
                    if payload._json['in_reply_to_status_id'] == self.gameID:
                        # Correct status to reply to

                        # Update payload with the new mention
                        self.known[gid].updatePayload(payload)
                        # Check if the player has made a valid move
                        if self.known[gid].validMove():
                            # Made a Valid Move

                            # Computer will now select a move
                            self.known[gid].computerMove()

                            # Reset the Error Counter
                            self.known[gid].error = 0

                            # Respond to the tweet appropriately 
                            self.API.sendTweet(self.known[gid].currentBoard(),self.known[gid].payload)

                            # Store the RID
                            self.known[gid].RID = self.API.getRecentPost()

                        else:
                            # Did not make a valid move
                            self.known[gid].error += 1

                            # Respond to the tweet appropriately 
                            self.API.sendTweet("You responded to the correct tweet but I don't understand what you mean.",self.known[gid].payload)
                            
                    else:
                        # New and Active Player is SPAM
                        self.known[gid].error += 1

                        # Respond to the tweet appropriately 
                        self.API.sendTweet("I'm ignoring you.",self.known[gid].payload)
                        
                else:
                    # New Player is not ACTIVE 
                    self.known[gid].error += 1

                    # Respond to the tweet appropriately
                    self.API.sendTweet("You don't have enough followers to play. :'(",self.known[gid].payload)
                    
            else:
                # Known Player
                # Update the payload
                
                self.known[gid].updatePayload(payload)
                if payload._json['in_reply_to_status_id'] == self.known[gid].getRID():
                    # Known Player responded to the correct tweet
                    
                    
                    if self.known[gid].validMove():
                        # Known Player Made a Valid Move

                        # Check for win
                        win = self.known[gid].checkWin(self.known[gid].playerMoves)

                        if win[0] == True:
                            if win[1] == 'tie':
                                # Tie
                                self.API.sendTweet(f"We {win[1]}d: \n {self.known[gid].currentBoard()}",self.known[gid].payload)
                                self.known[gid].score[2] += 1
                                # Set game back to start and begin looking for a new response to original game tweet
                                self.known[gid].resetGame()
                                self.known[gid].RID = self.gameID
                        
                                # break function
                                return
                            else:
                                # Player won
                                self.API.sendTweet(f"You won {win[1]}ly: \n {self.known[gid].currentBoard()}",self.known[gid].payload)

                                # Add a win
                                self.known[gid].score[0] += 1

                                # Set game back to start and begin looking for a new response to original game tweet
                                self.known[gid].resetGame()
                                self.known[gid].RID = self.gameID

                                # break function
                                return
                        else:
                            # Computer will now choose a move
                            self.known[gid].computerMove()

                            # Check for win or tie
                            win = self.known[gid].checkWin(self.known[gid].playerMoves)
                            if win[0] == True:
                                # Computer Won
                                self.API.sendTweet(f"I won {win[1]}ly: \n {self.known[gid].currentBoard()}",self.known[gid].payload)
                                self.known[gid].score[1] += 1
                                # Set game back to start and begin looking for a new response to original game tweet
                                self.known[gid].resetGame()
                                self.known[gid].RID = self.gameID
                                
                                # break function
                                return
                        self.known[gid].error = 0
                        self.API.sendTweet(self.known[gid].currentBoard(),self.known[gid].payload)
                        self.known[gid].RID = self.API.getRecentPost()
                    else:
                        # Did not make a valid move
                        self.API.sendTweet("You responded to the correct tweet but I don't understand what you mean, try again on my previous response.",self.known[gid].payload)
                        self.known[gid].error += 1
                else:
                    # Known Player responded to the wrong tweet
                    self.API.sendTweet('Your responded to the wrong tweet, double check that you responded to the correct tweet.',self.known[gid].payload)
                    self.known[gid].error += 1
            if self.known[gid].error == 14:
                self.API.sendTweet('Play correctly or not at all, final warning.',self.known[gid].payload)
            elif self.known[gid].error > 14:
                self.API.API.create_block(gid)
        except:
            self.API.sendTweet('u breaky me code, i sendy u $',self.known[gid].payload)
            print(sys.exc_info()[0])
            file_object = open(r'exceptions.txt','a')
            file_object.write(f'{datetime.now().strftime("%c")}: {payload}\n')
            file_object.close()
    def startMain(self,):
        numLoops = 0
        while self.__active == True:
            # Find new mentions
            new = self.API.getRecentMention(self.lastID)

            # Handle each mention in chronological order FIFO
            handled = list(map(lambda x: self.handle(x), reversed(new)))
            del handled

            heartbeat()
            numLoops += 1
            time.sleep(self.__intMain)
    def kill(self,):
        self.__active = False


mainloop = aGame(keyPayload)

#temp = test.known[812177924]
#test.API.sendTweet(temp.currentBoard(),temp.payload)

#test.API.sendTweet('test')
#temp.payload._json['user']['screen_name']
#temp = test.known