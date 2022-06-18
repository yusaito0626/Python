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
import time

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
    
    #Add ETH
    insList.append("ETH-USDT")
    rest_url = "https://www.okx.com/"
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=ETH-USD"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=ETH-USD"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        
    feedReceiver = OKExFeedReceiver.FeedReceiver()
    feedReceiver.Initialize()
    
    today = datetime.datetime.utcnow()
    filename = datapath + "OKExFeed_" + today.date().isoformat() + ".log"
    f = open(filename,'w')
    
    trials = 1
    
    while(trials < 11):
        try:
            feedReceiver.Connect(url)
            print("Connection establised.")
            feedReceiver.StartListenOrderBook(insList)
            feedReceiver.StartListenTrade(insList)
            currentDay = today.day
            currentMin = today.minute
    
            print("Start Collecting Data From OKEx. Attempts:" + str(trials))
            print("Start:" + today.isoformat())
            print("Instrument List:")
            for ins in insList:
                print(ins)
            
            while True:
                txt = feedReceiver.recv()
                if(txt != ""):
                    if(txt=="ERROR"):
                        raise Exception("Error while receiving feed.")
                    f.write(txt + "\n")
                    today = datetime.datetime.utcnow()
                    if(today.hour == 8 and currentDay != today.day):
                        f.flush()
                        f.close()
                        trials = 99
                        break
                    elif(currentMin != today.minute):
                        currentMin = today.minute
                        print(today.isoformat())
        except:
            feedReceiver.Disconnect()
            if(trials > 10):
                print("Exception Thrown.")
                print("The number of attempts exceeded 10 times.")
                break
            print("Exception Thrown. Reconnecting in 5min.")
            time.sleep(300)
            print("Reconnecting...")
            trials += 1
            today = datetime.datetime.utcnow()
        
        
    print("Process Ending...")
    feedReceiver.Disconnect()
    sys.exit()
        