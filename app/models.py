from app import login
from random import randint
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


ACCESS = {
    'visitor' : 0,
    'student' : 1,
    'instructor' : 2,
    'registrar' : 3
}


class User(UserMixin):
    def __init__(self, username, password, access=ACCESS['student']):
        self.username = username
        self.email = ""
        self.password_hash = generate_password_hash(password)
        self.posts = []
        self.access = access


    def allowed(self, access_level):
        return self.access >= access_level

    def is_registrar(self):
        return (self.access == ACCESS['registrar'])

    def set_registrar(self):
        self.access = ACCESS['registrar']

    def set_instructor(self):
        self.access = ACCESS['instructor']

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def generate_StudentID(digits):
        student_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, digits)])
        return student_id


    def __repr__(self):
        return '<User {}, Password {}>'.format(self.username,
                                               self.password_hash)

    @classmethod
    def get(cls, username):
        for user in registered_users_table:
            if username == user.username:
                return user
        print("User Not Found in DB")
        return None

    
    @property
    def id(self):
        return self.username



    
    class Complaint():
        def __init__(self, name, subject):
            self.name = name
            self.subject = subject
            self.content = None

        def set_complaint(self, content):
            self.content = content


        def __repr__(self):
            return '<Name {}\n, Subject {}\n, Content {}\n>'.format(self.name,
                                                                    self.subject,
                                                                    self.content)


class Student(User):
    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self.student_id = User.generate_StudentID(8)
        self.grades = {}
        self.droppedCourses = {}
        self.currentClasses = {}
        self.suspended = False
        self.terminated = False
        self.warning = 0
        self.overallGPA = 0
        self.gpaBySemester = []
        self.coursesBySemester = []


    def addGrade(self, courseID, grade, course, credits, year):
        self.grades[courseID] = [grade, course, credits, year]


    @staticmethod
    def convertLetterToGrade(letterGrade):
        if letterGrade == "A+" or letterGrade == "A":
            return 4
        elif letterGrade == "A-":
            return 3.7
        elif letterGrade == "B+":
            return 3.3
        elif letterGrade == "B":
            return 3
        elif letterGrade == "B-":
            return 2.7
        elif letterGrade == "C+":
            return 2.3
        elif letterGrade == "C":
            return 2
        elif letterGrade == "C-":
            return 1.7
        elif letterGrade == "D+":
            return 1.3
        elif letterGrade == "D":
            return 1
        elif letterGrade == "D-":
            return 0.7
        else: 
            return 0
        

    def calculateGPA(self):
        grade_value = 0
        credit = 0
        numOfCredits = 0
        for key, value in self.grades.items():
            grade_value += Student.convertLetterToGrade(value[0])
            credit += int(value[2])
            numOfCredits += 1
            print("Grade value {}, credits {}".format(grade_value, credit))
        gpa = float(grade_value / numOfCredits)
        self.gpaBySemester.append(gpa)
        return gpa

    def evaluateGPA(self):
        semester_gpa = self.calculateGPA()
        overall_gpa = 0

        for i in self.gpaBySemester:
            overall_gpa += i
        self.overallGPA = overall_gpa / len(self.gpaBySemester)

        if semester_gpa >= 2 and semester_gpa <= 2.25:
            self.addWarnings(1)

        if semester_gpa >= 3.75 or self.overallGPA > 3.5:
            self.honorRoll = True
            # Can remove 1 warning if any
            if self.warning > 0:
                self.warning -= 1



    def applyForGraduation(self):
        self.evaluateGPA()
        if len(self.grades) >= 8 and self.overallGPA >= 2:
            self.graduationStatus = True
            print("Student Eligible for Graduation!")
        else:
            print("Reckless Graduation application")
            self.addWarnings(1)


    def addWarnings(self, warningCount):
        self.warning += warningCount
        if self.warning >= 3:
            self.suspended = True
            print("Student Will be suspended")

    def addClass(self, courseID, course, credits, year):
        self.currentClasses[courseID] = ["N/A", course, credits, year]

    def dropClass(self, courseID):
        try:
            course_info = self.currentClasses[courseID] 
            self.currentClasses.pop(courseID)
            self.droppedCourses[courseID] = ["W", course_info[1], course_info[2], course_info[3]]
            if len(self.currentClasses) == 0:
                self.addWarnings(3)

        except KeyError as ex:
            print("No such Course: '%s'" % ex.message)

    
    def __repr__(self):
        return '<Student {}, {}>'.format(self.student_id, self.username)


@login.user_loader
def load_user(user):
    return User.get(user)



# Dummy Data

registered_users_table = [
    User("susan", 'cat'), # Registrars
    User("john", 'dog'), # Instructor
    User("tom",'fish')] # Student

registered_users_complaints = [
    User('susan', 'cat').Complaint('susan', '332')
]


def generateDummyStudent():
    s = Student("damien", "singh")
    s.addGrade("a", "C+", "swe", "3", "2021")
    s.addGrade("b", "A+", "sw", "4", "2021")
    s.addGrade("c", "A-", "sw", "4", "2021")
    s.addGrade("d", "B-", "sw", "4", "2021")
    s.addGrade("e", "A-", "sw", "3", "2021")
    s.addGrade("f", "A-", "sw", "3", "2021")
    s.addGrade("g", "B", "sw", "3", "2021")

    # Current classes

    s.addClass("1", "www", "4", "2021")
    s.addClass("3", "yyy", "3", "2021")
    s.addClass("4", "xxx", "4", "2021")
    s.addClass("2", "zzz", "3", "2021")
    s.addClass("5", "aaa", "4", "2021")
    
    s.dropClass("5")
    s.applyForGraduation()
    return s





