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
    
    logPath = "D:\\OKExFeed\\log\\histData.log"
    lf = open(logPath,'w')
    
    d = open(dateFile,'r')
    day = d.readline()
    d.close()
    
    print("date:" + day)
    lf.write("date:" + day + "\n")
    
    histdatapath = datapath + "histData\\histdata_" + day + ".csv"

    filepath = datapath + "feed"
    filename = "OKExFeed_" + day + ".log"

    filereader.setFileNameAndPath(filepath, filename)
    filereader.setFile(day)
    print("Create Ins List.")
    lf.write("Create Ins List.\n")
    today = datetime.datetime.utcnow()
    print(today.isoformat())

    masterfilepath = datapath + "master"
    masterfilename = "OKExMaster_" + day + ".txt"
    
    lf.write("Master File:" + masterfilename + "\n")
    filereader.setMasterFile(masterfilepath, masterfilename)

    insList = filereader.readMasterFile(day)
    
    print("Ins List:")
    lf.write("Ins List:\n")
    for i in insList.values():
        print(i.instId)
        lf.write(i.instId + "\n")
    print("Start Reading")
    lf.write("Start Reading\n")
    lf.write("Feed File Name:" + filename + "\n")
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
    lf.write("Finished Reading\n")
    outputFile = open(histdatapath,'w')
    for i in insList.values():
        outputFile.write(day + "," + i.outputHistData() + "\n")
    outputFile.flush()
    outputFile.close()
    today = datetime.datetime.utcnow()
    print(today.isoformat())