# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 14:07:15 2022

@author: yusai
"""

import math
from Utils import params
import OKExEnums
import OKExMessage
import OKExOrder
from Utils import Utils

class Book:
    def __init__(self,org=None):
        if(org==None):
            self.side = OKExEnums.side.NONE
            self.px = 0
            self.sz = 0.0
            self.szSell = 0.0
            self.szBuy = 0.0
            self.liqOrd = 0
            self.numOfOrdBuy = 0
            self.numOfOrdSell = 0
            self.myOrders = {}#For Backtest
            self.myOrdSz = 0.0
            self.myNumOfOrd = 0
            self.idx = 0
            self.next = 0#Use idx as iterator.
            self.prev = 0#Use idx as iterator.
            self.ts = 0
        else:
            self.side = org.side
            self.px = org.px
            self.sz = org.sz
            self.szSell = org.szSell
            self.szBuy = org.szBuy
            self.liqOrd = org.liqOrd
            self.numOfOrdBuy = org.numOfOrdBuy
            self.numOfOrdSell = org.numOfOrdSell
            for o in org.myOrders:
                self.myOrders[o.clOrdId] = o
            self.myOrdSz = org.myOrdSz
            self.myNumOfOrd = org.myNumOfOrd
            self.idx = org.idx
            self.next = org.next
            self.prev = org.prev
            self.ts = org.ts
        
    def ToString(self):
        line = str(self.ts) + "," + str(self.side) + "," + str(self.px) + "," + str(self.sz) + ","
        line += str(self.liqOrd) + "," + str(self.numOfOrdBuy) + ","  + str(self.numOfOrdSell) + "," 
        line += str(self.idx) + "," + str(self.next) + "," + str(self.prev)
        return line
    
    def initialize(self):
        self.side = OKExEnums.side.NONE
        self.px = 0
        self.sz = 0.0
        self.szSell = 0.0
        self.szBuy = 0.0
        self.liqOrd = 0
        self.numOfOrdBuy = 0
        self.numOfOrdSell = 0
        self.myOrders = {}#For Backtest
        self.myOrdSz = 0.0
        self.myNumOfOrd = 0
        self.ts = 0
        #self.idx = 0 Don't init idx
        self.next = 0#Use idx as iterator.
        self.prev = 0#Use idx as iterator.
        
    def UpdateBook(self,msgBook, side, priceUnit,ts):
        #if(self.ts >= ts and self.side != side and self.sz > 0 and msgBook.qty == 0):
        #    return 
        if(side == OKExEnums.side.BUY):
            self.szBuy = msgBook.qty
            self.numOfOrdBuy = msgBook.NumOfOrd
        elif(side == OKExEnums.side.SELL):
            self.szSell = msgBook.qty
            self.numOfOrdSell = msgBook.NumOfOrd
        
        if(self.szBuy - self.szSell > 0):
            self.sz = self.szBuy - self.szSell
            self.side = OKExEnums.side.BUY
        elif(self.szBuy - self.szSell < 0):
            self.sz = self.szSell - self.szBuy
            self.side = OKExEnums.side.SELL
        else:
            self.sz = 0
            self.side = OKExEnums.side.NONE

        self.px = int(msgBook.px * priceUnit)
        #self.sz = msgBook.qty
        self.liqOrd = msgBook.LiqOrd
        self.ts = ts


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
        self.books = {}
        self.booksBestAsk = self.aend
        self.booksBestBid = self.bend
        self.maxAsk = self.aend
        self.minBid = self.bend
        self.numOfBooks = 0
        self.ts = 0
        self.priceUnit = 1#Price multiplier to convert price to int
        self.depth = 0
        self.ctType = OKExEnums.ctType.NONE
        self.ctVal = 1
        self.ordList = {} #Pair of Id and order object
        self.liveOrdList = {}
        
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
    
    def setOrder(self,order):
        #order = OKExOrder.order()
        if(order.status == OKExEnums.orderState.WAIT_NEW):
            self.liveOrdList[order.clOrdId] = order
            idx = self.findBook(order.side, order.px * self.priceUnit)
            if(idx > 0):
                if(order.side == OKExEnums.side.BUY):
                    self.bids[idx].myOrders[order.clOrdId] = order
                elif(order.side == OKExEnums.side.SELL):
                    self.asks[idx].myOrders[order.clOrdId] = order
        #Update orders when ack received if it is mod or can.
    
    def setAckMsg(self,msg):
        #Update orders. check execution.
        msg = OKExMessage.msgOrder()
        if(msg.op == "order" or msg.op == "batch-order"):#New
            for ack in msg.ackList:
                if(ack.clOrdId in self.liveOrdList):
                    order = self.liveOrdList[ack.clOrdId]
                    order.live = True
                    order.status = OKExEnums.orderState.LIVE
                    idx = self.findBook(order.side, order.px * self.priceUnit)
                    if(idx > 0):
                        if(order.side == OKExEnums.side.BUY):
                            order.priorQuantity = self.bids[idx].sz
                        elif(order.side == OKExEnums.side.SELL):
                            order.priorQuantity = self.asks[idx].sz
                    else:
                        if(order.side == OKExEnums.side.BUY):
                            idxOtherSide = self.findBook(OKExEnums.side.SELL, order.px * self.priceUnit)
                            
                        elif(order.side == OKExEnums.side.SELL):
                            order.priorQuantity = self.asks[idx].sz
                        order.priorQuantity = -1
        elif(msg.op == "amend-order" or msg.op == "batch-amend-order"):#Mod
            for ack in msg.ackList:
                if(ack.clOrdId in self.liveOrdList):
                    order = self.liveOrdList[ack.clOrdId]
                    #if(order.px == order.newPx):

        #elif(msg.op == "cancel-order" or msg.op == "batch-cancel-order"):#Can
        
    #def orderUpdate(self,newbook,side):
        
    def printBooks(self,depth=0,side=OKExEnums.side.NONE):
        line = ""
        if(side==OKExEnums.side.NONE or side==OKExEnums.side.SELL):
            #Reverse
            ask = self.booksBestAsk
            i = 0
            while(ask.px <= self.maxAsk.px):
                line = str(ask.side) + "," + str(ask.sz) + "," + str(ask.px) + "\n" + line
                i += 1
                if(depth!=0 and i >=depth):
                    break
                else:
                    ask = self.books[ask.px + 1]
        if(side==OKExEnums.side.NONE or side==OKExEnums.side.BUY):
            bid = self.booksBestBid
            i = 0
            while(bid.px >= self.minBid.px):
                line += str(bid.side) + ",       ," + str(bid.px) + "," + str(bid.sz) + "\n"
                i += 1
                if(depth>0 and i >=depth):
                    break
                else:
                    bid = self.books[bid.px - 1]
        return line
        
    def findBest(self,px,side):
        temppx = px
        if(not temppx in self.books):
            return None
        if(side == OKExEnums.side.BUY):
            while(temppx >= self.minBid.px):
                book = self.books[temppx]
                if(book.sz > 0 and book.side == OKExEnums.side.BUY):
                    return book
                else:
                    temppx -= 1
        elif(side == OKExEnums.side.SELL):
            while(temppx <= self.maxAsk.px):
                book = self.books[temppx]
                if(book.sz > 0 and book.side == OKExEnums.side.SELL):
                    return book
                else:
                    temppx += 1
    
    def reshapeBooks(self):
        print("Reshaping books Current Best Price  Bid:" + str(self.booksBestBid.px) + "   Ask:" + str(self.booksBestAsk.px))
        print("Current price range  min:" + str(self.minBid.px) + "   max:" + str(self.maxAsk.px))        
        numOfBids = self.booksBestBid.px - self.minBid.px
        numOfAsks = self.maxAsk.px - self.booksBestAsk.px
        numOfMovingObj = int((numOfBids - numOfAsks) / 2)
        if(numOfMovingObj > 0):#Bid to Ask
            prevpx = self.minBid.px
            obj = self.minBid
            px_dif = self.maxAsk.px - self.minBid.px + 1
            while(numOfMovingObj > 0):
                obj = self.books.pop(prevpx)
                obj.initialize()
                obj.px = prevpx + px_dif
                self.books[obj.px] = obj
                self.maxAsk = obj
                prevpx += 1
                self.minBid = self.books[prevpx]
                numOfMovingObj -= 1
        elif(numOfMovingObj < 0):#Ask to Bid
            prevpx = self.maxAsk.px
            obj = self.maxAsk
            px_dif = self.minBid.px - self.maxAsk.px - 1
            while(numOfMovingObj < 0):
                obj = self.books.pop(prevpx)
                obj.initialize()
                obj.px = prevpx + px_dif
                self.books[obj.px] = obj
                self.minBid = obj
                prevpx -= 1
                self.maxAsk = self.books[prevpx]
                numOfMovingObj += 1
        print("New price range  min:" + str(self.minBid.px) + "   max:" + str(self.maxAsk.px))
    def initializeBoard(self,snapshot,depth):
        self.bids.clear()
        self.asks.clear()
        self.books.clear()
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
                    bk.UpdateBook(b, OKExEnums.side.BUY, self.priceUnit,self.ts)
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
    
            i = 0                
            for a in data.asks:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    a.qty *= float(self.ctVal) / float(a.px) * float(self.priceUnit)
                else:
                    a.qty *= float(self.ctVal)
                if(i < depth):
                    bk = Book()
                    bk.UpdateBook(a, OKExEnums.side.SELL, self.priceUnit,self.ts)
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

        #Initialize books
        self.numOfBooks = 10000
        bpx = self.BestBid.px + 1
        bestaskpx = self.BestAsk.px
        cnt = 0
        while(bpx < bestaskpx):
            bk = Book()
            bk.px = bpx
            self.books[bpx] = bk
            bpx += 1
            cnt += 1
        bid = self.BestBid
        ask = self.BestAsk
        bidpx = self.BestBid.px
        askpx = self.BestAsk.px
        while(cnt < 10000):
            if(bid.idx >= 0 and bidpx == bid.px):
                bk = Book(bid)
                self.books[bk.px] = bk
                if(self.booksBestBid.idx < 0 or bk.px > self.booksBestBid.px):
                    self.booksBestBid = bk
                self.minBid = bk
                cnt += 1
                if(bid.next < 0):
                    bidpx = bid.px - 1
                    bid = self.bend
                else:
                    bid = self.bids[bid.next]
            else:
                bk = Book()
                bk.px = bidpx
                self.books[bk.px] = bk
                bidpx -= 1
                cnt += 1
                self.minBid = bk
                
            if(ask.idx >= 0 and askpx == ask.px):
                bk = Book(ask)
                self.books[bk.px] = bk
                if(self.booksBestAsk.idx < 0 or bk.px < self.booksBestAsk.px):
                    self.booksBestAsk = bk
                self.maxAsk = bk
                cnt += 1
                if(ask.next < 0):
                    askpx = ask.px + 1
                    ask = self.aend
                else:
                    ask = self.asks[ask.next]
            else:
                bk = Book()
                bk.px = askpx
                self.books[bk.px] = bk
                self.maxAsk = bk
                askpx += 1
                cnt += 1
                
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
                    bk.side = OKExEnums.side.BUY
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
                    blank.side = OKExEnums.side.BUY
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
        ask = self.BestAsk
        j = 0
        while(True):
            if(ask.px + 1 == self.asks[ask.next].px):
                ask = self.asks[ask.next]
            else:
                if(i < depth):
                    bk = Book()
                    bk.px = ask.px + 1
                    bk.side = OKExEnums.side.SELL
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
                    blank.side = OKExEnums.side.SELL
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
                if(int(b.px * self.priceUnit) in self.books):
                    book = self.books[int(b.px * self.priceUnit)]
                    orgSide = book.side
                    book.UpdateBook(b,OKExEnums.side.BUY,self.priceUnit,self.ts)
                    if(book.side == OKExEnums.side.BUY):
                        if(book.sz > 0 and book.px > self.booksBestBid.px):
                            self.booksBestBid = book
                        elif(book.px == self.booksBestBid.px and book.sz == 0):
                            temp_bid = self.findBest(book.px, OKExEnums.side.BUY)
                            if(temp_bid != None):
                                self.booksBestBid = temp_bid
                            else:
                                print("Couldn't find BestBid")
                    else:
                        temp_bid = self.findBest(self.booksBestBid.px, OKExEnums.side.BUY)
                        if(temp_bid != None):
                            self.booksBestBid = temp_bid
                        else:
                            print("Couldn't find BestBid")
                    if(orgSide != book.side and book.px >= self.booksBestBid.px):
                        temp_ask = self.findBest(self.booksBestAsk.px, OKExEnums.side.SELL)
                        if(temp_ask != None):
                            self.booksBestAsk = temp_ask
                        else:
                            print("Couldn't find BestAsk")
                            #print(self.printBooks(20))
                    if(self.booksBestBid.px -self.minBid.px < 2000):
                        self.reshapeBooks()
                #bidx = self.findBook(OKExEnums.side.BUY,int(b.px * self.priceUnit))
                #if(bidx >= 0):
                #    bid = self.bids[bidx]
                #    bid.UpdateBook(b,OKExEnums.side.BUY,self.priceUnit)
                #    if(bid.px == self.BestBid.px and bid.sz == 0):
                #        cnt = 0
                #        while(True):
                #            endprev = self.bids[self.bend.prev]
                #            newpx = int(endprev.px - 1)
                #            nxtbk = self.bids[bid.next]
                #            bid.initialize()
                #            bid.px = newpx
                #            bid.side = OKExEnums.side.BUY
                #            bid.prev = self.bend.prev
                #            bid.next = endprev.next
                #            self.bend.prev = bid.idx
                #            endprev.next = bid.idx
                #            if(nxtbk.sz > 0):
                #                self.BestBid = nxtbk
                #                break
                #            else:
                #                bid = nxtbk
                #                newpx -= 1
                #                cnt += 1
                #                if(cnt >= self.depth):
                #                    self.BestBid = bid
                #                    print("The bid books are all 0. instId:" + self.instId)
                #                    #print(self.strBids())
                #                    break
                #            
                #elif(b.px * self.priceUnit > self.BestBid.px and b.qty > 0):#Higher than bestbid. Ignore if sz == 0
                #    newpx = int(self.BestBid.px + 1)
                #    i = 0
                #    while(i < self.depth):
                #        blank = self.bids[self.bend.prev]
                #        prev = self.bids[blank.prev]
                #        self.bend.prev = prev.idx
                #        prev.next = blank.next
                #        blank.initialize()
                #        if(int(b.px * self.priceUnit) == newpx):
                #            blank.UpdateBook(b, OKExEnums.side.BUY,self.priceUnit)
                #            self.BestBid.prev = blank.idx
                #            blank.next = self.BestBid.idx
                #            self.BestBid = blank
                #            break
                #        else:
                #            blank.px = newpx
                #            blank.sz = 0
                #            self.BestBid.prev = blank.idx
                #            blank.next = self.BestBid.idx
                #            self.BestBid = blank
                #            newpx += 1
                #            i += 1
            #print(len(self.bids))
            for a in data.asks:
                if(self.ctType == OKExEnums.ctType.INVERSE):
                    a.qty *= float(self.ctVal) / float(a.px) * float(self.priceUnit)
                else:
                    a.qty *= float(self.ctVal)
                if(int(a.px * self.priceUnit) in self.books):
                    book = self.books[int(a.px * self.priceUnit)]
                    orgSide = book.side
                    #if(book.side == OKExEnums.side.BUY):
                    #    print(book.ToString())
                    book.UpdateBook(a,OKExEnums.side.SELL,self.priceUnit,self.ts)
                    if(book.side==OKExEnums.side.SELL):
                        if(book.sz > 0 and book.px < self.booksBestAsk.px):
                            self.booksBestAsk = book
                        elif(book.px == self.booksBestAsk.px and book.sz == 0):
                            temp_ask = self.findBest(book.px, OKExEnums.side.SELL)
                            if(temp_ask != None):
                                self.booksBestAsk = temp_ask
                            else:
                                print("Couldn't find BestAsk")
                    else:
                        temp_ask = self.findBest(self.booksBestAsk.px, OKExEnums.side.SELL)
                        if(temp_ask != None):
                            self.booksBestAsk = temp_ask
                        else:
                            print("Couldn't find BestAsk")
                    if(orgSide != book.side and book.px <= self.booksBestAsk.px):
                        temp_bid = self.findBest(self.booksBestBid.px, OKExEnums.side.BUY)
                        if(temp_bid != None):
                            self.booksBestBid = temp_bid
                        else:
                            print("Couldn't find BestBid")
                            #print(self.printBooks(20))
                    if(self.maxAsk.px - self.booksBestAsk.px < 2000):
                        self.reshapeBooks()
                #aidx = self.findBook(OKExEnums.side.SELL,int(a.px * self.priceUnit))
                #if(aidx >= 0):
                #    ask = self.asks[aidx]
                #    ask.UpdateBook(a,OKExEnums.side.SELL,self.priceUnit)
                #    if(ask.px == self.BestAsk.px and ask.sz == 0):
                #        cnt = 0
                #        endprev = self.asks[self.aend.prev]
                #        newpx = int(endprev.px + 1)
                #        nxtbk = self.asks[ask.next]
                #        while(True):
                #            ask.initialize()
                #            ask.px = newpx
                #            ask.side = OKExEnums.side.SELL
                #            ask.prev = endprev.idx
                #            ask.next = self.aend.idx
                #            self.aend.prev = ask.idx
                #            endprev.next = ask.idx
                #            if(nxtbk.sz > 0):
                #                self.BestAsk = nxtbk
                #                break
                #            else:
                #                endprev = ask
                #                ask = nxtbk
                #                nxtbk = self.asks[ask.next]
                #                newpx += + 1
                #                cnt += 1
                #                if(cnt >= self.depth):
                #                    self.BestAsk = ask
                #                    print("The ask books are all 0. instId:" + self.instId)
                                    #print(self.strAsks())
                #                    break
                #            
                #elif(a.px * self.priceUnit < self.BestAsk.px) and a.qty > 0:#Lower than bestask
                #    newpx = int(self.BestAsk.px - 1)
                #    i = 0
                #    while(i < self.depth):
                #        blank = self.asks[self.aend.prev]
                #        prev = self.asks[blank.prev]
                #        self.aend.prev = prev.idx
                #        prev.next = self.aend.idx
                #        blank.initialize()
                #        if(int(a.px * self.priceUnit) == newpx):
                #            blank.UpdateBook(a, OKExEnums.side.SELL, self.priceUnit)
                #            self.BestAsk.prev = blank.idx
                #            blank.next = self.BestAsk.idx
                #            self.BestAsk = blank
                #            break
                #        else:
                #            blank.px = newpx
                #            blank.sz = 0
                #            self.BestAsk.prev = blank.idx
                #            blank.next = self.BestAsk.idx
                #            self.BestAsk = blank
                #            newpx -= 1
                #            i += 1
            #print(len(self.asks))
        if(self.booksBestAsk.px <= self.booksBestBid.px):
            print("Ask:" + str(self.booksBestAsk.px) + "  Bid:" + str(self.booksBestBid.px))
            #print(self.printBooks(20))
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
        self.bookDepth = 2000
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
        
        self.avgSqrBookImbalance = 0.0
        self.avgSpread = 0.0
        self.startTimeBI = 0
        self.lastTimeBI= 0
        self.startTimeSP = 0
        self.lastTimeSP= 0
        
        #From File
        self.histVolatility = 0.0
        self.histAvgSpread = 0
        self.maxPos = 0
        
        self.minSp = 0
        self.topOfBook = 0.0
        self.skew = 0
        self.maxVol = 0
        
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
        #print("Update Trades Called")
        #self.instId = ""
        #self.tradeId = ""
        #self.px = 0.0
        #self.sz = 0.0
        #self.side = OKExEnums.side.NONE
        #self.ts = 0
        #msg = OKExMessage.pushData()
        #print(msg.ToString())
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
            
    def calcHistData(self):        
        if(self.startTimeBI == 0):
            self.startTimeBI = self.ts
            self.lastTimeBI = self.ts
        else:
            self.avgSqrBookImbalance += (self.ts - self.lastTimeBI) * self.bookImbalance * self.bookImbalance
            self.lastTimeBI = self.ts
        if(self.startTimeSP == 0):
            self.startTimeSP = self.ts
            self.lastTimeSP = self.ts
        elif(self.Books.booksBestAsk.px > 0 and self.Books.booksBestBid.px > 0 and self.Books.booksBestAsk.px  > self.Books.booksBestBid.px):
            self.avgSpread += (self.ts - self.lastTimeSP) * (self.Books.booksBestAsk.px - self.Books.booksBestBid.px)
            self.lastTimeSP = self.ts
            
    def outputHistData(self):
        self.avgSpread /= self.lastTimeSP - self.startTimeSP
        self.avgSqrBookImbalance /= self.lastTimeBI - self.startTimeBI
        return  self.instId + "," + str(self.avgSpread) + ","  + \
            str(self.realizedVolatility) + "," + str(self.avgSqrBookImbalance) + ","  + \
            str(self.execAskCnt) + ","  + str(self.execAskVol)  + ","  + str(self.execAskAmt) + "," + \
            str(self.execBidCnt) + ","  + str(self.execBidVol)  + ","  + str(self.execBidAmt)
    
    def updateBooks(self,msg):#get pushData
        #msg = OKExMessage.pushData()
        if(msg.arg["channel"]=="books"):#snapshot or update
            for d in msg.data:
                if(self.ts < d.ts):
                    self.ts = d.ts
                    self.calcHistData()
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
                    self.bestBidPxRing[self.ringIdx].add(self.Books.booksBestBid.px)
                    self.bestAskPxRing[self.ringIdx].add(self.Books.booksBestAsk.px)
                    self.ringDataCount += 1
                    if(self.ringDataCount > params.posMAPeriod * 60):
                        maPos = 0.0
                        i = 0
                        while(i < params.posMAPeriod):
                            maPos += self.posRing[self.ringIdx].relative(-i)
                            i += 1
                        maPos /= params.posMAPeriod
                        self.posMARing[self.ringIdx].add(maPos)
                    if(self.ringDataCount > params.midMAPeriod * 60):
                        maMid = 0.0
                        i = 0
                        while(i < params.midMAPeriod):#Check Price?
                            maMid += self.bestAskPxRing[self.ringIdx].relative(-i) + self.bestBidPxRing[self.ringIdx].relative(-i)
                            i += 1
                        maMid /= params.posMAPeriod * 2
                        self.midMARing[self.ringIdx].add(maMid)
                    count += 1
                    if(count > 10000):
                        #error
                        break
                    
    def updateOrder(self,tkt):
        i = 0
    def updatePosition(self,msg):
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