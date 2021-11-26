from app import app 
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, ComplaintForm, RegistrationForm
from app.functions.package import userInfo
from app.models import User, registered_users_table, registered_users_complaints
from app.database import DB
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse



''' All Handlers go here. For example: 
    Login function -> login(),
    Register function -> register()...
    
*** Keep ONLY those types of functions in here
'''

# Home Page 
@app.route('/')
@app.route("/index")
def index():
    database=DB()
    high_class_data = database.getTopRatedClass()
    low_class_data = database.getLowRatedClass()
    student_grade = database.getTopStudents()
    return render_template('index.html',high_class_data=high_class_data,low_class_data=low_class_data,student_grade=student_grade)




# TODO: Fix: if we enter any registered username AND
#            any registered password, the user is logged in

# Login Page
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        if user in registered_users_table:
            # if user found, return the index
            user_index = registered_users_table.index(user)
            # Test for the right password
            if registered_users_table[user_index].check_password(form.password.data):
                flash(form.password.data)
                flash('Valid Login')
                login_user(user, remember=form.remember_me.data)

                session['username'] = request.form['username']
                session['user_index'] = user_index
                flash(session['username'])

                return redirect(url_for('index'))
            else:
                flash('Invalid Username or Password')
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        '''
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
        ''' 

    return render_template('login.html', title='Sign In', form=form)



# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('user_index', None)
    return redirect(url_for('index'))


# Register Page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        user.set_email(form.email.data)

        # If user is already registered
        if user in registered_users_table:
            flash('Already Registered User. Please Login')
        else:
            flash('Congratulations, you are now registered')
            registered_users_table.append(user)

        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form) 


# User Info Page
@app.route("/account")
@login_required
def account():
    userPackage = userInfo()
    return render_template('account.html', title='User Info', packages=userPackage)

# Course Page
@app.route("/course")
def course():
    return render_template('course.html', title='Course Page')


# Complaints Page
@app.route("/complaint", methods=['GET', 'POST'])
@login_required
def complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        user_index = session['user_index']
        flash(user_index)
        new_complaint = registered_users_table[user_index].Complaint(form.name.data,
                                                                     form.subject.data)
        new_complaint.set_complaint(form.complaint.data)
        registered_users_complaints.append(new_complaint)
        flash('Your Complaint has been submitted for review')
        print('Recent Complaint: {}\n'.format(new_complaint.content))
        return redirect(url_for('index'))
    return render_template('complaint.html', title='Complaints', form=form)

