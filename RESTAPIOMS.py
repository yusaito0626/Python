# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 21:28:53 2022

@author: yusai
"""

import time
import hmac
import hashlib
import base64

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
    byte_key = bytes(key, 'UTF-8')
    rawmsg = strtime + method + requestPath + body 
    hmacmsg = hmac.new(byte_key, rawmsg.encode(), hashlib.sha256)
    out = base64.b64encode(hmacmsg.hexdigest().encode()).decode()
    return out

    
