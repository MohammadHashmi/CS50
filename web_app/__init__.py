from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_session import Session

db = SQLAlchemy()
DB_NAME = 'trackr.db'

def init_app():
    # Creates app
    app = Flask(__name__)

    # Code from finance pset to refresh web app
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Code from finance pset to make the session use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # Doesn't track modifications
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Imports the route blue print that I defined in routes.py, registers it as a blueprint
    from .routes import route
    app.register_blueprint(route, url_prefix='/')
    
    # Initializes the database
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .models import User
    from .models import Earned

    # Creates database
    create_db(app)

    # Returns the app
    return app

# Creates the db if it doesn't exist already
def create_db(app):
    if not path.exists("web_app/" + DB_NAME):
        db.create_all(app=app)