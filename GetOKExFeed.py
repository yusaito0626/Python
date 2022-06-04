# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python")
import OKExFeedReceiver
import requests
import json
import pandas

if __name__ == "__main__":    
    f = open("C:\\Users\\yusai\\Documents\\test.csv",'w')
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
        
    OKExFeedReceiver.Connect(url)
    OKExFeedReceiver.StartListenOrderBook(insList,10)
    i = 0
    while i < 101:
        txt = OKExFeedReceiver.recv()
        f.write(txt + "\n")
        #f.flush()
        #print(txt)
        if(i == 100):
            print(txt)
            i = 0
        else:
            i += 1
        