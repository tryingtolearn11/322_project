from app import app 
from flask import render_template, url_for, redirect, flash, request, session
from app.forms import LoginForm, ComplaintForm, InstructorRegistrationForm, StudentRegistrationForm
from app.functions.package import userInfo
from app.models import *
from app.database import DB
from flask_login import current_user, login_user, logout_user, login_required
from functools import wraps
from werkzeug.urls import url_parse
from collections import Counter


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
            for u in all_registrars:
                if session['username'] == u.username:
                    user.set_registrar()

            for i in all_instructors:
                if session['username'] == i.username:
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
@requires_access_level(ACCESS['student'])
def course_registration():
    courses = registered_courses_table_nextSemester
    cart = 0     
    #TODO condition for instructor                                   
    if isinstance(current_user, Student):
        student = current_user
        cart = current_user.shoppingCart
        if len(cart) == 0:
            cart = 0
            flash("Your Cart is empty")
    return render_template('course_registration.html', title='Course Registration',courses=courses, cart=cart,
                           student=student)


@app.route('/course-registration/<string:courseID>')
@login_required
@requires_access_level(ACCESS['student'])
def course_page_registration(courseID):
    course = Course.get(courseID)
    class_list = course.class_list
    print(class_list)
    if class_list == None:
        flash("No classes available")
        return redirect(url_for('course_registration'))

    return render_template('course_page_registration.html',
                           title="{}".format(course.courseName),
                           class_list=class_list)




@app.route('/course-registration/<string:courseID>/add')
def addToCart(courseID):
    if isinstance(current_user, Student):
        current_user.addToShoppingCart(courseID)
        return redirect(url_for('course_registration'))
    else:
        flash("User is Not a Student")
        return redirect(url_for('course_registration'))
    

@app.route('/course-registration/<string:courseID>/remove')
def removeFromCart(courseID):
    if isinstance(current_user, Student):
        current_user.removeFromShoppingCart(courseID)
        return redirect(url_for('course_registration'))
    else:
        flash("User is Not a Student")
        return redirect(url_for('course_registration'))



@app.route('/grading')
@login_required
@requires_access_level(ACCESS['instructor'])
def grading_period():
    if isinstance(current_user, Instructor):
        courses = current_user.current_classes
    else:
        flash("You Have no Classes")
        return redirect(url_for('manage_course'))
    return render_template('grading.html', title='Grading', courses=courses)


@app.route('/manage-course')
@login_required
@requires_access_level(ACCESS['instructor'])
def manage_course():
    return render_template('manage_course.html', title='Manage')



# Instructor Classes
@app.route('/your-classes')
@login_required
@requires_access_level(ACCESS['student'])
def instructor_classes():
    current_classes = 0
    # Show current classes if User is student
    if isinstance(current_user, Student):
        if len(current_classes) != 0:
            current_classes = current_user.currentClasses

    # If User is Instructor
    if isinstance(current_user, Instructor):
        if len(current_classes) != 0:
            current_classes = current_user.current_classes

    if isinstance(current_user, User) and current_user in all_registrars:
        flash("You have no classes")
        return redirect(url_for('manage_course'))

    print(current_classes)
    return render_template('instructor_classes.html', title='Classes', current_classes=current_classes)

# --------------------------------------------------------------------


@app.route('/courses/<string:courseID>', methods=['GET', 'POST'])
@login_required
def course_page(courseID):
    course = Course.get(courseID)
    print(course.class_list)
    class_list = course.class_list

    return render_template('course_page.html',
                           title="{}".format(course.courseName),
                           class_list=class_list)


@app.route('/courses/<string:courseID>/<string:studentUsername>/assignGrade', methods=['GET', 'POST'])
@login_required
def assignGrade(studentUsername, courseID):
    data = request.form['text']
    print(data)
    student = User.get(studentUsername)
    course = Course.get(courseID)
    student.addGrade(data.upper(), course)

    return redirect(url_for('course_page', courseID=courseID))
    

    
    


@app.route('/students/<string:studentUsername>')
@login_required
def student_page(studentUsername):
    student = User.get(studentUsername)
    gpa = student.evaluateGPA()
    if gpa == None:
        flash("GPA unavailable")
    return render_template('student_page.html', student=student)

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
    
                for u in all_registrars:
                    if session['username'] == u.username:
                        user.set_registrar()

                for u in all_instructors:
                    if session['username'] == u.username:
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


# Register Page for Instructor
@app.route("/register-instructor", methods=['GET', 'POST'])
def registerInstructor():
    form = InstructorRegistrationForm()
    if form.validate_on_submit():
        user = Instructor(form.username.data, form.password.data)
        user.set_email(form.email.data)
        user.set_instructor()


        # If user is already registered
        if user in registered_users_table:
            flash('Already Registered User. Please Login')
        else:
            flash('Congratulations, you are now registered')
            registered_users_table.append(user)

        return redirect(url_for('login'))
    return render_template('registerInstructor.html', title='Register', form=form) 


# Register Page for Student
@app.route("/register-student", methods=['GET', 'POST'])
def registerStudent():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        if float(form.oldGPA.data) > 3.0:
            user = Student(form.username.data, form.password.data)
            user.set_email(form.email.data)
        else:
            user = User(form.username.data, form.password.data)
            flash("Your application has been sent in and You will hear back soon")


        # If user is already registered
        if user in registered_users_table:
            flash('Already Registered User. Please Login')
        else:
            if isinstance(user, Student):
                flash('Congratulations, you are now registered as a Student')
            else:
                flash('Congratulations, you are now registered as a User')
            registered_users_table.append(user)

        return redirect(url_for('login'))
    return render_template('registerStudent.html', title='Register', form=form) 

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

@app.route("/account/apply-for-grad")
@login_required
def applyForGrad():
    grad_status = None
    if isinstance(current_user, Student):
        student = current_user
        grad_status = current_user.applyForGraduation()
    else:
        flash("User is not a student -> Cannot Apply")
        return redirect(url_for('account'))
    return render_template('apply_for_grad.html', grad_status=grad_status,
                           student=student)


@app.route("/course_registration/register")
@login_required
def register_class():
    if isinstance(current_user, Student):
        current_user.enrollCart()
    else:
        flash('Unable to Register for Courses : User is not a Student')
    return redirect(url_for('course_registration'))
   # return render_template('register_class.html', title='Register for Class')


# Course Page
# Lists all the courses
@app.route("/course")
def course():
    courses = registered_courses_table
    return render_template('course.html', title='Course Page', courses=courses)


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


#Tutorial Page
@app.route("/tutorial")
@login_required
def tutorial():
    return render_template('tutorial.html', title='Tutorial')

@app.route("/addreview",methods=["post"])
@login_required
def addReview():
    database=DB()
    review_for = request.form.get("review_for")
    rating = request.form.get("rating")
    review = request.form.get("review")
    taboo_words = database.getTabooWords()
    word_counter = Counter(review.split(" "))
    for word in taboo_words:
        review = review.replace(word,"***")
    database.insertReview(session["user_index"],review_for,rating,review)
    return {"Message":"Review Successfully Inserted","review":review}

