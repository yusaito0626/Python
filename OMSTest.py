# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 20:59:26 2022

@author: yusai
"""

import OKExOMS

url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
apikey = "8af2e318-bec8-46e3-a394-187795d3e537"
passphrase = ""
secretKey = "9E2115F70CBD9CD806FD7E8AF360C16D"

OKExOMS.SetURL(url)
OKExOMS.SetKeys(apikey, passphrase, secretKey)
chk = OKExOMS.GetURL()
print(chk)
chk = OKExOMS.__GetSign('1538054050', '22582BD0CFF14C41EDBF1AB98506286D', 'GET', '/users/self/verify')
ret = OKExOMS.Connect(url,apikey, passphrase, secretKey)