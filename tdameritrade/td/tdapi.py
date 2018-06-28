'''
Created on Jun 27, 2018

@author: mdl
'''
from tdameritrade.td.tdhelper import TDHelper
import datetime as dt

class TDApi(object):
    
    tdh = None
    datetime_format = "%Y-%m-%dT%H:%M:%S"

    def __init__(self):
        self.tdh = TDHelper()
    
    # https://developer.tdameritrade.com/account-access/apis
    
    # https://developer.tdameritrade.com/account-access/apis/delete/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0
    def cancel_order(self, account_id:str, order_id:str) -> dict:
        url = "https://api.tdameritrade.com/v1/accounts/%s/orders/%s"%(str(account_id), str(order_id))
        d = self.tdh.dodelete(url)
        return(d)

    # https://developer.tdameritrade.com/account-access/apis/get/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0
    def get_order(self, account_id:str, order_id:str) -> dict:
        url = "https://api.tdameritrade.com/v1/accounts/%s/orders/%s"%(str(account_id), str(order_id))
        d = self.tdh.doget(url)
        return(d)
    
    # https://api.tdameritrade.com/v1/accounts/{accountId}/orders
    def get_orders_by_path(self, account_id, max_results:int, from_time:dt.datetime, to_time:dt.datetime, status) -> dict:
        url = "https://api.tdameritrade.com/v1/accounts/%s/orders"%account_id
        reqvars = {'maxResults': max_results, 'fromEnteredTime':from_time.strftime(self.datetime_format), 
                   'toEnteredTime':to_time.strftime(self.datetime_format), 'status':status}
        d = self.tdh.doget(url, reqvars=reqvars)
        return(d)
    
    def get_orders_by_query(self, account_id, max_results:int, from_time:dt.datetime, to_time:dt.datetime, status):
        url = "https://api.tdameritrade.com/v1/orders"
        reqvars = {'maxResults': max_results, 'fromEnteredTime':from_time.strftime(self.datetime_format), 
                   'toEnteredTime':to_time.strftime(self.datetime_format), 'status':status, 'accountId':account_id}
        d = self.tdh.doget(url, reqvars=reqvars)
        return(d)
    
    # https://api.tdameritrade.com/v1/accounts/{accountId}/orders
    # There are too many options for adding individual variables -- see the url above for details
    def place_order(self, account_id:str, data:dict):
        url = "https://api.tdameritrade.com/v1/accounts/%s/orders"%account_id
        d = self.tdh.doget(url, reqvars=data)
        return(d)
    
    # https://developer.tdameritrade.com/account-access/apis/put/accounts/%7BaccountId%7D/orders/%7BorderId%7D-0
    def replace_order(self, account_id:str, order_id:str, data:dict):
        url = "https://api.tdameritrade.com/v1/accounts/%s/orders/%s"%(account_id, order_id)
        d = self.tdh.doput(url, reqvars=data)
        return(d)
    
    def get_quote(self, symbol):
        raise Exception("Unimplemented")
    
    #see: https://developer.tdameritrade.com/quotes/apis/get/marketdata/quotes
    def get_quotes(self, symbols):
        url = "https://api.tdameritrade.com/v1/marketdata/quotes"
        reqvars = {'symbol': ','.join(symbols)}
        mydict = self.tdh.doget(url, reqvars=reqvars)
        return(mydict)
        
    
    