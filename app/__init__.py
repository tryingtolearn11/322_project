from flask import Flask
from config import Config
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)


login = LoginManager(app)
login.login_view = 'login'

app.jinja_env.filters['zip'] = zip

from app import routes
