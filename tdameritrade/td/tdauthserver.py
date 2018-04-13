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

import json
from bottle import route, request, ServerAdapter, run
import urllib
from tdameritrade.td.tdhelper import AuthManager
from tdameritrade import CONFIGDIR

appConfigFile = '%s/td_app_config'%(CONFIGDIR)
with open(appConfigFile) as tdconfig:
    config = json.load(tdconfig)

authcode = ""
selfsrv = None

redirect_uri = 'https://%s:%s/code'%(config['redirect_host'], config['redirect_port'])
baseurl = "https://auth.tdameritrade.com/auth"
v = {'response_type':'code', 'redirect_uri':redirect_uri,'client_id': config.get("oauthid")} 
url = baseurl+"?"+urllib.parse.urlencode(v)

@route('/code')
def code():
    return handleCodeRequest()

@route('/')
def index():
    return handleCodeRequest()

def handleCodeRequest():
    getvars = request.query.decode()
    if "code" in getvars:
        authcode = getvars["code"]
        authcode = urllib.parse.unquote(authcode)
        am = AuthManager()
        am.saveCode({'code':authcode}, srv=selfsrv)
        return('code: '+authcode)
    return "<a href='"+url+"'>Authorize</a>"  

@route('/decode')
def decode():
    unencoded = urllib.parse.unquote(authcode)
    return unencoded

# copied from bottle. Only changes are to import ssl and wrap the socket
class SSLWSGIRefServer(ServerAdapter):

    global CONFIGDIR
    quiet = False

    def run(self, handler):
        global selfsrv
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(self, *args, **kw): pass
            self.options['handler_class'] = QuietHandler
        selfsrv = make_server(self.host, self.port, handler, **self.options)
        certFile = '%s/cert.pem'%(CONFIGDIR)
        # print("using certfile: ", certFile)
        selfsrv.socket = ssl.wrap_socket (
            selfsrv.socket,
            certfile=certFile,  # path to certificate
            server_side=True)
        print("Starting Server - open the following in a browser to authenticate: ", redirect_uri)
        selfsrv.serve_forever()
        print("After server_forever() call")

    def stop(self):
        selfsrv.shutdown()

def startServer(host, port):
    selfsrv = SSLWSGIRefServer(host=host, port=port)
    run(server=selfsrv)
    return(selfsrv) 

# if __name__ == '__main__':
#     app = Bottle()
#     app.run(host=config.get('redirect_host'), port=config.get('redirect_port'))

