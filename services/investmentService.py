# investmentService.py
import traceback
import requests
import config.data_lake as datalakeAPI
from utils.stockUtil import get_all_stock_ltp
from exception.apiError import APIError

def getInvestment(email,portfolioId):
    
    try:
      get_investment_url = datalakeAPI.GET_INVESTMENT_API.format(email,portfolioId)
      investmentList = requests.get(get_investment_url).json()['investmentList']
      dates,investments,holdings,profits,getInvestmentResponse = [],[],[],[],{}

      for inv in investmentList:
          dates.append(str(inv['holdingDate']))
          investments.append(inv['investmentAmount'])
          holdings.append(inv['holdingValue'])
          profits.append(inv['profitLoss'])

      getInvestmentResponse['dates'] = dates
      getInvestmentResponse['investments'] = investments
      getInvestmentResponse['holdings'] = holdings
      getInvestmentResponse['profits'] = profits
      
      return getInvestmentResponse
    except Exception:
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while loading investments' )

# this can be a job

def createInvestment(email,portfolioId): 
    try:
      get_holding_url = datalakeAPI.GET_HOLDING_API.format(email,portfolioId)
      create_investment_url = datalakeAPI.CREATE_INVESTMENT_API.format(email,portfolioId)

      holdingList = requests.get(get_holding_url).json()['holdingList']

      stockCodes = [ holding['stockCode'] for holding in holdingList]
      stockLTPdict = get_all_stock_ltp(stockCodes)

      r = requests.post(create_investment_url, json={"stockLTPs": stockLTPdict})
      status = r.status_code
      if status == 200:
        return {'msg' : 'user investment created successfully!'}
      else:
        raise APIError(statusCode = 400, message = 'error occured while creating user investment' )

    except Exception:
      print(traceback.format_exc())
      raise APIError(statusCode = 400, message = 'error occured while creating user investment' )
