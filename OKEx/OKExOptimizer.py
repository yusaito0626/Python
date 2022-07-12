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
    
    #def __init__(self):
        
        
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
        ins = OKExInstrument.Instrument()
        self.oms = OKExOMS.OMS()
        #Sp:Volatility, Spread
        askPx = 0
        bidPx = 0
        expectingAskQty = 0
        expectingBidQty = 0
        liveSellOrders = 0
        liveBuyOrders = 0
        
        Spr = ins.CurrentRV * ins.Mid#Half Spread
        if(Spr < ins.minSp / 2):
            Spr = ins.minSp / 2
        
        Skew = 0
        posRatio = ins.pos / ins.maxPos
        if(posRatio > 0.3):#Long
            if(posRatio > 1):
                posRatio = 1
            Skew -= posRatio * Spr
        elif(posRatio <  - 0.3):
            if(posRatio < -1):
                posRatio = -1
            Skew -= posRatio * Spr 
            
        if(ins.bookImbalance > 0.3):
            Skew += ins.bookImbalance * Spr
        elif(ins.bookImbalance < -0.3):
            Skew += ins.bookImbalance * Spr
            
        if(Skew > Spr):
            Skew = Spr
        elif(Skew < -Spr):
            Skew = -Spr
            
        if(Skew > 0):
            askPx = math.floor((ins.Mid + Spr + Skew) / ins.tickSz) * ins.tickSz
            bidPx = math.floor((ins.Mid - Spr + Skew) / ins.tickSz) * ins.tickSz
        elif(Skew < 0):
            askPx = math.ceil((ins.Mid + Spr + Skew) / ins.tickSz) * ins.tickSz
            bidPx = math.ceil((ins.Mid - Spr + Skew) / ins.tickSz) * ins.tickSz
        else:
            askPx = math.ceil((ins.Mid + Spr + Skew) / ins.tickSz) * ins.tickSz
            bidPx = math.floor((ins.Mid - Spr + Skew) / ins.tickSz) * ins.tickSz
            
        if(askPx < ins.lastAskPx and ins.lastAskPx > 0):
            expectingAskQty = (ins.lastAskPx - askPx) * ins.topOfBook
            
        if(bidPx > ins.lastBidPx and ins.lastBidPx > 0):
            expectingBidQty = (bidPx - ins.lastBidPx) * ins.topOfBook
        
        liveBuyOrders = expectingBidQty
        liveSellOrders = expectingAskQty
        #Always Cancel -> New
        tempAsk = ins.lastAskPx
        while(tempAsk < ins.lastMaxAskPx):
            odr = ins.sellOrders[tempAsk]
            if(tempAsk < askPx or liveSellOrders >= ins.maxPos):
                self.oms.sendCanOrder(ins, odr.clOrdId)
            else:
                liveSellOrders += odr.sz
                if(liveSellOrders >= ins.maxPos):
                    ins.lastMaxAskPx = tempAsk
            tempAsk += 1
            
        tempBid = ins.lastBidPx
        while(tempBid > ins.lastMinBidPx):
            odr = ins.buyOrders[tempBid]
            if(tempBid > bidPx or liveBuyOrders >= ins.maxPos):
                self.oms.sendCanOrder(ins, odr.clOrdId)
            else:
                liveBuyOrders += odr.sz
                if(liveBuyOrders >= ins.maxPos):
                    ins.lastMinBidPx = tempBid
            tempBid -= 1
            
        if(expectingBidQty > 0):
            tempBid = ins.bidPx
            while(tempBid > ins.lastBidPx):
                self.oms.sendNewOrder(ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, ins.topOfBook,tempBid)
                tempBid -= 1
                liveBuyOrders += ins.topOfBook
                expectingBidQty -= ins.topOfBook
                if(expectingBidQty <= 0 or liveBuyOrders >= ins.maxPos):
                    break
                
        if(expectingAskQty > 0):
            tempAsk = ins.askPx
            while(tempAsk < ins.lastAskPx):
                self.oms.sendNewOrder(ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.SELL, OKExEnums.orderType.LIMIT, ins.topOfBook,tempAsk)
                tempAsk += 1
                liveSellOrders += ins.topOfBook
                expectingAskQty -= ins.topOfBook
                if(expectingAskQty <= 0 or liveSellOrders >= ins.maxPos):
                    break
                
        if(liveSellOrders < ins.maxPos):
            tempAsk = ins.lastMaxAskPx
            while(liveSellOrders < ins.maxPos):
                tempAsk += 1
                self.oms.sendNewOrder(ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.SELL, OKExEnums.orderType.LIMIT, ins.topOfBook,tempAsk)
                liveSellOrders += ins.topOfBook
            ins.lastMaxAskPx = tempAsk
            
        if(liveBuyOrders < ins.maxPos):
            tempBid = ins.lastBidPx
            while(liveBuyOrders < ins.maxPos):
                tempBid -= 1
                self.oms.sendNewOrder(ins, OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, ins.topOfBook,tempBid)
                liveBuyOrders += ins.topOfBook
            ins.lastMinBidPx = tempBid
            
        ins.askPx = askPx
        ins.bidPx = bidPx