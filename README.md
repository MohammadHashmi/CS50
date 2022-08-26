# TRACKR
#### Video Demo:  https://youtu.be/DXzALcjRJGo
### WHAT IS IT?
Made with Python, Flask, Flask-sqlalchemy, HTML, CSS, and Javascript, Trackr was created to provide a hassle-free way to track your finances with an easy to understand user interface. 

The website greets the user with a login page and allows the user to create an account if they haven't already. Once it authenticates a login/register it takes the user to the home page. There, the user can see their yearly income, expenses and the money they have left over. The user can report any income they earnt. After submitting an income they can see it appear on the chart and can add as many incomes as they want. The expenses page works very similarly but it takes care of how much the user spent in a certain month.

### FILE DESIGN AND FUNCTION
_pycache_, .venv and flask_session: Folders made by the system to be able to run the program in a virtual flask environment

web_app: The folder where majority of my program was written (Everything except app.py, requirements.txt and the README!)

web_app/static: The static folder just contained a CSS file written for the webpage

web_app/templates: The templates folder contained all the HTML files used in the website

web_app/templates/layout.html: This was the basic layout of the website and mainly consisted of the navbar

web_app/templates/login.html and web_app/templates/register.html: These two files were used to create an interface where users can sign in and register

web_app/templates/index.html: The homepage

web_app/templates/income.html and web_app/templates/expenses.html: Used chart.js to create a page where the user could enter the information they wanted and have the chart update automatically. 

web_app/templates/apology.html: In case of an error, the developer can print an error message telling the user what went wrong

web_app/_init_.py: This file was made to define the functions that would be called to initialize the app and database.

web_app/models.py: This file contained the flask-sqlalchemy models for the database

web_app/routes.py: The file that was responsible for controlling what happened when the user went to a certain page and did certain actions

web_app/trackr.db: The actual database containing all the information

app.py: Responsible for calling the init_app function and actually creating the web app

requirements.txt: All the libraries required to run this

README.md: This!

### STRUGGLES AND SOLUTIONS
This was my first time coding outside of the CS50 IDE and it was tough at first to figure out how to set up an IDE of my own with everything I needed. I used plenty of documentation and looked at a few tutorials to ultimately set it up for myself.  
Wanting to build the project without any of the training wheels from CS50, I had to learn flask-sqlalchemy to make my project. It took a lot of effort and tutorials but in the end I found what worked for me and was able to effectively implement it into my code
Using something like chart.js for the first time was a struggle but also a great learning experience. It helped me understand how to use resources online to make my projects aesthetic and functional.
One struggle I faced early on was trying to make sure my code was well designed and organized from the start to save me from having to fix it later on. I used a tutorial (which I have linked in my code) to make sure the file organization was neat and well done to make it easy to understand. In terms of code I just made sure to double check my code after writing it to see if I knew a way to make it more efficient

### FINAL NOTICES
All of the resources I used to help me while making this are linked in the code, respective to where I implemented them. You can feel free to message me on discord Dubi#8195 if you have any concerns. Thanks!
