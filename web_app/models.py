# Much of the set up for the database was inspired from https://www.youtube.com/watch?v=W4GItcW7W-U&t=417s&ab_channel=TechWithTim

from . import db

# Creates the first model/table: Users
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    total_cash = db.Column(db.Integer, default=0)
    total_income = db.Column(db.Integer, default=0)
    total_expenses = db.Column(db.Integer, default=0)

    # Constructor to take arguments. Syntax from https://www.youtube.com/watch?v=v6b4tggM7M0&ab_channel=RedEyedCoderClub
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Creates Earned table to track the money earned by the user over a period of months
class Earned(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Text)
    Value  = db.Column(db.Integer, default=0)
    primary = db.Column(db.Integer, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Expenses(db.Model):
    user_id = db.Column(db.Integer, nullable=False)
    Month = db.Column(db.Text)
    Value  = db.Column(db.Integer, default=0)
    primary = db.Column(db.Integer, primary_key=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
