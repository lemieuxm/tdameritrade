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
    loggedIn = False
    requestCounter = 0
    isClosed = False
    debug = False
    tdh = None
    userInfo = None
    start_time = None
    
    def __init__(self, debug=False):
        self.debug = debug
        self.tdh = tdhelper.TDHelper()
        self.userInfo = self.tdh.getStreamerInfo()
    
    def on_message_wrapper(self, messageHandler):
        def on_message(ws, message):
            self.on_message_internal(ws, message, messageHandler)
        return(on_message)
    
    def on_message_internal(self, ws, message, messageHandler):  # @UnusedVariable
        #print("Start time to response time: %f"%(dt.datetime.utcnow() - self.start_time).total_seconds())
        m = json.loads(message)
        if m.get('notify') is not None:
            if len(m.get('notify')) > 0:
                if m.get('notify')[0].get('heartbeat') is not None:
                    #n = round(time.time()*1000)
                    #print("%i-%s"%(n, m.get('notify')[0].get('heartbeat'))) 
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
        messageHandler(m)

                    
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
    
    
    def on_open_wrapper(self, messages):
        def on_open(ws):
            self.on_open_internal(ws, messages)
        return(on_open)
    
    def on_open_internal(self, ws, messages):
        def run(*args):  # @UnusedVariable
            try:
                if not self.loggedIn:
                    loginMessage = self.loginMessage(self.userInfo)
                    ws.send(loginMessage)

                while not self.loggedIn and not self.isClosed:
                    time.sleep(1)
                
                if self.loggedIn:
                    requests = []
                    for message in messages:
                        baseRequest = self.baseRequest(self.requestId())
                        message.update(baseRequest)
                        requests.append(message)
                    
                    callMessage = json.dumps({'requests': requests}, indent=4, sort_keys=True) 
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


    def start(self, messages, messageHandler):
        am = tdhelper.AuthManager()
        authData = am.get_token()
        host = "wss://"+self.userInfo['streamerInfo']['streamerSocketUrl']+"/ws"
        websocket.enableTrace(False)
        authValue = authData['token_type'] + ' ' + authData['access_token']
        ws = websocket.WebSocketApp (
            host, on_message=self.on_message_wrapper(messageHandler),
            on_error=self.on_error,
            on_close=self.on_close, 
            on_data=self.on_data,
            header = ['Authorization: '+authValue],
            on_cont_message=self.on_cont_message
            )
        ws.on_open = self.on_open_wrapper(messages)
        try:
            #self.start_time = dt.datetime.utcnow()
            ws.run_forever()
        except Exception as e:
            print(e)
            print(os.sys.exc_info()[0:2])
            print("done reporting exception") 

    def requestId(self):
        ret = self.requestCounter
        self.requestCounter += 1
        return(ret)
        
    def baseRequest(self, requestId):
        request = {
                "requestid": requestId,
                "account": self.userInfo['accounts'][0]['accountId'],
                "source": self.userInfo['streamerInfo']['appId']
                }
        return(request)
        
    def levelone_forex(self, symbol, dataHandler, fields="0,1,2,3,4,5,6,7,8,9,10,11,12,13"):
        messages = [self.levelone_forex_msg(symbol, fields)]
        self.start(messages, dataHandler)

    def levelone_forex_msg(self, symbol, fields="0,1,2,3,4,5,6,7,8,9,10,11,12,13"):
        message = {
            "service": "LEVELONE_FOREX",
            "command": "SUBS",
            "parameters": {
                "keys": symbol,
                "fields": fields
                }
            }
        return(message)

    def chart_futures(self, symbol, dataHandler=defaultHandler, fields="0,1,2,3,4,5,6,7,8"):
        self.chart_type("CHART_FUTURES", symbol, dataHandler, fields)

    def chart_futures_msg(self, symbol, fields="0,1,2,3,4,5,6,7,8"):
        return(self.chart_type_msg("CHART_FUTURES", symbol, fields))

    def chart_type(self, service, symbol, dataHandler, fields):
        self.start([self.chart_type_msg(service, symbol, fields)], dataHandler)        

    def chart_type_msg(self, service, symbol, fields):
        message = {
            "service": service,
            "command": "SUBS",
            "parameters": {
                "keys": symbol,
                "fields": fields
            }
        }
        return(message)


    def chartHistory(self, symbol, frequency, startTime, endTime, dataHandler=defaultHandler):
        tdData = tddata.TdData()
        data = tdData.loadDataForDateRange(symbol, startTime, endTime, frequency)
        if data is not None:
            dataHandler(data)
            return
        def callHandler(data):
            tdData.saveDataForDateRange(symbol, startTime, endTime, frequency, data)
            dataHandler(data)
        self.start([self.chart_history_msg(symbol, frequency, startTime, endTime)], callHandler)   
        
    def chart_history_msg(self, symbol, frequency, startTime, endTime):
        startMillis = int(startTime.timestamp()*1000.0)
        endMillis = int(endTime.timestamp()*1000.0)  
        message = {
            "service": "CHART_HISTORY_FUTURES",
            "command": "GET",
            "parameters": {
                "symbol": symbol,
                "frequency": frequency,
                "START_TIME": startMillis,
                "END_TIME": endMillis
            }
        }
        return(message)
        
    # see https://developer.tdameritrade.com/content/streaming-data#_Toc504640594
    #   Need authorization
    def news_headline(self, symbols, fields = "0,1,2,3,4,5,6,7,8,9,10", dataHandler=defaultHandler):
        self.start([self.news_headline_msg(symbols, fields)], dataHandler)  

    def news_headline_msg(self, symbols, fields = "0,1,2,3,4,5,6,7,8,9,10"):
        message = { "service": "NEWS_HEADLINE","command": "SUBS",
            "parameters": {"keys": ','.join(symbols),"fields": fields }
            }
        return(message)
    
    def news_headlinelist(self, symbols, fields = "0,1,2,3,4,5,6,7,8,9,10", dataHandler=defaultHandler):
        self.start([self.news_headline_msg(symbols, fields)], dataHandler)  
    
    def news_headlinelist_msg(self, symbols, fields = "0,1,2,3,4,5,6,7,8,9,10"):
        message = { "service": "NEWS_HEADLINE_LIST","command": "GET",
            "parameters": {"keys": ','.join(symbols),"fields": fields }
            }
        return(message)
    
    def news_story(self, story_id, fields = "0,1,2,3,4,5,6,7,8,9,10", dataHandler=defaultHandler):
        self.start([self.news_story_msg(story_id, fields)], dataHandler)  
    
    def news_story_msg(self, symbols, fields = "0,1,2,3,4,5,6,7,8,9,10"):
        message = { "service": "NEWS_STORY","command": "GET",
            "parameters": {'keys': ','.join(symbols),"fields": fields }
            }
        return(message)
    
    # Frequency: m1, m5, m10, m30, h1, d1, w1, n1
    # Period: d5, w4, n10, y1, y10
    def chart_history_period_msg(self, symbol, frequency, period):
        message =  {"service": "CHART_HISTORY_FUTURES", "command": "GET",
           "parameters": {"symbol": symbol,"frequency": frequency,"period": period}
        }
        return(message)

    def loginMessage(self, userInfo):
        timestamp = dt.datetime.strptime(userInfo['streamerInfo']['tokenTimestamp'], "%Y-%m-%dT%H:%M:%S+0000").replace(tzinfo=pytz.UTC)
        timestamp = (timestamp - EPOCH).total_seconds() * 1000
        credential = {
            'userid': userInfo['accounts'][0]['accountId'],
            'token': userInfo['streamerInfo']['token'],
            'company': userInfo['accounts'][0]['company'],
            'segment': userInfo['accounts'][0]['segment'],
            'cddomain': userInfo['accounts'][0]['accountCdDomainId'],
            'usergroup': userInfo['streamerInfo']['userGroup'],
            'accesslevel': userInfo['streamerInfo']['accessLevel'],
            'authorized': 'Y',
            'timestamp': int(timestamp),
            'appid': userInfo['streamerInfo']['appId'],
            'acl': userInfo['streamerInfo']['acl']
            }
        sendObj = {}
        sendObj['requests'] = [{
            'service': 'ADMIN',
            'command': 'LOGIN',
            'requestid': self.requestId(),
            'account': userInfo['accounts'][0]['accountId'],
            'source': userInfo['streamerInfo']['appId'],
            'parameters': {
                'credential': urllib.parse.urlencode(credential),
                'token': userInfo['streamerInfo']['token'],
                'version': '1.0'
                }
            }
        ]                
        jsonString = json.dumps(sendObj, indent=4, sort_keys=False) 
        return jsonString
    

