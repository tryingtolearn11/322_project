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


PERIOD = {
    'class-setup': 0,
    'course-registration': 1,
    'class-running': 2,
    'grading': 3
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
    def generate_ID(digits):
        object_id = ''.join(["{}".format(randint(0, 9)) for num in range(0, digits)])
        return object_id


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










# Instructor Format
class Instructor(User):
    def __init__(self, *args, **kwargs):
        super(Instructor, self).__init__(*args, **kwargs)
        self.past_classes = {}
        self.current_classes = {}
        self.cancelled_classes = {}
        self.terminated = False
        self.suspended = False
        self.warning = 0


    def addWarnings(self, warningCount):
        self.warning += warningCount
        if self.warning >= 3:
            self.suspended = True
            print("Instructor Will be suspended")


    def addClass(self, course_class):
        course = Course.get(course_class)
        if course != None:
            print(course)
            self.current_classes[course.courseID] = course
        else:
            print("Class doesn't exist")


    def __repr__(self):
        return '<Instructor {}, Teaching {}>'.format(self.username, self.current_classes)




# Student Format
class Student(User):
    def __init__(self, *args, **kwargs):
        super(Student, self).__init__(*args, **kwargs)
        self.student_id = User.generate_ID(8)
        self.oldGPA = None
        self.grades = {}
        self.droppedCourses = {}
        self.currentClasses = {}
        self.suspended = False
        self.terminated = False
        self.warning = 0
        self.overallGPA = 0
        self.gpaBySemester = []
        self.coursesBySemester = []
        self.shoppingCart = []
        self.registered_next_semester = []


    def addToShoppingCart(self, courseID):
        c = CourseClass.get(courseID)
        if c not in self.shoppingCart:
            self.shoppingCart.append(c)
        else:
            print("Class {} is already in shopping cart".format(CourseClass.get(courseID).classID))

    def removeFromShoppingCart(self, courseID):
        c = CourseClass.get(courseID)
        if c in self.shoppingCart:
            self.shoppingCart.remove(c)
            print("{} Class is removed".format(c.courseName))
        else:
            print("Class {} is not in shopping cart".format(CourseClass.get(courseID).classID))



    def enrollCart(self):
        if len(self.shoppingCart) == 0:
            print("Empty Cart")
        else:
            for c in self.shoppingCart:
                self.registered_next_semester.append(c)
                c.seatsNextSemester += 1
                c.enrolledNextSemester.append(self)
            self.shoppingCart = []

    def addGrade(self, grade, course):
        self.grades[course.courseID] = [grade, course]
        print(self.currentClasses)
        classes = course.class_list
        for c in classes:
            if self in c.roster:
                print("{} is found in class {}".format(self.username, c.classID))
                c.removeStudent(self)
                c.passedStudents.append(self)
                self.currentClasses.pop(c.courseID)
                print("{} Grades : {}".format(self.username, self.grades))
            else:
                print("Student {} not found in this class".format(self.username))



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
        numOfClasses = 0
        if len(self.grades) == 0:
            return None
        for key, value in self.grades.items():
            grade_value += Student.convertLetterToGrade(value[0])
            numOfClasses += 1
        print("Grade value {}, credits {}".format(grade_value, credit))
        gpa = float(grade_value / numOfClasses)
        self.gpaBySemester.append(gpa)
        print(gpa)
        return gpa

    def evaluateGPA(self):
        semester_gpa = self.calculateGPA()
        overall_gpa = 0
        
        if semester_gpa == None:
            return None

        else:
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
            print("Student Eligible for Graduation!")
            self.graduationStatus = True
        else:
            print("Reckless Graduation application")
            self.addWarnings(1)
            self.graduationStatus = False
        return self.graduationStatus


    def addWarnings(self, warningCount):
        self.warning += warningCount
        if self.warning >= 3:
            self.suspended = True
            print("Student Will be suspended")

    def addClass(self, class1):
        self.currentClasses[class1.courseName] = class1

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


class Course:
    def __init__(self, courseID, courseName, credits, year, professorName, avg_rating, time, room, status):
        self.courseID = courseID
        self.courseName = courseName
        self.credits = credits
        self.year = year
        self.professorName = professorName
        self.avg_rating = avg_rating
        self.time = time
        self.room = room
        self.status = status
        self.cancelled = False
        self.class_list = []

    # def assignInstructor(self, instructor):

    def addClass(self, class1):
        self.class_list.append(class1)


    def __repr__(self):
        return '<Course {}, {}>'.format(self.courseID, self.courseName)


    @classmethod
    def get(cls, courseID):
        for course in registered_courses_table:
            if courseID == course.courseID:
                return course
        for course in registered_courses_table_nextSemester:
            if courseID == course.courseID:
                return course
        print("Course Not Found in DB")
        return None




class CourseClass(Course):
    def __init__(self, *args, **kwargs):
        super(Course, self).__init__(*args, **kwargs)
        self.classID = User.generate_ID(5)
        self.roster = []
        self.instructor = None
        self.courseID = None
        self.courseName = None
        self.credits = None
        self.year = None
        self.passedStudents = []
        self.enrolledNextSemester = []
        self.seatsNextSemester = 0

    def setCourseID(self, courseID):
        course = Course.get(courseID)
        if course in registered_courses_table or course in registered_courses_table_nextSemester:
            #print("found")
            #print(course)
            self.courseID = course.courseID
            self.courseName = course.courseName
            self.credits = course.credits
            self.year = course.year
        else:
            print("Course ID Not Found")



    # quick hack version of addStudent
    def addStudent(self, student):
        self.roster.append(student)
        student.currentClasses[self.courseID] = self

    def removeStudent(self, student):
        self.roster.remove(student)

    def checkClassStatus(self):
        if len(self.roster) < 5:
            self.cancelled = True

    def assignInstructor(self, instructor):
        self.instructor = instructor
        instructor.current_classes[self.classID] = self



    @classmethod
    def get(cls, courseID):
        for c in registered_classes_table:
            if courseID == c.courseID:
                return c
        for c in registered_classes_table_nextSemester:
            if courseID == c.courseID:
                return c
        print("Class Not Found in DB")
        return None

    def __repr__(self):
        return '<Class {}, {}>'.format(self.classID, self.courseName)






# Dummy Data
registered_users_table = [
    User("susan", 'cat'), # Registrars
    User("josh", "miranda"),
    User("jinx", 'arcane'),
    Instructor("john", 'dog'), # Instructor
    Instructor("mary", 'bad'),
    Instructor("hank",'bird'),
    Instructor("bob", 'duncan'),
    Instructor("julia", 'twitch'),
    Student("tom",'fish'),
    Student("max",'mouse'),
    Student("jax",'rat'),
    Student("sofia",'snake'),
    Student("damien",'singh'),
    Student("bill", 'monkey'),
    Student("frank",'night'),
    Student("katy", "wenis")
]

all_registrars = [
    User("susan", 'cat'),
    User("josh", "miranda"),
    User("jinx", 'arcane')]

all_instructors = [
    Instructor("john", 'dog'),
    Instructor("mary", 'bad'),
    Instructor("hank",'bird'),
    Instructor("bob", 'duncan'),
    Instructor("julia", 'twitch')]

all_students = [
    Student("tom",'fish'),
    Student("max",'mouse'),
    Student("jax",'rat'),
    Student("sofia",'snake'),
    Student("damien",'singh'),
    Student("bill", 'monkey'),
    Student("frank",'night'),
    Student("katy", "wenis")]





registered_courses_table = [
    Course("1A", "Software", "3", "2021", "john", "5", "9:00 am - 10:15 am", "NAC 1/103", "Open"),
    Course("1B", "Software", "3", "2021", "mary", "5", "11:00 am - 2:15 pm", "ONLINE", "Open"),
    Course("2A", "Data Structures", "3", "2021", "john", "3", "10:00 am - 11:15 am", "NAC 2/203", "Open"),
    Course("3A", "Algorithms", "3", "2021", "john", "3", "11:00 am - 12:15 pm", "NAC 2/204", "Closed"),
    Course("4A", "Statistics", "3", "2021", "mary", "4", "9:00 am - 11:15 am", "ONLINE", "Closed"),
    Course("5A", "Operating System", "4", "2021", "hank", "1", "8:00 am - 10:15 am", "NAC 1/115", "Open"),
    Course("6A", "Intro to Computer Science", "3", "2021", "hank", "2", "12:00 pm - 3:15 pm", "NAC 5/502", "Open"),
    Course("7A", "Java", "3", "2021", "bob", "1", "10:00 am - 11:15 am", "Sheperd 2/209", "Open"),
    Course("8A", "Technical Elective 1", "3", "2021", "mary", "4", "8:00 am - 9:00 am", "NAC 3/306", "Open"),
    Course("9A", "Technical Elective 2", "3", "2021", "julia", "2", "3:00 pm - 4:15 pm", "NAC 1/104", "Closed")]



registered_courses_table_nextSemester = [
        Course("1B", "Software", "3", "2022", "100", "5", "9:00 am - 10:15 am", "NAC 1/103", "Open"),
        Course("2B", "Data Structures", "3", "2022", "100", "2", "10:00 am - 11:15 am", "NAC 2/203", "Open"),
        Course("3B", "Algorithms", "3", "2022", "100", "1", "11:00am - 12:15 pm", "NAC 2/204", "Closed"),
        Course("4B", "Statistics", "3", "2022", "100","4", "9:00 am - 11:15 am", "ONLINE","Closed"),
        Course("5B", "Operating System", "4", "2022", "100", "1", "8:00 am - 10:15 am", "NAC 1/115", "Open")]



registered_users_complaints = [
    User('susan', 'cat').Complaint('susan', '332')
]


# Classes
c1 = CourseClass()
c1.setCourseID("1A")
c1.addStudent(User.get("max"))
c1.addStudent(User.get("jax"))
c1.addStudent(User.get("sofia"))
c1.assignInstructor(User.get("john"))

course1A = Course.get("1A")
course1A.addClass(c1)


c2 = CourseClass()
c2.setCourseID("2A")
c2.addStudent(User.get("max"))
c2.addStudent(User.get("jax"))
c2.addStudent(User.get("sofia"))
c1.assignInstructor(User.get("mary"))

c3 = CourseClass()
c3.setCourseID("3A")



c1B = CourseClass()
c1B.setCourseID("1B")
Course.get("1B").addClass(c1B)



registered_classes_table = [c1, c2, c3]
registered_classes_table_nextSemester = [c1B]

Max = User.get("max")





Tom = User.get("tom")
Tom.addGrade("A", Course.get("1A"))
Tom.addGrade("B+", Course.get("2A"))
Tom.addGrade("C-", Course.get("3A"))
Tom.addGrade("A+", Course.get("4A"))
Tom.addGrade("A", Course.get("5A"))

# Current classes
Tom.addClass(CourseClass.get("1A"))
Tom.addClass(CourseClass.get("2A"))
Tom.addClass(CourseClass.get("3A"))
Tom.evaluateGPA()

