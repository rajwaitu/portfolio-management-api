
import requests
import pandas as pd
import json
import random
import datetime,time
import logging
import re
from nsepy import get_history
from scipy.signal import argrelmax
import numpy as np
import concurrent.futures
from exception.apiError import APIError
from utils.datetimeUtil import getDateRange

mode ='local'

if(mode=='local'):

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
    }

def __nsesymbolpurify(symbol):
    symbol = symbol.replace('&','%26') #URL Parse for Stocks Like M&M Finance
    return symbol

def __nsefetch(payload):
        try:
            output = requests.get(payload,headers=headers).json()
            #print(output)
        except ValueError:
            s =requests.Session()
            output = s.get("http://nseindia.com",headers=headers)
            output = s.get(payload,headers=headers).json()
        return output

def nse_marketStatus():
    payload = __nsefetch('https://nseindia.com/api/marketStatus')
    #print(payload)
    return payload['marketState'][0]['marketStatus']

def get_stock_ltp(symbol):
    try:
     priceInfoAttr = 'lastPrice'
     market_stataus = nse_marketStatus()
     if market_stataus == 'Closed':
        priceInfoAttr = 'close'

     symbol = __nsesymbolpurify(symbol)
     payload = __nsefetch('https://www.nseindia.com/api/quote-equity?symbol='+symbol)
     #print(payload)
     ltp = payload['priceInfo'][priceInfoAttr]
    except Exception as ex:
        raise APIError(statusCode = 400, message = 'Exception while fetching ltp' )
    return ltp

def stockLTPJob(stockCodes):
    stockLTP = {}
    for symbol in stockCodes:
        ltp = get_stock_ltp(symbol)
        stockLTP[symbol] = ltp
    return stockLTP

def get_all_stock_ltp(symbolList):
    stockCodesSublist = [symbolList[i:i+1] for i in range(0,len(symbolList),1)]
    stockLTPDict = {}

    s1 = time.time()

    with concurrent.futures.ThreadPoolExecutor() as executor:
     futures = []
     for stockCodes in stockCodesSublist:
        futures.append(executor.submit(stockLTPJob, stockCodes))

     for future in concurrent.futures.as_completed(futures):
        result = future.result()
        for key in result:
            stockLTPDict[key] = result[key]


    s2 = time.time()
    print("time taken to fetch all LTPs in sec  =",round((s2-s1),2))
    return stockLTPDict

def get_stock_depth(stockLTPdict):
    dates = getDateRange(6)
    stockDepthdict = {}

    s1 = time.time()

    for key in stockLTPdict.keys():
        data = get_history(symbol=key,start=dates[1],end=dates[0])
        close_price_list = data['Close'].tolist()
        max_price_list= []
        maxima_indices = argrelmax(np.array(close_price_list))
        for idx in np.ravel(maxima_indices):
            max_price_list.append(close_price_list[idx])

        maxima_price = np.array(max_price_list).max()
        stock_ltp = stockLTPdict[key]
        depth = round(((maxima_price - stock_ltp)/maxima_price)*100,2)
        stockDepthdict[key] = (maxima_price,depth)

    s2 = time.time()
    print("time taken to calculate depth  in sec  =",round((s2-s1),2))
    return stockDepthdict

