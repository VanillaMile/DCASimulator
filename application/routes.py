from application import app, mongo
from flask import render_template, request
from application.forms import *
from application.simulationValidation import simulationValidation
from application.simulation import simulation
import json

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
        "predict_days": request.form.get("predict_days")
    }

    returnStatus = simulationValidation(simulationData['initial_investment'], simulationData['investment_amount'], simulationData['investment_interval'], 
                                        simulationData['investment_period'], simulationData['stock_data'])

    if returnStatus != [None, None, None, None, None]:
        return render_template("simulationForm.html",   title = "Simulation Form", stock_names = getStocks(), return_status = returnStatus)
    
    data = simulation(simulationData)
    return render_template("simulation.html",   title = "Simulation", investment_data = data, json_data = json.dumps(data))