# DISCLAIMER: For good design purposes, I made my Flask template very similar to the one seen in the video below, I did not come up with most of the design myself
# https://www.youtube.com/watch?v=GQcM8wdduLI&list=PLzMcBGfZo4-nK0Pyubp7yIG0RdXp6zklu&index=1


from web_app import init_app
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

if __name__ == "__main__":
    app = init_app()
    app.run(debug=True)