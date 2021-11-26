from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.email = ""
        self.password_hash = generate_password_hash(password)
        self.posts = []

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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




@login.user_loader
def load_user(user):
    return User.get(user)




# Dummy Data
registered_users_table = [
    User("susan", 'cat'),
    User("john", 'dog'),
    User("tom",'fish')]

registered_users_complaints = [
    User('susan', 'cat').Complaint('susan', '332')
]





