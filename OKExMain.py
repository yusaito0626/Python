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


if __name__ == "__main__":
    #Start Feed Receiver, OMS
    feedReceiver = OKExFeedReceiver.FeedReceiver()
    parser = OKExParser.OKExParser()
    optimizer = OKExOptimizer.Optimizer()
    oms = OKExOMS.OMS()
    
    feedReceiver.Initialize()
    
    keyfile = "D:\\OKExKeys.txt" 
    logPath = "D:\\OKExFeed\\OKExMain.log"
    lf = open(logPath,'w')
    
    ulyList = ["BTC-USDT","ETH-USDT"]
    
    looping = True
    print("Hello Trader!")
    while(looping):
        print("Feed,OMS,Trade,Exit")
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
                url = "wss://ws.okx.com:8443/ws/v5/public"
                insList = feedReceiver.getInstrmentList(ulyList)
                print("Instrument List")
                for i in insList.values():
                    print(i.instId)
                feedReceiver.Connect(url)
                feedReceiver.StartListenOrderBook(insList)
                feedReceiver.StartListenTrade(insList)
                feedReceiver.startUpdatingBoardTh(parser, optimizer)
            elif(FRdirection=="Stop"):
                print("Stop")
            #End of if(FRdirection=="Start"):
        #End of if(direction == "Feed"):
        elif(direction== "OMS"):
            print("OMS:")
            OMSstatus = ""
            if(feedReceiver.isListening):
                OMSstatus = "Current Status:Listening"
            else:
                OMSstatus = "Current Status:Not Listening"
            print("Start,Stop")
            print(">>>")
            OMSdirection = input()
            if(OMSdirection=="Start"):
                oms.readKeyFile(keyfile)
                oms.Connect()