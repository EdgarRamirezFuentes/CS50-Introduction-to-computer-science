import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name").strip()
        month = int(request.form.get("month"))
        day = int(request.form.get("day"))
        try:
            db.execute("INSERT INTO birthdays (name, month, day) VALUES(?,?,?)", name, month, day)
        except ValueError as e:
            print(e)
        finally:
            return redirect("/")

    else:
        birthdays = None
        try:
            birthdays = db.execute("SELECT name, month, day FROM birthdays;");
        except ValueError as e:
            print(e)
        finally:
            return render_template("index.html", birthdays=birthdays)


