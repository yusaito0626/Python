# -*- coding: utf-8 -*-
"""
Created on Mon May 30 13:02:29 2022

@author: yusai
"""

import websocket

__FeedReceiver = websocket.WebSocket()
__url=""

def SetParam(url):
    __url = url
    
def Connect(url):
    __url = url
    __FeedReceiver.connect(__url)

def Subscribe(msg):
    __FeedReceiver.send(msg)
    
def StartListenTicker(InsList):
    strargs="["
    for ins in InsList:
        strargs += "{\"channel\":\"tickers\",\"instId\":\"" + ins + "\"},"
    strargs=strargs[0:len(strargs)-1] + "]"
    reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
    Subscribe(reqmsg)
    
def StartListenOrderBook(InsList,depth):
    strargs="["
    for ins in InsList:
        strargs += "{\"channel\":\"books\",\"instId\":\"" + ins + "\",\"sz\":\"" + str(depth) + "\"},"
    strargs=strargs[0:len(strargs)-1] + "]"
    reqmsg="{\"op\":\"subscribe\",\"args\":" + strargs + "}"
    Subscribe(reqmsg)
    
def recv():
    return __FeedReceiver.recv()
