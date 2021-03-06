# holdingService.py
import traceback
import requests
import time
import config.data_lake as datalakeAPI
from exception.apiError import APIError
from utils.portfolioUtil import getPortfolioHoldingResponse
from utils.stockUtil import get_all_stock_ltp

def getHolding(email,portfolioId):
    try:
      get_holding_url = datalakeAPI.GET_HOLDING_API.format(email,portfolioId)
      
      s1 = time.time()
      holdingList = requests.get(get_holding_url).json()['holdingList']
      s2 = time.time()
      print("time taken to fetch holdingList in sec  =",round((s2-s1),2))

      return getPortfolioHoldingResponse(holdingList)
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating holding view' )

def createHolding(email,portfolioId,holdingListObj):
    try:
      updatedHoldingList = []
      stockCodes = []

      for holding in holdingListObj.holdingList:
        stockCodes.append(holding['scrip'])
      
      stockLTPdict = get_all_stock_ltp(stockCodes)

      for x in holdingListObj.holdingList:
        x['ltp'] = stockLTPdict[x['scrip']]
        updatedHoldingList.append(x)

      create_holding_url = datalakeAPI.CREATE_HOLDING_API.format(email,portfolioId)
      return requests.post(create_holding_url, json={"holdingList": updatedHoldingList}).json()
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating holding' )

def updateHolding(email,portfolioId,holdingListObj):
    try:
      updatedHoldingList = []
      get_holding_url = datalakeAPI.GET_HOLDING_API.format(email,portfolioId)
      holdingList = requests.get(get_holding_url).json()['holdingList']

      # if id is not in holdingPayload then get id from holdingList
      for holdingPayload in holdingListObj.holdingList:
        if "id" not in holdingPayload:
          scrip = holdingPayload['scrip']
          for x in holdingList:
            if x['stockCode'] == scrip:
              holdingPayload['id'] = x['id']
              updatedHoldingList.append(holdingPayload)
              break
        else:
          updatedHoldingList.append(holdingPayload)

      create_holding_url = datalakeAPI.CREATE_HOLDING_API.format(email,portfolioId)
      return requests.put(create_holding_url, json={"holdingList": updatedHoldingList}).json()

    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while updating holding ' )

def deleteHolding(email,portfolioId,scripObj):
  try:
      delete_holding_url = datalakeAPI.CREATE_HOLDING_API.format(email,portfolioId)
      return requests.delete(delete_holding_url, json={"scrip": scripObj.scrip}).json()
        
  except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while deleting user holdings' )

def getUserPortfolio(email):
    try:
      get_portfolio_url = datalakeAPI.GET_USER_PORTFOLIO_API.format(email)
      user_portfolio = requests.get(get_portfolio_url).json()
      return user_portfolio
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while fetching user portfolio' )
