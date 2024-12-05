from application import app
from flask import render_template
from application import *

@app.route("/")
def index():
    return render_template("layout.html", title = "DCASimulator")

@app.route("/stocks")
def stocks():
    return render_template("stocks.html", title = "Stocks")