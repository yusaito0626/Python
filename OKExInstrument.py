# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 14:07:15 2022

@author: yusai
"""

import OKExEnums

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
        line += str(self.liqOrd) + "," + str(self.NumOfOrd) + "," 
        line += str(self.idx) + "," + str(self.next) + "," + str(self.prev)
        return line
    
    def initialize(self):
        self.bs = OKExEnums.side.NONE
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
        self.px = (msgBook.px * priceUnit)
        self.sz = msgBook.qty
        self.liqOrd = msgBook.LiqOrd
        self.NumOfOrd = msgBook.NumOfOrd


class Board:
    def __init__(self):
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
                if(bid.next < 0 or j >= self.depth):
                    break
            i = 0                
            for a in data.asks:
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
                if(ask.next < 0 or j >= self.depth):
                    break
                
    def updateBooks(self,dataUpdate):    
        for data in dataUpdate.data:
            if(data.ts > self.ts):
                self.ts = data.ts
            #If the price is found in dict,replace
            #else if the price is inside of best bid and ask, replace end.__prev to new price
            for b in data.bids:
                bidx = self.findBook(OKExEnums.side.BUY,b.px * self.priceUnit)
                if(bidx >= 0):
                    bid = self.bids[bidx]
                    bid.UpdateBook(b,OKExEnums.side.BUY,self.priceUnit)
                    if(bid.px == self.BestBid.px and bid.sz == 0):
                        cnt = 0
                        while(True):
                            endprev = self.bids[self.bend.prev]
                            newpx = endprev.px - 1
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
                                    print("The bid books are all 0.")
                                    break
                            
                elif(b.px * self.priceUnit > self.BestBid.px and b.qty > 0):#Higher than bestbid. Ignore if sz == 0
                    newpx = self.BestBid.px + 1
                    i = 0
                    while(i < self.depth):
                        blank = self.bids[self.bend.prev]
                        prev = self.bids[blank.prev]
                        self.bend.prev = prev.idx
                        prev.next = blank.next
                        blank.initialize()
                        if(b.px * self.priceUnit == newpx):
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
            for a in data.asks:
                aidx = self.findBook(OKExEnums.side.SELL,a.px * self.priceUnit)
                if(aidx >= 0):
                    ask = self.asks[aidx]
                    ask.UpdateBook(a,OKExEnums.side.SELL,self.priceUnit)
                    if(ask.px == self.BestAsk.px and ask.sz == 0):
                        cnt = 0
                        while(True):
                            endprev = self.asks[self.aend.prev]
                            newpx = endprev.px + 1
                            nxtbk = self.asks[ask.next]
                            ask.initialize()
                            ask.px = newpx
                            ask.bs = OKExEnums.side.SELL
                            ask.prev = self.aend.prev
                            ask.next = endprev.next
                            self.aend.prev = ask.idx
                            endprev.next = ask.idx
                            if(nxtbk.sz > 0):
                                self.BestAsk = nxtbk
                                break
                            else:
                                ask = nxtbk
                                newpx += + 1
                                cnt += 1
                                if(cnt >= self.depth):
                                    print("The ask books are all 0.")
                                    break
                            
                elif(a.px * self.priceUnit < self.BestAsk.px) and a.qty > 0:#Lower than bestask
                    newpx = self.BestAsk.px - 1
                    i = 0
                    while(i < self.depth):
                        blank = self.asks[self.aend.prev]
                        prev = self.asks[blank.prev]
                        self.aend.prev = prev.idx
                        prev.next = blank.next
                        blank.initialize()
                        if(a.px * self.priceUnit == newpx):
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
class Instrument:
    
    def __init__(self):
        self.instId = ""
        self.Books = Board()
        self.ordList = {} #Pair of Id and order object
        self.liveOrdList = {}

        
    
        self.Mid = 0.0
    
        self.ts = 0
    
        #Factors

        