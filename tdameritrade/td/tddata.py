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
from pathlib import Path
import json
from tdameritrade.td import tdhelper as tdh
import urllib
from tdameritrade import DATADIR, DATE_FORMAT, UTC

class TdData(object):
    '''
    Class for getting and caching TdData
    '''
    ONE_DAY = dt.timedelta(days=1)
    tdHelper = None

    def __init__(self):
        # Path(self.DATA_DIR).mkdir(parents=True, exist_ok=True)
        self.tdHelper = tdh.TDHelper()
        
    #Story the data, one file per day
    # expect a dt.datetime
    def getNMinByDay(self, symbol, startDate, endDate, freq): #end date inclusive
        data = {}
        curDate = startDate
        needDates = [] 
        while curDate <= endDate:
            curData = self.loadDataForDate(symbol, curDate.strftime(DATE_FORMAT), freq)
            if curData is None:
                needDates.append(curDate)
            else:
                dateString = curDate.strftime(DATE_FORMAT)
                data[dateString] = curData 
            curDate += self.ONE_DAY
        if len(needDates) > 0:
            minDate = min(needDates)
            maxDate = max(needDates)
            newData = self.fetchData(symbol, minDate, maxDate, freq)
            if newData is not None:
                data.update(newData)
        return data
    
    def fetchData(self, symbol, startDate, endDate, freq, extendedHours="true"):
        authManager = tdh.AuthManager()
        authData = authManager.get_token()
        url = "https://api.tdameritrade.com/v1/marketdata/"+urllib.parse.quote(symbol, safe='')+"/pricehistory"
        reqvars = {'apikey': authManager.config['oauthid'],
                   'periodType': 'day', 'frequencyType': 'minute',
                   'frequency': freq, 'needExtendedHoursData': extendedHours,
                   'startDate': int(startDate.timestamp()*1000), 
                   'endDate': int(endDate.timestamp()*1000) }
        authHeader = "Bearer" + ' ' + authData['access_token']
        headers = {'Authorization': authHeader}
        data = self.tdHelper.doget(url, headers, reqvars)
        fetchedData = {}
        if data['empty'] is False:
            candles = data['candles']
            for candle in candles:
                candleDatetime = int(candle['datetime'])
                candleDate = dt.datetime.fromtimestamp(candleDatetime/1000.0, UTC)
                dateString = candleDate.strftime(DATE_FORMAT)
                if dateString not in fetchedData:
                    fetchedData[dateString] = []
                fetchedData[dateString].append(candle)
        tmpDate = startDate
        while tmpDate <= endDate:
            dateString = tmpDate.strftime(DATE_FORMAT)
            value = fetchedData.get(dateString)
            if value is None:
                value = []
            self.saveDataForDate(symbol, dateString, freq, value)
            tmpDate += dt.timedelta(days=1)
        return(fetchedData)
    
    
    def toFileName(self, symbol):
        out = symbol.replace('/', '_').replace('=', '_').replace(' ', '_').replace(':', '_')
        return(out)
    
    def saveDataForDate(self, symbol, date, freq, data):
        symbolName = self.toFileName(symbol)
        fileName = symbolName+"_"+str(freq)+"_"+self.toFileName(str(date))+"_td"
        fileDir = DATADIR+"/"+symbolName+"/price"
        Path(fileDir).mkdir(parents=True, exist_ok=True)
        fullFileName = fileDir+"/"+fileName
        pathObject = Path(fileDir)
        if pathObject.exists():
            with open(fullFileName, 'w') as fileObject:
                json.dump(data, fileObject, sort_keys=True, indent=4, separators=(',', ': '))
                return True
        return False
        
    def loadDataForDate(self, symbol, date, freq):
        symbolName = self.toFileName(symbol)
        fileName = symbolName+"_"+str(freq)+"_"+self.toFileName(str(date))+"_td"
        fileDir = DATADIR+"/"+symbolName+"/price"
        fullFileName = fileDir+"/"+fileName
        pathObject = Path(fullFileName)
        data = None
        if pathObject.exists():
            with open(fullFileName, 'r') as fileObject:
                data = json.load(fileObject)
        return data
        

    def saveDataForDateRange(self, symbol, startDate, endDate, freq, data):
        symbolName = self.toFileName(symbol)
        fileName = symbolName+"_"+str(freq)+"_"+self.toFileName(str(startDate))+"_to_"+self.toFileName(str(endDate))+"_td"
        fileDir = DATADIR+"/"+symbolName+"/price"
        Path(fileDir).mkdir(parents=True, exist_ok=True)
        fullFileName = fileDir+"/"+fileName
        pathObject = Path(fileDir)
        if pathObject.exists():
            with open(fullFileName, 'w') as fileObject:
                json.dump(data, fileObject, sort_keys=True, indent=4, separators=(',', ': '))
                return True
        return False
        
    def loadDataForDateRange(self, symbol, startDate, endDate, freq):
        symbolName = self.toFileName(symbol)
        fileName = symbolName+"_"+str(freq)+"_"+self.toFileName(str(startDate))+"_to_"+self.toFileName(str(endDate))+"_td"
        fileDir = DATADIR+"/"+symbolName+"/price"
        fullFileName = fileDir+"/"+fileName
        pathObject = Path(fullFileName)
        data = None
        if pathObject.exists():
            with open(fullFileName, 'r') as fileObject:
                data = json.load(fileObject)
        return data

