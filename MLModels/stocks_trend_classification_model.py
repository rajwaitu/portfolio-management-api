from nsepy import get_history
from datetime import date
import os
from csv import writer
import pandas as pd

from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

from utils.datetimeUtil import getDate
from exception.apiError import APIError

def preprocess_stock_trend_data():
    print("preprocessing of stock trend label data started")
    all_stocks = []

    with open('stock_trends_label_data.csv') as stock_trends_file:
        for line in stock_trends_file:
            try:
                stock_dict = {idx:d for idx,d in enumerate(line.split(sep=','))}
                stockTrends = StockTrendsLabel(stock_dict[0],getDate(stock_dict[1]),getDate(stock_dict[2]),int(stock_dict[3].replace('\n', '')))
                all_stocks.append(stockTrends)
            except Exception :
                stock_trends_file.close()
                raise APIError(statusCode = 400, message = 'error occured while processing stocks data')
        stock_trends_file.close()

    if os.path.exists("stock_trends_training.csv"):
        os.remove("stock_trends_training.csv")

    # add header in csv file
    data = get_history(symbol=all_stocks[0].scrip,start=all_stocks[0].start_date,end=all_stocks[0].end_date)
    close_price_list = data['Close'].tolist()
    features = ['C'+str(idx + 1) for idx,d in enumerate(close_price_list)]
    header = []
    header.append('scrip')
    header.extend(features)
    header.append('label')
    with open('stock_trends_training.csv', mode='a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(header)
            f_object.close()

    # add rows in csv file
    for stock in all_stocks:
        row = []
        row.append(stock.scrip)

        data = get_history(symbol=stock.scrip,start=stock.start_date,end=stock.end_date)
        close_prices = data['Close'].tolist()
        row.extend(close_prices)
        row.append(stock.label)
        
        with open('stock_trends_training.csv', mode='a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(row)
            f_object.close()

    print("preprocessing of stock trend label data completed")

def train_stock_classification_model():
    df = pd.read_csv('stock_trends_training.csv')
    features = df.loc[:, "C1":"C386"]
    labels = df.loc[:, ["label"]]

    pipelines = []
    for model in [LogisticRegression(), DecisionTreeClassifier(), SVC()]:
        pipeline = make_pipeline(model)
        pipelines.append(pipeline)
    
    trainX,testX,trainY,testY = train_test_split(features, labels)
    for pipeline in pipelines:
        pipeline.fit(trainX, trainY)

def predict_stock_classification():
    pass

class StockTrendsLabel:
  def __init__(self, scrip, start_date,end_date,label):
    self.scrip = scrip
    self.start_date = start_date
    self.end_date = end_date
    self.label = label