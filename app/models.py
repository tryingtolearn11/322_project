from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin):

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.password_hash = None
        self.posts = []

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '<User {}, Email {}>'.format(self.username, self.email)

    
    @property
    def id(self):
        return self.username

@login.user_loader
def load_user(user):
    return User.get(user)
    
