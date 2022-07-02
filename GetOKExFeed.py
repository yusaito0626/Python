# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python\\OKEx")
import requests
import datetime
import time
import json

import OKExFeedReceiver




if __name__ == "__main__":
    datapath = "D:\\OKExFeed\\"
    url = "wss://ws.okx.com:8443/ws/v5/public"
    
    today = datetime.datetime.utcnow()
    
    masterfilename = datapath + "master\\tempOKExMaster_"+ today.date().isoformat() + ".txt"
    master = open(masterfilename,'w')
    
    insList = list()
    #insList.append("BTC-USDT")
    rest_url = "https://www.okx.com/"
    spot_reqmsg ="api/v5/public/instruments?instType=SPOT&instId=BTC-USDT"
    response = requests.get(rest_url+spot_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=BTC-USDT"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=BTC-USDT"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    
    #Add ETH
    insList.append("ETH-USDT")
    rest_url = "https://www.okx.com/"
    spot_reqmsg ="api/v5/public/instruments?instType=SPOT&instId=ETH-USDT"
    response = requests.get(rest_url+spot_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    fut_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=ETH-USDT"
    response = requests.get(rest_url+fut_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    swap_reqmsg="api/v5/public/instruments?instType=SWAP&uly=ETH-USDT"
    response = requests.get(rest_url+swap_reqmsg)
    obj=response.json()
    for elem in obj['data']:
        insList.append(elem['instId'])
        master.write(json.dumps(elem) + "\n")
    master.flush()
    master.close()
     
    feedReceiver = OKExFeedReceiver.FeedReceiver()
    feedReceiver.Initialize()
    
    filename = datapath + "feed\\OKExFeed_" + today.date().isoformat() + ".log"
    f = open(filename,'w')
    
    trials = 1
    currentDay = today.day
    
    while(trials < 11):
        try:
            feedReceiver.Connect(url)
            print("Connection establised.")
            feedReceiver.StartListenOrderBook(insList)
            feedReceiver.StartListenTrade(insList)
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
        