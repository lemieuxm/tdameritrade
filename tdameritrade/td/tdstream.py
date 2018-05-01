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

import tdameritrade.td.tdhelper as tdhelper
import tdameritrade.td.tddata as tddata
import datetime as dt
from tdameritrade import EPOCH
import urllib
import json
import websocket
from threading import Thread, Timer
import time
import os
import pytz

def defaultHandler(data):
    print(data)

class TDStream(object):
    streamInfo = None
    loggedIn = False
    requestCounter = 0
    isClosed = False
    apiCallMessage = None
    messageHandler = None
    debug = False
    
    def __init__(self, debug=False):
        self.debug = debug
        pass
    
    def on_message(self, ws, message):  # @UnusedVariable
        m = json.loads(message)
        if m.get('notify') is not None:
            if len(m.get('notify')) > 0:
                if m.get('notify')[0].get('heartbeat') is not None:
                    pass # This is a heartbeat ... not needed to 
                else: 
                    print("NOTIFY: "+str(m.get('notify')))
            return
        elif m.get("response") is not None:
            if len(m.get("response")) > 0:
                if m.get("response")[0].get("service") is not None and m.get("response")[0].get("command") == "LOGIN":
                    if m.get("response")[0].get("content").get("code") == 0:
                        self.loggedIn = True
                        return
        self.messageHandler(m)

                    
    def on_cont_message(self, ws, message):  # @UnusedVariable
        #print(message)
        if True:
            self.loggedIn = True
        
    def on_data(self, ws, data, a, b):
        # do nothing for now
        pass
    
    def on_error(self, ws, error):  # @UnusedVariable
        print(error)
    
    def on_close(self, ws):  # @UnusedVariable
        if not self.loggedIn:
            self.loggedIn = True
            t = Timer(1.0, self.start, ())
            t.start()
        else: 
            self.isClosed = True
            print("### closed ###")
    
    
    def on_open(self, ws):
        def run(*args):  # @UnusedVariable
            try:
                if not self.loggedIn:
                    loginMessage = self.loginMessage(self.streamInfo)
                    ws.send(loginMessage)

                while not self.loggedIn and not self.isClosed:
                    time.sleep(1)
                
                if self.loggedIn:
                    callMessage = self.apiCallMessage(self.requestId(), self.streamInfo) 
                    ws.send(callMessage)
                
                # send the message, then wait
                # so thread doesn't exit and socket
                # isn't closed
                while not self.loggedIn and not self.isClosed:
                    time.sleep(1)
                
            except Exception as e:
                print(str(e))
                print(os.sys.exc_info()[0:2])
                print("end exception")
            
            #ws.close()
            print("Thread terminating...")
    
        try: 
            Thread(target=run).start()
        except Exception as e:
            print(str(e))
            print(os.sys.exc_info()[0:2])
            print("end exception")

    def start(self, getRequest):
        tdh = tdhelper.TDHelper()
        am = tdhelper.AuthManager()
        authData = am.get_token()
        self.streamInfo = tdh.getStreamerInfo()
        self.apiCallMessage = getRequest
        host = "wss://"+self.streamInfo['streamerInfo']['streamerSocketUrl']+"/ws"
        websocket.enableTrace(True)
        authValue = authData['token_type'] + ' ' + authData['access_token']
        ws = websocket.WebSocketApp (
            host, on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close, 
            on_data=self.on_data,
            header = ['Authorization: '+authValue],
            on_cont_message=self.on_cont_message
            )
        ws.on_open = self.on_open
        try:
            ws.run_forever()
        except Exception as e:
            print(e)
            print(os.sys.exc_info()[0:2])
            print("done reporting exception") 


    def requestId(self):
        ret = self.requestCounter
        self.requestCounter += 1
        return(ret)
        
    def levelone_forex(self, symbol, dataHandler, fields="0,1,2,3,4,5,6,7,8,9,10,11,12,13"):
        self.messageHandler = dataHandler
        def apiCallFunction(requestId, streamInfo):
            request = {
                "requests": [
                    {
                        "service": "LEVELONE_FOREX",
                        "requestid": requestId,
                        "command": "SUBS",
                        "account": streamInfo['accounts'][0]['accountId'],
                        "source": streamInfo['streamerInfo']['appId'],
                        "parameters": {
                            "keys": symbol,
                            "fields": fields
                            }
                     }
                ]
            }
            jsonString = json.dumps(request, indent=4, sort_keys=True) 
            return jsonString 
        self.start(apiCallFunction)

    def chart_forex(self, symbol, dataHandler=defaultHandler, fields="0,1,2,3,4,5,6,7,8"):
        self.chart_type("CHART_FOREX", symbol, dataHandler, fields)

    def chart_futures(self, symbol, dataHandler=defaultHandler, fields="0,1,2,3,4,5,6,7,8"):
        self.chart_type("CHART_FUTURES", symbol, dataHandler, fields)

    def chart_type(self, service, symbol, dataHandler, fields):
        self.messageHandler = dataHandler
        def apiCallFunction(requestId, streamInfo):
            request = {
                "requests": [
                    {
                        "service": service,
                        "requestid": requestId,
                        "command": "SUBS",
                        "account": streamInfo['accounts'][0]['accountId'],
                        "source": streamInfo['streamerInfo']['appId'],
                        "parameters": {
                            "keys": symbol,
                            "fields": fields
                            }
                     }
                ]
            }
            jsonString = json.dumps(request, indent=4, sort_keys=True) 
            return jsonString 
        self.start(apiCallFunction)        


    def chartHistory(self, symbol, frequency, startTime, endTime, dataHandler=defaultHandler):
        tdData = tddata.TdData()
        data = tdData.loadDataForDateRange(symbol, startTime, endTime, frequency)
        startMillis = int(startTime.timestamp()*1000.0)
        endMillis = int(endTime.timestamp()*1000.0)
        if data is not None:
            dataHandler(data)
            return
        def apiCallFunction(requestId, streamInfo):
            request = {
                "requests": [
                    {
                        "service": "CHART_HISTORY_FUTURES",
                        "requestid": requestId,
                        "command": "GET",
                        "account": streamInfo['accounts'][0]['accountId'],
                        "source": streamInfo['streamerInfo']['appId'],
                        "parameters": {
                            "symbol": symbol,
                            "frequency": frequency,
                            "START_TIME": startMillis,
                            "END_TIME": endMillis
                        }
                     }
                ]
            }
            jsonString = json.dumps(request, indent=4, sort_keys=True) 
            return jsonString
        def callHandler(data):
            tdData.saveDataForDateRange(symbol, startTime, endTime, frequency, data)
            dataHandler(data)
        self.messageHandler = callHandler
        self.start(apiCallFunction)   
        

    # not finished
    def chartHistoryPeriod(self, symbol, frequency, period, dataHandler=defaultHandler):
        self.messageHandler = dataHandler
        def apiCallFunction(requestId, streamInfo):
            request = {
                "requests": [
                    {
                        "service": "CHART_HISTORY_FUTURES",
                        "requestid": requestId,
                        "command": "GET",
                        "account": streamInfo['accounts'][0]['accountId'],
                        "source": streamInfo['streamerInfo']['appId'],
                        "parameters": {
                            "symbol": symbol,
                            "frequency": frequency,
                            "period": period
                        }
                     }
                ]
            }
            jsonString = json.dumps(request, indent=4, sort_keys=True) 
            return jsonString 
        self.start(apiCallFunction)          


    def loginMessage(self, streamInfo):
        timestamp = dt.datetime.strptime(streamInfo['streamerInfo']['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S+0000").replace(tzinfo=pytz.UTC)
        timestamp = (timestamp - EPOCH).total_seconds() * 1000
        credential = {
            'userid': streamInfo['accounts'][0]['accountId'],
            'token': streamInfo['streamerInfo']['token'],
            'company': streamInfo['accounts'][0]['company'],
            'segment': streamInfo['accounts'][0]['segment'],
            'cddomain': streamInfo['accounts'][0]['accountCdDomainId'],
            'usergroup': streamInfo['streamerInfo']['userGroup'],
            'accesslevel': streamInfo['streamerInfo']['accessLevel'],
            'authorized': 'Y',
            'timestamp': int(timestamp),
            'appid': streamInfo['streamerInfo']['appId'],
            'acl': streamInfo['streamerInfo']['acl']
            }
        sendObj = {}
        sendObj['requests'] = [{
            'service': 'ADMIN',
            'command': 'LOGIN',
            'requestid': self.requestId(),
            'account': streamInfo['accounts'][0]['accountId'],
            'source': streamInfo['streamerInfo']['appId'],
            'parameters': {
                'credential': urllib.parse.urlencode(credential),
                'token': streamInfo['streamerInfo']['token'],
                'version': '1.0'
                }
            }
        ]                
        jsonString = json.dumps(sendObj, indent=4, sort_keys=False) 
        return jsonString
    
