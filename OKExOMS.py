# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 20:25:42 2022

@author: yusai
"""

#WebSocket
import websocket
import time
import hmac
import hashlib
import base64
import requests
import json
import queue
import threading

class OMS:
    
    def StartCheckingMsg(self):#Create a thread for this function
        while True:
            msg = self.oms.recv()
            if(msg==""):#websocket has been closed
                break
            else:
                self.ackQueue.put(msg)

    oms = websocket.WebSocket()

    __url = ""
    __apiKey = ""
    __passphrase = ""
    __secretKey = ""
    
    ackQueue = queue.Queue()
    AckCheckingTh = threading.Thread(target=StartCheckingMsg)

    def SetKeys(self,apiKey,passphrase,secretKey):
        self.__apiKey = apiKey
        self.__passphrase = passphrase
        self.__secretKey = secretKey
    
    def SetURL(self,url):
        self.__url = url
        
    def GetURL(self):
        return self.__url
    
    def Connect(self):
        if(self.__url==""):
            return "Error: Invalid URL"
        if(self.__apiKey==""):
            return "Error: Invalid API Key"
        if(self.__passphrase==""):
            return "Error: Invalid Pass Phrase"
        if(self.__secretKey==""):
            return "Error: Invalid Secret Key"
        tm = str(int(time.time()))
        sign = self.__GetSign(tm,self.__secretKey,"GET","/users/self/verify","")
        LoginMsg = "{\"op\":\"login\",\"args\":[{\"apiKey\":\"" + self.__apiKey + "\",\"passphrase\":\"" + self.__passphrase + "\",\"timestamp\":\"" + tm + "\",\"sign\":\"" + sign + "\"}]}"
    
        self.oms.connect(self.__url)
        self.oms.send(LoginMsg)
    
        msg =  self.oms.recv()   
        self.AckCheckingTh.start()
        return msg
    
    def ConnectWithInfo(self,url,apiKey,passphrase,secretKey):
        self.__apiKey = apiKey
        self.__passphrase = passphrase
        self.__secretKey = secretKey
        self.__url = url
        if(self.__url==""):
            return "Error: Invalid URL"
        if(self.__apiKey==""):
            return "Error: Invalid API Key"
        if(self.__passphrase==""):
            return "Error: Invalid Pass Phrase"
        if(self.__secretKey==""):
            return "Error: Invalid Secret Key"
        tm = str(int(time.time()))
        sign = self.__GetSign(tm,self.__secretKey,"GET","/users/self/verify","")
        LoginMsg = "{\"op\":\"login\",\"args\":[{\"apiKey\":\"" + self.__apiKey + "\",\"passphrase\":\"" + self.__passphrase + "\",\"timestamp\":\"" + tm + "\",\"sign\":\"" + sign + "\"}]}"
    
        self.oms.connect(self.__url)
        self.oms.send(LoginMsg)

        msg =  self.oms.recv()   
        self.AckCheckingTh.start()
        return msg
    
    def recv(self):
        if(self.ackQueue.empty()):
            return ""
        else:
            return self.ackQueue.get()
    
    def __Subscribe(self,args):#args starts with [
        msg = "{\"op\":\"subscribe\",\"args\":" + args + "}"
        self.oms.send(msg)
        #Do not receive ack here since other subscription may exist already.
        
    def __GetSign(self,strtime,key,method,requestPath,body=""):
        if(strtime ==""):
            strtime = str(time.time())
        rawmsg = strtime + method + requestPath + body
        hmacmsg = hmac.new(key.encode(), rawmsg.encode(), hashlib.sha256)
        return base64.b64encode(hmacmsg.digest()).decode()

    
