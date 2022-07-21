# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 22:03:04 2022

@author: yusai
"""

import math
from Utils import params
import OKExEnums
import OKExInstrument
import OKExOMS

class Optimizer:
    
    def __init__(self):
        self.optimizing = False    
        self.logFile = open("D:\\log\\Optimizer.log",'w')
        self. calcCount = 0
        
    def initialize(self,oms):
        self.oms = oms
        
    def calcBookImbalance(self,ins):
        bid = ins.Books.booksBestBid
        ask = ins.Books.booksBestAsk
        minsum = 0.01
        bidsum = 0
        asksum = 0
        i = 0
        while(i < params.biTicks):
            if(bid.idx >= 0):
                bidsum += bid.sz * math.exp(-math.log(ins.Books.booksBestBid.px / bid.px) * params.biDecayingParam)
                if(bid.px - 1 in ins.Books.books):
                    bid = ins.Books.books[bid.px - 1]
                else:
                    bid = ins.Books.bend
            if(ask.idx >= 0):
                asksum += ask.sz * math.exp(-math.log(ask.px / ins.Books.booksBestAsk.px) * params.biDecayingParam)
                if(ask.px + 1 in ins.Books.books):
                    ask = ins.Books.books[ask.px + 1]
                else:
                    ask = ins.Books.aend
            i += 1
        if(bidsum < minsum):
            bidsum = minsum
        if(asksum < minsum):
            asksum = minsum
        return math.log(asksum / bidsum)
    
    def calcFactors(self,ins):
        ins.updateRings()
        ins.bookImbalance = self.calcBookImbalance(ins)
        #print(ins.instId + ":" + str(ins.bookImbalance))
        if(ins.ringDataCount > params.RVPeriod * 60):
            ins.currentRV = math.pow(ins.realizedVolatility - ins.rvRing[ins.ringIdx].relative(-params.RVPeriod),0.5)
        
    def Optimize(self,ins):
        #ins = OKExInstrument.Instrument()
        if(self.optimizing == False or self.oms.connected == False or ins.isTrading == False):
            return
        if(ins.lastOptTs > 0 and ins.ts < ins.lastOptTs + ins.ordInterval):
            return
        ins.lastOptTs = ins.ts
        self.calcCount += 1
        self.logFile.write("Calc No:" + str(self.calcCount) + "\n")
        #Sp:Volatility, Spread
        askPx = 0
        bidPx = 0
        expectingAskQty = 0
        expectingBidQty = 0
        liveSellOrders = 0
        liveBuyOrders = 0
        
        Spr = ins.currentRV * ins.Mid    #Half Spread
        if(Spr < ins.minSp / 2):
            Spr = ins.minSp / 2
        #maxSp
        if(Spr > (ins.Books.booksBestAsk.px - ins.Books.booksBestBid.px) / 2 + 100):
            Spr = (ins.Books.booksBestAsk.px - ins.Books.booksBestBid.px) / 2 + 100
            
        Skew = 0
        #posRatio = ins.pos / ins.maxPos
        #if(posRatio > 0.3):#Long
        #    if(posRatio > 1):
        #        posRatio = 1
        #    Skew -= posRatio * Spr
        #elif(posRatio <  - 0.3):
        #    if(posRatio < -1):
        #        posRatio = -1
        #    Skew -= posRatio * Spr 
            
        #if(ins.bookImbalance > 0.3):
        #    Skew += ins.bookImbalance * Spr
        #elif(ins.bookImbalance < -0.3):
        #    Skew += ins.bookImbalance * Spr
            
        #if(Skew > Spr):
        #    Skew = Spr
        #elif(Skew < -Spr):
        #    Skew = -Spr
            
        if(Skew > 0):
            askPx = math.floor(ins.Mid + Spr + Skew) 
            bidPx = math.floor(ins.Mid - Spr + Skew) 
        elif(Skew < 0):
            askPx = math.ceil(ins.Mid + Spr + Skew)
            bidPx = math.ceil(ins.Mid - Spr + Skew)
        else:
            askPx = math.ceil(ins.Mid + Spr + Skew)
            bidPx = math.floor(ins.Mid - Spr + Skew)
            
        if(askPx < ins.lastAskPx and ins.lastAskPx > 0):
            expectingAskQty = (ins.lastAskPx - askPx) * ins.topOfBook
            
        if(bidPx > ins.lastBidPx and ins.lastBidPx > 0):
            expectingBidQty = (bidPx - ins.lastBidPx) * ins.topOfBook
            
        if(expectingAskQty > ins.maxliveOrd):
            expectingAskQty = ins.maxliveOrd
        if(expectingBidQty > ins.maxliveOrd):
            expectingBidQty = ins.maxliveOrd
        
        liveBuyOrders = expectingBidQty
        liveSellOrders = expectingAskQty
        
        currentMaxAskPx = askPx - 1
        currentMinBidPx = bidPx + 1
        #Always Cancel -> New
        
        self.logFile.write("AskPx:" + str(askPx) + "   BidPx:" + str(bidPx) + "\n")
        self.logFile.write("LastAskPx:" + str(ins.lastAskPx) + "   LastBidPx:" + str(ins.lastBidPx) + "\n")
        tempAsk = ins.lastAskPx
        while(tempAsk <= ins.lastMaxAskPx):
            self.logFile.write("tempAsk:" + str(tempAsk) + "\n")
            if(tempAsk in ins.sellOrders.keys()):
                self.logFile.write("Order Exist" + "\n")
                odr = ins.sellOrders[tempAsk]
                if(tempAsk < askPx):
                    self.oms.sendCanOrder(ins.ts, ins, odr.clOrdId)
                    self.logFile.write("Cancelled:" + odr.clOrdId + "\n")
                else:
                    if(liveSellOrders >= ins.maxliveOrd):
                        self.oms.sendCanOrder(ins.ts, ins, odr.clOrdId)
                        self.logFile.write("Cancelled:" + odr.clOrdId + "\n")
                    else:
                        self.logFile.write("Not Cancelled. liveSellOrders:" + str(liveSellOrders) + "\n")
                        liveSellOrders += odr.sz
                        currentMaxAskPx = tempAsk
                        #End of if(tempAsk < askPx):
            tempAsk += 1
     
        tempBid = ins.lastBidPx
        while(tempBid >= ins.lastMinBidPx):
            self.logFile.write("tempBid:" + str(tempBid) + "\n")
            if(tempBid in ins.buyOrders.keys()):
                self.logFile.write("Order Exists" + "\n")
                odr = ins.buyOrders[tempBid]
                if(tempBid > bidPx):
                    self.oms.sendCanOrder(ins.ts, ins, odr.clOrdId)
                    self.logFile.write("Cancelled:" + odr.clOrdId + "\n")
                else:
                    if(liveBuyOrders >= ins.maxliveOrd):
                        self.oms.sendCanOrder(ins.ts, ins, odr.clOrdId)
                        self.logFile.write("Cancelled:" + odr.clOrdId + "\n")
                    else:
                        self.logFile.write("Not Cancelled. liveBuyOrders:" + str(liveBuyOrders) + "\n")
                        liveBuyOrders += odr.sz
                        currentMinBidPx = tempBid
            #End of if(tempBid > bidPx):
            tempBid -= 1
            
        if(expectingBidQty > 0):
            self.logFile.write("expectingBidQty:" + str(expectingBidQty) + "\n")
            tempBid = bidPx
            while(tempBid > ins.lastBidPx or ins.lastBidPx == 0):
                self.oms.sendNewOrder(ins.ts, ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, ins.topOfBook,tempBid * ins.tickSz)                
                if(tempBid < currentMinBidPx):
                    currentMinBidPx = tempBid
                self.logFile.write("New Buy Order Sent:" + str(tempBid) + "\n")
                tempBid -= 1
                expectingBidQty -= ins.topOfBook
                if(expectingBidQty <= 0):
                    break
                
        if(expectingAskQty > 0):
            self.logFile.write("expectingAskQty:" + str(expectingAskQty) + "\n")
            tempAsk = askPx
            while(tempAsk < ins.lastAskPx or ins.lastAskPx == 0):
                self.oms.sendNewOrder(ins.ts, ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.SELL, OKExEnums.orderType.LIMIT, ins.topOfBook,tempAsk * ins.tickSz)
                if(tempAsk > currentMaxAskPx):
                    currentMaxAskPx = tempAsk
                self.logFile.write("New Sell Order Sent:" + str(tempAsk) + "\n")
                tempAsk += 1
                expectingAskQty -= ins.topOfBook
                if(expectingAskQty <= 0):
                    break
                
        if(liveSellOrders < ins.maxliveOrd):
            self.logFile.write("liveSellOrders:" + str(liveSellOrders) + "\n")
            while(liveSellOrders < ins.maxliveOrd):
                currentMaxAskPx += 1
                self.oms.sendNewOrder(ins.ts, ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.SELL, OKExEnums.orderType.LIMIT, ins.topOfBook,currentMaxAskPx * ins.tickSz)
                self.logFile.write("New Sell Order Sent:" + str(currentMaxAskPx) + "\n")
                liveSellOrders += ins.topOfBook
            
        if(liveBuyOrders < ins.maxliveOrd):
            self.logFile.write("liveBuyOrders:" + str(liveBuyOrders) + "\n")
            while(liveBuyOrders < ins.maxliveOrd):
                currentMinBidPx -= 1
                self.oms.sendNewOrder(ins.ts, ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, ins.topOfBook,currentMinBidPx * ins.tickSz)
                self.logFile.write("New Buy Order Sent:" + str(currentMinBidPx) + "\n")
                liveBuyOrders += ins.topOfBook
        
        
        ins.lastAskPx = askPx
        ins.lastBidPx = bidPx
        ins.lastMaxAskPx = currentMaxAskPx
        ins.lastMinBidPx = currentMinBidPx
        self.logFile.write("Ask:" + str(ins.lastAskPx) + "   " + str(ins.lastMaxAskPx) + "\n")
        self.logFile.write("Bid:" + str(ins.lastBidPx) + "   " + str(ins.lastMinBidPx) + "\n")
        self.logFile.flush()
        
    def startTrading(self):
        self.optimizing = True
        
    def readInsParam(self,insList,filename):
        f = open(filename,'r')
        print("Trading Instrument:")
        for line in f:
            lst = line.split(',')
            if(lst[0] in insList.keys()):
                ins = insList[lst[0]]
                ins.setParams(lst)
                if(ins.isTrading):
                    print(ins.instId)
                    

optimizer = Optimizer()
