from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dcaDatabase"

mongo = PyMongo(app)
client = mongo.db
stocks = client.stocks

from application import routes
