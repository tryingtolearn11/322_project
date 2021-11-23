from app import app 
from flask import render_template, url_for, redirect
from app.forms import LoginForm
from app.functions.package import userInfo


''' All Handlers go here. For example: 
    Login function -> login(),
    Register function -> register()...
    
*** Keep ONLY those types of functions in here
'''


# Home Page 
@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')


# Login Page
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

# User Info Page
@app.route("/account")
def account():
    userPackage = userInfo()
    return render_template('account.html', packages=userPackage)

# Register Page
@app.route("/register")
def register():
    return render_template('register.html')




