# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 19:58:10 2022

@author: yusai
"""
from OKEx import OKExEnums

class AckSubscribe:    
    def __init__(self):
        self.subtype = OKExEnums.subscribeType.NONE
        self.channel = ""
        self.insType = OKExEnums.instType.NONE
        self.uly = ""
        self.instId = ""
        self.ccy = ""
        
class pushData:
    def __init__(self):
        self.arg = {}
        self.data = []
        
    def ToString(self):
        msg = ""
        for a in self.arg.values():
            msg += a + ","
        for d in self.data:
            msg += d.ToString() + ","
        
        return msg[0:len(msg) - 1]
    

### Trade ###

class odrTicket:
    def __init__(self):
        self.instId = ""
        self.tdMode = OKExEnums.tradeMode.NONE
        self.ccy = ""
        self.ordId = ""
        self.clOrdId = ""
        self.tag = ""
        self.side = OKExEnums.side.NONE
        self.posSide = OKExEnums.positionSide.NONE
        self.ordType = OKExEnums.orderType.NONE
        self.sz = 0
        self.px = 0
        self.reduceOnly = False
        self.tgtCcy = OKExEnums.quantityType.NONE
        self.banAmend = False
    #Only Amend Orders
        self.cxlOnFail = False
        self.reqId = ""
        
    def ToString(self):
        return self.instId + "," + str(self.tdMode) + "," + self.ccy + "," + \
            self.ordId + "," + self.clOrdId + "," + self.tag + "," + str(self.side) + "," + \
            str(self.posSide) + "," + str(self.ordType) + "," + str(self.sz) + "," + \
            str(self.px) + "," + str(self.reduceOnly) + "," + str(self.tgtCcy) + "," + \
            str(self.banAmend) + "," + str(self.cxlOnFail) + "," + self.reqId
            
class ackTicket:
    def __init__(self):
        self.ordId = ""
        self.clOrdId = ""
        self.tag = ""
        self.sCode = 0
        self.sMsg = ""
        self.reqId = ""
    
    def ToString(self):
        return self.ordId + "," + self.clOrderId + "," + self.tag \
                + "," + str(self.sCode) + "," + self.sMsg + "," + self.reqId

class msgOrder:
    def __init__(self):
        self.uniId = ""
        self.op = ""
        self.errCode = 0
        self.errMsg = ""
        self.ackList = []#List of ackTicket
        self.orderList = []#List of odrTicket
        #Add one ticket each when initializing.
        #Add another as needed.
        self.ackList.append(ackTicket())
        self.orderList.append(odrTicket())
    
    def ToString(self):
        msg = self.uniId + "," + self.op + "," + str(self.errCode) + "," + self.errMsg + ","
        ackmsg = ","
        for ack in self.ackList:
            ackmsg += ack.ToString() + ","
        if(ackmsg != ","):
            msg += ackmsg
        ordmsg = ","
        for odr in self.orderList:
            ordmsg += odr.ToString() + ","
        if(ordmsg != ","):
            msg += ordmsg
        return msg[0:len(msg) - 1]
### Private Channel ###  
  
class dataAccDetail:
    def __init__(self):
        self.ccy = ""
        self.eq = ""
        self.cashBal = 0.0
        self.uTime = 0
        self.isoEq = 0.0
        self.availEq = 0.0
        self.disEq = 0.0
        self.availBal = 0.0
        self.frozenBal = 0.0
        self.ordFrozen = 0.0
        self.liab = 0.0
        self.upl = 0.0
        self.uolLiab = 0.0
        self.crossLiab = 0.0
        self.isoLiab = 0.0
        self.mgnRatio = 0.0
        self.interest = 0.0
        self.twap = 0.0
        self.maxLoan = 0.0
        self.eqUsd = 0.0
        self.notionalLever = 0.0
        self.coinUsdPrice = 0.0
        self.stgyEq = 0.0
        self.isoUpl = 0.0
    
class dataAccount:
    def __init__(self):
        self.uTime = 0
        self.totalEq = 0.0
        self.isoEq = 0.0
        self.adjEq = 0.0
        self.odrFroz = 0.0
        self.imr = 0.0
        self.mmr = 0.0
        self.mgnRatio = 0.0
        self.notionalUsd = 0.0
        self.details = []#List of dataAccDetail
    
class dataPosition:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.mgnMode = OKExEnums.mgnMode.NONE
        self.posSide = OKExEnums.positionSide.NONE
        self.pos = 0.0
        self.baseBal = 0.0
        self.quoteBal = 0.0
        self.posCcy = ""
        self.availPos = 0.0
        self.avgPx = 0.0
        self.upl = 0.0
        self.uplRatio = 0.0
        self.instId = ""
        self.lever = 0.0
        self.liqPx = 0.0
        self.markPx = 0.0
        self.imr = 0.0
        self.margin = 0.0
        self.mgnRatio = 0.0
        self.mmr = 0.0
        self.liab = 0.0
        self.liabCcy = 0.0
        self.interest = 0.0
        self.tradeId = ""
        self.notionalUsd = 0.0
        self.optVal = 0.0
        self.adl = 0
        self.ccy = ""
        self.last = 0.0
        self.usdPx = 0.0
        self.deltaBS = 0.0
        self.deltaPA = 0.0 
        self.gammaBS = 0.0
        self.gammaPA = 0.0
        self.thetaBS = 0.0
        self.thetaPA = 0.0
        self.vegaBS = 0.0
        self.vegaPA = 0.0
        self.cTime = 0
        self.uTime = 0
        self.pTime = 0
    
class dataBal:
    def __init__(self):
        self.ccy = ""
        self.cashBal = 0.0
        self.uTime = 0
    
class dataBalandPos:
    def __init__(self):
        self.pTime = 0
        self.eventType = OKExEnums.eventType.NONE
        self.balList = []#List of dataBal
        self.posList = []#List of dataPosition
    
class dataOrder:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.tgtCcy = OKExEnums.quantityType.NONE
        self.ccy = ""
        self.ordId = ""
        self.clOrdId = ""
        self.tag = ""
        self.px = 0.0
        self.sz = 0.0
        self.notionalUsd = 0.0
        self.ordType = OKExEnums.orderType.NONE
        self.side = OKExEnums.side.NONE
        self.posSide = OKExEnums.positionSide.NONE
        self.tdMode = OKExEnums.tradeMode.NONE
        self.fillPx = 0.0
        self.tradeId = ""
        self.fillSz = 0.0
        self.fillTime = 0
        self.fillFee = 0.0
        self.fillFeeCcy = ""
        self.execType = OKExEnums.execType.NONE
        self.accFillSz = 0.0
        self.fillNotionalUsd = 0.0
        self.avgPx = 0.0
        self.state = OKExEnums.orderState.NONE
        self.lever = 0.0
        self.tpTriggerPx = 0.0
        self.tpTriggerPxType = OKExEnums.priceType.NONE
        self.tpOrdPx = 0.0
        self.slTriggerPx = 0.0
        self.slTriggerPxType = OKExEnums.priceType.NONE
        self.slOrdPx = 0.0
        self.feeCcy = ""
        self.fee = 0.0
        self.rebateCcy = ""
        self.rebate = 0.0
        self.pnl = 0.0
        self.source = ""
        self.category = OKExEnums.category.NONE
        self.uTime = 0
        self.cTime = 0
        self.reqId = ""
        self.amendResult = OKExEnums.amendResult.NONE
        self.code = 0
        self.msg = ""
    #algo order channel
        self.algoId = ""
        self.actualSz = 0.0
        self.actualPx = 0.0
        self.actualSide = ""
        self.triggerTime = 0
    #Advanced algo order channel
        self.pxVar = 0.0
        self.pxSpread = 0.0
        self.szLimit = 0.0
        self.pxLimit = 0.0
        self.timeInterval = 0.0
        self.count = 0
        self.callbackRatio = 0.0
        self.callbackSpread = 0.0
        self.activePx = 0.0
        self.moveTriggerPx = 0.0
        self.pTime = 0
    
class dataLiquidationWarning:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.mgnMode = OKExEnums.mgnMode.NONE
        self.posSide = OKExEnums.positionSide.NONE
        self.pos = 0.0
        self.posCcy = ""
        self.availPos = 0.0
        self.avgPx = 0.0
        self.upl = 0.0
        self.uplRatio = 0.0
        self.instId = ""
        self.lever = 0.0
        self.liqPx = 0.0
        self.markPx = 0.0 
        self.imr = 0.0
        self.margin = 0.0
        self.mgnRatio = 0.0
        self.mmr = 0.0
        self.liab = 0.0
        self.liabCcy = ""
        self.interest = 0.0
        self.tradeId = ""
        self.notionalUsd = 0.0
        self.optVal = 0.0
        self.adl = 0
        self.ccy = ""
        self.last = 0.0
        self.deltaBS = 0.0
        self.deltaPA = 0.0 
        self.gammaBS = 0.0
        self.gammaPA = 0.0
        self.thetaBS = 0.0
        self.thetaPA = 0.0
        self.vegaBS = 0.0
        self.vegaPA = 0.0
        self.cTime = 0
        self.uTime = 0
        self.pTime = 0
    
class dataAccountGreeks:
    def __init__(self):
        self.deltaBS = 0.0
        self.deltaPA = 0.0 
        self.gammaBS = 0.0
        self.gammaPA = 0.0
        self.thetaBS = 0.0
        self.thetaPA = 0.0
        self.vegaBS = 0.0
        self.vegaPA = 0.0
        self.ccy = ""
        self.ts = 0
    
class rfqLeg:
    def __init__(self):
        self.InstId = ""
        self.sz = 0.0
        self.side = OKExEnums.side.NONE
        self.tgtCcy = OKExEnums.quantityType.NONE
    
class dataRfqs:
    def __init__(self):
        self.cTime = 0
        self.uTime = 0
        self.state = OKExEnums.rfqState.NONE
        self.counterparties = []#List of String
        self.validUntil = 0
        self.clRfqId = ""
        self.tradeCode = ""
        self.rfqId = ""
        self.legs = []#List of rfqLeg
    
class quoteLeg:
    def __init__(self):
        self.instId = ""
        self.sz = 0.0
        self.px = 0.0
        self.side = OKExEnums.side.NONE
        self.tgtCcy = OKExEnums.quantityType.NONE
    
class dataQuotes:
    def __init__(self):
        self.cTime = 0
        self.uTime = 0
        self.state = OKExEnums.rfqState.NONE
        self.validUntil = 0
        self.rfqId = ""
        self.clRfqId = ""
        self.quoteId = ""
        self.clQuoteID = ""
        self.quoteSide = OKExEnums.side.NONE
        self.legs = []#List of quoteLeg

class blockTradeLeg:
    def __init__(self):
        self.instId = ""
        self.px = 0.0
        self.sz = 0.0
        self.side = OKExEnums.side.NONE
        self.tgtCcy = OKExEnums.quantityType.NONE
        self.fee = 0.0
        self.feeCcy = ""
        self.tradeId = ""

class dataBlockTrade:
    def __init__(self):
        self.cTime = 0
        self.rfqId = ""
        self.clRfqId = ""
        self.blockTdId = ""
        self.tTraderCode = ""
        self.mTraderCode = ""
        self.legs = []#List of blockTradeLeg
    
class dataSpotGridAlgo:
    def __init__(self):
        self.algoId = ""
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.cTime = 0
        self.uTime = 0
        self.triggerTime = 0
        self.algoOrdType = ""#grid
        self.state = OKExEnums.algoState.NONE
        self.maxPx = 0.0 
        self.minPx = 0.0
        self.gridNum = 0
        self.runType = OKExEnums.gridType.NONE
        self.tpTriggerPx = 0.0
        self.slTriggerPx = 0.0
        self.tradeNum = 0
        self.arbitrageNum = 0
        self.singleAmt = 0.0
        self.perMinProfitRate = 0.0
        self.perMaxProfitRate = 0.0
        self.totalPnl = 0.0
        self.pnlRatio = 0.0
        self.investment = 0.0
        self.gridProfit = 0.0
        self.floatProfit = 0.0
        self.totalAnnualizedRate = 0.0
        self.annualizedRate = 0.0
        self.cancelType = OKExEnums.cancelType.NONE
        self.stopType = OKExEnums.stopType.NONE
        self.quoteSz = 0.0
        self.baseSz = 0.0
        self.curQuoteSz = 0.0
        self.curBaseSz = 0.0
        self.profit = 0.0
        self.stopResult = 0
        self.tag = ""
        self.pTime = 0
    
class dataContractGridAlgo:
    def __init__(self):
        self.algoId = ""
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.cTime = 0
        self.uTime = 0
        self.triggerTime = 0
        self.algoOrdType = ""#contract_grid
        self.state = OKExEnums.algoState.NONE
        self.maxPx = 0.0 
        self.minPx = 0.0
        self.gridNum = 0 
        self.runType = OKExEnums.gridType.NONE
        self.tpTriggerPx = 0.0
        self.slTriggerPx = 0.0
        self.tradeNum = 0
        self.arbitrageNum = 0
        self.singleAmt = 0.0
        self.perMinProfitRate = 0.0
        self.perMaxProfitRate = 0.0
        self.totalPnl = 0.0
        self.pnlRatio = 0.0
        self.investment = 0.0
        self.gridProfit = 0.0
        self.floatProfit = 0.0
        self.totalAnnualizedRate = 0.0
        self.annualizedRate = 0.0
        self.cancelType = OKExEnums.cancelType.NONE
        self.stopType = OKExEnums.stopType.NONE
        self.direction = OKExEnums.contractGridType.NONE
        self.basePos = 0.0
        self.sz = 0.0
        self.lever = 0.0
        self.actualLever = 0.0
        self.liqPx = 0.0
        self.riskRatio = 0.0
        self.uly = ""
        self.tag = ""
        self.pTime = 0
    
class dataGridPosition:
    def __init__(self):
        self.algoId = ""
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.cTime = 0
        self.uTime = 0
        self.avgPx = 0.0
        self.ccy = ""
        self.lever = 0.0
        self.liqPx = 0.0
        self.posSide = OKExEnums.positionSide.NONE
        self.pos = 0.0
        self.mgnMode = OKExEnums.mgnMode.NONE
        self.mgnRatio = 0.0
        self.imr = 0.0
        self.mmr = 0.0
        self.upl = 0.0
        self.uplRatio = 0.0
        self.last =0.0
        self.notionalUsd = 0.0
        self.adl = 0
        self.markPx = 0.0
        self.pTime = 0
    
class dataGridSubOrders:
    def __init__(self):
        self.algoId = ""
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.algoOrdType = ""#grid or contract grid. create enum?
        self.groupId = ""
        self.ordId = ""
        self.cTime = 0
        self.uTime = 0
        self.tdMode = OKExEnums.tradeMode.NONE
        self.ordType = OKExEnums.orderType.NONE
        self.sz = 0.0
        self.state = OKExEnums.subOrderState.NONE
        self.side = OKExEnums.side.NONE
        self.px = 0.0
        self.fee = 0.0
        self.feeCcy = ""
        self.avgPx = 0.0
        self.accFillSz = 0.0
        self.posSide = OKExEnums.positionSide.NONE
        self.pnl = 0.0
        self.ctVal = 0.0
        self.lever = 0.0
        self.pTime = 0.0
    
### Public Channel ###

class dataInstrument:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.uly = ""
        self.category = 0
        self.baseCcy = ""
        self.quoteCcy = ""
        self.settleCcy = ""
        self.ctVal = 0.0
        self.ctMulti = 0.0
        self.ctValCcy = ""
        self.optType = OKExEnums.optType.NONE
        self.stk = 0.0
        self.listTime = 0
        self.expTime = 0
        self.lever = 0.0
        self.tickSz = 0.0
        self.lotSz = 0.0
        self.minSz = 0.0
        self.ctType = OKExEnums.ctType.NONE
        self.alias = ""
        self.state = OKExEnums.insState.NONE
        self.maxLmtSz = 0.0
        self.maxMktSz = 0.0
        self.maxTwapSz = 0.0
        self.maxIcebergSz = 0.0
        self.maxTriggerSz = 0.0
        self.maxStopSz = 0.0
        
    def ToString(self):
        return str(self.instType) + "," + self.instId + "," + self.uly + "," +  \
            str(self.category) + "," + self.baseCcy + "," + self.quoteCcy + "," + \
            self.settleCcy + "," + str(self.ctVal) + "," + str(self.ctMulti) + "," + \
            self.ctValCcy + "," + str(self.optType) + "," + str(self.stk) + "," + \
            str(self.listTime) + "," + str(self.expTime) + "," + str(self.lever) + "," + \
            str(self.tickSz) + "," + str(self.lotSz) + "," + str(self.minSz) + "," + \
            str(self.ctType) + "," + self.alias + "," + str(self.state) + "," + \
            str(self.maxLmtSz) + "," + str(self.maxMktSz) + "," + str(self.maxTwapSz) + "," + \
            str(self.maxIcebergSz) + "," + str(self.maxTriggerSz) + "," + str(self.maxStopSz)
            
class dataTicker:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.last = 0.0
        self.lastSz = 0.0
        self.askPx = 0.0
        self.askSz = 0.0
        self.bidPx = 0.0
        self.bidSz = 0.0
        self.open24h = 0.0
        self.high24h = 0.0
        self.low24h = 0.0
        self.volCcy24h = 0.0
        self.vol24h = 0.0
        self.sodUtc0 = 0.0
        self.sodUtc8 = 0.0
        self.ts = 0
    
class dataOpenInterest:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.oi = 0.0
        self.oiCcy = ""
        self.ts = 0
    
class dataCandleStick:
    def __init__(self):
        self.ts = 0
        self.o = 0.0
        self.h = 0.0
        self.l = 0.0
        self.c = 0.0
        self.vol = 0.0
        self.volCcy = 0.0
    
class dataTrade:
    def __init__(self):
        self.instId = ""
        self.tradeId = ""
        self.px = 0.0
        self.sz = 0.0
        self.side = OKExEnums.side.NONE
        self.ts = 0
    
class dataEstimatedDelivery:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.settlePx = 0.0
        self.ts = 0
    
class dataMarkPrice:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.markPx = 0.0
        self.ts = 0
    
class dataMarkPxCandleStick:
    def __init__(self):
        self.ts = 0
        self.o = 0.0
        self.h = 0.0
        self.l = 0.0
        self.c = 0.0
    
class dataPriceLimit:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.buyLmt = 0.0
        self.sellLmt = 0.0
        self.ts = 0
    
class book:
    def __init__(self):
        self.px = 0.0
        self.qty = 0.0
        self.LiqOrd = 0.0
        self.NumOfOrd = 0
        
    def ToString(self):
        return str(self.px) + "," + str(self.qty) + "," + str(self.LiqOrd) + "," + str(self.NumOfOrd)
    
class dataOrderBook:
    def __init__(self):
        self.asks = []#List of book
        self.bids = []#List of book
        self.ts = 0
        self.checksum = 0
        
    def ToString(self):
        msg = str(self.ts) + ",asks,"
        for a in self.asks:
            msg += a.ToString() + ","
        msg += "bids,"
        for b in self.bids:
            msg += b.ToString() + ","
        msg += str(self.checksum)
        
class dataOptionSummary:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.uly = ""
        self.delta = 0.0
        self.gamma = 0.0
        self.vega = 0.0
        self.theta = 0.0
        self.lever = 0.0
        self.markVol = 0.0
        self.bidVol = 0.0
        self.askVol = 0.0
        self.realVol = 0.0
        self.fwdPx = 0.0
        self.ts = 0
    
class dataFundingRate:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.fundingRate = 0.0
        self.nextFundingRate = 0.0
        self.fundingTime = 0
    
class dataIndexCandleStick:
    def __init__(self):
        self.ts = 0
        self.o = 0.0
        self.h = 0.0
        self.l = 0.0
        self.c = 0.0
    
class dataIndexTicker:
    def __init__(self):
        self.instId = ""
        self.idxPx = 0.0
        self.open24h = 0.0
        self.high24h = 0.0
        self.low24h = 0.0
        self.sodUtc0 = 0.0
        self.sodUtc8 = 0.0
        self.ts = 0
    
class dataStatus:
    def __init__(self):
        self.title = ""
        self.state = OKExEnums.sysStatus.NONE
        self.begin = 0
        self.end = 0
        self.href = ""
        self.serviceType = OKExEnums.serviceType.NONE
        self.system = ""
        self.scheDesc = ""
        self.ts = 0
    
class blkTdLeg:
    def __init__(self):
        self.instId = ""
        self.px = 0.0
        self.sz = 0.0
        self.side = OKExEnums.side.NONE
        self.tradeId = ""
    
class dataPblStrBlkTd:
    def __init__(self):
        self.cTime = 0
        self.blockTdId = ""
        self.legs = []#List of blkTdLeg
    
class dataBlkTicker:
    def __init__(self):
        self.instType = OKExEnums.instType.NONE
        self.instId = ""
        self.volCcy24h = 0.0
        self.vol24h = 0.0
        self.ts = 0
    
    
    
    
    
    
    