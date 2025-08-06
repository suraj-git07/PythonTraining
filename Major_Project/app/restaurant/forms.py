from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, PasswordField, TimeField, URLField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo

class UpdateItemForm(FlaskForm) : 
    food_name = StringField("food name", validators=[DataRequired()])
    price = FloatField("price", validators=[DataRequired()])
    cuisine = StringField("cuisine", validators=[DataRequired()])
    category = StringField("category", validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')

class RestaurantForm(FlaskForm):
    name = StringField('Restaurant Name', validators=[DataRequired(), Length(max=80)])
    description = TextAreaField('Description', validators=[Length(max=255)])
    image_url = URLField('Image URL', validators=[Length(max=255)])
    opening_time = TimeField('Opening Time', validators=[DataRequired()])
    closing_time = TimeField('Closing Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Save')

class MenuItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(max=80)])
    price = FloatField('Price', validators=[DataRequired()])
    cuisine_id = SelectField('Cuisine', coerce=int, validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired(), Length(max=80)])
    is_special = SelectField('Today\'s Special', choices=[(0, 'No'), (1, 'Yes')], coerce=int, default=0)
    is_deal_of_day = SelectField('Deal of the Day', choices=[(0, 'No'), (1, 'Yes')], coerce=int, default=0)
    submit = SubmitField('Save')

class DishReviewForm(FlaskForm):
    rating = IntegerField('Dish Rating (1-5)', validators=[DataRequired()])
    review = TextAreaField('Dish Review', validators=[Length(max=255)])
    submit = SubmitField('Submit Dish Review')

class RestaurantReviewForm(FlaskForm):
    rating = IntegerField('Restaurant Rating (1-5)', validators=[DataRequired()])
    review = TextAreaField('Restaurant Review', validators=[Length(max=255)])
    submit = SubmitField('Submit Restaurant Review')

