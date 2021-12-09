# CUNYZero/GradSchoolZero - CSC 322 (Software Engineer) Project

Contributors: Jia Cong Lin, Damien Singh, Josh Miranda, Wally Hasnat (Group Z)

	Uses Python Flask, HTML, Booststrap, Jinja, and CSS

**Summary:** 

The vision of GradSchoolZero is to create a system similar to CUNYfirst but for managing graduate programs. The system will be used by visitors, students, instructors and the registar. Visitors can browse the site viewing basic information such as classes and students. Students can manage courses they are taking. Instructors access courses assigned by the registrar and the registrar is the administrator that manages the whole site. The features in this system will allow these users to access the information needed. Included in the system is the home, account, course page and complaints. Home will be the main page where all users will start off. Account will have basic information about the student and instructor. Course page manages the courses for students and instructors. Lastly, the complaints are for the complaints about other students, instructors or courses. To begin exploring and learning more about the website launch the website then Login and Register -> index.html.

We did our meetings on a frequency of once a week for this project since the meetings help us decide on what the next step was. 

Here is our first phase report: 
[Phase I Report](https://github.com/tryingtolearn11/322_project/blob/main/Software_Requirements_Spec.pdf)

Here is our second phase report:
[Phase II Report](https://github.com/tryingtolearn11/322_project/blob/main/Design_Report_Phase_2.pdf)

#File Structure and Set-Up
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

#Website Organization
-
- form.py - This is where all the forms we created are stored in and called when needed
- models.py - The mini database where data is created and stored
- routes.py - This is where all the code for routes are stored in
- database.py - This is where the functions using the database will be stored in eg. sorting functions
- All the html stuff is for each page 

#Create Virtual Environment from Python3

   	- Need to have pip installed
	- $ python3 -m venv venv
	- $ source venv/bin/activate

#Requirements

    - $ pip install -r requirements.txt  //install all packages needed

#Run the Program
	
	- $ flask run
