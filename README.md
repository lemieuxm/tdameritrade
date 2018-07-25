# MLTDAmeritrade

As of 20180725.... TDAmeritrade has refused to support Forex trading through the API.  I have moved all my money away from TDAmeritrade as a result.  I will no longer develop this librray. 


Python library for accessing TDAmeritrade API's. 

This is a work in progress.  I am currently working with the very helpful API support team at TDAmeritrade to get everything working.  The documentation for the API's are at https://developer.tdameritrade.com/.  This tool will only be useful to you if you have a TDAmeritrade account, which you can get at https://www.tdameritrade.com.  Pull requests are encouraged. 

### Notes

* There is a webserver that will automatically startup as needed to authenticate with TDAmeritrade as needed.  That server needs to run SSL, and needs a certificate.  Place the certificate and key in the following file: `~/.mltrading/config/cert.pem`.   See https://developer.tdameritrade.com/content/authentication-sample-python-3 for an example of how to create a self-signed certificate. 
* You will need to create the following file `~/.mltrading/config/td_app_config` with some configuration information (corresponding to your app and your confguration).  
```javascript
{
        "oauthid": "{oauthid}@AMER.OAUTHAP",
        "redirect_host": "localhost",
        "redirect_port": 39948
}
```
* Data is cached under `~/.mltrading/data/`.
* Authentication data is cached in two files:  `~/.mltrading/config/td_auth_code_config` and `~/.mltrading/config/td_auth_token_config`
* Look in `examples` for ways this can be used.   
* This package can be installed directly from github using the following command: `pip install git+https://github.com/lemieuxm/tdameritrade.git`
* This has been tested with Python 3.6
* Currently, the TD Ameritrade servers are allow a maximum of ONE connection per user to the streaming API.  I've made the request to the API dev team to increase (I suggested 5).  It is difficult as I have one constantly running stream to collect data for back testing, and want to create another for development, and when all is said and done, I will also have one actively trading.  
* FOREX data was and is my motivation for starting this.  Development on this library is slow mostly due to the fact that FOREX data access isn't working quite right on TD Ameritrades servers.  I'm working with the API team to resolve it.
* I am currently developing a private library that uses this library and does backtesting, trading, and data analysis.  As that matures, I may move some of those tools into this tool, if those things are desired (or move parts of the private library into a publicly available library).  I'm currently not planning to make my personal trading algorithm and methodology public, so parts of the private library will also remain private.  


Please send questions to: (Matthew) mdl@mlemieux.com 


