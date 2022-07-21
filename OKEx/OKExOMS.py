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
import OKExParser

class OMS:
    
    def sendPing(self,sec):
        while(True):
            time.sleep(sec)
            if(self.stopPing):
                self.stopPing = False
                break
            self.oms.send("ping")
    
    def StartCheckingMsg(self):#Create a thread for this function
        print("[OMS] OMS starts listening msg.")
        try:
            while True:
                msg = self.oms.recv()
                if(msg==""):#websocket has been closed
                    print("[OMS] The websocket disconnected.")
                    self.ackQueue.put("END")
                    self.isListening = False
                    self.connected = False
                    self.stopPing = True
                    break
                else:
                    self.ackQueue.put(msg)
                    self.tempOrdCheck.write(str(self.ts) + "," + msg + "\n")
        except:
            print("[OMS] Error Occured. Return ERROR text.")
            self.ackQueue.put("ERROR")
            self.isListening = False
            self.connected = False
            self.stopPing = True
            
    def updatingOrders(self,parser,insList):
        while(True):
            line = self.recv()
            if(line=="ERROR"):
                break
            if(line!="" and '{' in line and '}' in line):
                obj = parser.Parse(line)
                if(obj.dataType=="push"):
                    #obj = OKExMessage.pushData()
                    if(obj.arg["channel"]=="balance_and_position"):
                        for d in obj.data:
                            for bal in d.balList:
                                #Will Do
                                i = 0
                            for pos in d.posList:
                                if(pos.instId in self.insList.keys()):
                                    ins = self.insList[pos.instId]
                                    ins.updatePosition(pos)
                    elif(obj.arg["channel"]=="orders"):
                        for d in obj.data:
                            if(d.instId in self.insList.keys()):
                                ins = self.insList[d.instId]
                                ins.updateOrder(d)
                elif(obj.dataType=="order"):
                    for ack in obj.ackList:
                        odr = self.ordList[ack.clOrdId]
                        if(odr.instId in self.insList.keys()):
                            ins = self.insList[odr.instId]
                            ins.applyAckTkt(ack)
                    #print(obj.ToString())
                    #This is just the result of order. Do somothing if it's an error.
    
    def updatingOrdersSingle(self):
        while(True):
            line = self.recv()
            if(line=="ERROR"):
                print("ERROR Occuered.")
                break
            if(line!=""):
                if('{' in line and '}' in line):
                    obj = OKExParser.parser.Parse(line)
                    if(obj.dataType=="push"):
                        #obj = OKExMessage.pushData()
                        if(obj.arg["channel"]=="balance_and_position"):
                            for d in obj.data:
                                for bal in d.balList:
                                    #Will Do
                                    i = 0
                                for pos in d.posList:
                                    if(pos.instId in self.insList.keys()):
                                        ins = self.insList[pos.instId]
                                        ins.updatePosition(pos)
                        elif(obj.arg["channel"]=="orders"):
                            for d in obj.data:
                                if(d.instId in self.insList.keys()):
                                    ins = self.insList[d.instId]
                                    ins.updateOrder(d)
                    elif(obj.dataType=="order"):
                        for ack in obj.ackList:
                            odr = self.ordList[ack.clOrdId]
                            if(odr.instId in self.insList.keys()):
                                ins = self.insList[odr.instId]
                                ins.applyAckTkt(ack)
            else:#if(line!=""):
                break
            
    def __init__(self):
        self.tempOrdCheck = open("D:\\log\\oms.log",'w')
        
        self.oms = websocket.WebSocket()

        self.__url = ""
        self.__apiKey = ""
        self.__passphrase = ""
        self.__secretKey = ""
        
        self.connected = False
        self.stopPing = False
    
        self.ackQueue = queue.Queue()
        self.isListening = False
        self.ordIndex = 0
        
        self.ts = 0
        
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
        
    def initialize(self,insList):
        self.insList = insList
        
    def startListeningMsg(self):
        self.AckCheckingTh = threading.Thread(target=self.StartCheckingMsg,args=())
        self.isListening = True
        self.AckCheckingTh.start()
        self.sendPingTh = threading.Thread(target=self.sendPing,args=(20,))
        self.sendPingTh.start()
        
    def startUpdatingOrders(self,parser,insList):
        self.insList = insList
        self.updatingOrdTh = threading.Thread(target=self.updatingOrders,args=(parser,insList))
        self.updatingOrdTh.start()
        
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
        self.connected = True
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
        self.connected = True
        return msg
    
    def Disconnect(self):
        self.connected = False
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
        
    def subscribeOrders(self):
        args = "[{\"channel\":\"orders\",\"instType\":\"ANY\"}]"
        self.__Subscribe(args)
        
    def getId(self,instId):
        output = instId.replace('-','') + "{:06}".format(self.ordIndex)
        self.ordIndex += 1
        return output
        
    #Store tkt objects in the queue and return order object
    def sendNewOrder(self,ts,ins,tdMode,side,ordType,sz,px=0,ccy=""):
        #If you need specify other args, add them.
        #print(str(side) + " " + str(px) + " " + str(sz))
        self.ts = ts
        odr = self.orderPool.get()
        strId = self.getId(ins.instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"order\",\"args\":[{"
        strInstId = "\"instId\":\"" + ins.instId + "\""
        strClOrdId = "\"clOrdId\":\"" + strId + "\""
        strSide = ""
        strTdMode = ""
        strOrdType = ""
        strSz = ""
        strPx = ""
        strCcy = ""
        strPosSide =""
        if(side==OKExEnums.side.BUY):
            strSide = "\"side\":\"buy\""
            if(ins.instType == OKExEnums.instType.FUTURES or ins.instType == OKExEnums.instType.SWAP):
                if(ins.netpos < 0 and sz <= - ins.netpos):
                    strPosSide = "\"posSide\":\"short\""
                else:
                    strPosSide = "\"posSide\":\"long\""
        elif(side==OKExEnums.side.SELL):
            strSide = "\"side\":\"sell\""
            if(ins.instType == OKExEnums.instType.FUTURES or ins.instType == OKExEnums.instType.SWAP):
                if(ins.netpos > 0 and sz <=  ins.netpos):
                    strPosSide = "\"posSide\":\"long\""
                else:
                    strPosSide = "\"posSide\":\"short\""
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
        if(strPosSide!=""):
            msg += "," + strPosSide
        if(strCcy!=""):
            msg += "," + strCcy
        if(strPx != ""):
            msg += "," + strPx
        msg+="}]}"
        
        self.oms.send(msg)
        msgOrd = self.msgOrdPool.get()
        msgOrd.uniId = strId
        msgOrd.op = "order"
        msgOrd.orderList[0].instId = ins.instId
        msgOrd.orderList[0].tdMode = tdMode
        msgOrd.orderList[0].clOrdId = strId
        msgOrd.orderList[0].side = side
        msgOrd.orderList[0].sz = sz
        msgOrd.orderList[0].px = px
        self.tktQueue.put(msgOrd)
        self.tempOrdCheck.write(str(self.ts) + "," + msg + "\n")
        #odr.orderList.append(tkt)
        odr.ts = ts
        odr.org_ts = ts
        odr.clOrdId = strId
        odr.instId = ins.instId
        odr.side = side
        odr.px = px
        odr.sz = sz
        odr.openSz = sz
        odr.status = OKExEnums.orderState.WAIT_NEW
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        ins.liveOrdList[odr.clOrdId] = odr
        ins.ordList[odr.clOrdId] = odr
        if(side==OKExEnums.side.BUY):
            ins.buyOrders[int(odr.px / ins.tickSz)] = odr
        elif(side==OKExEnums.side.SELL):
            ins.sellOrders[int(odr.px / ins.tickSz)] = odr
        return odr
        
    def sendModOrder(self,ts,ins,clOrdId,newSz=-1,newPx=-1):#sz,px < 0 means no change
        self.ts = ts    
        odr = self.liveOrdList.get(clOrdId,self.nullOrd)
        if(odr.px < 0):
            return odr#nullOrd
        strId = self.getId(ins.instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"amend-order\",\"args\":[{"
            
        strInstId = "\"instId\":\"" + ins.instId + "\""
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
        msgOrd.orderList[0].instId = ins.instId
        msgOrd.orderList[0].clOrdId = clOrdId
        msgOrd.orderList[0].sz = newSz
        msgOrd.orderList[0].px = newPx
        self.tktQueue.put(msgOrd)
        odr.status = OKExEnums.orderState.WAIT_AMD
        odr.newSz = newSz
        odr.newPx = newPx
        odr.ts = ts
        #Do I need to do this? Not sure how it works on python...
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr
            
    def sendCanOrder(self,ts,ins,clOrdId):
        #print(clOrdId)
        self.ts = ts
        odr = self.liveOrdList.get(clOrdId,self.nullOrd)
        orgodr = odr.ToString()
        if(odr.px < 0):
            return odr#nullOrd
        strId = self.getId(ins.instId)
        msg = "{\"id\":\"" + strId + "\",\"op\":\"cancel-order\",\"args\":[{"
            
        strInstId = "\"instId\":\"" + ins.instId + "\""
        strClOrdId = "\"clOrdId\":\"" + clOrdId + "\""
        
        msg += strInstId + "," + strClOrdId + "}]}"
        
        self.oms.send(msg)
        msgOrd = self.msgOrdPool.get()
        
        msgOrd.uniId = strId
        msgOrd.op = "cancel-order"
        msgOrd.orderList[0].instId = ins.instId
        msgOrd.orderList[0].clOrdId = clOrdId
        
        self.tktQueue.put(msgOrd)
        self.tempOrdCheck.write(str(self.ts) + "," + msg + "\n")
        odr.status = OKExEnums.orderState.WAIT_CAN
        odr.live = False
        odr.newSz = 0.0
        odr.newPx = 0.0
        odr.ts = ts
        if(odr.side==OKExEnums.side.BUY):
            if(int(odr.px / ins.tickSz) in ins.buyOrders.keys()):
                ins.buyOrders.pop(int(odr.px / ins.tickSz))
            else:
                print("Couldn't find the buy order px:" + str(int(odr.px / ins.tickSz)))
                print(orgodr)
                for o in ins.buyOrders.values():
                    print(o.ToString())
        elif(odr.side==OKExEnums.side.SELL):
            if(int(odr.px / ins.tickSz) in ins.sellOrders.keys()):
                ins.sellOrders.pop(int(odr.px / ins.tickSz))
            else:
                print("Couldn't find the sell order px:" + str(int(odr.px / ins.tickSz)))
                print(orgodr)
                for o in ins.sellOrders.values():
                    print(o.ToString())
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

    

oms = OMS()