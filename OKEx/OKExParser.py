# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 18:31:58 2022

@author: yusai
"""

import json
import queue
import OKExEnums
import OKExMessage


class OKExParser:
    def __init__(self):
        self.PDATAQSIZE = 100000
        self.ORDBOOKQSIZE = 100000
        self.BOOKQSIZE = 1000000
        self.ORDQSIZE = 100000
        self.ACKTKTQSIZE = 10000
        self.SNDTKTQSIZE = 10000
        self.TRADEQSIZE = 100000
        self.pDataPool = queue.LifoQueue(self.PDATAQSIZE)
        self.ordBookPool = queue.LifoQueue(self.ORDBOOKQSIZE)
        self.bookPool = queue.LifoQueue(self.BOOKQSIZE)
        self.ordPool = queue.LifoQueue(self.ORDQSIZE)
        self.ackTktPool = queue.LifoQueue(self.ACKTKTQSIZE)
        self.sndtktPool = queue.LifoQueue(self.SNDTKTQSIZE)
        self.tradePool = queue.LifoQueue(self.TRADEQSIZE)
        
        i = 0
        while(True):
            chk = False
            if(i < self.PDATAQSIZE):
                self.pDataPool.put(OKExMessage.pushData())
                chk = True
            if(i < self.ORDBOOKQSIZE):
                self.ordBookPool.put(OKExMessage.dataOrderBook())
                chk = True
            if(i < self.BOOKQSIZE):
                self.bookPool.put(OKExMessage.book())
                chk = True
            if(i < self.ORDQSIZE):
                self.ordPool.put(OKExMessage.msgOrder())
                chk = True
            if(i < self.ACKTKTQSIZE):
                self.ackTktPool.put(OKExMessage.ackTicket())
                chk = True
            if(i < self.SNDTKTQSIZE):
                self.sndtktPool.put(OKExMessage.odrTicket())
                chk = True
            if(i < self.TRADEQSIZE):
                self.tradePool.put(OKExMessage.dataTrade())
                chk = True
            if(not chk):
                break
            else:
                i += 1
                
    def ParseOp(self,msg):
        data = json.loads(msg)
        out = self.ordPool.get()
        if(data["op"]=="order" or data["op"]=="batch-orders"):
            out.op = data["op"]
            out.uniId = data["id"]
            out.errCode = int(data["code"])
            out.errMsg = data["msg"]
            i = 0
            for d in data["data"]:
                if(i > 0):
                    out.ackList.append(self.ackTktPool.get())
                tkt = out.ackList[i]
                tkt.clOrdId = d["clOrdId"]
                tkt.ordId = d["ordId"]
                tkt.tag = d["tag"]
                tkt.sCode = int(d["sCode"])
                tkt.sMsg = d["sMsg"]
                i += 1
        elif(data["op"]=="cancel-order" or data["op"]=="batch-cancel-orders"):
            out.op = data["op"]
            out.uniId = data["id"]
            out.errCode = int(data["code"])
            out.errMsg = data["msg"]
            i = 0
            for d in data["data"]:
                if(i > 0):
                    out.ackList.append(self.ackTktPool.get())
                tkt = out.ackList[i]
                tkt.clOrdId = d["clOrdId"]
                tkt.ordId = d["ordId"]
                tkt.sCode = int(d["sCode"])
                tkt.sMsg = d["sMsg"]
                i += 1
        elif(data["op"]=="amend-order" or data["op"]=="batch-amend-orders"):
            out.op = data["op"]
            out.uniId = data["id"]
            out.errCode = int(data["code"])
            out.errMsg = data["msg"]
            i = 0
            for d in data["data"]:
                if(i > 0):
                    out.ackList.append(OKExMessage.ackTicket())
                tkt = out.ackList[i]
                tkt.clOrdId = d["clOrdId"]
                tkt.ordId = d["ordId"]
                tkt.reqId = d["reqId"]
                tkt.sCode = int(d["sCode"])
                tkt.sMsg = d["sMsg"]
                i += 1
        return out
    
    def ParseEvent(self,msg):
        data = json.loads(msg)
        pData = self.pDataPool.get()
        pData.dataType = "event"
        pData.arg = data["arg"]
        pData.arg["event"] = data["event"]
        if(data["event"]=="subscribe"):
            return pData
        elif(data["event"]=="unsubscribe"):
            return pData
        elif(data["event"]=="error"):
            return pData
    
    def ParsePushData(self,msg):
        #print("ParsePushData Called")
        js = json.loads(msg)
        pData = self.pDataPool.get()
        pData.dataType = "push"
        pData.arg = js["arg"]
        #print(type(js["data"]))
        if(js["arg"]["channel"]=="account"):
            for data in js["data"]:
                out = OKExMessage.dataAccount()
                out.uTime = int(data["uTime"])
                out.totalEq = float(data["totalEq"])
                out.isoEq = float(data["isoEq"])
                out.adjEq = float(data["adjEq"])
                out.ordFroz = float(data["ordFroz"])
                out.imr = float(data["imr"])
                out.mmr = float(data["mmr"])
                out.mgnRatio = float(data["mgnRatio"])
                out.notionalUsd = float(data["notionalUsd"])
                for d in data["details"]:
                    detail = OKExMessage.dataAccDetail()
                    detail.ccy = d["ccy"]
                    detail.eq = float(d["eq"])
                    detail.cashBal = float(d["cashBal"])
                    detail.uTime = int(d["uTime"])
                    detail.isoEq = float(d["isoEq"])
                    detail.availEq = float(d["availEq"])
                    detail.disEq = float(d["disEq"])
                    detail.availBal = float(d["availBal"])
                    detail.frozenBal = float(d["frozenBal"])
                    detail.ordFrozen = float(d["ordFrozen"])
                    detail.liab = float(d["liab"])
                    detail.upl = float(d["upl"])
                    detail.uplLiab = float(d["uplLiab"])
                    detail.crossLiab = float(d["crossLiab"])
                    detail.isoLiab = float(d["isoLiab"])
                    detail.mgnRatio = float(d["mgnRatio"])
                    detail.interest = float(d["interest"])
                    detail.twap = int(d["twap"])
                    detail.maxLoan = float(d["maxLoan"])
                    detail.eqUsd = float(d["eqUsd"])
                    detail.notionalLever = float(d["notionalLever"])
                    detail.coinUsdPrice = float(d["coinUsdPrice"])
                    detail.stgyEq = float(d["stgyEq"])
                    detail.isoUpl = float(d["isoUpl"])
                    out.details.append(detail)
                pData.data.append(out)
            return pData
        elif(js["arg"]["channel"]=="positions"):
        
            return pData
        elif(js["arg"]["channel"]=="balance_and_position"):
            for data in js["data"]:
                obj = OKExMessage.dataBalandPos()
                obj.pTime = data["pTime"]
                obj.eventType = data["eventType"]
                for bal in data["balData"]:
                    balobj = OKExMessage.dataBal(bal)
                    obj.balList.append(balobj)
                for pos in data["posData"]:
                    posobj = OKExMessage.dataPosition(pos)
                    obj.posList.append(posobj)
                pData.data.append(obj)
            return pData
        elif(js["arg"]["channel"]=="orders"):
            for data in js["data"]:
                obj = OKExMessage.dataOrder(data)
                pData.data.append(obj)
            return pData
        elif(js["arg"]["channel"]=="orders-algo"):
        
            return pData
        elif(js["arg"]["channel"]=="algo-advance"):
        
            return pData
        elif(js["arg"]["channel"]=="liquidation-warning"):
        
            return pData
        elif(js["arg"]["channel"]=="account-greeks"):
        
            return pData
        elif(js["arg"]["channel"]=="rfqs"):
        
            return pData
        elif(js["arg"]["channel"]=="quotes"):
        
            return pData
        elif(js["arg"]["channel"]=="struc-block-trades"):
        
            return pData
        elif(js["arg"]["channel"]=="grid-orders-spot"):
        
            return pData
        elif(js["arg"]["channel"]=="grid-orders-contraact"):
        
            return pData
        elif(js["arg"]["channel"]=="grid-positions"):
        
            return pData
        elif(js["arg"]["channel"]=="grid-sub-orders"):
        
            return pData
        elif(js["arg"]["channel"]=="instruments"):
        
            return pData
        elif(js["arg"]["channel"]=="tickers"):
        
            return pData
        elif(js["arg"]["channel"]=="open-interest"):
        
            return pData
        elif(js["arg"]["channel"][0:6]=="candle"):
        
            return pData
        elif(js["arg"]["channel"]=="estimated-price"):
        
            return pData
        elif(js["arg"]["channel"]=="mark-price"):
        
            return pData
        elif(js["arg"]["channel"][0:16]=="mark-price-candle"):
        
            return pData
        elif(js["arg"]["channel"]=="price-limit"):
        
            return pData
        elif(js["arg"]["channel"][0:5]=="books"):
            pData.arg["action"] = js["action"]#snapshot or update
            for data in js["data"]:#data contains asks,bids,ts,checksum
                ordbook = self.ordBookPool.get()
                ordbook.ts = int(data["ts"])
                ordbook.checksum = int(data["checksum"])
                for a in data["asks"]:
                    bk = self.bookPool.get()
                    bk.px = float(a[0])
                    bk.qty = float(a[1])
                    bk.LiqOrd = float(a[2])
                    bk.NumOfOrd = int(a[3])
                    ordbook.asks.append(bk)
                for b in data["bids"]:
                    bk = self.bookPool.get()
                    bk.px = float(b[0])
                    bk.qty = float(b[1])
                    bk.LiqOrd = float(b[2])
                    bk.NumOfOrd = int(b[3])
                    ordbook.bids.append(bk)
                pData.data.append(ordbook)
            return pData
        elif(js["arg"]["channel"]=="trades"):
            for data in js["data"]:#data contains asks,bids,ts,checksum
                trade = self.tradePool.get()
                trade.ts = int(data["ts"])
                trade.instId = data["instId"]
                trade.tradeId = data["tradeId"]
                trade.px = float(data["px"])
                trade.sz = float(data["sz"])
                if(data["side"]=="buy"):
                    trade.side = OKExEnums.side.BUY
                elif(data["side"]=="sell"):
                    trade.side = OKExEnums.side.SELL
                
                pData.data.append(trade)
            return pData
        elif(js["arg"]["channel"]=="opt-summary"):
        
            return pData
        elif(js["arg"]["channel"]=="funding-rate"):
        
            return pData
        elif(js["arg"]["channel"][0:12]=="index-candle"):
        
            return pData
        elif(js["arg"]["channel"]=="index-tickers"):
        
            return pData
        elif(js["arg"]["channel"]=="status"):
        
            return pData
        elif(js["arg"]["channel"]=="public-struc-block-trades"):
        
            return pData
        elif(js["arg"]["channel"]=="block-tickers"):

            return pData        

    def Parse(self,msg):
        idx = msg.find("\"op\"")
        if(idx > 0):
            return self.ParseOp(msg)
        else:
            idx = msg.find("\"event\"")
            if(idx > 0):
                return self.ParseEvent(msg)
            else:
                return self.ParsePushData(msg)
            
    def pushOrdObj(self,obj):
        i = 0
        tktInObj = None
        odrInObj = None
        for tkt in obj.ackList:
            tkt.init()
            if(i > 0):
                self.ackTktPool.put(tkt)
            else:
                tktInObj = tkt
                i += 1
        i = 0
        for odr in obj.orderList:
            odr.init()
            if(i > 0):
                self.sndtktPool.put(odr)
            else:
                odrInObj = odr
                i += 1
        obj.init(tktInObj,odrInObj)
        self.ordPool.put(obj)
    def pushPDataObj(self,obj):
        if(obj.arg["channel"]=="books"):
            for d in obj.data:
                #orderbook
                for a in d.asks:
                    a.init()
                    self.bookPool.put(a)
                for b in d.bids:
                    b.init()
                    self.bookPool.put(b)
                d.init()
                self.ordBookPool.put(d)
        elif(obj.arg["channel"]=="trades"):
            for d in obj.data:
                #trade
                d.init()
                self.tradePool.put(d)
        obj.init()
        self.pDataPool.put(obj)



parser = OKExParser()