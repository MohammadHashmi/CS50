from asyncio.windows_events import NULL
import re
from flask import Blueprint, render_template, request, session
from . import db 
from .models import User


# Creates blueprint
route = Blueprint("route", __name__)

# If the route is the homepage
@route.route("/")
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

@route.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")