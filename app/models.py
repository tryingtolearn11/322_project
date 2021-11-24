from app import login
from flask_login import UserMixin




class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.email = ""
        self.password_hash = password_hash
        self.posts = []

    def __repr__(self):
        return '<User> {}>'.format(self.username)

    
    @property
    def id(self):
        return self.username

@login.user_loader
def load_user(user):
    return User.get(user)
    
