# CUNYZero/GradSchoolZero - CSC 322 (Software Engineer) Project

Contributors: Jia Cong Lin, Damien Singh, Josh Miranda, Wally Hasnat (Group Z)

	Uses Python Flask, HTML, Booststrap, Jinja, and CSS

**Summary:** 

The vision of GradSchoolZero is to create a system similar to CUNYfirst but for managing graduate programs. The system will be used by visitors, students, instructors and the registar. Visitors can browse the site viewing basic information such as classes and students. Students can manage courses they are taking. Instructors access courses assigned by the registrar and the registrar is the administrator that manages the whole site. The features in this system will allow these users to access the information needed. Included in the system is the home, account, course page and complaints. Home will be the main page where all users will start off. Account will have basic information about the student and instructor. Course page manages the courses for students and instructors. Lastly, the complaints are for the complaints about other students, instructors or courses. To begin exploring and learning more about the website launch the website then Login and Register -> index.html.

We did our meetings on a frequency of once a week for this project since the meetings help us decide on what the next step was. 

Here is our first phase report:<br /> 
[Phase I Report](https://github.com/tryingtolearn11/322_project/blob/main/Software_Requirements_Spec.pdf)

Here is our second phase report:<br />
[Phase II Report](https://github.com/tryingtolearn11/322_project/blob/main/Design_Report_Phase_2.pdf)

# File Structure and Set-Up <br />
**Each file will contain the following:**
* \\-- app
  * \\-- static
    * \\-- css
        <br> &emsp;&emsp; &emsp;|-- class_setup.css
        <br> &emsp;&emsp; &emsp;|-- complaint.css
        <br> &emsp;&emsp; &emsp;|-- complaint.css
        <br> &emsp;&emsp; &emsp;|-- grading.css
        <br> &emsp;&emsp; &emsp;|-- login.css
        <br> &emsp;&emsp; &emsp;|-- site.css 
    * |-- img
   * \\-- templates
        <br> &emsp;&emsp; &emsp; |-- account.html
        <br> &emsp;&emsp; &emsp; |-- apply_for_grad.html
        <br> &emsp;&emsp; &emsp; |-- base.html
        <br> &emsp;&emsp; &emsp; |-- class_setup.html
        <br> &emsp;&emsp; &emsp; |-- complaint.html 
        <br> &emsp;&emsp; &emsp; |-- course_history.html 
        <br> &emsp;&emsp; &emsp; |-- course_page_registration.html
        <br> &emsp;&emsp; &emsp; |-- course_page.html
        <br> &emsp;&emsp; &emsp; |-- course_registration.html
        <br> &emsp;&emsp; &emsp; |-- course.html
        <br> &emsp;&emsp; &emsp; |-- grading.html
        <br> &emsp;&emsp; &emsp; |-- index.html
        <br> &emsp;&emsp; &emsp; |-- instructor_classes.html
        <br> &emsp;&emsp; &emsp; |-- login.html
        <br> &emsp;&emsp; &emsp; |-- manage_course.html
        <br> &emsp;&emsp; &emsp; |-- register_class.html
        <br> &emsp;&emsp; &emsp; |-- registerInstructor.html
        <br> &emsp;&emsp; &emsp; |-- registerStudent.html
        <br> &emsp;&emsp; &emsp; |-- student_page.html
        <br> &emsp;&emsp; &emsp; |-- tutorial.html
   * |-- _init_.py
   * |-- database.py
   * |-- forms.py
   * |-- models.py
   * |-- routes.py

# Website Organization

- form.py - This is where all the forms we created are stored in and called when needed.
- models.py - The mini database where data is created and stored.
- routes.py - This is where all the code for routes are stored in.
- database.py - This is where the functions using the database will be stored in eg. sorting functions.
- account.html - Basic account page with links to other pages thats centered around personal data for the user.
- apply_for_grad.html - Page coming from account page for users to apply to graduation.
- base.html - The basic page format which all other pages should have such as the header and footer.
- class_setup.html - Page for registrars to set up a class.
- complaint.html - Page for all users to file a complaint about someone else.
- course_history.html - personal record of the student coming from the account page with all their classes, grades, and GPA.
- course_page_registration.html - page for students to know more about a certain class and to either add/remove the class to their shopping cart.
- course_page.html - Page for instructor to input the grades for each student after clicking on a course in Grades page.
- course_registration.html - Students can see all the classes they can take and the classes in their shopping cart to be registered along with the classes they have already registered for next semester.
- course.html - Shows to everyone the courses that are offered.
- grading.html - Page for instructor to see all the classes that they are teaching and to input student grades if they click on the respective course name.
- index.html - The home page with a button that routes to sign in and the account page along with charts of highest and lowest rated classes and top students.
- instructor_classes.html - page for instructor to see each class they are teaching along with the grades they gave.
- login.html - login page with routes to sign up.
- manage_course.html - A page for the button Manage Course on the navigation bar.
- register_class.html - Register for class here.
- registerInstructor.html - Sign up page for a visitor to become an instructor.
- registerStudent.html - Sign up page for a visitor to become a student.
- student_page.html - Instructors can see this page for each student that they are teaching by going to grading->course name->student first name
- tutorial.html - A page with images and text to explain what each page can do for the users.

# Create Virtual Environment from Python3

   	- Need to have pip installed
	- $ python3 -m venv venv
	- $ source venv/bin/activate

# Requirements

    - $ pip install -r requirements.txt  //install all packages needed

# Run the Program
	
	- $ flask run
