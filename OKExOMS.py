# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 20:25:42 2022

@author: yusai
"""

#WebSocket
import websocket
import time
import hmac
import hashlib
import base64
import requests
import json

oms = websocket.WebSocket()

__url = ""
__apiKey = ""
__passphrase = ""
__secretKey = ""

def SetKeys(apiKey,passphrase,secretKey):
    __apiKey = apiKey
    __passphrase = passphrase
    __secretKey = secretKey
    
def SetURL(url):
    __url = url
def GetURL():
    return __url
    
def Connect(url,apiKey,passphrase,secretKey):
    if(url==""):
        return "Error: Invalid URL"
    if(apiKey==""):
        return "Error: Invalid API Key"
    if(passphrase==""):
        return "Error: Invalid Pass Phrase"
    if(secretKey==""):
        return "Error: Invalid Secret Key"
    tm = str(int(time.time()))
    sign = __GetSign(tm,secretKey,"GET","/users/self/verify","")
    LoginMsg = "{\"op\":\"login\",\"args\":[{\"apiKey\":\"" + apiKey + "\",\"passphrase\":\"" + passphrase + "\",\"timestamp\":\"" + tm + "\",\"sign\":\"" + sign + "\"}]}"
    
    oms.connect(url)
    oms.send(LoginMsg)
    
    return oms.recv()
    #return sign

def __GetSign(strtime,key,method,requestPath,body=""):
    if(strtime ==""):
        strtime = str(time.time())
    rawmsg = strtime + method + requestPath + body
    temp = base64.b64encode(rawmsg.encode()).decode()
    hmacmsg = hmac.new(key.encode(), rawmsg.encode(), hashlib.sha256)
    out = base64.b64encode(hmacmsg.digest()).decode()
    return out

    
