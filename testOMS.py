# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 13:04:19 2022

@author: yusai
"""

import sys
sys.path.append("C:\\Users\\yusai\\source\\repos\\Python")

import OKExOMS

oms = OKExOMS.OMS()
oms.readKeyFile("D:\\OKExKeys.txt")

oms.Connect()

oms.Disconnect()