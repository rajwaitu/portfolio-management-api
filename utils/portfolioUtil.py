import traceback
import locale

import config.app_env as env
from .stockUtil import get_all_stock_ltp

def getPortfolioHoldingResponse(holdingList):
    total_investment = 0
    total_holding = 0
    holdingviewList = []
    stockCodes = []

    for x in holdingList:
        stockCodes.append(x['stockCode'])

    if(env.real_time_ltp == True):
        stockLTPdict = get_all_stock_ltp(stockCodes)

    for holding in sorted(holdingList,key=lambda x: x['stockCode']):
        try:
         holding_qty = holding['holdingQuantity']

         if(env.real_time_ltp == True):
            stock_ltp = stockLTPdict[holding['stockCode']]
         else:
             stock_ltp = holding['ltp']

         holdingValue = holding_qty * float(stock_ltp)
         investment = holding_qty * holding['avaragePrice']
         profitLoss = holdingValue - investment
         netChange = (profitLoss/investment) * 100

         total_investment = total_investment + investment
         total_holding = total_holding + holdingValue

         locale.setlocale(locale.LC_MONETARY, 'en_IN')

         holdingview = {}
         holdingview['id'] = holding['stockCode']
         holdingview['company'] = holding['company']
         holdingview['qunatity'] = str(holding_qty)
         holdingview['avaragePrice'] = str(holding['avaragePrice'])
         holdingview['lastTradedPrice'] = str(stock_ltp)
         holdingview['investment'] = locale.currency(round(investment,2), grouping=True)
         holdingview['investmentasnumber'] = round(investment,2)
         holdingview['currentValue'] = locale.currency(round(holdingValue,2), grouping=True)
         holdingview['profitLoss'] = locale.currency(round(profitLoss,2), grouping=True)
         holdingview['netChange'] = str(round(netChange,2)) + "%"
         holdingview['maxima'] = str(holding['maxima'])
         holdingview['depth'] = str(holding['depth']) + "%"

         if profitLoss < 0 :
             holdingview['profitLoss'] = '-' + locale.currency(abs(round(profitLoss,2)),grouping=True)

         holdingviewList.append(holdingview)
         
        except Exception :
            #print(Exception)
            print(traceback.format_exc())
            return {'error' : 'error occured while getting stock quote from nse'}

    net_profit = total_holding - total_investment
    percentageNetProfit = round((net_profit/total_investment)*100, 2)

    getPortfolioHoldingResponse = {}
    getPortfolioHoldingResponse['holdings'] = holdingviewList
    getPortfolioHoldingResponse['totalInvestment'] = str(round(total_investment,2))
    getPortfolioHoldingResponse['currentValue'] = str(round(total_holding,2))
    getPortfolioHoldingResponse['totalProfitLoss'] = str(round(net_profit,2))
    getPortfolioHoldingResponse['percentageProfitLoss'] = str(percentageNetProfit)

    return getPortfolioHoldingResponse

