# -*- coding: utf-8 -*-
"""
Created on Sun Nov  6 18:56:39 2022

@author: junsup
"""

import pandas as pd
import pyupbit
import requests
import time

def get_tickers(watch_range=30, pass_ticker=['KRW-BTT','KRW-XEC']):
    ticker_df = pd.DataFrame()
    tickers = pyupbit.get_tickers(fiat="KRW")
    
    for ticker in tickers:
        url = "https://api.upbit.com/v1/ticker?markets=" + ticker
        response = requests.get(url)
        ticker_df = ticker_df.append(pd.DataFrame(response.json()))
        time.sleep(0.1)
        
    ticker_df = ticker_df.sort_values(by='acc_trade_price_24h', ascending=False).reset_index(drop=True)
    ticker_df = list(ticker_df['market'][0:watch_range])
    
    for pt in pass_ticker:
        if pt in tickers:
            tickers.remove(pt)
        else:
            pass
        
    return ticker_df

cnt = 10
volume_total = 0
curr_day = time.localtime().tm_mday
get_tickers_lst = get_tickers()

while True:
    #try:
    now_day = time.localtime().tm_mday
    if now_day != curr_day:
        get_tickers_lst = get_tickers()
        curr_day = now_day

    for coin_name in get_tickers_lst:
        print("----------------------------")
        coin = pyupbit.get_ohlcv(ticker=coin_name,interval='minute3',count=cnt)
        print(coin_name)
        print(coin['volume'])
        for i in range(cnt-1):
            volume_total += coin['volume'][i]
        volume_avg = volume_total / (cnt-1)
        print(coin.index[(cnt-1)])
        if coin['volume'][(cnt-1)] > volume_avg * 5:
            f = open("volume_check.txt", 'a')
            data = coin.index[(cnt-1)] + " // " + coin_name + " // " + coin['volume'][(cnt-1)] + "\n"  # 날짜, 코인이름, 거래량 저장
            f.wirte(data)
        time.sleep(0.1)


'''
    except:
        pass
'''   

