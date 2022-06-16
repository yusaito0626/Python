# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 14:07:15 2022

@author: yusai
"""

import OKExMessage
import OKExEnums
import queue

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
        self.__next = 0#Use price as iterator.
        self.__prev = 0#Use price as iterator.
        
    def UpdateBook(self,msgBook, side):
        self.bs = side
        self.px = msgBook.px
        self.sz = msgBook.qty
        self.LiqOrd = msgBook.LiqOrd
        self.NumOfOrd = msgBook.NumOfOrd

class Board:
    def __init__(self):
        self.bend = Book()
        self.aend = Book()
        self.aend.px = -1
        self.bend.px = -1
        self.BestAsk = self.aend
        self.BestBid = self.bend
        self.bids = {}
        self.asks = {}
        self.ts = 0
        self.priceUnit = 1
        self.depth = 0
        
    def initializeBoard(self,snapshot,depth):
        self.bids.clear()
        self.asks.clear()
        self.depth = depth
        for data in snapshot.data:
            if(data.ts > self.ts):
                self.ts = data.ts
            i = 0
            for b in data.bids:
                if(i < depth):
                    bk = Book()
                    bk.UpdateBook(b, OKExEnums.side.BUY)
                    self.bids.update({b.px * self.priceUnit,bk})
                    i += 1
                    if(self.BestBid.px == -1 or self.BestBid.px < bk.px):
                        self.BestBid.__prev = bk.px * self.priceUnit
                        bk.__next = self.BestBid.px * self.priceUnit
                        self.BestBid = bk
                    else:
                        tempbk = self.BestBid
                        while(True):
                            if(bk.px > tempbk.px or tempbk.px == -1):#Insert between books
                                prev = self.bids[tempbk.__prev]
                                prev.__next = bk.px * self.priceUnit
                                bk.__prev = prev.px * self.priceUnit
                                tempbk.__prev = bk.px * self.priceUnit
                                bk.__next = tempbk.px * self.priceUnit
                                break
                elif(b.px * self.priceUnit > self.bend.__prev):#if the price is larger than bend.__prev insert
                    blank = self.bids[self.bend.__prev]
                    current = self.bids[blank.__prev]
                    self.bend.__prev = current.px * self.priceUnit
                    current.__next = self.bend.px * self.priceUnit
                    blank.__init__()
                    blank.UpdateBook(b, OKExEnums.side().BUY)
                    nxt = self.bend
                    while(True):
                        if(current.px > blank.px):
                            nxt.__prev = blank.px * self.priceUnit
                            blank.__next = nxt.px * self.priceUnit
                            current.__next = blank.px * self.priceUnit
                            blank.__prev = current.px * self.priceUnit
                            break
                        elif(current.px == self.BestBid.px):#new book is bestbid
                            self.BestBid.__prev = blank.px * self.priceUnit
                            blank.__next = self.BestBid.px * self.priceUnit
                            self.BestBid = blank
                            break
                        else:
                            nxt = current
                            current = self.bids[nxt.__prev]
            #0 fill
            bid = self.BestBid
            while(True):
                if(bid.px * self.priceUnit - 1 in self.bids):
                    bid = self.bids[bid.px * self.priceUnit - 1]
                else:
                    blank = self.bids[self.bend.__prev]
                    self.bend.__prev = blank.__prev
                    self.bids[blank.__prev].next = blank.__next
                    blank.__init__()
                    blank.px = bid.px - 1.0 /self.priceUnit
                    blank.bs = OKExEnums.side.BUY
                    nxt = self.bids[bid.__next]
                    blank.__prev = nxt.__prev
                    blank.__next = bid.__next
                    bid.__next = bid.px * self.priceUnit - 1
                    nxt.__prev = bid.__next
                    bid = blank
                if(bid.__next < 0):
                    break
            i = 0                
            for a in data.asks:
                if(i < depth):
                    bk = Book()
                    bk.UpdateBook(a, OKExEnums.side.SELL)
                    self.asks.update({a.px * self.priceUnit,bk})
                    i += 1
                    if(self.BestAsk.px == -1 or self.BestAsk.px > bk.px):
                        self.BestAsk.__prev = bk.px * self.priceUnit
                        bk.__next = self.BestAsk.px * self.priceUnit
                        self.BestAsk = bk
                    else:
                        tempbk = self.BestAsk
                        while(True):
                            if(bk.px < tempbk.px or tempbk.px == -1):#Insert between books
                                prev = self.asks[tempbk.__prev]
                                prev.__next = bk.px * self.priceUnit
                                bk.__prev = prev.px * self.priceUnit
                                tempbk.__prev = bk.px * self.priceUnit
                                bk.__next = tempbk.px * self.priceUnit
                                break
                elif(a.px * self.priceUnit > self.aend.__prev):#if the price is larger than bend.__prev insert
                    blank = self.asks[self.aend.__prev]
                    current = self.asks[blank.__prev]
                    self.aend.__prev = current.px * self.priceUnit
                    current.__next = self.aend.px * self.priceUnit
                    blank.__init__()
                    blank.UpdateBook(a, OKExEnums.side.SELL)
                    nxt = self.aend
                    while(True):
                        if(current.px < blank.px):
                            nxt.__prev = blank.px * self.priceUnit
                            blank.__next = nxt.px * self.priceUnit
                            current.__next = blank.px * self.priceUnit
                            blank.__prev = current.px * self.priceUnit
                            break
                        elif(current.px == self.BestAsk.px):#new book is bestask
                            self.BestAsk.__prev = blank.px * self.priceUnit
                            blank.__next = self.BestAsk.px * self.priceUnit
                            self.BestAsk = blank
                            break
                        else:
                            nxt = current
                            current = self.asks[nxt.__prev]
            #0 fill
            ask = self.BestAsk
            while(True):
                if(ask.px * self.priceUnit + 1 in self.asks):
                    ask = self.asks[ask.px * self.priceUnit + 1]
                else:
                    blank = self.asks[self.aend.__prev]
                    self.aend.__prev = blank.__prev
                    self.asks[blank.__prev].next = blank.__next
                    blank.__init__()
                    blank.px = ask.px + 1.0 /self.priceUnit
                    blank.bs = OKExEnums.side.SELL
                    nxt = self.asks[ask.__next]
                    blank.__prev = nxt.__prev
                    blank.__next = ask.__next
                    ask.__next = ask.px * self.priceUnit + 1
                    nxt.__prev = ask.__next
                    ask = blank
                if(ask.__next < 0):
                    break
        
    def updateBooks(self,dataUpdate):    
        for data in dataUpdate.data:
            if(data.ts > self.ts):
                self.ts = data.ts
            #If the price is found in dict,replace
            #else if the price is inside of best bid and ask, replace end.__prev to new price
            for b in data.bids:
                if(b.px * self.priceUnit in self.bids):
                    bid = self.bids[b.px * self.priceUnit]
                    bid.UpdateBook(b,OKExEnums.side.BUY)
                    if(bid.px == self.BestBid.px and bid.sz == 0):
                        newpx = self.bend.__prev - 1
                        endprev = self.bids[self.bend.__prev]
                        cnt = 0
                        while(True):
                            nxtbk = self.bids[bid.__next]
                            bid.__init__()
                            bid.px = float(newpx) / self.priceUnit
                            bid.bs = OKExEnums.side.BUY
                            bid.__prev = self.bend.__prev
                            bid.__next = endprev.__next
                            self.bend.__prev = newpx
                            endprev.__next = newpx
                            endprev = bid
                            if(nxtbk.sz > 0):
                                self.BestBid = nxtbk
                                break
                            else:
                                bid = nxtbk
                                cnt += 1
                                if(cnt >= self.depth):
                                    print("The bid books are all 0.")
                                    break
                            
                elif(b.px > self.BestBid.px):
                    blank = self.bids[self.bend.__prev]
                    prev = self.bids[blank.__prev]
                    self.bend.__prev = prev.px * self.priceUnit
                    prev.__next = blank.__next
                    blank.__init__()
                    blank.UpdateBook(b, OKExEnums.side.BUY)
                    self.BestBid.__prev = blank.px * self.priceUnit
                    blank.__next = self.BestBid.px * self.priceUnit
                    self.BestBid = blank
            for a in data.asks:
                if(a.px * self.priceUnit in self.asks):
                    ask = self.asks[a.px * self.priceUnit]
                    ask.UpdateBook(a,OKExEnums.side.SELL)
                    if(ask.px == self.BestAsk.px and ask.sz == 0):
                        newpx = self.aend.__prev + 1
                        endprev = self.asks[self.aend.__prev]
                        cnt = 0
                        while(True):
                            nxtbk = self.asks[ask.__next]
                            ask.__init__()
                            ask.px = float(newpx) / self.priceUnit
                            ask.bs = OKExEnums.side.SELL
                            ask.__prev = self.aend.__prev
                            ask.__next = endprev.__next
                            self.aend.__prev = newpx
                            endprev.__next = newpx
                            endprev = ask
                            if(nxtbk.sz > 0):
                                self.BestAsk = nxtbk
                                break
                            else:
                                ask = nxtbk
                                cnt += 1
                                if(cnt >= self.depth):
                                    print("The ask books are all 0.")
                                    break
                            
                elif(a.px < self.BestAsk.px):
                    blank = self.asks[self.aend.__prev]
                    prev = self.asks[blank.__prev]
                    self.aend.__prev = prev.px * self.priceUnit
                    prev.__next = blank.__next
                    blank.__init__()
                    blank.UpdateBook(a, OKExEnums.side.SELL)
                    self.BestAsk.__prev = blank.px * self.priceUnit
                    blank.__next = self.BestAsk.px * self.priceUnit
                    self.BestAsk = blank
class Instrument:
    
    instId = ""
    Books = {} #Pair of Price and book object
    ordList = {} #Pair of Id and order object
    liveOrdList = {}
    
    BestAsk = OKExMessage.book()
    BestBid = OKExMessage.book()

    priceUnit = 1#Price multiplier to convert price to int
    
    Mid = 0.0
    
    ts = 0
    
    #Factors
    
    
    def UpdateBooks(self,pdata):
        if(pdata.arg["action"]=="snapshot"):#refresh books
            self.Books.clear()
            for data in pdata.data:
                if(data.ts > self.ts):
                    self.ts = data.ts
                for b in data.bids:
                    self.Books.update({b.px * self.priceUnit,b})
                    if(self.BestBid.px == 0 or self.BestBid.px < b.px):
                        self.BestBid = b
                for a in data.asks:
                    self.Books.update({a.px * self.priceUnit,a})
                    if(self.BestAsk.px == 0 or self.BestAsk.px < a.px):
                        self.BestAsk = a
        else:#update
            for data in pdata.data:
                if(data.ts > self.ts):
                    self.ts = data.ts
                for b in data.bids:
                    self.Books[b.px * self.priceUnit] = b
                    if(self.BestBid.px == 0 or self.BestBid.px < b.px):
                        self.BestBid = b
                for a in data.asks:
                    self.Books[a.px * self.priceUnit] = a
                    if(self.BestAsk.px == 0 or self.BestAsk.px < a.px):
                        self.BestAsk = a
        