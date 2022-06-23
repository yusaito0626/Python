# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:04:19 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python")

import threading
import time
import requests
import OKExOMS
import OKExEnums
import OKExInstrument

oms = OKExOMS.OMS()

def getOrderLog(filename):
    isLoggingRunning = True
    logfile = open(filename,'a')
    while(isLoggingRunning):
        msg = ""
        msg = oms.recv()
        if(msg != ""):
            print(msg)
            logfile.write(msg + "\n")
        if(msg=="ERROR" or msg=="END"):
            break
    isLoggingRunning = False
    logfile.flush()
    logfile.close()
    print("getOrderLog Thread ended.")

if __name__ == "__main__":

    insList = {}
    rest_url = "https://www.okx.com/"
    spot_reqmsg ="api/v5/public/instruments?instType=SPOT&instId=BTC-USDT"
    response = requests.get(rest_url+spot_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=BTC-USD"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=BTC-USD"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
    
    #Add ETH
    spot_reqmsg ="api/v5/public/instruments?instType=SPOT&instId=ETH-USDT"
    response = requests.get(rest_url+spot_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=ETH-USD"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=ETH-USD"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        ins = OKExInstrument.Instrument()
        ins.setInsData(elem)
        insList[ins.instId] = ins
        
    oms.readKeyFile("D:\\OKExKeys.txt")

    oms.Connect()
    logfilename = "D:\\log\\OKEx_OMS.log"
    ordLogTh = threading.Thread(target=getOrderLog,args=[logfilename])
    ordLogTh.start()
    
    oms.subscribeBalAndPos()
    
    oms.sendNewOrder("BTC-USD-SWAP", OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, 0.001,19500.0,"USDT")
    time.sleep(1)
    oms.sendModOrder("BTC-USD-SWAP", "BTCUSDT000000",0.0005)
    time.sleep(1)
    #oms.sendCanOrder("BTC-USD-SWAP", "BTCUSDT000000")
    time.sleep(1)
#    oms.sendNewOrder("BTC-USDT", OKExEnums.tradeMode.CROSS, OKExEnums.side.BUY, OKExEnums.orderType.LIMIT, 0.001,19500.0,"USDT")
#    time.sleep(1)
#    oms.sendModOrder("BTC-USDT", "BTCUSDT000003",0.001,21000.0)
#    time.sleep(1)
    oms.Disconnect()
    time.sleep(1)
    ordLogTh.join()
    