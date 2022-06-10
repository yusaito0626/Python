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
    ccy = ""
    
    def __init__(self):
        self.subtype = OKExEnums.subscribeType.NONE
        self.channel = ""
        self.insType = OKExEnums.instType.NONE
        self.uly = ""
        self.instId = ""
        self.ccy = ""
        
class pushData:
    arg = {}
    data = []
    

### Trade ###

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
  
### Private Channel ###  
  
class dataAccDetail:
    ccy = ""
    eq = ""
    cashBal = 0.0
    uTime = 0
    isoEq = 0.0
    availEq = 0.0
    disEq = 0.0
    availBal = 0.0
    frozenBal = 0.0
    ordFrozen = 0.0
    liab = 0.0
    upl = 0.0
    uolLiab = 0.0
    crossLiab = 0.0
    isoLiab = 0.0
    mgnRatio = 0.0
    interest = 0.0
    twap = 0.0
    maxLoan = 0.0
    eqUsd = 0.0
    notionalLever = 0.0
    coinUsdPrice = 0.0
    stgyEq = 0.0
    isoUpl = 0.0
    
class dataAccount:
    uTime = 0
    totalEq = 0.0
    isoEq = 0.0
    adjEq = 0.0
    odrFroz = 0.0
    imr = 0.0
    mmr = 0.0
    mgnRatio = 0.0
    notionalUsd = 0.0
    details = []#List of dataAccDetail
    
class dataPosition:
    instType = OKExEnums.instType.NONE
    mgnMode = OKExEnums.mgnMode.NONE
    posSide = OKExEnums.positionSide.NONE
    pos = 0.0
    baseBal = 0.0
    quoteBal = 0.0
    posCcy = ""
    availPos = 0.0
    avgPx = 0.0
    upl = 0.0
    uplRatio = 0.0
    instId = ""
    lever = 0.0
    liqPx = 0.0
    markPx = 0.0
    imr = 0.0
    margin = 0.0
    mgnRatio = 0.0
    mmr = 0.0
    liab = 0.0
    liabCcy = 0.0
    interest = 0.0
    tradeId = ""
    notionalUsd = 0.0
    optVal = 0.0
    adl = 0
    ccy = ""
    last = 0.0
    usdPx = 0.0
    deltaBS = 0.0
    deltaPA = 0.0 
    gammaBS = 0.0
    gammaPA = 0.0
    thetaBS = 0.0
    thetaPA = 0.0
    vegaBS = 0.0
    vegaPA = 0.0
    cTime = 0
    uTime = 0
    pTime = 0
    
class dataBal:
    ccy = ""
    cashBal = 0.0
    uTime = 0
    
class dataBalandPos:
    pTime = 0
    eventType = OKExEnums.eventType.NONE
    balList = []#List of dataBal
    posList = []#List of dataPosition
    
class dataOrder:
    instType = OKExEnums.instType.NONE
    instId = ""
    tgtCcy = OKExEnums.quantityType.NONE
    ccy = ""
    ordId = ""
    clOrdId = ""
    tag = ""
    px = 0.0
    sz = 0.0
    notionalUsd = 0.0
    ordType = OKExEnums.orderType.NONE
    side = OKExEnums.side.NONE
    posSide = OKExEnums.positionSide.NONE
    tdMode = OKExEnums.tradeMode.NONE
    fillPx = 0.0
    tradeId = ""
    fillSz = 0.0
    fillTime = 0
    fillFee = 0.0
    fillFeeCcy = ""
    execType = OKExEnums.execType.NONE
    accFillSz = 0.0
    fillNotionalUsd = 0.0
    avgPx = 0.0
    state = OKExEnums.orderState.NONE
    lever = 0.0
    tpTriggerPx = 0.0
    tpTriggerPxType = OKExEnums.priceType.NONE
    tpOrdPx = 0.0
    slTriggerPx = 0.0
    slTriggerPxType = OKExEnums.priceType.NONE
    slOrdPx = 0.0
    feeCcy = ""
    fee = 0.0
    rebateCcy = ""
    rebate = 0.0
    pnl = 0.0
    source = ""
    category = OKExEnums.category.NONE
    uTime = 0
    cTime = 0
    reqId = ""
    amendResult = OKExEnums.amendResult.NONE
    code = 0
    msg = ""
    #algo order channel
    algoId = ""
    actualSz = 0.0
    actualPx = 0.0
    actualSide = ""
    triggerTime = 0
    #Advanced algo order channel
    pxVar = 0.0
    pxSpread = 0.0
    szLimit = 0.0
    pxLimit = 0.0
    timeInterval = 0.0
    count = 0
    callbackRatio = 0.0
    callbackSpread = 0.0
    activePx = 0.0
    moveTriggerPx = 0.0
    pTime = 0
    
class dataLiquidationWarning:
    instType = OKExEnums.instType.NONE
    mgnMode = OKExEnums.mgnMode.NONE
    posSide = OKExEnums.positionSide.NONE
    pos = 0.0
    posCcy = ""
    availPos = 0.0
    avgPx = 0.0
    upl = 0.0
    uplRatio = 0.0
    instId = ""
    lever = 0.0
    liqPx = 0.0
    markPx = 0.0 
    imr = 0.0
    margin = 0.0
    mgnRatio = 0.0
    mmr = 0.0
    liab = 0.0
    liabCcy = ""
    interest = 0.0
    tradeId = ""
    notionalUsd = 0.0
    optVal = 0.0
    adl = 0
    ccy = ""
    last = 0.0
    deltaBS = 0.0
    deltaPA = 0.0 
    gammaBS = 0.0
    gammaPA = 0.0
    thetaBS = 0.0
    thetaPA = 0.0
    vegaBS = 0.0
    vegaPA = 0.0
    cTime = 0
    uTime = 0
    pTime = 0
    
class dataAccountGreeks:
    deltaBS = 0.0
    deltaPA = 0.0 
    gammaBS = 0.0
    gammaPA = 0.0
    thetaBS = 0.0
    thetaPA = 0.0
    vegaBS = 0.0
    vegaPA = 0.0
    ccy = ""
    ts = 0
    
class rfqLeg:
    InstId = ""
    sz = 0.0
    side = OKExEnums.side.NONE
    tgtCcy = OKExEnums.quantityType.NONE
    
class dataRfqs:
    cTime = 0
    uTime = 0
    state = OKExEnums.rfqState.NONE
    counterparties = []#List of String
    validUntil = 0
    clRfqId = ""
    tradeCode = ""
    rfqId = ""
    legs = []#List of rfqLeg
    
class quoteLeg:
    instId = ""
    sz = 0.0
    px = 0.0
    side = OKExEnums.side.NONE
    tgtCcy = OKExEnums.quantityType.NONE
    
class dataQuotes:
    cTime = 0
    uTime = 0
    state = OKExEnums.rfqState.NONE
    validUntil = 0
    rfqId = ""
    clRfqId = ""
    quoteId = ""
    clQuoteID = ""
    quoteSide = OKExEnums.side.NONE
    legs = []#List of quoteLeg

class blockTradeLeg:
    instId = ""
    px = 0.0
    sz = 0.0
    side = OKExEnums.side.NONE
    tgtCcy = OKExEnums.quantityType.NONE
    fee = 0.0
    feeCcy = ""
    tradeId = ""

class dataBlockTrade:
    cTime = 0
    rfqId = ""
    clRfqId = ""
    blockTdId = ""
    tTraderCode = ""
    mTraderCode = ""
    legs = []#List of blockTradeLeg
    
class dataSpotGridAlgo:
    algoId = ""
    instType = OKExEnums.instType.NONE
    instId = ""
    cTime = 0
    uTime = 0
    triggerTime = 0
    algoOrdType = ""#grid
    state = OKExEnums.algoState.NONE
    maxPx = 0.0 
    minPx = 0.0
    gridNum = 0
    runType = OKExEnums.gridType.NONE
    tpTriggerPx = 0.0
    slTriggerPx = 0.0
    tradeNum = 0
    arbitrageNum = 0
    singleAmt = 0.0
    perMinProfitRate = 0.0
    perMaxProfitRate = 0.0
    totalPnl = 0.0
    pnlRatio = 0.0
    investment = 0.0
    gridProfit = 0.0
    floatProfit = 0.0
    totalAnnualizedRate = 0.0
    annualizedRate = 0.0
    cancelType = OKExEnums.cancelType.NONE
    stopType = OKExEnums.stopType.NONE
    quoteSz = 0.0
    baseSz = 0.0
    curQuoteSz = 0.0
    curBaseSz = 0.0
    profit = 0.0
    stopResult = 0
    tag = ""
    pTime = 0
    
class dataContractGridAlgo:
    algoId = ""
    instType = OKExEnums.instType.NONE
    instId = ""
    cTime = 0
    uTime = 0
    triggerTime = 0
    algoOrdType = ""#contract_grid
    state = OKExEnums.algoState.NONE
    maxPx = 0.0 
    minPx = 0.0
    gridNum = 0 
    runType = OKExEnums.gridType.NONE
    tpTriggerPx = 0.0
    slTriggerPx = 0.0
    tradeNum = 0
    arbitrageNum = 0
    singleAmt = 0.0
    perMinProfitRate = 0.0
    perMaxProfitRate = 0.0
    totalPnl = 0.0
    pnlRatio = 0.0
    investment = 0.0
    gridProfit = 0.0
    floatProfit = 0.0
    totalAnnualizedRate = 0.0
    annualizedRate = 0.0
    cancelType = OKExEnums.cancelType.NONE
    stopType = OKExEnums.stopType.NONE
    direction = OKExEnums.contractGridType.NONE
    basePos = 0.0
    sz = 0.0
    lever = 0.0
    actualLever = 0.0
    liqPx = 0.0
    riskRatio = 0.0
    uly = ""
    tag = ""
    pTime = 0
    
class dataGridPosition:
    algoId = ""
    instType = OKExEnums.instType.NONE
    instId = ""
    cTime = 0
    uTime = 0
    avgPx = 0.0
    ccy = ""
    lever = 0.0
    liqPx = 0.0
    posSide = OKExEnums.positionSide.NONE
    pos = 0.0
    mgnMode = OKExEnums.mgnMode.NONE
    mgnRatio = 0.0
    imr = 0.0
    mmr = 0.0
    upl = 0.0
    uplRatio = 0.0
    last =0.0
    notionalUsd = 0.0
    adl = 0
    markPx = 0.0
    pTime = 0
    
class dataGridSubOrders:
    algoId = ""
    instType = OKExEnums.instType.NONE
    instId = ""
    algoOrdType = ""#grid or contract grid. create enum?
    groupId = ""
    ordId = ""
    cTime = 0
    uTime = 0
    tdMode = OKExEnums.tradeMode.NONE
    ordType = OKExEnums.orderType.NONE
    sz = 0.0
    state = OKExEnums.subOrderState.NONE
    side = OKExEnums.side.NONE
    px = 0.0
    fee = 0.0
    feeCcy = ""
    avgPx = 0.0
    accFillSz = 0.0
    posSide = OKExEnums.positionSide.NONE
    pnl = 0.0
    ctVal = 0.0
    lever = 0.0
    pTime = 0.0
    
### Public Channel ###

class dataInstrument:
    instType = OKExEnums.instType.NONE
    instId = ""
    uly = ""
    category = 0
    baceCcy = ""
    quoteCcy = ""
    settleCcy = ""
    ctVal = 0.0
    ctMulti = 0.0
    ctValCcy = ""
    optType = OKExEnums.optType.NONE
    stk = 0.0
    listTime = 0
    expTime = 0
    lever = 0.0
    tickSz = 0.0
    lotSz = 0.0
    minSz = 0.0
    ctType = OKExEnums.ctType.NONE
    alias = ""
    state = OKExEnums.insState.NONE
    maxLmtSz = 0.0
    maxMktSz = 0.0
    maxTwapSz = 0.0
    maxIcebergSz = 0.0
    maxTriggerSz = 0.0
    maxStopSz = 0.0
    
class dataTicker:
    instType = OKExEnums.instType.NONE
    instId = ""
    last = 0.0
    lastSz = 0.0
    askPx = 0.0
    askSz = 0.0
    bidPx = 0.0
    bidSz = 0.0
    open24h = 0.0
    high24h = 0.0
    low24h = 0.0
    volCcy24h = 0.0
    vol24h = 0.0
    sodUtc0 = 0.0
    sodUtc8 = 0.0
    ts = 0
    
class dataOpenInterest:
    instType = OKExEnums.instType.NONE
    instId = ""
    oi = 0.0
    oiCcy = ""
    ts = 0
    
class dataCandleStick:
    ts = 0
    o = 0.0
    h = 0.0
    l = 0.0
    c = 0.0
    vol = 0.0
    volCcy = 0.0
    
class dataTrade:
    instId = ""
    tradeId = ""
    px = 0.0
    sz = 0.0
    side = OKExEnums.side.NONE
    ts = 0
    
class dataEstimatedDelivery:
    instType = OKExEnums.instType.NONE
    instId = ""
    settlePx = 0.0
    ts = 0
    
class dataMarkPrice:
    instType = OKExEnums.instType.NONE
    instId = ""
    markPx = 0.0
    ts = 0
    
class dataMarkPxCandleStick:
    ts = 0
    o = 0.0
    h = 0.0
    l = 0.0
    c = 0.0
    
class dataPriceLimit:
    instType = OKExEnums.instType.NONE
    instId = ""
    buyLmt = 0.0
    sellLmt = 0.0
    ts = 0
    
class book:
    px = 0.0
    qty = 0.0
    LiqOrd = 0.0
    NumOfOrd = 0
    
class dataOrderBook:
    asks = []#List of book
    bids = []#List of book
    ts = 0
    checksum = 0
    
class dataOptionSummary:
    instType = OKExEnums.instType.NONE
    instId = ""
    uly = ""
    delta = 0.0
    gamma = 0.0
    vega = 0.0
    theta = 0.0
    lever = 0.0
    markVol = 0.0
    bidVol = 0.0
    askVol = 0.0
    realVol = 0.0
    fwdPx = 0.0
    ts = 0
    
class dataFundingRate:
    instType = OKExEnums.instType.NONE
    instId = ""
    fundingRate = 0.0
    nextFundingRate = 0.0
    fundingTime = 0
    
class dataIndexCandleStick:
    ts = 0
    o = 0.0
    h = 0.0
    l = 0.0
    c = 0.0
    
class dataIndexTicker:
    instId = ""
    idxPx = 0.0
    open24h = 0.0
    high24h = 0.0
    low24h = 0.0
    sodUtc0 = 0.0
    sodUtc8 = 0.0
    ts = 0
    
class dataStatus:
    title = ""
    state = OKExEnums.sysStatus.NONE
    begin = 0
    end = 0
    href = ""
    serviceType = OKExEnums.serviceType.NONE
    system = ""
    scheDesc = ""
    ts = 0
    
class blkTdLeg:
    instId = ""
    px = 0.0
    sz = 0.0
    side = OKExEnums.side.NONE
    tradeId = ""
    
class dataPblStrBlkTd:
    cTime = 0
    blockTdId = ""
    legs = []#List of blkTdLeg
    
class dataBlkTicker:
    instType = OKExEnums.instType.NONE
    instId = ""
    volCcy24h = 0.0
    vol24h = 0.0
    ts = 0
    
    
    
    
    
    
    