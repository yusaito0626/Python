# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 15:54:56 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python\\OKEx")
import datetime
import OKExFileReader
import OKExParser
import OKExOptimizer


if __name__ == "__main__":

    filereader = OKExFileReader.FeedFileReader()
    parser = OKExParser.OKExParser()
    optimizer = OKExOptimizer.Optimizer()
    
    datapath = "D:\\OKExFeed\\"
    dateFile = datapath + "date.txt"
    
    d = open(dateFile,'r')
    day = d.readline()
    d.close()
    
    print("date:" + day)
    
    histdatapath = datapath + "histData\\histdata_" + day + ".csv"

    filepath = datapath + "feed"
    filename = "OKExFeed_YYYY-MM-DD.log"

    filereader.setFileNameAndPath(filepath, filename)
    filereader.setFile(day)
    print("Create Ins List.")
    today = datetime.datetime.utcnow()
    print(today.isoformat())

    masterfilepath = datapath + "master"
    masterfilename = "OKExMaster_YYYY-MM-DD.txt"
    filereader.setMasterFile(masterfilepath, masterfilename)

    insList = filereader.readMasterFile(day)
    
    print("Ins List:")
    for i in insList.values():
        print(i.instId)
    print("Start Reading")
    today = datetime.datetime.utcnow()
    print(today.isoformat())
    line = ""
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

    
    print("Finished reading.")
    outputFile = open(histdatapath,'w')
    for i in insList.values():
        outputFile.write(day + "," + i.outputHistData() + "\n")
    outputFile.flush()
    outputFile.close()
    today = datetime.datetime.utcnow()
    print(today.isoformat())