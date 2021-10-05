# holdingService.py
import traceback
import requests
import config.data_lake as datalakeAPI
from exception.apiError import APIError
from utils.portfolioUtil import getPortfolioHoldingResponse

def getHolding(email,portfolioId):
    try:
      get_holding_url = datalakeAPI.GET_HOLDING_API.format(email,portfolioId)
      holdingList = requests.get(get_holding_url).json()['holdingList']
      return getPortfolioHoldingResponse(holdingList)
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating holding view' )

def getUserPortfolio(email):
    try:
      get_portfolio_url = datalakeAPI.GET_USER_PORTFOLIO_API.format(email)
      user_portfolio = requests.get(get_portfolio_url).json()
      return user_portfolio
    except Exception :
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while fetching user portfolio' )
