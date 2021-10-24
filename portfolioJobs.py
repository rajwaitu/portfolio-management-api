import requests
import time

import config.data_lake as datalakeAPI
from utils.stockUtil import get_all_stock_ltp,get_stock_depth
from services.investmentService import createInvestment

#this can be read from db instead
email = 'rajwaitu@gmail.com'
portfolio_ids = [1,2,3,4]

def createInvestment():
    for portfolio in portfolio_ids:
        print('investment creation for portfolio id: ' + str(portfolio) + ' started...')
        createInvestment(email,portfolio)
        print('investment creation for portfolio id: ' + str(portfolio) + ' completed...')



def calculate_holding_ltp_maxima_depth():
    get_user_portfolio_url = datalakeAPI.GET_USER_PORTFOLIO_API.format(email)
    equityPortfolioList = requests.get(get_user_portfolio_url).json()['Equity']

    try:
        s1 = time.time()
        
        for portfolioDict in equityPortfolioList:
            portfolio_id = portfolioDict['id']
            print('processing portfolio with id ' + str(portfolio_id) + ' is started...')

            get_user_holding_url = datalakeAPI.GET_HOLDING_API.format(email,portfolio_id)
            holdingList = requests.get(get_user_holding_url).json()['holdingList']
            updatedHoldingList = []
            stockCodes = []

            for x in holdingList:
                stockCodes.append(x['stockCode'])

            stockLTPdict = get_all_stock_ltp(stockCodes)
            stockDepthdict = get_stock_depth(stockLTPdict)

            for x in holdingList:
                x['ltp'] = stockLTPdict[x['stockCode']]
                x['maxima'] = stockDepthdict[x['stockCode']][0]
                x['depth'] = stockDepthdict[x['stockCode']][1]
                updatedHoldingList.append(x)

            create_holding_url = datalakeAPI.CREATE_HOLDING_API.format(email,portfolio_id)
            print('calling update holding api')
            requests.post(create_holding_url, json={"holdingList": updatedHoldingList})
            print('processing portfolio with id ' + str(portfolio_id) + ' is completed!!')

        s2 = time.time()
    except Exception:
        print('error occured while updating user holdings')
        

if __name__ == "__main__":
    createInvestment()
    calculate_holding_ltp_maxima_depth()