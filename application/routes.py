from application import app, mongo
from flask import render_template, request
from application.forms import *
from application.simulationValidation import simulationValidation
from application.simulation import simulation

@app.route("/")
def index():
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