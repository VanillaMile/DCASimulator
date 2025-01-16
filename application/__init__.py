from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/dcaDatabase"
app.secret_key = 'super_secret_key'
mongo = PyMongo(app)
client = mongo.db
stocks = client.stocks
db = client['dcaDatabase']
users_collection =['users']
mongo.db.users.create_index('username', unique=True)

try:
    mongo.db.users.find_one()
    print("Połączenie z MongoDB zostało nawiązane.")
except Exception as e:
    print(f"Błąd połączenia z MongoDB: {e}")

from application import routes