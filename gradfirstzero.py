from app import app
from app.models import User, registered_users_table, Student, generateDummyStudent, Course

@app.shell_context_processor
def make_shell_context():
    return {'User' : User, 'registered_users_table': registered_users_table,
            'Student' : Student, 'generateDummyStudent' : generateDummyStudent,
            'Course' : Course}



