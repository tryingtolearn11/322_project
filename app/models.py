
class User():
    id = 0
    username = ""
    email = ""
    password_hash = ""
    posts = []

    def __repr__(self):
        return '<User> {}>'.format(self.username)

    
