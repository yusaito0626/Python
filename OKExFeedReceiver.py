# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:02:29 2022

@author: yusai
"""
import requests
import websocket

f = open("C:\\Users\\yusai\\Documents\\test.csv",'w')
   
if __name__ == "__main__":
    rest_url = "https://www.okx.com/"
    rest_reqmsg="api/v5/public/instruments?instType=FUTURES&uly=BTC-USD"
    response = requests.get(rest_url+rest_reqmsg)
    strargs="[{\"channel\":\"tickers\",\"instId\":\"BTC-USDT\"}]";
    reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
    url = "wss://ws.okx.com:8443/ws/v5/public"
    ws = websocket.WebSocket()
    ws.connect(url)
    ws.send(reqmsg)
    i = 0
    while i < 1:
        f.write(ws.recv() + "\n")
        f.flush()
        print(ws.recv())