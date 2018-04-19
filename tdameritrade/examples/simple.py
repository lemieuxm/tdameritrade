"""
    Copyright (C) 2018 Matthew LeMieux
    
    This file is part of a third party TDAmeritrade API Library, called MLTDAmeritrade.

    MLTDAmeritrade is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MLTDAmeritrade is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MLTDAmeritrade.  If not, see <http://www.gnu.org/licenses/>.
"""

import datetime as dt
import tdameritrade.td.tddata as tdd
import tdameritrade.td.tdhelper as tdh
import tdameritrade.td.tdstream as tds
import json

def nminbyday(symbol):  
    tdData = tdd.TdData()
    startDate = dt.datetime(2018, 4, 1)
    endDate = startDate + dt.timedelta(days=5)
    data = tdData.getNMinByDay(symbol, startDate, endDate, 5)
    print(json.dumps(data, indent=4, sort_keys=True))
    print("finished running nminbyday") 

def watchlists():
    tdhelper = tdh.TDHelper() 
    data = tdhelper.getWatchLists()
    print(json.dumps(data, indent=4, sort_keys=True))
    print("watchlists")

def searchinstruments(symbol):
    tdhelper = tdh.TDHelper() 
    data = tdhelper.searchInstruments(symbol)
    print(json.dumps(data, indent=4, sort_keys=True))
    print("watchlists")

def getAuth():
    authManager = tdh.AuthManager()
    token = authManager.get_token()
    print(json.dumps(token, indent=4, sort_keys=True))  

def streamerInfo():
    tdhelper = tdh.TDHelper()  # @UnusedVariable
    data = tdhelper.getStreamerInfo()
    print(json.dumps(data, indent=4, sort_keys=True))
    print("streamerInfo done")

def levelOne():
    tdstream = tds.TDStream()
    tdstream.levelone_forex("EUR/USD", dataHandler)
    print("finished")

def chartForex():
    tdstream = tds.TDStream()
    tdstream.chart_forex("EUR/USD")
    print("finished")

def chartFutures():
    tdstream = tds.TDStream()
    tdstream.chart_futures("/ES")
    print("finished")    

def dataHandler(data):
    print(data)

if __name__ == '__main__':
    #nminbyday()
    #watchlists()
    #searchinstruments("EUR/USD")
    #nminbyday("SPY")
    #nminbyday("SPY")
    #streamerInfo()
    #levelOne()
    chartForex()
    #chartFutures()
    
# {
#     "EUR/USD": {
#         "assetType": "FOREX",
#         "description": "Euro/USDollar Spot",
#         "exchange": "GFT",
#         "symbol": "EUR/USD"
#     }
# }


