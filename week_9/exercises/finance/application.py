import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, repeated_username, registered_username, login_required, shares_success, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user_data = db.execute("SELECT username, cash FROM users WHERE id = (?);", user_id)
    username = user_data[0]["username"]
    cash = user_data[0]["cash"]
    stocks = db.execute("SELECT stock_id, shares FROM user_stocks WHERE username_id = (?) ORDER BY stock_id;", user_id)
    stocks_information = []
    stocks_total = 0
    # The user has stocks
    for stock in stocks:
        stock_data = lookup(stock["stock_id"])
        if stock_data:
            stocks_information.append({
                "symbol": stock["stock_id"],
                "name" : stock_data["name"],
                "price": stock_data["price"],
                "quantity": stock["shares"]
            })
            stocks_total += stock_data["price"] + stock["shares"]
    return render_template("index.html", username=username, stocks=stocks_information, stock_total_value=stocks_total, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        user_data = db.execute("SELECT username, cash FROM users WHERE id = (?)", session["user_id"])
        username = user_data[0]["username"]
        cash = user_data[0]["cash"]
        return render_template("buy.html", username=username, cash=cash)
    if request.method == "POST":
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = (?)", user_id)[0]["cash"]

        # User form input
        stock_id = request.form.get("stock_id")
        shares = request.form.get("shares")

        # Look up the information about the symbol 
        symbol_data = lookup(stock_id)
        
        # Ensures that the symbol belongs to a stock
        if not symbol_data:
            return apology("Enter a valid stock symbol", 503)

        if not shares.isnumeric():
            return apology("Enter a valid number of shares", 503)

        # Ensures that the user don't buy more than 100 shares
        if int(shares) > 100:
            return apology("The max shares that you can purchase are 100", 503)

        price = float(symbol_data["price"])

        # Substracts the current total share price from the current cash
        cash -= float(price * int(shares))

        # Ensures that the user has enogh money to buy the shares
        if (cash < 0):
            return apology("You do not have enough money to buy these shares", 503)

        # Checks if it is the user already owned shares of this stock
        has_shares = db.execute("SELECT id, shares FROM user_stocks WHERE username_id = (?) AND stock_id = (?)", user_id, stock_id)

        # Keeps track of the id from the user_stocks table that contains the user-stock relation in the DB
        transaction_id = None


        if has_shares:
            transaction_id = has_shares[0]["id"]
            # Adds the bought shares
            new_shares = has_shares[0]["shares"] + int(shares)
            # Update the total shares owned
            db.execute("UPDATE user_stocks SET shares = (?) WHERE username_id = (?) AND stock_id = (?);", new_shares, user_id, stock_id)
        else:
            # Create a new row in the DB to keep track of the user-stock relation
            transaction_id = db.execute("INSERT INTO user_stocks (username_id, stock_id, shares) VALUES(?,?,?)", user_id, stock_id, shares)

        # Adds the new transaction in the user history
        db.execute("INSERT INTO user_history (user_stocks_id, shares, price, transaction_type) VALUES (?,?,?,?)", transaction_id, shares, price, "buy")
        # Update the current cash after the purchase
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)", cash, user_id)

        return shares_success("Congrats!", f"You have owned {symbol_data['name']} shares successfully")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = (?)", user_id)[0]["username"]
    history = db.execute("SELECT stocks.stock_id AS stock_id, history.shares AS shares, history.price AS price, history.date AS date, history.transaction_type AS type FROM user_stocks as stocks INNER JOIN user_history AS history ON stocks.id = history.user_stocks_id WHERE stocks.username_id = (?) ORDER BY history.date, stocks.stock_id", user_id)
    return render_template("history.html", history=history, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        user_id = rows[0]["id"]

        # Remember which user has logged in
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = (?)", session["user_id"])[0]["username"]
        return render_template("quote.html", username=username)
    elif request.method == "POST":
        print(request.get_json(force=True))
        symbol = request.get_json(force=True)["symbol"]
        symbol_data = lookup(symbol)
        return jsonify(symbol_data)
    return apology("Something went wrong")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation_password = request.form.get("confirmation")
        if username and password:
            '''
            Source: https://mkyong.com/regular-expressions/how-to-validate-username-with-regular-expression/
            Username requirements:
                - Username first character must be a letter [a-z]
                - Username consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
                - Username allowed of the dot (.), underscore (_), and hyphen (-).
                - The dot (.), underscore (_), or hyphen (-) must not be the first or last character.
                - The dot (.), underscore (_), or hyphen (-) does not appear consecutively, e.g., user..name
                - The number of characters must be between 5 to 20.
            '''
            username_regex = "^[a-z]([._-](?![._-])|[a-z0-9]){3,18}[a-z0-9]$"

            '''
            Password requirements:
                - Password consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
                - The number of characters must be between 8 to 10.
            '''
            password_regex = "^[a-z0-9]{8,10}$"

            if re.fullmatch(username_regex,  username, flags=re.IGNORECASE) and re.fullmatch(password_regex, password, flags=re.IGNORECASE):
                if password == confirmation_password:
                    # Get the a username with the given username if it exists
                    username_row = db.execute("SELECT username FROM users where username = ?", username)
                    if len(username_row) == 0:
                        password = generate_password_hash(password)
                        db.execute("INSERT INTO users(username, hash) VALUES (?,?)", username, password)
                        return registered_username("Using C$50 Finance", "stonks")
                    else:
                        # Tell the user that the given user already exists
                        return repeated_username("You", "Someone else using the same username")
                else:
                    return apology("must match password and confirmation password", 403)
            else:
                return apology("must provide a valid username and a valid password", 403)
        else:
            return apology("must provide username and password", 403)
    return apology("Something went wrong", 500)

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
