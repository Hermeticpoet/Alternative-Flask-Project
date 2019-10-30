import os
from os import environ
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session, g
from functools import wraps
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm
import sqlite3

# Create the Application Object
app = Flask(__name__)

app.secret_key = "magic session key"
app.database = "cookbook.db"

# app.config["SECRET_KEY"] = '9039e1a76014f85ad2fea4415a793bd8'
# app.config["MONGO_DBNAME"] = 'CookBook'
# app.config["MONGO_URI"] = 'mongodb+srv://root:mongoDB2019@myfirstcluster-oyutj.mongodb.net/test?retryWrites=true&w=majority'

#  Mongo Database Variable
# mongo = PyMongo(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to log in first.")
            return redirect(url_for("login"))
    return wrap

#  Use decorators to link the function to a URL
@app.route("/")
@app.route("/index")
@login_required
def home():
    # G used by Flask to store temporary object
    g.db = connect_db()
    cur = g.db.execute("select * from recipes")
    recipes = []
    for row in cur.fetchall():
        recipes.append(dict(title=row[0], description=row[1]))
    g.db.close()
    return render_template("index.html", title="Home", recipes=recipes) 


# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            session["logged_in"] = True
            flash("You are now logged in!")
            return redirect(url_for("home"))
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    session.pop("logged_in", None) # will pop user session logged_in and replace with None
    flash("You are now logged out!")
    return redirect(url_for("home"))


def connect_db():
    return sqlite3.connect(app.database)
    
if __name__ == "__main__":
    app.run(debug=True)