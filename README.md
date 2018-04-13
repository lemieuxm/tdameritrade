# MLTDAmeritrade
Library for accessing TDAmeritrade API's. 

This is a work in progress.  I am currently working with the very helpful API support team at TDAmeritrade to get everything working.  The documentation for the API's are at https://developer.tdameritrade.com/.  This tool will only be useful to you if you have a TDAmeritrade account, which you can get at https://www.tdameritrade.com.  

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
* Look at the `driver.py` file for examples of how to call some of the methods.  
* This package can be installed directly from github using the following command: `pip install git+https://github.com/lemieuxm/tdameritrade.git`
* This has been tested with Python 3.6
