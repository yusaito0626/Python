# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 22:03:04 2022

@author: yusai
"""

import math
from OKEx.Utils import params
from OKEx import OKExInstrument
from OKEx import OKExOMS

class Optimizer:
    
    #def __init__(self):
        
        
    def initialize(self,oms):
        self.oms = oms
        
    def calcBookImbalance(ins):
        bid = ins.Books.BestBid
        ask = ins.Books.BestAsk
        minsum = 0.01
        bidsum = 0
        asksum = 0
        i = 0
        while(i < params.biTicks):
            if(bid.idx > 0):
                bidsum += bid.sz * math.exp(-math.log(ins.Books.BestBid.px / bid.px) * params.biDecayingParam)
                if(bid.next > 0):
                    bid = ins.Books.bids[bid.next]
                else:
                    bid = ins.Books.bend
            if(ask.idx > 0):
                asksum += ask.sz * math.exp(-math.log(ask.px / ins.Books.BestAsk.px) * params.biDecayingParam)
                if(ask.next > 0):
                    ask = ins.Books.asks[ask.next]
                else:
                    ask = ins.Books.aend
            i += 1
        if(bidsum < minsum):
            bidsum = minsum
        if(asksum < minsum):
            asksum = minsum
            
        return math.log(asksum / bidsum)
    
    def calcFactors(self,ins):
        ins = OKExInstrument.Instrument()
        ins.updateRings()
        ins.bookImbalance = self.calcBookImbalance(ins)
        if(ins.ringDataCount > params.RVPeriod * 60):
            ins.currentRV = math.pow(ins.realizedVolatility - ins.rvRing[ins.ringIdx].relative(-params.RVPeriod),0.5)
        
    #def Optimize(self,ins):