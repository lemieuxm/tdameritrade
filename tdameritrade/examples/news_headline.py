'''
Created on May 1, 2018

@author: mdl
'''

import tdameritrade.td.tdstream as tds
import json

def newsHeadline():
    tdstream = tds.TDStream()
    data = tdstream.news_headline("SPY", fields="0,1,2,3,4,5,6,7,8,9,10")
    print(json.dumps(data, indent=4, sort_keys=True))

if __name__ == '__main__':
    newsHeadline()