# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 13:47:53 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python\\OKEx")
import datetime
import OKExFileReader
import OKExParser
import OKExInstrument
import OKExOptimizer

parser = OKExParser.OKExParser()

Filename = "D:\\log\\BalAndPosTest.log"
f= open(Filename,'r')
txt = f.readline()
obj = parser.Parse(txt)
obj.ToString()