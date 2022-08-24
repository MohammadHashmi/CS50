from flask import Blueprint, render_template, request, session, redirect, json
from . import db 
from .models import User, Earned, Expenses
import sqlite3
import bcrypt

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

# Code from CS50 pset to format values to a comma seperated currency
def csc(value):
    return f"${value:,.2f}"

# If the route is the homepage
@route.route("/")
@confirm_login
def index():
    income_earned = User.query.filter_by(id=session["user_id"]).first().total_income
    income_spent = User.query.filter_by(id=session["user_id"]).first().total_expenses
    total_income = User.query.filter_by(id=session["user_id"]).first().total_cash
    if income_earned == None:
        income_earned = 0
    if income_spent == None:
        income_spent = 0
    if total_income == None:
        income_spent = 0
    return render_template("index.html", income_earned=csc(income_earned), income_spent=csc(income_spent), total_income=csc(total_income))

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

        # Hash password: https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
        pass_secure = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(pass_secure, salt)
        print(hashed)

        # Creates person then adds them to database
        person = User(username=user_name, password=hashed)
        db.session.add(person)
        db.session.commit()

        # Sets a session for the current user
        session["user_id"] = person.id

        # Returns them to home page
        return redirect("/")
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
        pass_encode = password.encode('utf-8')
        user_exists = User.query.filter_by(username=user_name).first()

        # Checks for errors 
        if not user_name:
            return render_template("apology.html", message="Enter a valid username")
        elif not password:
            return render_template("apology.html", message="Enter a valid password")
        elif not user_exists:
            return render_template("apology.html", message="Account doesn't exist")

        # Checks whether password matches with the user: https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
        elif user_exists:
            user_pass = user_exists.password
            match = bcrypt.checkpw(pass_encode, user_pass)
            if match == True:
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

    # If the user reports any income
    if request.method == "POST": 

        # Gets the values the user inputted
        amount = request.form.get("amount")
        month = request.form.get("month")

        # Error check
        if not amount or month == "Choose...":
            return render_template("apology.html", message="Fields can't be blank")
        elif float(amount) < 0:
            return render_template("apology.html", message="Enter a valid amount")

        # Checks whether a user with this id has reported an income in this month
        person_id = Earned.query.filter_by(user_id=session["user_id"], Month=month).first()

        # Adds the income to the users total income and total cash
        user = User.query.filter_by(id=session["user_id"]).first()
        user.total_cash += float(amount)
        user.total_income += float(amount)
        db.session.commit()


        # If that user has not already earned an income in a certain month
        if person_id == None:
            user_earned = Earned(user_id=session["user_id"], Month=month, Value=amount)
            db.session.add(user_earned)
            db.session.commit()

        # Updates their values if they've already previously made money in a certain month
        else:
            person_id.Value += float(amount)
            db.session.commit()

        # Declares an empty list to store all the values
        data = []

        # Iterates through every month
        for i in months1:

            # Finds the values this user has for the current month
            current_m = Earned.query.filter_by(user_id=session["user_id"], Month=i).first()

            # If the user has reported an income for the current month, it finds the value and adds it to the list
            if current_m != None:
                current_value = current_m.Value
                data.append(current_value)

            # Otherwise the value should stay at 0
            else:
                data.append(0)

        # Makes the data usable for the js
        data_final = json.dumps(data)
        
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
@confirm_login
def expenses():
    # Most of this code is very similar to the expenses page as the format is quite similar

    # Months list formed for the chart to be able to make labels; json format
    months = json.dumps(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    
    # Months list for the jinja code and python
    months1 = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    # If the user submits the form
    if request.method == "POST":

        # Gets the values the user inputted
        amount = request.form.get("amount")
        month = request.form.get("month")

        # Error check
        if not amount or month == "Choose...":
            return render_template("apology.html", message="Fields can't be blank")
        elif float(amount) < 0:
            return render_template("apology.html", message="Enter a valid amount")

        # Takes away the amount of cash the user inputted from their total cash and adds it to their expense count
        user = User.query.filter_by(id=session["user_id"]).first()
        user.total_cash -= float(amount)
        user.total_expenses += float(amount)
        db.session.commit()

        # Checks whether a user with this id has reported an expense in this month
        person_id = Expenses.query.filter_by(user_id=session["user_id"], Month=month).first()
        # If no income was reported, create a row in the db table for this person
        if person_id == None:
            user_spent = Expenses(user_id=session["user_id"], Month=month, Value=amount)
            db.session.add(user_spent)
            db.session.commit()
        
        # Otherwise update the row
        else: 
            person_id.Value += float(amount)
            db.session.commit()

        # Makes an empty list to store all the values for the chart
        data = []

        # Iterates through the list of the months
        for i in months1:

            # Finds the values this user has for the current month
            current_m = Expenses.query.filter_by(user_id=session["user_id"], Month=i).first()

            # If the user reported an expense before for the current month, it adds it to the list
            if current_m != None:
                month_value = current_m.Value
                data.append(month_value)
            
            # Otherwise if the user didn't report an expense for the current month, just leave the value at 0
            else:
                data.append(0)
            
            # Make the data usable for the js
            data_final = json.dumps(data)
            
        # Renders the template
        return render_template("expenses.html", months=months, data=data_final, months1=months1)
    
    # If the user lands on the page
    else:
        # Same code as above to display the proper values for the chart
        data = []
        for i in months1:
            current_m = Expenses.query.filter_by(user_id=session["user_id"], Month=i).first()
            if current_m != None:
                month_value = current_m.Value
                data.append(month_value)
            else:
                data.append(0)
            
            data_final = json.dumps(data)
            
        # Renders the template
        return render_template("expenses.html", months=months, data=data_final, months1=months1)

@route.route("/logout")
def logout():
    # Clears the users session
    session.clear()
    return redirect("/login")