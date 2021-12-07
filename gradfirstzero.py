from app import app
from app.models import User, registered_users_table,Student,generateDummyStudent, Course, registered_courses_table, CourseClass

@app.shell_context_processor
def make_shell_context():
    return {'User' : User, 'registered_users_table': registered_users_table,
            'Student' : Student, 'generateDummyStudent': generateDummyStudent,
            'Course' : Course, 'registered_courses_table':
            registered_courses_table, 'CourseClass': CourseClass}



