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
import queue
import threading

import OKExEnums
import OKExMessage
import OKExOrder

class OMS:
    
    def StartCheckingMsg(self):#Create a thread for this function
        print("OMS starts listening msg.")
        try:
            while True:
                msg = self.oms.recv()
                if(msg==""):#websocket has been closed
                    print("The websocket disconnected.")
                    self.ackQueue.put("END")
                    self.isListening = False
                    break
                else:
                    self.ackQueue.put(msg)
        except:
            print("Error Occured. Return ERROR text.")
            self.ackQueue.put("ERROR")
            self.isListening = False

    def __init__(self):
        self.oms = websocket.WebSocket()

        self.__url = ""
        self.__apiKey = ""
        self.__passphrase = ""
        self.__secretKey = ""
    
        self.ackQueue = queue.Queue()
        self.isListening = False
        self.ordIndex = 0
        
        self.lmt_sz = 0
        self.ordList = {}
        self.liveOrdList = {}#From sending new order to filled or receiving cancel ack
        self.nullOrd = OKExOrder.order()
        self.nullOrd.px = -1
        
        self.tktQueue = queue.Queue()#Store ticket object and output them at the end of the day.
        
        #Use Pool?
        self.numOfOrdObj = 100000
        self.orderPool = queue.LifoQueue(self.numOfOrdObj * 2)
        i = 0
        while(i < self.numOfOrdObj):
            self.orderPool.put(OKExOrder.order())
            i += 1
        self.numOfMsgOrd = 200000
        self.msgOrdPool = queue.LifoQueue(self.numOfMsgOrd * 2)
        i = 0
        while(i < self.numOfMsgOrd):
            self.msgOrdPool.put(OKExMessage.msgOrder())
            i += 1
            
        self.AckCheckingTh = threading.Thread(target=self.StartCheckingMsg,args=())
        
        
    def startListeningMsg(self):
        self.AckCheckingTh = threading.Thread(target=self.StartCheckingMsg,args=())
        self.isListening = True
        self.AckCheckingTh.start()
        
    def readKeyFile(self,filename):
        f= open(filename,'r')
        line = ""
        idx = -1
        key = ""
        value = ""
        while f:
            line = f.readline()
            idx = line.find('=')
            if(idx >= 0):
                line = line.strip()#Erase \n
                key = line[0:idx]
                value = line[idx+1:]
                if(key=="apiKey"):
                    self.__apiKey = value
                elif(key=="passphrase"):
                    self.__passphrase = value
                elif(key=="secretKey"):
                    self.__secretKey = value
                elif(key=="URL"):
                    self.__url = value
            if(not line):
                f.close()
                break

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
        if(self.isListening == False):
            self.startListeningMsg()
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
        if(self.isListening == False):
            self.startListeningMsg()
        return msg
    
    def Disconnect(self):
        self.oms.close()
        self.oms = websocket.WebSocket()
    
    def recv(self):
        if(self.ackQueue.empty()):
            return ""
        else:
            return self.ackQueue.get_nowait()
    
    def __Subscribe(self,args):#args starts with [
        msg = "{\"op\":\"subscribe\",\"args\":" + args + "}"
        self.oms.send(msg)
        #Do not receive ack here since other subscription may exist already.
    
    def subscribeAccount(self,ccy=""):
        args=""
        if ccy!="":
            args = "[{\"channel\":\"account\",\"ccy\":\"" + ccy + "\"}]"
        else:
            args = "[{\"channel\":\"account\"}]"
        self.__Subscribe(args)
    
    def subscribeBalAndPos(self):
        args = "[{\"channel\":\"balance_and_position\"}]"
        self.__Subscribe(args)
        
    def getId(self,instId):
        output = instId.replace('-','') + "{:06}".format(self.ordIndex)
        self.ordIndex += 1
        return output
        
    #Store tkt objects in the queue and return order object
    def sendNewOrder(self,instId,tdMode,side,ordType,sz,px=0,ccy=""):
        #If you need specify other args, add them.
        odr = self.orderPool.get()
        strId = self.getId(instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"order\",\"args\":[{"
        strInstId = "\"instId\":\"" + instId + "\""
        strClOrdId = "\"clOrdId\":\"" + strId + "\""
        strSide = ""
        strTdMode = ""
        strOrdType = ""
        strSz = ""
        strPx = ""
        strCcy = ""
        if(side==OKExEnums.side.BUY):
            strSide = "\"side\":\"buy\""
        elif(side==OKExEnums.side.SELL):
            strSide = "\"side\":\"sell\""
        else:
            odr.msg = "[REJECT]Invalid side"
            return odr
        
        if(tdMode==OKExEnums.tradeMode.CASH):#Non margin mode
            strTdMode = "\"tdMode\":\"cash\""
        elif(tdMode==OKExEnums.tradeMode.ISOLATED):
            strTdMode = "\"tdMode\":\"isolated\""
        elif(tdMode==OKExEnums.tradeMode.CROSS):
            strTdMode = "\"tdMode\":\"cross\""
        else:
            odr.msg = "[REJECT]Invalid trade mode"
            return odr
        
        if(ordType == OKExEnums.orderType.MARKET):
            strOrdType = "\"ordType\":\"market\""
        elif(ordType == OKExEnums.orderType.LIMIT):
            strOrdType = "\"ordType\":\"limit\""
        elif(ordType == OKExEnums.orderType.POST_ONLY):
            strOrdType = "\"ordType\":\"post_only\""
        elif(ordType == OKExEnums.orderType.FOK):
            strOrdType = "\"ordType\":\"fok\""
        elif(ordType == OKExEnums.orderType.IOC):
            strOrdType = "\"ordType\":\"ioc\""
        elif(ordType == OKExEnums.orderType.OPTIMAL_LIMIT_IOC):
            strOrdType = "\"ordType\":\"optimal_limit_ioc\""
        else:
            odr.msg = "[REJECT]Invalid order type"
            return odr
        
        if(sz <= 0):#Do Risk Check.
            odr.msg = "[REJECT]Invalid size"
            return odr
        else:
            strSz = "\"sz\":\"" + str(sz) + "\""
            
        if(px <= 0):
            if(ordType == OKExEnums.orderType.MARKET or ordType == OKExEnums.orderType.OPTIMAL_LIMIT_IOC):
                strPx = ""
            else:
                odr.msg = "[REJECT]Invalid price"
                return odr
        else:
            strPx = "\"px\":\"" + str(px) + "\""
            
        if(ccy!=""):
            strCcy = "\"ccy\":\"" + ccy + "\""
        
        msg += strInstId + "," + strClOrdId + "," + strSide + "," + strTdMode + "," + strOrdType + "," + strSz
        if(strCcy!=""):
            msg += "," + strCcy
        if(strPx != ""):
            msg += "," + strPx
        msg+="}]}"
        self.oms.send(msg)
        msgOrd = self.msgOrdPool.get()
        msgOrd.uniId = strId
        msgOrd.op = "order"
        msgOrd.orderList[0].instId = instId
        msgOrd.orderList[0].tdMode = tdMode
        msgOrd.orderList[0].clOrdId = strId
        msgOrd.orderList[0].side = side
        msgOrd.orderList[0].sz = sz
        msgOrd.orderList[0].px = px
        self.tktQueue.put(msgOrd)
        #odr.orderList.append(tkt)
        odr.clOrdId = strId
        odr.side = side
        odr.px = px
        odr.sz = sz
        odr.openSz = sz
        odr.status = OKExEnums.orderState.WAIT_NEW
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr
        
    def sendModOrder(self,instId,clOrdId,newSz=-1,newPx=-1):#sz,px < 0 means no change
        odr = self.liveOrdList.get(clOrdId,self.nullOrd)
        if(odr.px < 0):
            return odr#nullOrd
        strId = self.getId(instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"amend-order\",\"args\":[{"
            
        strInstId = "\"instId\":\"" + instId + "\""
        strClOrdId = "\"clOrdId\":\"" + clOrdId + "\""
        
        msg += strInstId + "," + strClOrdId
        
        if(newSz >= 0):
            msg += ",\"newSz\":\"" + str(newSz) + "\""
        if(newPx >= 0):
            msg += ",\"newPx\":\"" + str(newPx) + "\""
            
        msg += "}]}"
        
        self.oms.send(msg)
        msgOrd = self.msgOrdPool.get()
        
        msgOrd.uniId = strId
        msgOrd.op = "amend-order"
        msgOrd.orderList[0].instId = instId
        msgOrd.orderList[0].clOrdId = clOrdId
        msgOrd.orderList[0].sz = newSz
        msgOrd.orderList[0].px = newPx
        self.tktQueue.put(msgOrd)
        odr.status = OKExEnums.orderState.WAIT_AMD
        odr.newSz = newSz
        odr.newPx = newPx
        #Do I need to do this? Not sure how it works on python...
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr
            
    def sendCanOrder(self,instId,clOrdId):
        odr = self.liveOrdList.get(clOrdId,self.nullOrd)
        if(odr.px < 0):
            return odr#nullOrd
        strId = self.getId(instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"cancel-order\",\"args\":[{"
            
        strInstId = "\"instId\":\"" + instId + "\""
        strClOrdId = "\"clOrdId\":\"" + clOrdId + "\""
        
        msg += strInstId + "," + strClOrdId + "}]}"
        
        self.oms.send(msg)
        msgOrd = self.msgOrdPool.get()
        
        msgOrd.uniId = strId
        msgOrd.op = "cancel-order"
        msgOrd.orderList[0].instId = instId
        msgOrd.orderList[0].clOrdId = clOrdId
        
        self.tktQueue.put(msgOrd)
        odr.status = OKExEnums.orderState.WAIT_CAN
        odr.live = False
        odr.newSz = 0.0
        odr.newPx = 0.0
        #Do I need to do this? Not sure how it works on python...
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr
       
    def __GetSign(self,strtime,key,method,requestPath,body=""):
        if(strtime ==""):
            strtime = str(time.time())
        rawmsg = strtime + method + requestPath + body
        hmacmsg = hmac.new(key.encode(), rawmsg.encode(), hashlib.sha256)
        return base64.b64encode(hmacmsg.digest()).decode()

    
