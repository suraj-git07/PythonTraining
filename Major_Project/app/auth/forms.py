""" Forms for auth"""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields import StringField, IntegerField, PasswordField


class LoginForm(FlaskForm):

    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
