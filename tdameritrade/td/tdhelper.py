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


import requests
import json
import pickle
from pathlib import Path
import datetime as dt
import urllib
from urllib.request import Request, urlopen


class AuthManager():
    from tdameritrade import CONFIGDIR
    
    appConfigFile = '%s/td_app_config'%(CONFIGDIR)  
    configFile = '%s/td_auth_token_config'%(CONFIGDIR) 
    codeFile = '%s/td_auth_code_config'%(CONFIGDIR)    
    config = None
    
    def __init__(self):
        myConfigFile = Path(self.appConfigFile)
        if myConfigFile.exists():
            with open(self.appConfigFile, 'r') as file:
                self.config = json.load(file)
    
    def retrieve_refresh_token(self):
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        unencoded_code = self.get_unencoded_code()
        data = {'refresh_token': '', 'grant_type': 'authorization_code', 
                'access_type': 'offline', 'code': unencoded_code, 
                'client_id': self.config.get('oauthid'),
                'redirect_uri': 'https://%s:%s/code'%(self.config.get('redirect_host'), self.config.get('redirect_port'))}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        a = authReply.text
        jsondict = json.loads(a)
        self.saveToken(jsondict)
        return jsondict
    
    def get_unencoded_code(self):
        myCodeFile = Path(self.codeFile)
        codeData = {}
        if myCodeFile.exists():
            with open(myCodeFile, 'r') as file:
                codeData = json.load(file)
        currentTime = self.current_time()
        expireTime = 0
        if codeData.get("time") is not None:
            expireTime = codeData.get('time') + 60
        if expireTime < currentTime:
            # get a new code
            import tdameritrade.td.tdauthserver as tdas  
            global SERVER
            SERVER = tdas.startServer(self.config.get('redirect_host'), self.config.get('redirect_port'))
            myCodeFile = Path(self.codeFile)
            if myCodeFile.exists():
                with open(myCodeFile, 'r') as file:
                    codeData = json.load(file)
        code = codeData.get('code')
        return(code) 
    
    def retrieve_new_access_token(self, authdata):
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        data = {'refresh_token': authdata['refresh_token'], 'grant_type': 'refresh_token', 
                'access_type': 'offline', 
                'client_id': self.config['oauthid']}
        authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
        a = authReply.text
        jsondict = json.loads(a)
        self.saveToken(jsondict)
        return jsondict
        
    def get_token(self):
        myfile = Path(self.configFile)
        if myfile.exists():
            file = open(myfile, 'rb')
            self.authdata = pickle.load(file)
            file.close()
        else:
            self.authdata = {}
        # check access_token
        current_time = self.current_time()
        expiretime = 0
        if self.authdata.get('time') is not None and self.authdata.get('expires_in') is not None:
            expiretime = self.authdata.get('time') + self.authdata.get('expires_in')
        if self.authdata.get('refresh_token') is None:
            self.authdata = self.retrieve_refresh_token()
        elif expiretime < current_time: #access token is expired
            expiretime = self.authdata.get('time') + self.authdata.get('refresh_token_expires_in')
            if expiretime < current_time: # refresh token is expired
                self.authdata = self.retrieve_refresh_token()
            else: 
                self.authdata = self.retrieve_new_access_token(self.authdata)
        
        return self.authdata

    def current_time(self):
        return dt.datetime.utcnow().timestamp()

    def saveToken(self, jsondict):
        self.authdata = jsondict
        self.authdata['time'] = self.current_time()
        with open(self.configFile, 'wb') as file:
            pickle.dump(self.authdata, file)
            return True
        return self.authdata
        
    def saveCode(self, jsondict, srv):
        jsondict['time'] = self.current_time()
        with open(self.codeFile, 'w') as file:
            json.dump(jsondict, file)
        if srv is not None:
            import threading
            def shutdown():
                srv.shutdown()
            thread = threading.Thread(target=shutdown)
            thread.start()
            return True
        return False
            
    def getCode(self):
        'Consider starting the server... '
        myCodeFile = Path(self.codeFile)
        if myCodeFile.exists():
            with open(self.codeFile, 'r') as file:
                authCode = json.load(file)
                return authCode
        return None


class TDHelper():

    def dopost(self, url, headers={}, reqvars={}):
        authManager = AuthManager()
        authdata = authManager.get_token()
        headers['Authorization'] = authdata['token_type'] + ' ' + authdata['access_token']
        reply = requests.post(url, headers=headers, data=reqvars)
        jsontext = reply.text.encode()
        jsondict = json.loads(jsontext)
        return jsondict
    
    def dogetold(self, url, headers, reqvars):
        encurl = url + "?" + urllib.parse.urlencode(reqvars)
        reply = requests.get(encurl, headers)
        jsontext = reply.text.encode(encoding='utf-8')
        jsondict = json.loads(jsontext)
        return jsondict
    
    def doget(self, url, headers={}, reqvars={}):
        authManager = AuthManager()
        authdata = authManager.get_token()
        encurl = url + "?" + urllib.parse.urlencode(reqvars)
        q = Request(encurl)
        for key, value in headers.items():
            q.add_header(key, value)
        authHeader = authdata['token_type'] + ' ' + authdata['access_token']
        q.add_header("Authorization", authHeader)
        uo = urlopen(q)
        jsontext = uo.read()
        jsondict = json.loads(jsontext)
        return jsondict

    def getAccounts(self):
        url = "https://api.tdameritrade.com/v1/accounts"
        reqvars = {'fields': 'positions'}
        tdHelper = TDHelper()
        data = tdHelper.doget(url, reqvars=reqvars)
        return data

    def getPrimaryAccountId(self):
        data = self.getAccounts()
        return(data[0]["securitiesAccount"]["accountId"])
    
    def getWatchLists(self, accountId):
        url = "https://api.tdameritrade.com/v1/accounts/{0}/watchlists".format(accountId)
        data = self.doget(url)
        return(data)
    
    def searchInstruments(self, symbol, projection='symbol-search'):
        url = 'https://api.tdameritrade.com/v1/instruments'
        reqvars = {'symbol': symbol, 'projection': projection}
        data = self.doget(url, reqvars=reqvars)
        return(data)

    def getStreamerInfo(self):
        data = self.getUserPrincipals("streamerSubscriptionKeys,streamerConnectionInfo")
        return data 

    def getUserPrincipals(self, fields):
        url = "https://api.tdameritrade.com/v1/userprincipals"
        data = self.doget(url, reqvars = {'fields': fields})
        return data
# {
#     "EUR/USD": {
#         "assetType": "FOREX",
#         "description": "Euro/USDollar Spot",
#         "exchange": "GFT",
#         "symbol": "EUR/USD"
#     }
# }

        
