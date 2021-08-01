import re
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error_message, login_required, logout_required, multiverse_message, success_message

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SECRET_KEY'] = "Seraphine"  

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///task_manager.db")

@app.route("/")
@login_required
def index():
    user_data = db.execute("SELECT username, email FROM users WHERE id = ?", session["user_id"])
    username = user_data[0]["username"]
    email = user_data[0]["email"]
    return render_template("index.html", username=username, email=email)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return error_message("You must provide a username")
        if not password:
            return error_message("You must provide a password")
        if not confirmation:
            return error_message("You must confirm your password")
        
        # Trimming white spaces in the information
        username = username.strip()
        if email:
            email = email.strip()
        password = password.strip()
        confirmation = confirmation.strip()
        
        # Username requirements
        # - Only accept alphanumeric characters
        # - The first letter must be a letter
        # - The length of the username must be between 6 to 16 characters
        username_re = "^[a-z]([a-z0-9]){3,18}$"
        # Password requirements
        # - Only accepts alphanumeric characters
        # - The length of the username must be between 8 to 20 characters
        password_re = "^[a-z0-9]{8,20}$"  
        
        if not re.fullmatch(username_re, username, flags=re.IGNORECASE) :
            return error_message("You must provide a valid username")
        
        if not re.fullmatch(password_re, password, flags=re.IGNORECASE):
            return error_message("You must provide a valid password")
        
        if password != confirmation:
            return error_message("The confirmation does not match your password")
        
        # Check if the username and the email are unique
        existant_user = db.execute("SELECT username, email FROM users WHERE username = ? OR email = ?;", username, email)
        # There is a user that already registered the username or the email
        if existant_user:
            existant_username = existant_user[0]["username"]
            if existant_username == username:
                return multiverse_message("You", "Someone using the same username")
            existant_email = existant_user[0]["email"]
            if existant_email and existant_email == email:
                return multiverse_message("You", "Someone using the same email")
        
        if email:
            db.execute("INSERT INTO users (username, pass, email) VALUES (?, ?, ?)", 
                        username, generate_password_hash(password), email)
        else:
            db.execute("INSERT INTO users (username, pass) VALUES (?, ?)", 
                        username, generate_password_hash(password))
        return success_message("Welcome!", "Your account was created successfully!")


@app.route("/login", methods=["GET", "POST"])
@logout_required
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
    
    if not username:
        return error_message("You must provide a username")
    if not password:
        return error_message("You must provide a password")
    
    username = username.strip()
    password = password.strip()
    
    user_credentials = db.execute("SELECT id, pass FROM users WHERE username = ?", username)
    
    if not user_credentials :
        return error_message("Incorrect username")

    if not check_password_hash(user_credentials[0]["pass"], password):
        return error_message("Incorrect password")
    
    session["user_id"] = user_credentials[0]["id"]
    return redirect("/") 


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return error_message(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
