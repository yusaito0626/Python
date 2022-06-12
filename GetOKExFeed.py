# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python")
import OKExFeedReceiver
import requests
import datetime

if __name__ == "__main__":
    datapath = "D:\\OKExFeed\\"
    url = "wss://ws.okx.com:8443/ws/v5/public"
    
    
    insList = list()
    insList.append("BTC-USDT")
    rest_url = "https://www.okx.com/"
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=BTC-USD"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=BTC-USD"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        
    feedReceiver = OKExFeedReceiver.FeedReceiver()
    feedReceiver.Initialize()
    
    feedReceiver.Connect(url)
    feedReceiver.StartListenOrderBook(insList,10)
    today = datetime.datetime.utcnow()
    filename = datapath + "OKExFeed_" + today.date().isoformat() + ".log"
    f = open(filename,'w')
    currentDay = today.day
    currentMin = today.minute
    
    print("Start Collecting Data From OKEx.")
    print("Start:" + today.isoformat())
    print("Instrument List:")
    for ins in insList:
        print(ins)
    
    i = 0
    while True:
        txt = feedReceiver.recv()
        if(txt != ""):
            f.write(txt + "\n")
            today = datetime.datetime.utcnow()
            if(today.hour == 8 and currentDay != today.day):
                f.flush()
                f.close()
                print("Process Ending...")
                break
                #if(today.weekday()==6):
                #    print("Process Ending...")
                #    break
                #else:
                #    filename = datapath + "OKExFeed_" + today.date().isoformat() + ".log"
                #    print("Changing File. New File:")
                #    print(filename)
                #    f = open(filename(),'w')
                #    currentDay = today.day
            elif(currentMin != today.minute):
                currentMin = today.minute
                print(today.isoformat())
    sys.exit()
        