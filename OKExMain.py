# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 22:23:08 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python\\OKEx")

import OKExFeedReceiver
import OKExParser
import OKExOptimizer
import OKExOMS
from Utils import params

def readConfig(filename):
    config = open(filename,'r')
    for line in config:
        lst = line.split('=')
        if(lst[0]=="OMSKeyFileName"):
            params.OMSKeyFileName = lst[1].replace('\n','')
        elif(lst[0]=="insParamFileName"):
            params.insParamFileName = lst[1].replace('\n','')
        elif(lst[0]=="RVPeriod"):
            params.RVPeriod = int(lst[1].replace('\n',''))
        elif(lst[0]=="posMAPeriod"):
            params.posMAPeriod = int(lst[1].replace('\n',''))
        elif(lst[0]=="midMAPeriod"):
            params.midMAPeriod = int(lst[1].replace('\n',''))
        elif(lst[0]=="biTicks"):
            params.biTicks = int(lst[1].replace('\n',''))
        elif(lst[0]=="biDecayingParam"):
            params.biDecayingParam = int(lst[1].replace('\n',''))

if __name__ == "__main__":
    #Start Feed Receiver, OMS
    feedReceiver = OKExFeedReceiver.feedReceiver
    parser = OKExParser.parser
    optimizer = OKExOptimizer.optimizer
    oms = OKExOMS.oms
    
    feedReceiver.Initialize()
    
    readConfig("D:\\OKExFeed\\OKExMain.ini")
    
    logPath = "D:\\OKExFeed\\log\\OKExMain.log"
    lf = open(logPath,'w')
    
    ulyList = ["BTC-USDT","ETH-USDT"]
    
    looping = True
    print("Hello Trader!")
    while(looping):
        print("Feed,OMS,Trade,Info,Exit")
        print(">>>")
        direction = input()
        if(direction == "Feed"):
            print("FeedReceiver:")
            FRstatus = ""
            if(feedReceiver.isListening):
                FRstatus = "Current Status:Listening"
            else:
                FRstatus = "Current Status:Not Listening"
            print("Start,Stop")
            print(">>>")
            FRdirection = input()
            if(FRdirection=="Start"):
                url = "wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999"
                insList = feedReceiver.getInstrmentList(ulyList)
                print("Instrument List")
                for i in insList.values():
                    print(i.instId)
                feedReceiver.Connect(url)
                feedReceiver.StartListenOrderBook(insList)
                feedReceiver.StartListenTrade(insList)
                feedReceiver.startUpdatingBoardSingleTh()
            elif(FRdirection=="Stop"):
                print("Stop")
            else:
                print("Input word:" + FRdirection)
            #End of if(FRdirection=="Start"):
        #End of if(direction == "Feed"):
        elif(direction== "OMS"):
            print("OMS:")
            OMSstatus = ""
            print("Start,Stop")
            print(">>>")
            OMSdirection = input()
            if(OMSdirection=="Start"):
                oms.initialize(insList)
                oms.readKeyFile(params.OMSKeyFileName)
                oms.Connect()
                oms.subscribeBalAndPos()
                oms.subscribeOrders()
                #oms.startUpdatingOrders(parser,insList)
            elif(OMSdirection=="Stop"):
                print("Stop")
            else:
                print("Input word:" + OMSdirection)
        elif(direction=="Trade"):
            print("Optimizer:")
            OPTStatus = ""
            print("Start,Stop")
            print(">>>")
            OPTdirection = input()
            if(OPTdirection=="Start"):
                optimizer.initialize(oms)
                optimizer.readInsParam(insList, params.insParamFileName)
                optimizer.startTrading()
                print("Trade Started")
            elif(OPTdirection=="Stop"):
                optimizer.optimizing = False
            else:
                print("Input word:" + OPTdirection)
        elif(direction=="Info"):
            print("Info:")
            while(True):
                print("Input Keyword or exit")
                print(">>>")
                Infodirection = input()
                if(Infodirection in insList.keys()):
                    ins = insList[Infodirection]
                    print(ins.instId)
                    print("book,orders")
                    print(">>>")
                    insInfo = input()
                    if(insInfo == "book"):
                        print(ins.Books.printBooks(20))
                    elif(insInfo=="orders"):
                        print(ins.printLiveOrders())
                elif(Infodirection=="exit"):
                    break
                else:
                    print("Input word:" + Infodirection)
        else:
            print("Input word:" + direction)