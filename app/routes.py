from app import app 
from flask import render_template, url_for, redirect, flash
from app.forms import LoginForm
from app.functions.package import userInfo
from app.models import User, dummy_users_table
from flask_login import current_user, login_user, logout_user


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
@app.route("/login", methods=['GET', 'POST'])
def login():
#    if current_user.is_authenticated:
#        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        if user in dummy_users_table and user.check_password(form.password.data):
            flash('Valid Login')
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))

    return render_template('login.html', title='Sign In', form=form)



# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# User Info Page
@app.route("/account")
def account():
    userPackage = userInfo()
    return render_template('account.html', packages=userPackage)

# Course Page
@app.route("/course")
def course():
    return render_template('course.html')

# Complaints Page
@app.route("/complaint")
def complaint():
    return render_template('complaint.html')




