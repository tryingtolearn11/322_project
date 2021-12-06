from app import app 
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, ComplaintForm, RegistrationForm
from app.functions.package import userInfo
from app.models import User, Student, registered_users_table, registered_users_complaints, ACCESS, Tom
from app.database import DB
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from werkzeug.urls import url_parse



''' All Handlers go here. For example: 
    Login function -> login(),
    Register function -> register()...
    
*** Keep ONLY those types of functions in here
'''




# --------------- Periods ----------------------------------------

# Class Set-up Period
# Course Registration Period
# Class running period
# Grading Period



def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('username'):
                flash(session.get('username'))
                return redirect(url_for('login'))

            user = User.get(session.get('username'))
            if session['username'] == "susan":
                user.set_registrar()

            if session['username'] == "john":
                user.set_instructor()

            flash(user.access)
            if not user.allowed(access_level):
                flash("Sorry, you are not authorized to view")
                return redirect(url_for('index', message="restricted access"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@app.route('/class-setup')
@login_required
@requires_access_level(ACCESS['registrar'])
def class_setup():
    return render_template('class_setup.html', title='Class Setup')



@app.route('/course-registration')
@login_required
@requires_access_level(ACCESS['registrar'])
def course_registration():
    return render_template('course_registration.html', title='Course Registration')


@app.route('/grading')
@login_required
@requires_access_level(ACCESS['registrar'])
def grading_period():
    return render_template('grading.html', title='Grading')


@app.route('/manage-course')
@login_required
@requires_access_level(ACCESS['instructor'])
def manage_course():
    return render_template('manage_course.html', title='Manage')



# Instructor Classes

@app.route('/your-classes')
@login_required
@requires_access_level(ACCESS['instructor'])
def instructor_classes():
    return render_template('instructor_classes.html', title='Classes')

# --------------------------------------------------------------------

# Home Page 
@app.route('/')
@app.route("/index")
def index():
    database=DB()
    high_class_data = database.getTopRatedClass()
    low_class_data = database.getLowRatedClass()
    student_grade = database.getTopStudents()
    return render_template('index.html',high_class_data=high_class_data,low_class_data=low_class_data,student_grade=student_grade)



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
                # flash(form.password.data)
                flash('Valid Login')
                login_user(user, remember=form.remember_me.data)

                session['username'] = request.form['username']
                session['user_index'] = user_index
                session['email'] = user.email
    
                # Dummy Data
                if session['username'] == "susan":
                    user.set_registrar()
                if session['username'] == "john":
                    user.set_instructor()

                flash(user.access)

                session['access'] = user.access

                return redirect(url_for('index'))
            else:
                flash('Invalid Username or Password')
        else:
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)



# Logout Page
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username', None)
    session.pop('user_index', None)
    session.pop('email', None)
    session.pop('access', None)
    return redirect(url_for('index'))


# Register Page for Student
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


# Students Course History
@app.route("/account/course-history")
@login_required
def course_history():
    if isinstance(current_user, Student):
        print("User is a student")

        # Show List of Past Courses
        past_courses = current_user.grades
        print(current_user.grades)


    else:
        print("User is not a student")
        past_courses = 0


    return render_template('course_history.html', title='Course History',
                           past_courses=past_courses)








# Course Page
# Lists all the courses
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
#        flash(user_index)
        new_complaint = registered_users_table[user_index].Complaint(form.name.data,
                                                                     form.subject.data)
        new_complaint.set_complaint(form.complaint.data)
        registered_users_complaints.append(new_complaint)
        flash('Your Complaint has been submitted for review')
        print('Recent Complaint: {}\n'.format(new_complaint.content))
        return redirect(url_for('index'))
    return render_template('complaint.html', title='Complaints', form=form)

