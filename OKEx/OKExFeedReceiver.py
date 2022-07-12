# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:02:29 2022

@author: yusai
"""

import websocket
import queue
import threading
import requests

import OKExInstrument
import OKExParser

class FeedReceiver:
    __FeedReceiver = websocket.WebSocket()
    __url=""
    isListening = False
    
    feedQueue = queue.Queue()
    
    insList = {}
    
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
            
    def updatingBoard(self,parser,optimizer):
        while(True):
            line = self.recv()
            if(line=="ERROR"):
                break
            if(line!=""):
                obj = parser.Parse(line)
                if(obj.dataType=="push"):
                    if(obj.arg["instId"] in self.insList):
                        ins = self.insList[obj.arg["instId"]]
                        ins.updateBooks(obj)
                        optimizer.calcFactors(ins)
                parser.pushPDataObj(obj)
    
    def Initialize(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
        
    def StartListeningFeedTh(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
        self.isListening = True
        self.ListeningFeedTh.start()
        
    def startUpdatingBoardTh(self,parser,optimizer):
        self.updatingBoardTh = threading.Thread(target=self.updatingBoard,args=(parser,optimizer))
        self.updatingBoardTh.start()
        
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
            return self.feedQueue.get_nowait()
        
    def Disconnect(self):
        self.__FeedReceiver.close()
        self.__FeedReceiver = websocket.WebSocket()
        
    def getInstrmentList(self,ulyList):
        rest_url = "https://www.okx.com/"
        for uly in ulyList:
            spot_reqmsg ="api/v5/public/instruments?instType=SPOT&instId=" + uly
            response = requests.get(rest_url+spot_reqmsg)
            res=response.json()
            for obj in res["data"]:
                if(obj["instId"] in self.insList):
                    ins = self.insList[obj["instId"]]
                    ins.setInsData(obj)
                else:
                    ins = OKExInstrument.Instrument()
                    ins.setInsData(obj)
                    self.insList[ins.instId] = ins
            fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=" + uly
            response = requests.get(rest_url+fut_reqmsg)
            res=response.json()
            for obj in res["data"]:
                if(obj["instId"] in self.insList):
                    ins = self.insList[obj["instId"]]
                    ins.setInsData(obj)
                else:
                    ins = OKExInstrument.Instrument()
                    ins.setInsData(obj)
                    self.insList[ins.instId] = ins
            swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=" + uly
            response = requests.get(rest_url+swap_reqmsg)
            res=response.json()
            for obj in res["data"]:
                if(obj["instId"] in self.insList):
                    ins = self.insList[obj["instId"]]
                    ins.setInsData(obj)
                else:
                    ins = OKExInstrument.Instrument()
                    ins.setInsData(obj)
                    self.insList[ins.instId] = ins
                #End of if(obj["instId"] in self.insList):
        #End of for uly in ulyList:
        return self.insList
    #End of def getInstrmentList(self,ulyList):
 