from application import app, mongo

def chackCollectionsGames():
    collections = mongo.db.list_collection_names()
    if "games" not in collections:
        mongo.db.create_collection("games")

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

def addUserGame(username, money, stock):
    mongo.db.games.insert_one({
            "username": username,
            "stock_name": stock,
            "money": money,
            "stocks": 0,
            "stock_price": -1,
            "days_data": []
            })

def clearUserGame(username):
    mongo.db.games.update_one({"username": username}, 
                         {"$set": {
                        "money": 0,
                        "stocks": 0,
                        "stock_price": -1,
                        "days_data": []
                        }})
    
def getUserGame(username):
    return mongo.db.games.find_one({"username": username})

def getUserGameLimited(username):
    pipeline = [
        {
            "$match": {
                "username": username
            }
        },
        {
            "$project": {
                "username": 1,
                "stock_name": 1,
                "money": 1,
                "stocks": 1,
                "stock_price": 1,
                "days_data": 1
            }
        },
        {
            "$unwind": "$days_data"
        },
        {
            "$sort": {"days_data.day": -1}
        },
        {
            "$limit": 200
        }
    ]
    results = list(mongo.db.games.aggregate(pipeline))
    data = {
            "username": results[0]["username"],
            "stock_name": results[0]["stock_name"],
            "money": results[0]["money"],
            "stocks": results[0]["stocks"],
            "stock_price": results[0]["stock_price"],
            "days_data": []
        }

    for row in reversed(results):
        data["days_data"].append(row["days_data"])
    return data

def setUserGame(username, money, stock):
    mongo.db.games.update_one({"username": username}, 
                         {"$set": {
                        "stock_name": stock,
                        "money": money,
                        "stocks": 0,
                        "stock_price": -1,
                        "days_data": []
                        }})
    
def appendDaysToData(username, days):
    for day in days:
        mongo.db.games.update_one({"username": username}, 
                         {"$push": {
                        "days_data": day
                        }})
    mongo.db.games.update_one({"username": username}, 
                         {"$set": {
                        "stock_price": days[len(days) - 1]['price']
                        }})