from asyncio.windows_events import NULL
from email import message
from multiprocessing.sharedctypes import Value
from pydoc import render_doc
import re
from flask import Blueprint, render_template, request, session, redirect, json
from . import db 
from .models import User, Earned
import sqlite3

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
    unique_name = User.query.filter_by(id=session["user_id"]).first()
    print(unique_name.id)
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
        if not user_name or not password or not password_confirm:
            return render_template("apology.html", message="Fields can't be blank")

        
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

        # Checks for errors 
        if not user_name:
            return render_template("apology.html", message="Enter a valid username")
        elif not password:
            return render_template("apology.html", message="Enter a valid password")
        elif not user_exists:
            return render_template("apology.html", message="Account doesn't exist")

        # Checks whether password matches with the user
        elif user_exists:
            if user_exists.password == password:
                session["user_id"] = user_exists.id
                return redirect("/")
            else:
                return render_template("apology.html", message="Invalid password")

# Why I used endpoint function https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
@route.route("/income", endpoint='income', methods=["POST", "GET"])
@confirm_login
def income():
    # Months array for select menu using json: https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3
    months = json.dumps(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    # Month array to be used for plain html
    months1 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # Initialize variables for js data
    january=february=march=april=may=june=july=august=september=october=november=december = 0
    # Data to be used in javascript
    data1 = json.dumps([january, february, march, april, may, june, july, august, september, october, november, december])
    
    # If the user reports any income
    if request.method == "POST": 

        # Gets the values the user inputted
        amount = request.form.get("amount")
        month = request.form.get("month")

        if not amount or month == "Choose...":
            return render_template("apology.html", message="Fields can't be blank")

        # Gets info from the database
        person_id = Earned.query.filter_by(user_id=session["user_id"], Month=month).first()

        # If that user has not already earned an income in a certain month
        if person_id == None:
            user_earned = Earned(user_id=session["user_id"], Month=month, Value=amount)
            print(user_earned.Value)
            db.session.add(user_earned)
            db.session.commit()

        # Updates their values if they've already previously made money in a certain month
        else:
            person_id.Value += int(amount)
            db.session.commit()

        # Declares an empty list to store all the values
        data1 = []

        # Iterates through every month
        for i in months1:

            # Finds the current month 
            current_m = Earned.query.filter_by(user_id=session["user_id"], Month=i).first()

            # If the user has reported an income for the current month, it finds the value and adds it to the list
            if current_m != None:
                current_value = current_m.Value
                data1.append(current_value)

            # Otherwise the value should stay at 0
            else:
                data1.append(0)

        # Makes the data usable for the json
        data_final = json.dumps(data1)
        
        # Renders the template
        return render_template("income.html", months=months, data=data_final, months1=months1)
    
    # If the user lands on the page
    elif request.method == "GET":

        # Same code as the POST method to display the data
        data1 = []
        for i in months1:
            current_m = Earned.query.filter_by(user_id=session["user_id"], Month=i).first()
            if current_m != None:
                current_value = current_m.Value
                data1.append(current_value)
            else:
                data1.append(0)
        data_final = json.dumps(data1)

        # Renders the page
        return render_template("income.html", months=months, data=data_final, months1=months1)

@route.route("/expenses", endpoint='expenses', methods=["GET", "POST"])
def expenses():
    return render_template("expenses.html")

@route.route("/logout")
def logout():
    # Clears the users session
    session.clear()
    return redirect("/login")