from asyncio.windows_events import NULL
from email import message
import re
from flask import Blueprint, render_template, request, session, redirect
from . import db 
from .models import User


# Creates blueprint
route = Blueprint("route", __name__)

# Simple function to redirect user to login page if they aren't signed in yet:
# https://blog.teclado.com/protecting-endpoints-in-flask-apps-by-requiring-login/
def confirm_login(func):
    def require_login():
        if session.get("user_id") is None:
            return redirect("/login")
        return func()
    return require_login

# If the route is the homepage
@route.route("/")
@confirm_login
def index():
    return render_template("index.html")

# If the user tries to register
@route.route("/register", methods=["POST", "GET"])
def register():

    # If the user submits a login form
    if request.method == "POST":

        # Gets the information from the user
        user_name = request.form.get("username")
        password = request.form.get("password")
        password_confirm = request.form.get("password_confirm")


        # Checks for errors
        user_exists = User.query.filter_by(username=user_name).first()
        if user_exists:
            return render_template("apology.html", message="Username taken")
        if password != password_confirm:
            return render_template("apology.html", message="Passwords don't match")
        
        # Creates person then adds them to database
        person = User(username=user_name, password=password)
        db.session.add(person)
        db.session.commit()

        # Sets a session for the current user
        session["user_id"] = person.id

        # Returns them to home page
        return render_template("index.html")
    else:
        return render_template("register.html")


@route.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:

        # Same code as the one in register to see if the user is in the database
        user_name = request.form.get("username")
        password = request.form.get("password")
        user_exists = User.query.filter_by(username=user_name).first()

        # Checks whether password matches with the user
        if user_exists:
            if user_exists.password == password:
                session["user_id"] = user_exists.id
                return redirect("/")
            else:
                return render_template("apology.html", message="Invalid password")

@route.route("/logout")
def logout():
    # Clears the users session
    session.clear()
    return redirect("/login")