# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 18:31:58 2022

@author: yusai
"""

import json
from OKEx import OKExMessage

def ParseOp(msg):
    data = json.loads(msg)
    if(data["op"]=="order" or data["op"]=="batch-orders"):
        out = OKExMessage.msgOrder()
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
            tkt.tag = d["tag"]
            tkt.sCode = int(d["sCode"])
            tkt.sMsg = d["sMsg"]
            i += 1
        return out
    elif(data["op"]=="cancel-order" or data["op"]=="batch-cancel-orders"):
        out = OKExMessage.msgOrder()
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
            tkt.sCode = int(d["sCode"])
            tkt.sMsg = d["sMsg"]
            i += 1
        return out
    elif(data["op"]=="amend-order" or data["op"]=="batch-amend-orders"):
        out = OKExMessage.msgOrder()
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
    
def ParseEvent(msg):
    data = json.loads(msg)
    if(data["event"]=="subscribe"):
        return data
    elif(data["event"]=="unsubscribe"):
        return data
    elif(data["event"]=="error"):
        return data
    
def ParsePushData(msg):
    print("ParsePushData Called")
    js = json.loads(msg)
    pData = OKExMessage.pushData()
    pData.arg = js["arg"]
    print(type(js["data"]))
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
        
        return pData
    elif(js["arg"]["channel"]=="orders"):
        
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
    elif(js["arg"]["channel"]=="trades"):
        
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
            ordbook = OKExMessage.dataOrderBook()
            ordbook.ts = int(data["ts"])
            ordbook.checksum = int(data["checksum"])
            for a in data["asks"]:
                bk = OKExMessage.book()
                bk.px = float(a[0])
                bk.qty = float(a[1])
                bk.LiqOrd = float(a[2])
                bk.NumOfOrd = int(a[3])
                ordbook.asks.append(bk)
            for b in data["bids"]:
                bk = OKExMessage.book()
                bk.px = float(b[0])
                bk.qty = float(b[1])
                bk.LiqOrd = float(b[2])
                bk.NumOfOrd = int(b[3])
                ordbook.bids.append(bk)
            pData.data.append(ordbook)
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

def Parse(msg):
    idx = msg.find("\"op\"")
    if(idx > 0):
        return ParseOp(msg)
    else:
        idx = msg.find("\"event\"")
        if(idx > 0):
            return ParseEvent(msg)
        else:
            return ParsePushData(msg)
    