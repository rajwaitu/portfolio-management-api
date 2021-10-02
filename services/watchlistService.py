# watchlistService.py
import traceback
import requests
import config.data_lake as datalakeAPI
from exception.apiError import APIError

def getUserWatchList(email):
    try:
      get_watchlist_url = datalakeAPI.GET_WATCHLSIT_API.format(email)
      user_watchlist = requests.get(get_watchlist_url).json()['watchlist']
      watchlist,response = [],{}

      for w in user_watchlist:
          watchlist_dist = {}
          watchlist_dist['companyCode'] = w['companyCode']
          watchlist_dist['price'] = str(w['watchlistPrice'])
          watchlist_dist['created'] = str(w['created'])
          watchlist.append(watchlist_dist)

      response['watchlist'] = watchlist
      return response
      
    except Exception:
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while loading watchlist' )