import random

def simulation(simulationData, game = False, buySell = False, amount = 0):
    if game:
        return __predictDynamicDays(buySell, simulationData, amount)
    return __predictDays(simulationData)

from application import app, mongo
def __getLastPrice(stock_name):
    stock_data = mongo.db.stocks.find_one({"stock_name": stock_name})
    return stock_data['daily_data'][len(stock_data['daily_data']) - 1]['close_price']

def __getDailyData(stock_name):
    stock_data = mongo.db.stocks.find_one({"stock_name": stock_name})
    return stock_data['daily_data']

from application.forms import *
def __performBuy(username, amount):
    data = getUserGame(username)
    stocks = data['stocks']
    stock_price = data['stock_price']

    stocks = stocks + amount / stock_price
    money = data['money'] - amount
    mongo.db.games.update_one({"username": username},
                                {"$set": {
                                    "stocks": stocks,
                                    "money": money
                                }})
    
def __performSell(username, amount):
    data = getUserGame(username)
    stocks = data['stocks']
    stock_price = data['stock_price']

    stocks = stocks - amount / stock_price
    money = data['money'] + amount
    mongo.db.games.update_one({"username": username},
                                {"$set": {
                                    "stocks": stocks,
                                    "money": money
                                }})
    


def __predictDays(simulationData):
    initialInvestment = float(simulationData['initial_investment'])
    investmentAmount = float(simulationData['investment_amount'])
    investmentInterval = int(simulationData['investment_interval'])
    investmentPeriod = int(simulationData['investment_period'])
    stockData = simulationData['stock_data']

    data = {
        "stock": simulationData['stock'],
        "initial_investment": initialInvestment,
        "investment_amount": investmentAmount,
        "investment_interval": investmentInterval,
        "investment_period": investmentPeriod,
        "input": initialInvestment,
        "days": []
    }

    day = {
        "day": 0,
        "value": initialInvestment,
        "shares": initialInvestment / stockData['daily_data'][len(stockData['daily_data']) - 1]['close_price'],
        "stock_price": stockData['daily_data'][len(stockData['daily_data']) - 1]['close_price'],
        "change": 0,
        "action": "Initial Investment"
    }

    data['days'].append(day)

    investDays = investmentInterval
    daysOfWeek = 1
    for i in range(1, investmentPeriod + 1):
        if daysOfWeek == 6 or daysOfWeek == 7:
            day = {
                "day": i,
                "value": data['days'][i - 1]['value'],
                "shares": data['days'][i - 1]['shares'],
                "stock_price": data['days'][i - 1]['stock_price'],
                "change": 1,
                "action": "Market Closed"
            }
            data['days'].append(day)
        if daysOfWeek == 6:
            daysOfWeek += 1
            investDays -= 1
            continue
        if daysOfWeek == 7:
            daysOfWeek = 1
            investDays -= 1
            continue
        randomIndex = random.randint(0, len(stockData['daily_data']) - 1)
        record = stockData['daily_data'][randomIndex]

        newPrice = data['days'][i - 1]['stock_price'] * record['change']

        if investDays < 0:
            investDays = investDays + investmentInterval
            day = {
                "day": i,
                "value": (data['days'][i - 1]['shares'] + investmentAmount / newPrice) * newPrice,
                "shares": data['days'][i - 1]['shares'] + investmentAmount / newPrice,
                "stock_price": newPrice,
                "change": record['change'],
                "action": "Buy"
            }
            data['input'] += investmentAmount
        else:
            day = {
                "day": i,
                "value": newPrice * data['days'][i - 1]['shares'],
                "shares": data['days'][i - 1]['shares'],
                "stock_price": newPrice,
                "change": record['change'],
                "action": "No Action"
            }
        data['days'].append(day)
        daysOfWeek += 1
        investDays -= 1
    return data

def __predictDynamicDays(buySell, data, amount = 0):
    # data = {
    #     "money": float,
    #     "stock": string,
    #     "stocks": float, // number of stocks owened
    #     "stock_price": float, 
    #     "days_data": [[
    #         "Day", "Price", "Buy", "Sell"
    #     ]]
    # }
    if data['stock_price'] == -1:
        data['stock_price'] = __getLastPrice(data['stock_name'])

    if not data['days_data']:
        lastDayNumber = 0
    else:
        lastDayNumber = data['days_data'][len(data["days_data"]) - 1]['day']
    dailyData = __getDailyData(data['stock_name'])
    days = []
    # dafault time period is 10 days
    randomIndex = random.randint(0, len(dailyData)  - 1)
    newPrice = data['stock_price'] * dailyData[randomIndex]['change']
    newPrice = round(newPrice, 2)
    day = {
        "day": 1 + lastDayNumber,
        "price": newPrice,
        "buy": "No Action",
        "sell": "No Action"
    }
    if amount != 0:
        if buySell == "buy":
            if amount <= data['money']:
                day['buy'] = "Buy"
                day['sell'] = "No Action"
                __performBuy(data['username'], amount)
            else:
                day['buy'] = "Buy not possible"
                day['sell'] = "No Action"
        elif buySell == "sell":
            if amount <= data['stocks'] * data['stock_price']:
                day['buy'] = "No Action"
                day['sell'] = "Sell"
                __performSell(data['username'], amount)
            else:
                day['buy'] = "No Action"
                day['sell'] = "Sell not possible"
    days.append(day)
    for i in range(2, 11):
        randomIndex = random.randint(0, len(dailyData) - 1)
        newPrice = days[len(days) - 1]['price'] * dailyData[randomIndex]['change']
        newPrice = round(newPrice, 2)
        day = {
            "day": i + lastDayNumber,
            "price": newPrice,
            "buy": "No Action",
            "sell": "No Action"
        }
        days.append(day)
    return days