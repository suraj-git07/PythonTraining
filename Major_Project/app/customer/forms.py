""" forms for customer"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    name_filter = StringField('Search')
    submit = SubmitField('Search')

class UpdateProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=50)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10, max=100)])
    submit = SubmitField('Update Profile', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')

class DishReviewForm(FlaskForm):
    rating = IntegerField('Dish Rating (1-5)', validators=[DataRequired()])
    review = TextAreaField('Dish Review', validators=[Length(max=255)])
    submit = SubmitField('Submit Dish Review')

class RestaurantReviewForm(FlaskForm):
    rating = IntegerField('Restaurant Rating (1-5)', validators=[DataRequired()])
    review = TextAreaField('Restaurant Review', validators=[Length(max=255)])
    submit = SubmitField('Submit Restaurant Review')