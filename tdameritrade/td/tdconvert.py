'''
Created on Jun 11, 2018

@author: mdl
'''

import datetime as dt
import math


def level_one_to_ml(message):
    messages = []
    for q in message['content']:
        a = {}
        a = setif(a, 'symbol', q, 'key')
        a = setif(a, 'is_delayed', q, 'delayed')
        a = setif(a, 'bid', q, '1')
        a = setif(a, 'ask', q, '2')
        a = setif(a, 'last_trade', q, '3')
        a = setif(a, 'bid_size', q, '4')
        a = setif(a, 'ask_size', q, '5')
        a = setif(a, 'total_volume', q, '6')
        a = setif(a, 'last_size', q, '7')
        a = setif(a, 'quote_time_raw', q, '8', 0)
        a = setif(a, 'trade_time_raw', q, '9', 0)
        a = setif(a, 'high_price', q, '10')
        a = setif(a, 'low_price', q, '11')
        a = setif(a, 'close_price', q, '12')
        a = setif(a, 'exchange_id', q, '13')
        a = setif(a, 'description', q, '14')
        a = setif(a, 'open', q, '15')
        a = setif(a, 'net_change', q, '16')
        a = setif(a, 'pct_change', q, '17')
        a = setif(a, 'exchange_name', q, '18')
        a = setif(a, 'digits', q, '19')
        a = setif(a, 'security_status', q, '20')
        a = setif(a, 'tick', q, '21')
        a = setif(a, 'tick_amount', q, '22')
        a = setif(a, 'product', q, '23')
        a = setif(a, 'is_tradable', q, '24')
        a = setif(a, 'market_maker', q, '25')
        a = setif(a, 'year_high', q, '26')
        a = setif(a, 'year_low', q, '27')
        a = setif(a, 'mark', q, '28')
        akeys = a.keys()
        if (a['quote_time_raw'] > 0 or a['trade_time_raw'] > 0) and 'symbol' in akeys and ('bid' in akeys or 'ask' in akeys or 'net_change' in akeys):
            a['message_ts'] = message['timestamp']
            a['insert_ts'] = dt.datetime.utcnow().timestamp()*1000
            messages.append(a)
        else:
            print('This should not happen: '+str(a))
    return(messages)

def setif(a, name, q, num, default=None):
    x = q.get(num)
    if x is not None and (type(x) is str or not math.isnan(x)):
        a[name] = x
    elif default is not None:
        a[name] = default
    return(a)

def chart_history_to_ml(message):
    messages = []
    for q in message['content']:
        a = {'symbol': q['key'], 'numCandles': q['2'], 'source': 'td'}
        aa = []
        for s in q['3']:
            aaq = {}
            aaq['quote_time_raw'] = s['0']
            aaq['quote_time'] = dt.datetime.fromtimestamp(s['0']/1000.0, dt.timezone.utc)
            aaq['open'] = s['1']
            aaq['high'] = s['2']
            aaq['low'] = s['3']
            aaq['close'] = s['4']
            aaq['volume'] = s['5']
            aa.append(aaq)
        a['candles'] = aa
        messages.append(a)
    return(messages) 
             
def headline_to_ml(message):
    messages = []
    for q in message['content']:
        a = {}
        a = setif(a, 'symbol', q, 'key')
        a = setif(a, 'error_code', q, '1')        
        a = setif(a, 'story_time', q, '2')        
        a = setif(a, 'headline_id', q, '3')        
        a = setif(a, 'status', q, '4')        
        a = setif(a, 'headline', q, '5')        
        a = setif(a, 'story_id', q, '6')        
        a = setif(a, 'keyword_count', q, '7')        
        a = setif(a, 'keywords', q, '8')        
        a = setif(a, 'is_hot', q, '9')        
        a = setif(a, 'source', q, '10')
        a['message_ts'] = message['timestamp']
        a['insert_ts'] = dt.datetime.utcnow().timestamp()*1000      
        messages.append(a)
    return(messages)
    pass

def headlinelist_to_ml(message):
    messages =[]
    for q in message['content']:
        a = {}
        
        
    return(messages)

