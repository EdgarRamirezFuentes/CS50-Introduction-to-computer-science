"""Render message as an apology to user."""
import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps

def escape(s):
    """
    Escape special characters.

    https://github.com/jacebrowning/memegen#special-characters
    """
    for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                    ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
        s = s.replace(old, new)
        return s

def error_message(message, code=400, username=""):
    return render_template("error_message.html", top=code, bottom=escape(message), username=username), code

def multiverse_message(message1, message2, username=""):
    return render_template("multiverse_message.html", top=escape(message1), bottom=escape(message2) , username=username)

def success_message(message1, message2, username=""):
    return render_template("success_message.html", top=escape(message1), bottom=escape(message2) , username=username)

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id"):
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function