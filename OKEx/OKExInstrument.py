# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 14:07:15 2022

@author: yusai
"""

import math
from Utils import params
import OKExEnums
import OKExMessage
from Utils import Utils

class Book:
    def __init__(self):
        self.bs = OKExEnums.side.NONE
        self.px = 0
        self.sz = 0.0
        self.liqOrd = 0
        self.numOfOrd = 0
        self.myOrders = {}#For Backtest
        self.myOrdSz = 0.0
        self.myNumOfOrd = 0
        self.idx = 0
        self.next = 0#Use idx as iterator.
        self.prev = 0#Use idx as iterator.
        
    def ToString(self):
        line = str(self.bs) + "," + str(self.px) + "," + str(self.sz) + ","
        line += str(self.liqOrd) + "," + str(self.numOfOrd) + "," 
        line += str(self.idx) + "," + str(self.next) + "," + str(self.prev)
        return line
    
    def initialize(self):
        #self.bs = OKExEnums.side.NONE
        self.px = 0
        self.sz = 0.0
        self.liqOrd = 0
        self.numOfOrd = 0
        self.myOrders = {}#For Backtest
        self.myOrdSz = 0.0
        self.myNumOfOrd = 0
        #self.idx = 0 Don't init idx
        self.next = 0#Use idx as iterator.
        self.prev = 0#Use idx as iterator.
        
    def UpdateBook(self,msgBook, side, priceUnit):
        self.bs = side
        self.px = int(msgBook.px * priceUnit)
        self.sz = msgBook.qty
        self.liqOrd = msgBook.LiqOrd
        self.NumOfOrd = msgBook.NumOfOrd


class Board:
    def __init__(self):
        self.instId = ""
        self.bend = Book()
        self.aend = Book()
        self.aend.idx = -1
        self.bend.idx = -1
        self.BestAsk = self.aend
        self.BestBid = self.bend
        self.bids = []
        self.asks = []
        self.ts = 0
        self.priceUnit = 1#Price multiplier to convert price to int
        self.depth = 0
        self.ctType = OKExEnums.ctType.NONE
        self.ctVal = 1
        
    def ToString(self,side=OKExEnums.side.NONE):
        line = ""
        if(side == OKExEnums.side.NONE or side == OKExEnums.side.SELL):
            ask = self.asks[self.aend.prev] 
            while(True):
                line += str(ask.idx) + "," + str(ask.sz) + "," + str(ask.px) + "\n"
                if(ask.px == self.BestAsk.px):
                    break
                else:
                    ask = self.asks[ask.prev]
        if(side == OKExEnums.side.NONE or side == OKExEnums.side.BUY):
            bid = self.BestBid
            while(True):
                line += str(bid.idx) + ",      ," + str(bid.px) + "," + str(bid.sz) + "\n"
                if(bid.next < 0):
                    break
                else:
                    bid = self.bids[bid.next]
        return line
    
    def strAsks(self):
        line = ""
        for a in self.asks:
            line += a.ToString() + "\n"
        return line
    
    def strBids(self):
        line = ""
        for b in self.bids:
            line += b.ToString() + "\n"
        return line
    def findBook(self,side,px):
        if(side == OKExEnums.side.BUY):
            if(self.BestBid.px - px >= self.depth or px > self.BestBid.px):
                return -1
            else:
                i = 0
                if(self.BestBid.px - px < self.depth):
                    bid = self.BestBid
                    while(i < self.depth):
                        if(bid.px == px):
                            return bid.idx
                        else:
                            i += 1
                            bid = self.bids[bid.next]
                else:
                    bid = self.bids[self.bend.prev]
                    while(i < self.depth):
                        if(bid.px == px):
                            return bid.idx
                        else:
                            i += 1
                            bid = self.bids[bid.prev]
        elif(side == OKExEnums.side.SELL):
            if(px - self.BestAsk.px >= self.depth or px < self.BestAsk.px):
                return -1
            else:
                i = 0
                if(px - self.BestAsk.px < self.depth):
                    ask = self.BestAsk
                    while(i < self.depth):
                        if(ask.px == px):
                            return ask.idx
                        else:
                            i += 1
                            ask = self.asks[ask.next]
                else:
                    ask = self.asks[self.aend.prev]
                    while(i < self.depth):
                        if(ask.px == px):
                            return ask.idx
                        else:
                            i += 1
                            ask = self.asks[ask.prev]
        return -1
    
    def initializeBoard(self,snapshot,depth):
        self.bids.clear()
        self.asks.clear()
        self.depth = depth
        self.BestBid = self.bend
        self.BestAsk = self.aend
        for data in snapshot.data:
            if(data.ts > self.ts):
                self.ts = data.ts
            i = 0
            for b in data.bids:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    b.qty *= float(self.ctVal) / float(b.px) * float(self.priceUnit)
                else:
                    b.qty *= float(self.ctVal)
                if(i < depth):
                    bk = Book()
                    bk.UpdateBook(b, OKExEnums.side.BUY, self.priceUnit)
                    bk.idx = i
                    self.bids.append(bk)
                    i += 1
                    if(self.BestBid.idx == -1 or self.BestBid.px < bk.px):
                        self.BestBid.prev = bk.idx
                        bk.next = self.BestBid.idx
                        self.BestBid = bk
                    else:
                        tempbk = self.BestBid
                        while(True):
                            if(tempbk.next < 0):
                                nxt = self.bend
                                nxt.prev = bk.idx
                                bk.next = nxt.idx
                                tempbk.next = bk.idx
                                bk.prev = tempbk.idx
                                break
                            else:
                                nxt = self.bids[tempbk.next]
                                if(bk.px > nxt.px):#Insert between books
                                    nxt.prev = bk.idx
                                    bk.next = nxt.idx
                                    tempbk.next = bk.idx
                                    bk.prev = tempbk.idx
                                    break
                                else:
                                    tempbk = nxt
                                
                elif(b.px * self.priceUnit  > self.bids[self.bend.prev].px):#if the price is larger than bend.__prev insert
                    blank = self.bids[self.bend.prev]
                    current = self.bids[blank.prev]
                    self.bend.prev = current.idx
                    current.next = self.bend.idx
                    blank.initialize()
                    blank.UpdateBook(b, OKExEnums.side.BUY,self.priceUnit)
                    nxt = self.bend
                    while(True):
                        if(current.px > blank.px):
                            nxt.prev = blank.idx
                            blank.next = nxt.idx 
                            current.next = blank.idx
                            blank.prev = current.idx
                            break
                        elif(current.px == self.BestBid.px):#new book is bestbid
                            self.BestBid.prev = blank.idx
                            blank.next = self.BestBid.idx
                            self.BestBid = blank
                            break
                        else:
                            nxt = current
                            current = self.bids[nxt.prev]
            #0 fill
            bid = self.BestBid
            j = 0
            while(True):
                if(bid.px - 1 == self.bids[bid.next].px):
                    bid = self.bids[bid.next]
                else:
                    if(i < depth):
                        bk = Book()
                        bk.px = bid.px - 1
                        bk.bs = OKExEnums.side.BUY
                        bk.idx = i
                        if(bid.next < 0):
                            nxt = self.bend
                        else:
                            nxt = self.bids[bid.next]
                        bk.prev = nxt.prev
                        bk.next = bid.next
                        bid.next = bk.idx
                        nxt.prev = bk.idx
                        self.bids.append(bk)
                        bid = bk
                        i += 1
                    else:
                        blank = self.bids[self.bend.prev]
                        self.bend.prev = blank.prev
                        self.bids[blank.prev].next = blank.next
                        blank.initialize()
                        blank.px = bid.px - 1
                        blank.bs = OKExEnums.side.BUY
                        if(bid.next < 0):
                            nxt = self.bend
                        else:
                            nxt = self.bids[bid.next]
                        blank.prev = nxt.prev
                        blank.next = bid.next
                        bid.next = blank.idx
                        nxt.prev = blank.idx
                        bid = blank
                    j += 1
                if((bid.next < 0 and i == depth) or j >= self.depth):
                    break
            i = 0                
            for a in data.asks:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    a.qty *= float(self.ctVal) / float(a.px) * float(self.priceUnit)
                else:
                    a.qty *= float(self.ctVal)
                if(i < depth):
                    bk = Book()
                    bk.UpdateBook(a, OKExEnums.side.SELL, self.priceUnit)
                    bk.idx = i
                    self.asks.append(bk)
                    i += 1
                    if(self.BestAsk.idx == -1 or self.BestAsk.px > bk.px):
                        self.BestAsk.prev = bk.idx
                        bk.next = self.BestAsk.idx
                        self.BestAsk = bk
                    else:
                        tempbk = self.BestAsk
                        while(True):
                            if(tempbk.next < 0):
                                nxt = self.aend
                                nxt.prev = bk.idx
                                bk.next = nxt.idx
                                tempbk.next = bk.idx
                                bk.prev = tempbk.idx
                                break
                            else:
                                nxt = self.asks[tempbk.next]
                                if(bk.px < nxt.px):#Insert between books
                                    nxt.prev = bk.idx
                                    bk.next = nxt.idx
                                    tempbk.next = bk.idx
                                    bk.prev = tempbk.idx
                                    break
                                else:
                                    tempbk = nxt
                elif(a.px * self.priceUnit > self.asks[self.aend.prev].px):#if the price is larger than bend.__prev insert
                    blank = self.asks[self.aend.prev]
                    current = self.asks[blank.prev]
                    self.aend.prev = current.idx
                    current.next = self.aend.idx
                    blank.initialize()
                    blank.UpdateBook(a, OKExEnums.side.SELL,self.priceUnit)
                    nxt = self.aend
                    while(True):
                        if(current.px < blank.px):
                            nxt.prev = blank.idx
                            blank.next = nxt.idx
                            current.next = blank.idx
                            blank.prev = current.idx
                            break
                        elif(current.px == self.BestAsk.px):#new book is bestask
                            self.BestAsk.prev = blank.idx
                            blank.next = self.BestAsk.idx
                            self.BestAsk = blank
                            break
                        else:
                            nxt = current
                            current = self.asks[nxt.prev]
            #0 fill
            ask = self.BestAsk
            j = 0
            while(True):
                if(ask.px + 1 == self.asks[ask.next].px):
                    ask = self.asks[ask.next]
                else:
                    if(i < depth):
                        bk = Book()
                        bk.px = ask.px + 1
                        bk.bs = OKExEnums.side.SELL
                        bk.idx = i
                        if(ask.next < 0):
                            nxt = self.aend
                        else:
                            nxt = self.asks[ask.next]
                        bk.prev = nxt.prev
                        bk.next = ask.next
                        ask.next = bk.idx
                        nxt.prev = bk.idx
                        self.asks.append(bk)
                        ask = bk
                        i += 1
                    else:
                        blank = self.asks[self.aend.prev]
                        self.aend.prev = blank.prev
                        self.asks[blank.prev].next = blank.next
                        blank.initialize()
                        blank.px = ask.px + 1
                        blank.bs = OKExEnums.side.SELL
                        if(ask.next < 0):
                            nxt = self.aend
                        else:
                            nxt = self.asks[ask.next]
                        blank.prev = nxt.prev
                        blank.next = ask.next
                        ask.next = blank.idx
                        nxt.prev = blank.idx
                        ask = blank
                    j += 1
                if((ask.next < 0 and i == depth) or j >= self.depth):
                    break
            #print("Bids:" + str(len(self.bids)))
            #print("Asks:" + str(len(self.asks)))    
    def updateBooks(self,dataUpdate):    
        for data in dataUpdate.data:
            if(data.ts > self.ts):
                self.ts = data.ts
            #If the price is found in dict,replace
            #else if the price is inside of best bid and ask, replace end.__prev to new price
            for b in data.bids:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    b.qty *= float(self.ctVal) / float(b.px) * float(self.priceUnit)
                else:
                    b.qty *= float(self.ctVal)
                bidx = self.findBook(OKExEnums.side.BUY,int(b.px * self.priceUnit))
                if(bidx >= 0):
                    bid = self.bids[bidx]
                    bid.UpdateBook(b,OKExEnums.side.BUY,self.priceUnit)
                    if(bid.px == self.BestBid.px and bid.sz == 0):
                        cnt = 0
                        while(True):
                            endprev = self.bids[self.bend.prev]
                            newpx = int(endprev.px - 1)
                            nxtbk = self.bids[bid.next]
                            bid.initialize()
                            bid.px = newpx
                            bid.bs = OKExEnums.side.BUY
                            bid.prev = self.bend.prev
                            bid.next = endprev.next
                            self.bend.prev = bid.idx
                            endprev.next = bid.idx
                            if(nxtbk.sz > 0):
                                self.BestBid = nxtbk
                                break
                            else:
                                bid = nxtbk
                                newpx -= 1
                                cnt += 1
                                if(cnt >= self.depth):
                                    self.BestBid = bid
                                    print("The bid books are all 0. instId:" + self.instId)
                                    #print(self.strBids())
                                    break
                            
                elif(b.px * self.priceUnit > self.BestBid.px and b.qty > 0):#Higher than bestbid. Ignore if sz == 0
                    newpx = int(self.BestBid.px + 1)
                    i = 0
                    while(i < self.depth):
                        blank = self.bids[self.bend.prev]
                        prev = self.bids[blank.prev]
                        self.bend.prev = prev.idx
                        prev.next = blank.next
                        blank.initialize()
                        if(int(b.px * self.priceUnit) == newpx):
                            blank.UpdateBook(b, OKExEnums.side.BUY,self.priceUnit)
                            self.BestBid.prev = blank.idx
                            blank.next = self.BestBid.idx
                            self.BestBid = blank
                            break
                        else:
                            blank.px = newpx
                            blank.sz = 0
                            self.BestBid.prev = blank.idx
                            blank.next = self.BestBid.idx
                            self.BestBid = blank
                            newpx += 1
                            i += 1
            #print(len(self.bids))
            for a in data.asks:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    a.qty *= float(self.ctVal) / float(a.px) * float(self.priceUnit)
                else:
                    a.qty *= float(self.ctVal)
                aidx = self.findBook(OKExEnums.side.SELL,int(a.px * self.priceUnit))
                if(aidx >= 0):
                    ask = self.asks[aidx]
                    ask.UpdateBook(a,OKExEnums.side.SELL,self.priceUnit)
                    if(ask.px == self.BestAsk.px and ask.sz == 0):
                        cnt = 0
                        endprev = self.asks[self.aend.prev]
                        newpx = int(endprev.px + 1)
                        nxtbk = self.asks[ask.next]
                        while(True):
                            ask.initialize()
                            ask.px = newpx
                            ask.bs = OKExEnums.side.SELL
                            ask.prev = endprev.idx
                            ask.next = self.aend.idx
                            self.aend.prev = ask.idx
                            endprev.next = ask.idx
                            if(nxtbk.sz > 0):
                                self.BestAsk = nxtbk
                                break
                            else:
                                endprev = ask
                                ask = nxtbk
                                nxtbk = self.asks[ask.next]
                                newpx += + 1
                                cnt += 1
                                if(cnt >= self.depth):
                                    self.BestAsk = ask
                                    print("The ask books are all 0. instId:" + self.instId)
                                    #print(self.strAsks())
                                    break
                            
                elif(a.px * self.priceUnit < self.BestAsk.px) and a.qty > 0:#Lower than bestask
                    newpx = int(self.BestAsk.px - 1)
                    i = 0
                    while(i < self.depth):
                        blank = self.asks[self.aend.prev]
                        prev = self.asks[blank.prev]
                        self.aend.prev = prev.idx
                        prev.next = self.aend.idx
                        blank.initialize()
                        if(int(a.px * self.priceUnit) == newpx):
                            blank.UpdateBook(a, OKExEnums.side.SELL, self.priceUnit)
                            self.BestAsk.prev = blank.idx
                            blank.next = self.BestAsk.idx
                            self.BestAsk = blank
                            break
                        else:
                            blank.px = newpx
                            blank.sz = 0
                            self.BestAsk.prev = blank.idx
                            blank.next = self.BestAsk.idx
                            self.BestAsk = blank
                            newpx -= 1
                            i += 1
            #print(len(self.asks))
class Instrument:
    
    def __init__(self):
        self.instId = ""
        self.instType = OKExEnums.instType.NONE
        self.baseCcy = ""
        self.quoteCcy = ""
        self.settleCcy = ""
        self.uly = ""
        self.category = 0
        self.ctMulti = 1
        self.ctType = OKExEnums.ctType.NONE
        self.ctVal = 0
        self.ctValCcy = ""
        self.expTime = 0
        self.lever = 1
        self.listTime = 0
        self.lotSz = 1
        self.maxIcebergSz = 0
        self.maxLmtSz = 0
        self.maxMktSz = 0
        self.maxStopSz = 0
        self.maxTriggerSz = 0
        self.maxTwapSz = 0
        self.minSz = 0
        self.state = OKExEnums.insState.NONE
        self.tickSz = 0#priceUnit should be 1 / tickSz
        
        self.Books = Board()
        self.bookDepth = 400
        self.ordList = {} #Pair of Id and order object
        self.liveOrdList = {}
        self.pos = 0.0
        
        self.last = 0.0
        self.Mid = 0.0
    
        self.ts = 0
    
        #Factors
        self.bookImbalance = 0.0
        self.realizedVolatility = 0.0
        self.currentRV = 0.0
        self.execAskCnt = 0
        self.execBidCnt = 0
        self.execAskVol = 0.0
        self.execBidVol = 0.0
        self.execAskAmt = 0.0#To Calc VWAP
        self.execBidAmt = 0.0#To Calc VWAP
        
        self.ringIdx = -1
        self.ringDataCount = 0
        self.lastRingUpdatedTime = 0
        self.posRing = []#List of Utils.Ring(180)
        self.biRing = []
        self.rvRing = []
        self.exeAskCRing = []
        self.exeBidCRing = []
        self.exeAskVRing = []
        self.exeBidVRing = []
        self.bestBidPxRing = []
        self.bestAskPxRing = []
        self.posMARing = []
        self.midMARing = []
        
        i = 0
        while(i<60):
            self.posRing.append(Utils.Ring(180))
            self.biRing.append(Utils.Ring(180))
            self.rvRing.append(Utils.Ring(180))
            self.exeAskCRing.append(Utils.Ring(180))
            self.exeBidCRing.append(Utils.Ring(180))
            self.exeAskVRing.append(Utils.Ring(180))
            self.exeBidVRing.append(Utils.Ring(180))
            self.bestBidPxRing.append(Utils.Ring(180))
            self.bestAskPxRing.append(Utils.Ring(180))
            self.posMARing.append(Utils.Ring(180))
            self.midMARing.append(Utils.Ring(180))
            i += 1
            
    def setInsData(self,dict_info):
        self.instId = dict_info["instId"]
        if(dict_info["instType"]=="SPOT"):
            self.instType = OKExEnums.instType.SPOT
        elif(dict_info["instType"]=="SWAP"):
            self.instType = OKExEnums.instType.SWAP
        elif(dict_info["instType"]=="FUTURES"):
            self.instType = OKExEnums.instType.FUTURES
        elif(dict_info["instType"]=="MARGIN"):
            self.instType = OKExEnums.instType.MARGIN
        else:
            self.instType = OKExEnums.instType.NONE
        self.baseCcy = dict_info["baseCcy"]
        self.quoteCcy = dict_info["quoteCcy"]
        self.settleCcy = dict_info["settleCcy"]
        self.uly = dict_info["uly"]
        if(dict_info["category"]!=""):
            self.category = int(dict_info["category"])
        if(dict_info["ctMult"]!=""):
            self.ctMulti = int(dict_info["ctMult"])
        if(dict_info["ctType"]=="inverse"):
            self.ctType = OKExEnums.ctType.INVERSE
            self.Books.ctType = self.ctType
        else:
            self.ctType = OKExEnums.ctType.LINEAR
            self.Books.ctType = self.ctType
        if(dict_info["ctVal"]!=""):
            self.ctVal = float(dict_info["ctVal"])
            self.Books.ctVal = self.ctVal
        else:
            self.ctVal = 1
            self.Books.ctVal = 1
        self.ctValCcy = dict_info["ctValCcy"]
        if(dict_info["expTime"]!=""):
            self.expTime = int(dict_info["expTime"])
        if(dict_info["lever"]!=""):
            self.lever = float(dict_info["lever"])
        if(dict_info["listTime"]!=""):
            self.listTime = int(dict_info["listTime"])
        if(dict_info["lotSz"]!=""):
            self.lotSz = float(dict_info["lotSz"])
        if(dict_info["maxIcebergSz"]!=""):
            self.maxIcebergSz = float(dict_info["maxIcebergSz"])
        if(dict_info["maxLmtSz"]!=""):
            self.maxLmtSz = float(dict_info["maxLmtSz"])
        if(dict_info["maxMktSz"]!=""):
            self.maxMktSz = float(dict_info["maxMktSz"])
        if(dict_info["maxStopSz"]!=""):
            self.maxStopSz = float(dict_info["maxStopSz"])
        if(dict_info["maxTriggerSz"]!=""):
            self.maxTriggerSz = float(dict_info["maxTriggerSz"])
        if(dict_info["maxTwapSz"]!=""):
            self.maxTwapSz = float(dict_info["maxTwapSz"])
        if(dict_info["minSz"]!=""):
            self.minSz = float(dict_info["minSz"])
        
        if(dict_info["state"]=="live"):
            self.state = OKExEnums.insState.LIVE
        elif(dict_info["state"]=="suspend"):
            self.state = OKExEnums.insState.SUSPEND
        elif(dict_info["state"]=="expired"):
            self.state = OKExEnums.insState.EXPIRED
        elif(dict_info["state"]=="preopen"):
            self.state = OKExEnums.insState.PREOPEN
        elif(dict_info["state"]=="settlement"):
            self.state = OKExEnums.insState.SETTLEMENT
        else:
            self.state = OKExEnums.insState.NONE
        if(dict_info["tickSz"]!=""):
            self.tickSz = float(dict_info["tickSz"])
            self.Books.priceUnit = 1 / self.tickSz
            
    def updateTrades(self,msg):
        #self.instId = ""
        #self.tradeId = ""
        #self.px = 0.0
        #self.sz = 0.0
        #self.side = OKExEnums.side.NONE
        #self.ts = 0
        msg = OKExMessage.pushData()
        for d in msg.data:
            if(d.ts > self.ts):
                self.ts = d.ts
            if(self.last > 0 and self.last != d.px):
                self.realizedVolatility += math.pow(math.log(self.last/d.px),2)
            self.last = d.px
            if(self.ctType == OKExEnums.ctType.INVERSE):
                if(d.side == OKExEnums.side.BUY):#this means the market order is BUY
                    #exec on ask side
                    self.execAskCnt += 1
                    self.execAskVol += d.sz * self.ctVal / d.px
                    self.execAskAmt += d.sz * self.ctVal
                elif(d.side == OKExEnums.side.SELL):#this means the market order is SELL
                    #exec on bid side
                    self.execBidCnt += 1
                    self.execBidVol += d.sz * self.ctVal / d.px
                    self.execBidAmt += d.sz * self.ctVal
            else:
                if(d.side == OKExEnums.side.BUY):#this means the market order is BUY
                    #exec on ask side
                    self.execAskCnt += 1
                    self.execAskVol += d.sz * self.ctVal
                    self.execAskAmt += d.px * d.sz * self.ctVal
                elif(d.side == OKExEnums.side.SELL):#this means the market order is SELL
                    #exec on bid side
                    self.execBidCnt += 1
                    self.execBidVol += d.sz * self.ctVal
                    self.execBidAmt += d.px * d.sz * self.ctVal
            
            
    def updateBooks(self,msg):#get pushData
        #msg = OKExMessage.pushData()
        if(msg.arg["channel"]=="books"):#snapshot or update
            for d in msg.data:
                if(self.ts < d.ts):
                    self.ts = d.ts
                if(msg.arg["action"]=="snapshot"):
                    #print(self.instId)
                    self.Books.initializeBoard(msg, self.bookDepth)
                    self.Books.instId = self.instId
                elif(msg.arg["action"]=="update"):
                    self.Books.updateBooks(msg)
        elif(msg.arg["channel"]=="trades"):
            self.updateTrades(msg)
            
    def updateRings(self):
        if(self.lastRingUpdatedTime == 0):
            if(self.ts > 0):
                self.lastRingUpdatedTime = int(self.ts / 1000) * 1000
        else:
            if(self.ts - self.lastRingUpdatedTime >= 1000):
                self.ringIdx += 1
                if(self.ringIdx > 59):
                    self.ringIdx = 0
                count = 0
                while(self.ts - self.lastRingUpdatedTime >= 1000):
                    self.lastRingUpdatedTime += 1000
                    self.posRing[self.ringIdx].add(self.pos)
                    self.biRing[self.ringIdx].add(self.bookImbalance)
                    self.rvRing[self.ringIdx].add(self.realizedVolatility)
                    self.exeAskCRing[self.ringIdx].add(self.execAskCnt)
                    self.exeBidCRing[self.ringIdx].add(self.execBidCnt)
                    self.exeAskVRing[self.ringIdx].add(self.execAskVol)
                    self.exeBidVRing[self.ringIdx].add(self.execBidVol)
                    self.bestBidPxRing[self.ringIdx].add(self.Books.BestBid.px)
                    self.bestAskPxRing =[self.ringIdx].add(self.Books.BestAsk.px)
                    self.ringDataCount += 1
                    if(self.ringDataCount > params.posMAPeriod * 60):
                        maPos = 0.0
                        i = 0
                        while(i < params.posMAPeriod):
                            maPos += self.posRing[self.ringIdx].relative(-i)
                            i += 1
                        maPos /= params.posMAPeriod
                        self.posMARing.add(maPos)
                    if(self.ringDataCount > params.midMAPeriod * 60):
                        maMid = 0.0
                        i = 0
                        while(i < params.midMAPeriod):#Check Price?
                            maMid += self.bestAskPxRing[self.ringIdx].relative(-i) + self.bestBidPxRing[self.ringIdx].relative(-i)
                            i += 1
                        maMid /= params.posMAPeriod * 2
                        self.midMARing.add(maMid)
                    count += 1
                    if(count > 10000):
                        #error
                        break
                    
    def updateOrder(self,tkt):
        i = 0

    def ToString(self):
        outputline = self.instId + "," + str(self.instType) + "," \
                    + self.baseCcy + "," + self.quoteCcy + "," \
                    + self.settleCcy + "," + self.uly + "," \
                    + str(self.category) + "," + str(self.ctMulti) + "," \
                    + str(self.ctType) + "," + str(self.ctVal) + "," \
                    + self.ctValCcy + "," + str(self.expTime) + "," \
                    + str(self.lever) + "," + str(self.listTime) + "," \
                    + str(self.lotSz) + "," + str(self.maxIcebergSz) + "," \
                    + str(self.maxLmtSz) + "," + str(self.maxMktSz) + "," \
                    + str(self.maxStopSz) + "," + str(self.maxTriggerSz) + "," \
                    + str(self.maxTwapSz) + "," + str(self.minSz) + "," \
                    + str(self.state) + "," + str(self.tickSz) + "," \
                    + str(self.pos) + "," + str(self.Mid) + "," \
                    + str(self.ts)
        return outputline
    def ToJsonString(self):
        outputline = "" 
    def ToJson(self):
        line = self.ToJsonString()