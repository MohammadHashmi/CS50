from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = 'database.db'

def init_app():
    # Creates app
    app = Flask(__name__)

    # Code from finance pset to refresh web app
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # Doesn't track modifications
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Imports the route blue print that I defined in routes.py, registers it as a blueprint
    from .routes import route
    app.register_blueprint(route, url_prefix='/')
    
    # Initializes the database
    app.config["SQL_ALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Creates database
    create_db(app)
    return app

#Creates the db if it doesn't exist already
def create_db(app):
    if not path.exists("CS50/" + DB_NAME):
        db.create_all(app=app)