# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 18:31:58 2022

@author: yusai
"""

import OKExMessage
import json

def ParseOp(msg):
    data = json.loads(msg)
    if(data["op"]=="order" or data["op"]=="batch-orders"):
        out = OKExMessage.AckOrder()
        out.op = data["op"]
        out.uniId = data["id"]
        out.errCode = int(data["code"])
        out.errMsg = data["msg"]
        for d in data["data"]:
            tkt = OKExMessage.ackTicket()
            tkt.clOrdId = d["clOrdId"]
            tkt.ordId = d["ordId"]
            tkt.tag = d["tag"]
            tkt.sCode = int(d["sCode"])
            tkt.sMsg = d["sMsg"]
            out.ackList.append(tkt)
        return out
    elif(data["op"]=="cancel-order" or data["op"]=="batch-cancel-orders"):
        out = OKExMessage.AckOrder()
        out.op = data["op"]
        out.uniId = data["id"]
        out.errCode = int(data["code"])
        out.errMsg = data["msg"]
        for d in data["data"]:
            tkt = OKExMessage.ackTicket()
            tkt.clOrdId = d["clOrdId"]
            tkt.ordId = d["ordId"]
            tkt.sCode = int(d["sCode"])
            tkt.sMsg = d["sMsg"]
            out.ackList.append(tkt)
        return out
    elif(data["op"]=="amend-order" or data["op"]=="batch-amend-orders"):
        out = OKExMessage.AckOrder()
        out.op = data["op"]
        out.uniId = data["id"]
        out.errCode = int(data["code"])
        out.errMsg = data["msg"]
        for d in data["data"]:
            tkt = OKExMessage.ackTicket()
            tkt.clOrdId = d["clOrdId"]
            tkt.ordId = d["ordId"]
            tkt.reqId = d["reqId"]
            tkt.sCode = int(d["sCode"])
            tkt.sMsg = d["sMsg"]
            out.ackList.append(tkt)
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
    js = json.loads(msg)
    pData = OKExMessage.pushData()
    pData.arg = js["arg"]
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
    elif(data["arg"]["channel"]=="positions"):
        out = OKExMessage.dataPosition()
        
    elif(data["arg"]["channel"]=="balance_and_position"):

    elif(data["arg"]["channel"]=="orders"):

    elif(data["arg"]["channel"]=="orders-algo"):

    elif(data["arg"]["channel"]=="algo-advance"):

    elif(data["arg"]["channel"]=="liquidation-warning"):

    elif(data["arg"]["channel"]=="account-greeks"):

    elif(data["arg"]["channel"]=="rfqs"):

    elif(data["arg"]["channel"]=="quotes"):

    elif(data["arg"]["channel"]=="struc-block-trades"):

    elif(data["arg"]["channel"]=="grid-orders-spot"):

    elif(data["arg"]["channel"]=="grid-orders-contraact"):

    elif(data["arg"]["channel"]=="grid-positions"):

    elif(data["arg"]["channel"]=="grid-sub-orders"):

    elif(data["arg"]["channel"]=="instruments"):

    elif(data["arg"]["channel"]=="tickers"):

    elif(data["arg"]["channel"]=="open-interest"):

    elif(data["arg"]["channel"][0:5]=="candle"):

    elif(data["arg"]["channel"]=="trades"):

    elif(data["arg"]["channel"]=="estimated-price"):

    elif(data["arg"]["channel"]=="mark-price"):

    elif(data["arg"]["channel"][0:15]=="mark-price-candle"):

    elif(data["arg"]["channel"]=="price-limit"):

    elif(data["arg"]["channel"][0:4]=="books"):

    elif(data["arg"]["channel"]=="opt-summary"):

    elif(data["arg"]["channel"]=="funding-rate"):

    elif(data["arg"]["channel"][0:11]=="index-candle"):

    elif(data["arg"]["channel"]=="index-tickers"):

    elif(data["arg"]["channel"]=="status"):

    elif(data["arg"]["channel"]=="public-struc-block-trades"):

    elif(data["arg"]["channel"]=="block-tickers"):
        

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
    