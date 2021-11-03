from app import app 
from flask import render_template

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
    return render_template('login.html')




