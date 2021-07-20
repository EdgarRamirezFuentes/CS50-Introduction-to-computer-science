import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, repeated_username, registered_username, login_required, lookup, usd, success

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
    # Get the owned shares
    stocks = db.execute("SELECT stock_id AS symbol, shares AS quantity FROM user_stocks WHERE username_id = (?) AND quantity > 0 ORDER BY symbol;", user_id)
    # Keep track of the stocks' total value
    stocks_total = 0

    # Add the needed information of each owned shares
    for stock in stocks:
        # Get the needed information from IEX
        stock_data = lookup(stock["symbol"])
        if stock_data:
            stock["price"] = stock_data["price"]
            stock["name"] = stock_data["name"]
            stocks_total += stock_data["price"] * stock["quantity"]
    return render_template("index.html", username=username, stocks=stocks, stock_total_value=stocks_total, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    username = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
    cash = db.execute("SELECT cash FROM users WHERE id = (?);", session["user_id"])[0]["cash"]

    if request.method == "GET":
        return render_template("buy.html", username=username, cash=cash)
    if request.method == "POST":

        user_id = session["user_id"]
        # Symbol
        stock_id = request.form.get("stock_id")
        shares = request.form.get("shares")

        # Get the needed information from IEX
        symbol_data = lookup(stock_id)

        # Ensure the user sent a valid symbol
        if not symbol_data:
            return apology("must provide a valid symbol", 400, username)
        # Ensure the submitted shares are valid
        if not shares.isnumeric():
            return apology("must provide a valid number of shares", 400, username)
        # Ensure the user is not trying to buy more than 100 shares
        shares = abs(int(shares))
        if shares > 100:
            return apology("The max shares that you can purchase are 100", 400, username)

        price = float(symbol_data["price"])

        # Substract the total value of the purchase from its current cash
        cash -= float(price * shares)

        # Ensure that the user has enough money to purchase the selected shares
        if (cash < 0):
            return apology("You do not have enough money to buy these shares", 400, username)

        # Check if it is the user already owned shares of this stock
        has_shares = db.execute("SELECT id, shares FROM user_stocks WHERE username_id = (?) AND stock_id = (?);", user_id, stock_id)

        transaction_id = None

        if has_shares:
            transaction_id = has_shares[0]["id"]
            new_shares = has_shares[0]["shares"] + int(shares)
            db.execute("UPDATE user_stocks SET shares = (?) WHERE username_id = (?) AND stock_id = (?);", new_shares, user_id, stock_id)
        else:
            # It is the first time that this user buys these shares
            transaction_id = db.execute("INSERT INTO user_stocks (username_id, stock_id, shares) VALUES(?,?,?);", user_id, stock_id, shares)

        # Adds the transaction to the user' history
        db.execute("INSERT INTO user_history (user_stocks_id, shares, price, transaction_type) VALUES (?,?,?,?);", transaction_id, shares, price, "buy")
        # Update they're current cash
        db.execute("UPDATE users SET cash = (?) WHERE id = (?);", cash, user_id)

        return success("Congrats!", f"You have owned {symbol_data['name']} shares successfully", username)




@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = (?);", user_id)[0]["username"]
    history = db.execute("SELECT history.id as id, stocks.stock_id AS stock_id, history.shares AS shares, history.price AS price, history.date AS date, history.transaction_type AS type FROM user_stocks as stocks INNER JOIN user_history AS history ON stocks.id = history.user_stocks_id WHERE stocks.username_id = (?) ORDER BY history.date DESC, stocks.stock_id;", user_id)
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
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?;", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 400)

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


@app.route("/quote")
@login_required
def quote():
    """Get stock quote."""
    username = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
    if request.method == "GET":
        return render_template("quote.html", username=username)
    return apology("Something went wrong", 500, username)


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
                    username_row = db.execute("SELECT username FROM users where username = ?;", username)
                    if len(username_row) == 0:
                        password = generate_password_hash(password)
                        db.execute("INSERT INTO users(username, hash) VALUES (?,?)", username, password)
                        return registered_username("Using C$50 Finance", "stonks")
                    else:
                        # Tell the user that the given user already exists
                        return repeated_username("You", "Someone else using the same username")
                else:
                    return apology("must match password and confirmation password", 400)
            else:
                return apology("must provide a valid username and a valid password", 400)
        else:
            return apology("must provide username and password", 400)
    return apology("Something went wrong", 500)


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    username = db.execute("SELECT username FROM users WHERE id = (?)", session["user_id"])[0]["username"]
    if request.method == "GET":
        stocks = db.execute("SELECT stock_id as symbol, shares FROM user_stocks WHERE username_id=(?) AND shares > 0 ORDER BY symbol;", session["user_id"])
        return render_template("sell.html", username=username, stocks=stocks)
    if request.method == "POST":
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = (?);", user_id)[0]["cash"]

        stock_id = request.form.get("symbol")
        shares = request.form.get("shares")

        symbol_data = lookup(stock_id)

        # Ensure the sumbitted symbol is valid
        if not symbol_data:
            return apology("must provide a valid stock symbol", 400, username)
        # Ensure that the sumbitted shares are valid
        if not shares.isnumeric():
            return apology("must provide a valid number of shares", 400, username)
        # Ensure the user is not trying to sell more than 100 shares
        shares = abs(int(shares))
        if shares > 100:
            return apology("The max shares that you can purchase are 100", 400, username)

        price = float(symbol_data["price"])
        cash += price * shares

        # Check if the user already owned shares of this stock
        shares_data = db.execute("SELECT id, shares FROM user_stocks WHERE username_id = (?) AND stock_id = (?) and shares > 0;", user_id, stock_id)
        transaction_id = None

        if shares_data:
            transaction_id = shares_data[0]["id"]
            # Update the new shares
            new_shares = shares_data[0]["shares"] - int(shares)
            if new_shares >= 0:
                db.execute("UPDATE user_stocks SET shares = (?) WHERE username_id = (?) AND stock_id = (?);", new_shares, user_id, stock_id)
            else:
                # The user does not have enough shares to sell
                return apology(f"You do not have enough {symbol_data['name']} shares to sell", 400, username)
        else:
            # The user has not owned any share from this symbol
            return apology(f"You have not owned {symbol_data['name']} shares", 400, username)

        # Add the transaction to the user' history
        db.execute("INSERT INTO user_history (user_stocks_id, shares, price, transaction_type) VALUES (?,?,?,?);", transaction_id, shares, price, "sell")
        # Update the current cash
        db.execute("UPDATE users SET cash = (?) WHERE id = (?);", cash, user_id)

        return success("Congrats!", f"You have sold {symbol_data['name']} shares successfully", username)


@app.route("/stock-info", methods=["GET", "POST"])
@login_required
def get_stock_info():
    username = db.execute("SELECT username FROM users WHERE id = (?)", session["user_id"])[0]["username"]
    if request.method == "GET":
        # Get the needed information about a symbol
        symbol = request.args.get("symbol")
        symbol_data = lookup(symbol)
        if symbol_data:
            shares = db.execute("SELECT shares FROM user_stocks WHERE username_id = (?) AND stock_id = (?);", session["user_id"], symbol)[0]["shares"]
            # Add the current shares that the user have
            symbol_data["shares"] = shares
            return jsonify(symbol_data)
        return None
    if request.method == "POST":
        # Return the needed information about a symbol
        symbol = request.get_json(force=True)["symbol"]
        symbol_data = lookup(symbol)
        return jsonify(symbol_data)
    return apology("Something went wrong", 500, username)

@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    username = db.execute("SELECT username FROM users WHERE id = (?);", session["user_id"])[0]["username"]
    if request.method == "GET":
        return render_template("change-password.html", username=username)
    if request.method == "POST":
        user_id = session["user_id"]
        current_password = request.form.get("current_password")
        new_password = request.form.get("password")
        confirmation_password = request.form.get("confirmation")
        # Ensure the user provided they're current password
        if not current_password:
            return apology("must provide your current password", 400, username)
        # Ensure the user provided they're new password
        if not new_password:
            return apology("must provide your password", 400, username)
        # Ensure the user provided they're new password confirmation
        if not confirmation_password:
            return apology("must confirm your new password", 400, username)
        # Ensure the confirmation password matches the new password
        if new_password != confirmation_password:
            return apology("confirmation password does not match your new password", 400, username)

        '''
        Password requirements:
            - Password consists of alphanumeric characters (a-z0-9), lowercase, or uppercase.
            - The number of characters must be between 8 to 10.
        '''
        password_regex = "^[a-z0-9]{8,10}$"
        # Ensure the new password meets all the requirements
        if re.fullmatch(password_regex,  new_password, flags=re.IGNORECASE):
            user_credentials = db.execute("SELECT hash FROM users WHERE id = (?)", user_id)
            # Check if the provided current password is correct
            if not check_password_hash(user_credentials[0]["hash"], current_password):
                return apology("wrong current password", 400, username)
            else:
                # Hash the new password and update the new password
                new_password = generate_password_hash(new_password)
                db.execute("UPDATE users SET hash = (?) WHERE id = (?);", new_password, user_id)
                return success("You have changed your password", "successfully", username)
        else:
            return apology("must provide a valid new password", 400, username)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
