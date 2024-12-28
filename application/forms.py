from application import app, mongo

def getStocks():
    stocks = mongo.db.stocks.find()
    stocksNames = []
    for stock in stocks:
        stocksNames.append(stock["stock_name"])
    return stocksNames