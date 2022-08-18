from flask import Blueprint, render_template, request

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
        
        # Returns them to home page
        return render_template("index.html")
    else:
        return render_template("register.html")