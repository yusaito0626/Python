# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 19:35:17 2022

@author: yusai
"""

import json
import OKExInstrument

class FeedFileReader:
    def __init__(self):
        self.filePath = ""
        self.fileName = ""
        self.masterFilePath = ""
        self.masterFileName = ""
        self.isFileSet = False
        self.insList = {}
        
    def setFileNameAndPath(self,path,name):#Name should contain YYYY-MM-DD
        self.filePath = path
        self.fileName = name
        
    def setFile(self,day):#YYYY-MM-DD
        file = self.filePath + "\\" + self.fileName.replace("YYYY-MM-DD",day)
        self.f = open(file,'r')
        self.isFileSet = True
        
    def setMasterFile(self,path,name):
        self.masterFilePath = path
        self.masterFileName = name
        
    def readMasterFile(self,day):
        file = self.masterFilePath + "\\" + self.masterFileName.replace("YYYY-MM-DD",day)
        with open(file,'r') as master:
            for line in master:
                data = json.loads(line)
                if(data["instId"] in self.insList):
                    ins = self.insList[data["instId"]]
                    ins.setInsData(data)
                else:
                    ins = OKExInstrument.Instrument()
                    ins.setInsData(data)
                    self.insList[ins.instId] = ins
        return self.insList
                    
    def readline(self):
        if(self.isFileSet):
            line = self.f.readline()
            if(line==""):
                self.f.close()
                self.isFileSet = False
                return "\0"
            else:
                return line
        else:
            return ""