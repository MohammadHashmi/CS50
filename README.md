# TRACKR
#### Video Demo:  https://youtu.be/DXzALcjRJGo
#### Description:

### WHAT IS IT?
Made with Python, Flask, Flask-sqlalchemy, HTML, CSS, and Javascript, Trackr was created to provide a hassle-free way to track your finances with an easy to understand user interface. 

The website greets the user with a login page and allows the user to create an account if they haven't already. Once it authenticates a login/register it takes the user to the home page. There, the user can see their yearly income, expenses and the money they have left over. The user can report any income they earnt. After submitting an income they can see it appear on the chart and can add as many incomes as they want. The expenses page works very similarly but it takes care of how much the user spent in a certain month.

### FILE DESIGN AND FUNCTION
__pycache__, .venv and flask_session: Folders made by the system to be able to run the program in a virtual flask environment

web_app: The folder where majority of my program was written (Everything except app.py, requirements.txt and the README!)

web_app/static: The static folder just contained a CSS file written for the webpage

web_app/templates: The templates folder contained all the HTML files used in the website

web_app/templates/layout.html: This was the basic layout of the website and mainly consisted of the navbar

web_app/templates/login.html and web_app/templates/register.html: These two files were used to create an interface where users can sign in and register

web_app/templates/index.html: The homepage

web_app/templates/income.html and web_app/templates/expenses.html: Used chart.js to create a page where the user could enter the information they wanted and have the chart update automatically. 

web_app/templates/apology.html: In case of an error, the developer can print an error message telling the user what went wrong

web_app/__init__.py: This file was made to define the functions that would be called to initialize the app and database.

web_app/models.py: This file contained the flask-sqlalchemy models for the database

web_app/routes.py: The file that was responsible for controlling what happened when the user went to a certain page and did certain actions

web_app/trackr.db: The actual database containing all the information

app.py: Responsible for calling the init_app function and actually creating the web app

requirements.txt: All the libraries required to run this

README.md: This!
