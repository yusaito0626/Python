# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 21:58:19 2022

@author: yusai
"""

import OKExEnums

class Order:
    instId = ""
    tdMode = OKExEnums.tradeMode.NONE
    ccy = ""
    clOdrId = ""
    tag = ""
    side = OKExEnums.Side.NONE
    posSide = OKExEnums.positionSide.NONE
    ordType = OKExEnums.orderType.NONE
    sz = 0
    px = 0
    reduceOnly = False
    tgtCcy = OKExEnums.quantityType.NONE
    banAmend = False
    