from flask import Flask

app = Flask(__name__)

# TODO: This secret key is temporary
# It will need its own file in the future
# that will not get pushed to the repo.
# FOR NOW, it remains here and just ignore it
app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes
