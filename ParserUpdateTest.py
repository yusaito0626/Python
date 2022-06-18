# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 19:46:08 2022

@author: yusai
"""


import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python")

import OKExEnums
import OKExParser
import OKExMessage
import OKExInstrument


Filename = "D:\\OKExFeed\\feedtest.log"
f= open(Filename,'r')
txt = f.readline()
outputFileName = "D:\\OKExFeed\\Board.csv"
out = open(outputFileName,'w')

parsedData = OKExParser.Parse(txt)
books = OKExInstrument.Board()
books.priceUnit = 10
books.initializeBoard(parsedData, 400)
print(books.ToString())
out.write(books.ToString())

up = f.readline()
updateData = OKExParser.Parse(up)
books.updateBooks(updateData)
print(books.ToString())
out.write(books.ToString())
