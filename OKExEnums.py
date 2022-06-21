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
    ERROR = 3

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
    
class mgnMode(Enum):
    NONE = 0
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
    
class eventType(Enum):
    NONE = 0
    SNAPSHOT = 1
    DELIVERED = 2
    EXERCISED = 3
    TRANSFERRED = 4
    FILLED = 5
    LIQUIDATION = 6
    CLAW_BACK = 7
    ADL = 8
    FUNDING_FEE = 9
    ADJUST_MARGIN = 10
    SET_LEVERAGE = 11
    INTEREST_DEDUCTION = 12
    
class execType(Enum):
    NONE = 0
    Taker = 1
    Maker = 2
    
class orderState(Enum):
    NONE = 0
    LIVE = 1
    CANCELED = 2
    PARTIALLY_FILLED = 3
    FILLED = 4
    WAIT_NEW = 11
    WAIT_AMD = 12
    WAIT_CAN = 13
    
class priceType(Enum):
    NONE = 0
    LAST = 1
    INDEX = 2
    MARK = 3
    
class category(Enum):
    NONE = 0
    NORMAL = 1
    TWAP = 2
    ADL = 3
    FULL_LIQUIDATION = 4
    PARTIAL_LIQUIDATION = 5
    DELIVERY = 6
    DDH = 7
    
class amendResult(Enum):
    NONE = -99
    FAILURE = -1
    SUCCESS = 0
    AUTO_CANCEL = 1
    
class rfqState(Enum):
    NONE = 0
    ACTIVE = 1
    QUOTED = 2
    CANCELED = 3
    FILLED = 4
    EXPIRED = 5
    TRADED_AWAY = 6
    FAILED = 7
    
class algoState(Enum):
    NONE = 0
    STARTING = 1
    RUNNING = 2
    STOPPING = 3
    NO_CLOSE_POSITION = 4
    
class gridType(Enum):
    NONE = 0
    ARITHMETIC = 1
    GEOMETRIC = 2
    
class cancelType(Enum):
    NONE = 0
    MANUALSTOP = 1
    TAKEPROFIT = 2
    STOPLOSS = 3
    RISKCONTROL = 4
    DELIVERY = 5
    
class stopType(Enum):
    NONE = 0
    SELLBASECCY = 1
    KEEPBASECCY = 2
    MKTCLOSEALLPOS = 3
    KEEPPOS = 4
    
class contractGridType(Enum):
    NONE = 0
    LONG = 1
    SHORT = 2
    NUETRAL = 3
    
class subOrderState(Enum):
    NONE = 0
    CANCELED = 1
    LIVE = 2
    PARTIAL_FILLED = 3
    FILLED = 4
    CANCELLING = 5
    
class optType(Enum):
    NONE = 0
    CALL = 1
    PUT = 2
    
class ctType(Enum):
    NONE = 0
    LINEAR = 1
    INVERSE = 2
    
class insState(Enum):
    NONE = 0
    LIVE = 1
    SUSPEND = 2
    EXPIRED = 3
    PREOPEN = 4
    SETTLEMENT = 5
    
class sysStatus(Enum):
    NONE = 0
    SCHEDULED = 1
    ONGOING = 2
    COMPLETED = 3
    CANCELED = 4
    
class serviceType(Enum):
    NONE = -1
    WEBSOCKET = 0
    SPOTMERGIN = 1
    FUTURES = 2
    PERPETUAL = 3
    OPTIONS = 4
    TRADING = 5