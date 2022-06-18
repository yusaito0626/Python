# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:02:29 2022

@author: yusai
"""

import websocket
import queue
import threading

class FeedReceiver:
    __FeedReceiver = websocket.WebSocket()
    __url=""
    isListening = False
    
    feedQueue = queue.Queue()
    
    def ListeningFeed(self):
        print("ListeningFeed Thread started.")
        try:
            while True:
                msg = self.__FeedReceiver.recv()
                if(msg==""):#websocket has been closed
                    print("Connection Closed.")
                    self.isListening = False
                    break
                else:
                    self.feedQueue.put(msg)
        except:
            print("Error Occured. Return ERROR text.")
            self.feedQueue.put("ERROR")
            self.isListening = False
    
    def Initialize(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
    
    def StartListeningFeedTh(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
        self.isListening = True
        self.ListeningFeedTh.start()
        
    def SetParam(self,url):
        self.__url = url
    
    def Connect(self,url):
        self.__url = url
        self.__FeedReceiver.connect(self.__url)
    
    def Subscribe(self,msg):
        self.__FeedReceiver.send(msg)
    
    def StartListenTicker(self,InsList):
        strargs="["
        for ins in InsList:
            strargs += "{\"channel\":\"tickers\",\"instId\":\"" + ins + "\"},"
        strargs=strargs[0:len(strargs)-1] + "]"
        reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
        self.Subscribe(reqmsg)
        if(self.isListening == False):
            self.StartListeningFeedTh()
            
    
    def StartListenOrderBook(self,InsList):
        strargs="["
        for ins in InsList:
            strargs += "{\"channel\":\"books\",\"instId\":\"" + ins + "\"},"
        strargs=strargs[0:len(strargs)-1] + "]"
        reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
        self.Subscribe(reqmsg)
        if(self.isListening == False):
            self.StartListeningFeedTh()
    
    def StartListenTrade(self,InsList):
        strargs="["
        for ins in InsList:
            strargs += "{\"channel\":\"trades\",\"instId\":\"" + ins + "\"},"
        strargs=strargs[0:len(strargs)-1] + "]"
        reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
        self.Subscribe(reqmsg)
        if(self.isListening == False):
            self.StartListeningFeedTh()
    
    def recv(self):
        if(self.feedQueue.empty()):
            return ""
        else:
            return self.feedQueue.get()
        
    def Disconnect(self):
        self.__FeedReceiver.close()
        self.__FeedReceiver = websocket.WebSocket()