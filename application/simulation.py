import random

def simulation(simulationData):
    return __predictDays(simulationData)

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
    

        