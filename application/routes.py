from application import app, mongo
from flask import render_template, request
from application.forms import *
from application.simulationValidation import simulationValidation
from application.simulation import simulation

@app.route("/")
def index():
    chackCollectionsGames()
    return render_template("layout.html", title = "DCASimulator", stock_names = getStocks())

@app.route("/stock", methods=["POST"])
def stock():
    stock = request.form.get("stock")
    stockData = mongo.db.stocks.find_one({"stock_name": stock})
    if stockData is None:
        return render_template("stockNotFound.html", title = stock, stockData = None, stock = stock)
    return render_template("stock.html", title = stock, stock_data = stockData)

@app.route("/simulationForm")
def simulationForm():
    return render_template("simulationForm.html", title = "Simulation Form", stock_names = getStocks())

@app.route("/simulationResults", methods = ["POST"])
def simulationResults():
    simulationData = {
        "initial_investment": request.form.get("initial_investment"),
        "investment_amount": request.form.get("investment_amount"),
        "investment_interval": request.form.get("investment_interval"),
        "investment_period": request.form.get("investment_period"),
        "stock": request.form.get("stock"),
        "stock_data": mongo.db.stocks.find_one({"stock_name": request.form.get("stock")}),
    }

    # Validation
    returnStatus = simulationValidation(simulationData['initial_investment'], simulationData['investment_amount'], simulationData['investment_interval'], 
                                        simulationData['investment_period'], simulationData['stock_data'])
    if returnStatus != [None, None, None, None, None]:
        return render_template("simulationForm.html",   title = "Simulation Form", stock_names = getStocks(), return_status = returnStatus)
    
    # Simulation
    data = simulation(simulationData)
    return render_template("simulation.html",   title = "Simulation", investment_data = data)

@app.route("/submitRankingSubmit", methods = ["POST"])
def submitRankingSubmit():
    userName = request.form.get("username")
    stockName = request.form.get("stock_name")
    initialInvestment = request.form.get("initial_investment")
    investmentAmount = request.form.get("investment_amount")
    investmentInterval = request.form.get("investment_interval")
    investmentPeriod = request.form.get("investment_period")
    input = request.form.get("input")
    profit = request.form.get("profit")
    profitPercentage = request.form.get("profit_percent")
    insertRankingResult(userName, stockName, initialInvestment, investmentAmount, investmentInterval, investmentPeriod, profit, profitPercentage, input)
    rankingData = getSortedRankingData()
    return render_template("ranking.html", title = "Ranking", ranking_data = rankingData)

@app.route("/seeRanking")
def seeRanking():
    rankingData = getSortedRankingData()
    return render_template("ranking.html", title = "Ranking", ranking_data = rankingData)

@app.route("/playGame")
def playGame():
    return render_template("playGame.html", title = "Game", stock_names = getStocks())

@app.route("/selectToContinue", methods = ["POST"])
def selectToContinue():
    username = request.form.get("username")
    money = request.form.get("money")
    stock = request.form.get("stock")
    try:
        money = float(money)
    except:
        money = 404
    exists = mongo.db.games.find_one({"username": username})
    if exists is None:
        addUserGame(username, money, stock)
        data = getUserGame(username)
        daysToAppend = simulation(simulationData=data, game=True, buySell="hold")
        appendDaysToData(username, daysToAppend)
        return render_template("game.html", title = "Game", data = getUserGameLimited(username))
    else:
        prevData = mongo.db.games.find_one({"username": username})
        return render_template("selectToContinue.html", title = "Select to continue", username = username, money = money, stock = stock, prevData = prevData)

@app.route("/dataCleared", methods = ["POST"])
def dataCleared():
    clearData = request.form.get("clearData")
    cleared = "0"
    if clearData == "True":
        clearUserGame(request.form.get("username"))
        username = request.form.get("username")
        stock = request.form.get("stock")
        money = request.form.get("money")
        try:
            money = float(money)
        except:
            money = 404
        setUserGame(username, money, stock)
        cleared = "1"
    getData = getUserGame(request.form.get("username"))
    return render_template("dataCleared.html", title = "Game", data = getData, cleared = cleared)


@app.route("/game", methods = ["POST"])
def game():
    username = request.form.get("username")
    buySell = request.form.get("buySell")
    try:
        amount = float(request.form.get("amount"))
    except:
        amount = 0
    data = getUserGame(username)
    daysToAppend = simulation(simulationData=data, game=True, buySell=buySell, amount=amount)
    appendDaysToData(username, daysToAppend)
    return render_template("game.html", title = "Game", data = getUserGameLimited(username))