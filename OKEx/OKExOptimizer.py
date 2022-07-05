# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 22:03:04 2022

@author: yusai
"""

import math
from Utils import params
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
            if(bid.idx > 0):
                bidsum += bid.sz * math.exp(-math.log(ins.Books.booksBestBid.px / bid.px) * params.biDecayingParam)
                if(bid.px - 1 in ins.Books.books):
                    bid = ins.Books.books[bid.px - 1]
                else:
                    bid = ins.Books.bend
            if(ask.idx > 0):
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
        #print(ins.bookImbalance)
        if(ins.ringDataCount > params.RVPeriod * 60):
            ins.currentRV = math.pow(ins.realizedVolatility - ins.rvRing[ins.ringIdx].relative(-params.RVPeriod),0.5)
        
    #def Optimize(self,ins):