from app import app
from app.models import User,registered_users_table,Student,Course,registered_courses_table, CourseClass, Instructor, registered_classes_table

@app.shell_context_processor
def make_shell_context():
    return {'User' : User, 'registered_users_table': registered_users_table,
            'Student' : Student, 'Course' : Course, 'registered_courses_table': registered_courses_table, 
            'CourseClass': CourseClass, 'Instructor': Instructor,
            'registered_classes_table': registered_classes_table}



