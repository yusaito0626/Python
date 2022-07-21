# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:02:29 2022

@author: yusai
"""

import websocket
import queue
import threading
import requests
import time

import OKExInstrument
import OKExParser
import OKExOptimizer
import OKExOMS

class FeedReceiver:
    __FeedReceiver = websocket.WebSocket()
    __url=""
    isListening = False
    stopPing = False
    
    feedQueue = queue.Queue()
    
    insList = {}
    
    def sendPing(self,sec):
        while(True):
            time.sleep(sec)
            if(self.stopPing):
                self.stopPing = False
                break
            self.__FeedReceiver.send("ping")
    
    def ListeningFeed(self):
        print("[FeedReceiver] ListeningFeed Thread started.")
        try:
            while True:
                msg = self.__FeedReceiver.recv()
                if(msg==""):#websocket has been closed
                    print("[FeedReceiver] Connection Closed.")
                    self.isListening = False
                    break
                else:
                    self.feedQueue.put(msg)
        except:
            print("[FeedReceiver] Error Occured. Return ERROR text.")
            self.feedQueue.put("ERROR")
            self.isListening = False
            
    def updatingBoard(self,parser,optimizer):
        while(True):
            line = self.recv()
            if(line=="ERROR"):
                break
            if(line!="" and '{' in line and '}' in line):
                obj = parser.Parse(line)
                if(obj.dataType=="push"):
                    if(obj.arg["instId"] in self.insList):
                        ins = self.insList[obj.arg["instId"]]
                        blOptimize = ins.updateBooks(obj)
                        optimizer.calcFactors(ins)
                        if(blOptimize):
                            optimizer.Optimize(ins)
                parser.pushPDataObj(obj)
    
    def updatingBoardSingle(self):
        while(True):
            line = self.recv()
            if(line=="ERROR"):
                break
            if(line!="" and '{' in line and '}' in line):
                obj = OKExParser.parser.Parse(line)
                if(obj.dataType=="push"):
                    if(obj.arg["instId"] in self.insList):
                        ins = self.insList[obj.arg["instId"]]
                        blOptimize = ins.updateBooks(obj)
                        OKExOMS.oms.updatingOrdersSingle()
                        OKExOptimizer.optimizer.calcFactors(ins)
                        if(blOptimize):
                            OKExOptimizer.optimizer.Optimize(ins)
                OKExParser.parser.pushPDataObj(obj)
    
    
    def Initialize(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
        
    def StartListeningFeedTh(self):
        self.ListeningFeedTh = threading.Thread(target=self.ListeningFeed,args=())
        self.isListening = True
        self.ListeningFeedTh.start()
        #self.sendPingTh = threading.Thread(target=self.sendPing,args=(20,))
        #self.sendPingTh.start()
        
    def startUpdatingBoardTh(self,parser,optimizer):
        self.updatingBoardTh = threading.Thread(target=self.updatingBoard,args=(parser,optimizer))
        self.updatingBoardTh.start()

    def startUpdatingBoardSingleTh(self):
        self.updatingBoardTh = threading.Thread(target=self.updatingBoardSingle,args=())
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

        


feedReceiver = FeedReceiver()
 