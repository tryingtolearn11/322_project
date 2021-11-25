from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from wtforms import TextField, TextAreaField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')



class ComplaintForm(FlaskForm):
    name = TextField("Name")
    subject = TextField("Subject")
    complaint = TextAreaField("Complaint")
    send = SubmitField("Submit")
    



