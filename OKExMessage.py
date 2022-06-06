# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:58:10 2022

@author: yusai
"""
import OKExEnums

class AckSubscribe:
    subtype = OKExEnums.subscribeType.NONE
    channel = ""
    insType = OKExEnums.instType.NONE
    uly = ""
    instId = ""

class odrTicket:
    instId = ""
    tdMode = OKExEnums.tradeMode.NONE
    ccy = ""
    ordId = ""
    clOrdId = ""
    tag = ""
    side = OKExEnums.Side.NONE
    posSide = OKExEnums.positionSide.NONE
    ordType = OKExEnums.orderType.NONE
    sz = 0
    px = 0
    reduceOnly = False
    tgtCcy = OKExEnums.quantityType.NONE
    banAmend = False
    #Only Amend Orders
    cxlOnFail = False
    reqId = ""
    
class SndOrder:
    uniId = ""
    op = ""
    orderList = []#List of odrTicket
    
class ackTicket:
    ordId = ""
    clOrdId = ""
    tag = ""
    sCode = 0
    sMsg = ""
    reqId = ""
    
class AckOrder:
    uniId = ""
    op = ""
    errCode = 0
    errMsg = ""
    ackList = []#List of ackTicket
    
    