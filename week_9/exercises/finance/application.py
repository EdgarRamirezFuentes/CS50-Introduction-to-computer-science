import os
import re
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, repeated_username, registered_username, login_required, lookup, usd

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
    stocks = db.execute("SELECT stock_id, quantity FROM user_stocks WHERE user_id = (?) ORDER BY stock_id;", user_id)
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
                "quantity": stock["quantity"]
            })
            stocks_total += stock_data["price"] + stock["quantity"]
    return render_template("index.html", username=username, stocks=stocks_information, stock_total_value=stocks_total, cash=cash)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


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
