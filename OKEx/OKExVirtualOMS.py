# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 21:47:04 2022

@author: yusai
"""

import queue

import OKExEnums
import OKExMessage
import OKExOrder
from Utils import params

class VirtualOMS:

    def __init__(self):
    
        self.waitQueue = queue.Queue()
        self.waitPeek = None
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
        self.numOfAckTkt = 200000
        self.ackPool = queue.LifoQueue(self.numOfAckObj * 2)
        i = 0
        while(i < self.numOfAckTkt):
            self.ackPool.put(OKExMessage.ackTicket())
    
    def recv(self,time):
        if(self.ackQueue.empty()):
            return ""
        else:
            return self.ackQueue.get_nowait()
            
    def getId(self,instId):
        output = instId.replace('-','') + "{:06}".format(self.ordIndex)
        self.ordIndex += 1
        return output
        
    #Store tkt objects in the queue and return order object
    def sendNewOrder(self,tm,ins,tdMode,side,ordType,sz,px=0,ccy=""):
        #If you need specify other args, add them.
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
                if(ins.pos < 0 and sz <= - ins.pos):
                    strPosSide = "\"posSide\":\"short\""
                else:
                    strPosSide = "\"posSide\":\"long\""
        elif(side==OKExEnums.side.SELL):
            strSide = "\"side\":\"sell\""
            if(ins.instType == OKExEnums.instType.FUTURES or ins.instType == OKExEnums.instType.SWAP):
                if(ins.pos > 0 and sz <=  ins.pos):
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
        #self.oms.send(msg)
        #See Ticket Queue instead of checking ack
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
        self.waitQueue.put(msgOrd)
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
        
    def sendModOrder(self,tm,ins,clOrdId,newSz=-1,newPx=-1):#sz,px < 0 means no change
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
        self.waitQueue.put(msgOrd)
        odr.status = OKExEnums.orderState.WAIT_AMD
        odr.newSz = newSz
        odr.newPx = newPx
        #Do I need to do this? Not sure how it works on python...
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr
            
    def sendCanOrder(self,tm,ins,clOrdId):
        odr = self.liveOrdList.get(clOrdId,self.nullOrd)
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
        self.waitQueue.put(msgOrd)
        odr.status = OKExEnums.orderState.WAIT_CAN
        odr.live = False
        odr.newSz = 0.0
        odr.newPx = 0.0
        #Do I need to do this? Not sure how it works on python...
        self.liveOrdList[odr.clOrdId] = odr
        self.ordList[odr.clOrdId] = odr
        return odr

    def createAck(self,tm,msg):
        msgOrd = self.msgOrdPool.get()
        msgOrd.uniId = msg.uniId
        msgOrd.op = msg.op
        msgOrd.code = 0
        msgOrd.msg = ""
        i = 0
        for o in msg.orderList:
            ack = msgOrd.ackList[0]
            if(i > 0):
                ack = self.ackPool.get()
                msgOrd.ackList.append(ack)
            ack.clOrdId = o.clOrdId
            ack.sCode = 0
            ack.sMsg = ""
            ack.reqId = ""
        return msgOrd
    
    def checkWaitQueue(self,tm):
        if(self.waitPeek==None):
            if(self.waitQueue.empty()):
                return
            else:
                self.waitPeek = self.waitQueue.get()
                
        if(tm >= self.waitPeek.tm + params.latency):
            while(not self.waitQueue.empty()):
                ack = self.createAck(tm,self.waitPeek)
                self.ackQueue.put(ack)
                self.waitPeek = self.waitQueue.get()
                if(tm < self.waitPeek.tm + params.latency):
                    break
            if(self.waitQueue.empty() and tm >= self.waitPeek.tm + params.latency):
                ack = self.createAck(tm,self.waitPeek)
                self.ackQueue.put(ack)
                self.waitPeek = None
                    
    def pushOrdObj(self,obj):
        o_temp = None
        a_temp = None
        i = 0
        for o in obj.orderList:
            o.init()
            if(i == 0):
                o_temp = o
                i += 1
            else:
                self.msgOrdPool.put(o)
        i = 0
        for a in obj.ackList:
            a.init()
            if(i == 0):
                a_temp = a
                i += 1
            else:
                self.ackPool.put(a)
        obj.init(a_temp,o_temp)
        self.orderPool.put(obj)
            
                    