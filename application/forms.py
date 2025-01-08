from application import app, mongo

def getStocks():
    stocks = mongo.db.stocks.find()
    stocksNames = []
    for stock in stocks:
        stocksNames.append(stock["stock_name"])
    return stocksNames

def insertRankingResult(userName, stockName, initialInvestment, investmentAmount, investmentInterval, investmentPeriod, profit, profitPercentage, input):
    if mongo.db.rankings.find_one({"username": userName}) is None:
        mongo.db.rankings.insert_one({
            "username": userName,
            "stock_name": stockName,
            "initial_investment": float(initialInvestment),
            "investment_amount": float(investmentAmount),
            "investment_interval": float(investmentInterval),
            "investment_period": float(investmentPeriod),
            "profit": float(profit),
            "profit_percentage": float(profitPercentage),
            "input": float(input)})
    else:
        mongo.db.rankings.update_one({"user_name": userName}, 
                         {"$set": {
                        "stockname": stockName,
                        "initial_investment": float(initialInvestment),
                        "investment_amount": float(investmentAmount), 
                        "investment_interval": float(investmentInterval),
                        "investment_period": float(investmentPeriod),
                        "profit": float(profit),
                        "profit_percentage": float(profitPercentage),
                        "input": float(input)}})

def getSortedRankingData():
    pipeline = [
        {
            "$group": {
                "_id": "$username",
                "profit": {"$sum": "$profit"},
                "percentage_grow": {"$avg": "$profit_percentage"},
                "period": {"$avg": "$investment_period"},
                "stock_name": {"$first": "$stock_name"},
                "investment_amount": {"$first": "$investment_amount"},
                "initial_investment": {"$first": "$initial_investment"},
                "investment_interval": {"$first": "$investment_interval"},
                "input": {"$first": "$input"}
            }
        },
        {
            "$addFields": {
                "score": {
                    "$cond": {
                        "if": {"$eq": ["$period", 0]},
                        "then": 0,
                        "else": {"$divide": ["$percentage_grow", "$period"]}
                    }
                }
            }
        },
        {
            "$sort": {"score": -1}
        },
        {
            "$limit": 10
        }
    ]
    results = list(mongo.db.rankings.aggregate(pipeline))

    # print(results)
    # for row in results:
    #     print(f"Username: {row['_id']}")
    #     print(f"Profit: {row['profit']}")
    #     print(f"Percentage Grow: {row['percentage_grow']}")
    #     print(f"Period: {row['period']}")
    #     print(f"Score: {row['score']}")
    return results
