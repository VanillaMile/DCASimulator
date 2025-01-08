from application import app, mongo, users_collection
from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from application.forms import *
from application.simulationValidation import simulationValidation
from application.simulation import simulation
from datetime import datetime


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Nazwa użytkownika i hasło są wymagane.')
            return redirect(url_for('register'))

        try:
            # Haszowanie hasła i zapis do bazy danych
            hashed_password = generate_password_hash(password)
            result = mongo.db.users.insert_one({
                'username': username,
                'password': hashed_password,
                'lastLogin': None
            })

            # Sprawdzenie, czy dane zostały dodane do bazy
            if result.inserted_id:
                print(f"Użytkownik {username} został zapisany w bazie danych.")
                flash('Rejestracja zakończona sukcesem! Możesz się zalogować.')
                return redirect(url_for('login'))  # Przekierowanie na stronę logowania
            else:
                flash('Wystąpił problem z zapisaniem danych. Spróbuj ponownie.')
                return redirect(url_for('register'))

        except Exception as e:
            # Obsługa błędu, jeśli nazwa użytkownika już istnieje
            if 'duplicate key error' in str(e):
                flash('Nazwa użytkownika jest już zajęta. Wybierz inną.')
            else:
                flash('Wystąpił błąd podczas rejestracji. Spróbuj ponownie.')
            # Logowanie błędów do terminala
            print(f"Błąd podczas rejestracji: {e}")
            return redirect(url_for('register'))

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:  # Jeśli użytkownik jest już zalogowany
        flash('Jesteś już zalogowany!')
        return redirect(url_for('index'))  # Przekierowanie na stronę główną

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Wyszukiwanie użytkownika w bazie danych
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            # Ustawienie ciasteczka sesji
            session['user_id'] = str(user['_id'])

            # Aktualizacja ostatniego logowania w bazie danych
            mongo.db.users.update_one(
                {'_id': user['_id']},
                {'$set': {'lastLogin': datetime.now()}}
            )

            flash('Zalogowano pomyślnie!')
            return redirect(url_for('index'))  # Przekierowanie na stronę główną
        else:
            flash('Niepoprawna nazwa użytkownika lub hasło.')

    return render_template('login.html')


# Wylogowanie użytkownika
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Usunięcie ciasteczka sesji
    flash('Wylogowano pomyślnie.')
    return redirect(url_for('login'))


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