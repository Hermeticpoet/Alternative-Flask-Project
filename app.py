import os
from os import environ
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session
from functools import wrap
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import RegistrationForm, LoginForm

# Create the Application Object
app = Flask(__name__)

app.secret_key = "magic session key"

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
@login_required
def home():
    return render_template("index.html", title="Home") # render a template


# @app.route("/recipes")
# def recipes():
#     return render_template("recipes.html")


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

    
if __name__ == "__main__":
    app.run(debug=True)