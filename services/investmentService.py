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
'''
def createInvestment(email,portfolioId):
    
    try:
      user = db.getUserByEmail(email)
      if user == None:
          #raise APIError(400,'No user registered with given email')
          return {'error' : "No user registered with given email"}

      user_portfolio = db.getUserPortfolioById(int(portfolioId))
      if user_portfolio == None:
          #raise APIError(400,'No user portfolio found with given portfolio')
          return {'error' : "No user portfolio found with given portfolio"}
      
      holdingList = db.getHoldingByUserAndUserPortfolio(user.subscription_id,user_portfolio.id)

      totalInvestment,totalHoldings,netProfit = 0,0,0
      stockCodes = [ holding.stockCode for holding in holdingList]
      stockLTPdict = get_all_stock_ltp(stockCodes)

      for holding in holdingList:
          totalQTY = holding.holdingQuantity
          totalInvestment = totalInvestment + int(totalQTY * holding.avaragePrice)
          totalHoldings = totalHoldings + int(totalQTY * float(stockLTPdict[holding.stockCode]))

      netProfit = totalHoldings - totalInvestment

      print('totalInvestment : ' + str(totalInvestment))
      print('totalHoldings : ' + str(totalHoldings))
      print('netProfit : ' + str(netProfit))
     
    except Exception:
      print(traceback.format_exc())
      #raise APIError(400)
      return {'error' : "Exception occred while processing the request"}
'''
