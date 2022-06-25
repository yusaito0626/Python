# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 19:57:48 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python\\OKEx")
import datetime
import OKExFileReader
import OKExParser
import OKExInstrument

filereader = OKExFileReader.FeedFileReader()

filepath = "D:\\OKExFeed\\feed"
filename = "OKExFeed_YYYY-MM-DD.log"
day = "2022-06-25"

filereader.setFileNameAndPath(filepath, filename)
filereader.setFile(day)
print("Create Ins List.")
today = datetime.datetime.utcnow()

masterfilepath = "D:\\OKExFeed\\master"
masterfilename = "OKExMaster_YYYY-MM-DD.csv"
filereader.setMasterFile(masterfilepath, masterfilename)

insList = filereader.readMasterFile(day)
    
print("Ins List:")
for i in insList.values():
    print(i.instId)
print("Start Reading")

line = ""
i = 0
while(line!="\0"):
    line = filereader.readline()
    obj = OKExParser.Parse(line)
    if(obj.dataType=="push"):
        ins = insList[obj.arg["instId"]]
        ins.updateBooks(obj)
    i += 1
    if(i > 1000000):
        print(line)
        i = 0
    
print("Finished reading.")