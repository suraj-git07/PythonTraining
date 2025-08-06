from flask_sqlalchemy import SQLAlchemy
from . import db
from sqlalchemy import event
from datetime import datetime, timedelta
from sqlalchemy.orm import validates
from flask_login import UserMixin
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """Common model for restaurants and customers"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # 1 for Customer, 2 for restaurant
    code = db.Column(db.String(1), nullable=False)
    password = db.Column(db.String(80), nullable=False, unique=True)
    phone = db.Column(db.String(12), nullable=False, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)


class Restaurant(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # owner
    name = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.String(255))  # Optional description
    image_url = db.Column(db.String(
        255), default='https://ts2.mm.bing.net/th?id=OIP.flfRXchgvSimFVzipmTJXQAAAA&pid=15.1')
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)
    rating = db.Column(db.Float)
    # Relationship for easy access
    foods = db.relationship('Food', backref='restaurant', lazy=True)
    orders = db.relationship('OrderList', backref='restaurant', lazy=True)


class Address(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_address = db.Column(db.String(80), nullable=False, index=True)
    city = db.Column(db.String(80), nullable=False)
    location = db.Column(db.String(80), nullable=False, index=True)

class Food(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    cuisine_id = db.Column(db.Integer, db.ForeignKey(
        'cuisine.id'), nullable=False)
    # eg-starters,main course,desert etc.
    category = db.Column(db.String(80), nullable=False, default='All Dishes')
    is_special = db.Column(db.Boolean, default=False)  # Today's special
    is_deal_of_day = db.Column(db.Boolean, default=False)  # Deal of the day


class Cuisine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class OrderList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    # d-delivered, p-pending, c-cancelled
    status = db.Column(db.String(1), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    delivery_time = db.Column(db.DateTime)


class OrderDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(
        'order_list.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)



# PREFERENCES
class FavouriteRestaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    # 'a' for auto, 'm' for manual
    mode = db.Column(db.String(1), nullable=False)


class FavouriteFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    # 'a' for auto, 'm' for manual
    mode = db.Column(db.String(1), nullable=False)


class DishReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order_list.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255))
    review_time = db.Column(db.DateTime, nullable=False, default=datetime.now)


class RestaurantReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order_list.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(255))
    review_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

