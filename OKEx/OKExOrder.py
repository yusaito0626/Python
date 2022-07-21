# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:58:19 2022

@author: yusai
"""

import OKExEnums

class order:
    def __init__(self):
        self.clOrdId = ""
        self.ordId = ""#Provided by OKEx
        self.instId = ""
        self.status = OKExEnums.orderState.NONE
        self.side = OKExEnums.side.NONE
        self.px = 0.0
        self.sz = 0.0
        self.filledSz = 0.0
        self.openSz = 0.0
        self.avgPx = 0.0
        self.live = False#From receving ack to filled or sending cancel
        
        self.priorQuantity = 0
        
        #Store amending order infomation. Update px/sz when receiving ack.
        self.newPx = 0.0
        self.newSz = 0.0
        
        self.ts = 0
        self.org_ts = 0
        self.msg = ""
        
    def init(self):
        self.clOrdId = ""
        self.ordId = ""#Provided by OKEx
        self.instId = ""
        self.status = OKExEnums.orderState.NONE
        self.side = OKExEnums.side.NONE
        self.px = 0.0
        self.sz = 0.0
        self.filledSz = 0.0
        self.openSz = 0.0
        self.avgPx = 0.0
        self.live = False#From receving ack to filled or sending cancel
        
        self.priorQuantity = 0
        
        #Store amending order infomation. Update px/sz when receiving ack.
        self.newPx = 0.0
        self.newSz = 0.0
        
        self.ts = 0
        self.msg = ""
        
    def ToString(self):
        line = str(self.ts) + "," + self.instId + "," + self.clOrdId + "," + str(self.status) + "," + \
            str(self.side) + "," + str(self.px) + "," + str(self.sz) + "," + str(self.openSz) + "," + \
            str(self.filledSz) + "," + str(self.avgPx)
        return line
        
    #def update(self,ack):
    