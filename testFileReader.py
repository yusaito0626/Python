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
import OKExOptimizer

filereader = OKExFileReader.FeedFileReader()
parser = OKExParser.OKExParser()
optimizer = OKExOptimizer.Optimizer()

filepath = "D:\\OKExFeed\\feed"
filename = "OKExFeed_YYYY-MM-DD.log"
day = "2022-06-25"

filereader.setFileNameAndPath(filepath, filename)
filereader.setFile(day)
print("Create Ins List.")
today = datetime.datetime.utcnow()
print(today.isoformat())

masterfilepath = "D:\\OKExFeed\\master"
masterfilename = "OKExMaster_YYYY-MM-DD_test.txt"
filereader.setMasterFile(masterfilepath, masterfilename)

insList = filereader.readMasterFile(day)
    
print("Ins List:")
for i in insList.values():
    print(i.instId)
print("Start Reading")
today = datetime.datetime.utcnow()
print(today.isoformat())
line = ""
i = 0
while(line!="\0"):
    line = filereader.readline()
    if(line=="\0"):
        break
    obj = parser.Parse(line)
    if(obj.dataType=="push"):
        if(obj.arg["instId"] in insList):
            ins = insList[obj.arg["instId"]]
            ins.updateBooks(obj)
            optimizer.calcFactors(ins)
    parser.pushPDataObj(obj)
    i += 1
    if(i > 1000000):
        #print(line)
        i = 0
    
print("Finished reading.")
today = datetime.datetime.utcnow()
print(today.isoformat())