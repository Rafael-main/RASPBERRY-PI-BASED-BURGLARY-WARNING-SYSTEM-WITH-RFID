from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired, Email


class LoginForm(FlaskForm):
    login_username = StringField('Username', validators=[InputRequired()])
    login_password = PasswordField('Password', validators=[InputRequired()])
    login_submit = SubmitField('Log in')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    signup_submit = SubmitField('Sign Up')