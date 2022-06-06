# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 20:04:49 2022

@author: yusai
"""

from enum import Enum
 
class subscribeType(Enum):
    NONE = 0
    SUBSCRIBE = 1
    UNSUBSCRIBE = 2

class instType(Enum):
    NONE = 0
    SPOT = 1
    MARGIN = 2
    SWAP = 3
    FUTURES = 4
    OPTION = 5
    
class side(Enum):
    NONE = 0
    BUY = 1
    SELL = 2
    
class tradeMode(Enum):
    NONE = 0
    CASH = 1
    ISOLATED = 2
    CROSS = 3
    
class positionSide(Enum):
    NONE = 0
    NET = 1
    LONG = 2
    SHORT = 3
    
class orderType(Enum):
    NONE = 0
    MARKET = 1
    LIMIT = 2
    POST_ONLY = 3
    FOK = 4
    IOC = 5
    OPTIMAL_LIMIT_IOC = 6
    
class quantityType(Enum):
    NONE = 0
    BASE_CCY = 1
    QUOTE_CCY = 2