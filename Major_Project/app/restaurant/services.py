from app.models import User,Restaurant, Address, Food, Cuisine, OrderList, OrderDetail, Cart
from app import db
from collections import Counter
from functools import wraps
from flask_login import current_user
from flask import jsonify,flash
from datetime import timedelta,datetime
from sqlalchemy.sql import func
from .helper import *

def dont_allow_non_restaurants(function):
    @wraps(function)
    def wrapper(*args, **kwargs) :
        if current_user.code not in ('0','2') :  # 0 for admin , 2 for restaurants
            return jsonify({"error": "Functionality not allowed for customers"}), 403
        return function(*args, **kwargs)
    return wrapper

@check_transaction_complete
def get_restaurant_id_by_user_id(user_id):
    restaurant_id = Restaurant.query.join(User,Restaurant.user_id == user_id).filter(
        User.id == user_id).first().id
    return restaurant_id

@check_transaction_complete
def get_mostly_ordered_items(restaurant_id):

    ORDER_LIMIT = 3
    
    food_items = Food.query.join(Restaurant , Food.restaurant_id == Restaurant.id).join(
        OrderDetail,Food.id == OrderDetail.food_id).join(
            OrderList,OrderDetail.order_id == OrderList.id).filter(
                OrderList.order_time > datetime.now() - timedelta(hours=24)
            ).group_by(Food.id).having(
                func.count(Food.id)>=ORDER_LIMIT
            ).filter(Restaurant.id == restaurant_id).all()
   

    print("mostly ordered",food_items)
    return food_items


@check_transaction_complete
def get_orders_for_restaurant(restaurant_id):
    """
    Returns a list of orders for a given restaurant.
    """

    query = OrderList.query.filter(OrderList.restaurant_id==restaurant_id)

    pending_orders = query.filter(OrderList.status=='p').all()
    delivered_orders = query.filter(OrderList.status=='d').all()
    cancelled_orders = query.filter(OrderList.status=='c').all()

    return pending_orders, delivered_orders, cancelled_orders

@check_transaction_complete
def get_order_details(order_id):
    """
    Returns the details of an order.
    """
    query = OrderDetail.query.filter_by(order_id=order_id)

    customer_id = OrderList.query.filter(OrderList.id == order_id).first().customer_id

    return query.all(), customer_id

@check_transaction_complete
def get_menu_for_restaurant(restaurant_id):

    menu = Food.query.filter(Food.restaurant_id==restaurant_id).all()
    menu_items = []
    for item in menu :
        menu_items.append(
            {"id" : item.id,
             "name" : item.name,
             "price" :item.price,
             "cuisine" : Cuisine.query.join(Food,Cuisine.id == Food.cuisine_id).filter(Food.cuisine_id == item.cuisine_id).first().name,
             "category" : item.category
            
            }
        )
    return menu_items

@check_transaction_complete
def mark_order_delivered(order_id):
    """
    Marks an order as delivered.
    """
    order = OrderList.query.get(order_id)
    if order and order.status == 'p':
        order.status = 'd'
        order.delivery_time = datetime.now()
        db.session.commit()
        return True,"order marked as delivered"
    else:
        return False,"order not found or already delivered"
    
@check_transaction_complete
def remove_dish_from_menu(food_id):
    if current_user.code not in  ('0','2') :  # 0 for admin , 2 for restaurants
        return False, "You are not allowed to remove this dish"
    
    if Food.query.get(food_id).restaurant_id != get_restaurant_id_by_user_id(current_user.id):
        return False, "You are not allowed to remove this dish"

    food = Food.query.get(food_id)
    if food:
        db.session.delete(food)
        db.session.commit()
        return True, "Dish removed successfully"
    else:
        return False, "Dish not found in the menu"



@check_transaction_complete
def add_dish_to_menu(restaurant_id, food_name, price, cuisine_name, category):

    food_name = food_name.capitalize()
    cuisine_name = cuisine_name.capitalize()
    category = category.capitalize()
    # cuisine_name = cuisine_name.split('')

    cuisine= Cuisine.query.filter(Cuisine.name == cuisine_name).first()

    if not cuisine :
        return False,"Cuisine Does not exists in records"
    cuisine_id = cuisine.id
    food = Food(restaurant_id = restaurant_id, name = food_name , price = price , cuisine_id = cuisine_id, category = category)

    db.session.add(food)
    db.session.commit()
    return True, "Dish added succesfully"

def get_order_count_for_restaurant(restaurant_id):
    orders_for_restaurant = OrderList.query.join(OrderDetail,OrderDetail.order_id == OrderList.id).join(
        Food,OrderDetail.food_id == Food.id).join(
            Restaurant,Restaurant.id == Food.restaurant_id
        ).filter(Restaurant.id == restaurant_id)
    
    pending_order_counts = orders_for_restaurant.filter(OrderList.status =='p').count()
    cancelled_order_counts = orders_for_restaurant.filter(OrderList.status =='c').count()
    delivered_order_counts = orders_for_restaurant.filter(OrderList.status =='d').count()
    total_order_counts = pending_order_counts + cancelled_order_counts + delivered_order_counts

    return pending_order_counts, cancelled_order_counts, delivered_order_counts, total_order_counts

def delete_food_from_menu(food_id):
    food_item = Food.query.get(food_id)

    # If food exists, delete it
    if food_item:
        db.session.delete(food_item)
        db.session.commit()
        flash("Food item deleted successfully!", "success")
    else:
        flash("Food item not found.", "danger")

  
def get_restaurant_open_and_close_time(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        if datetime.now > restaurant.opening_time and datetime.now() < restaurant.closing_time:
            return True,restaurant.opening_time, restaurant.closing_time
        return False,restaurant.opening_time, restaurant.closing_time
    else:
        return None, None, None


def get_restaurant_details(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if not restaurant:
        return None, None
    location = Address.query.filter(
        Address.user_id == restaurant.user_id).first().location
    phone = User.query.filter(User.id == restaurant.user_id).first().phone
    email = User.query.filter(User.id == restaurant.user_id).first().email

    restaurant_info = {
        'id': restaurant.id,
        'name': restaurant.name,
        'location': location,
        'phone': phone,
        'email': email,
        'opening_time': restaurant.opening_time,
        'closing_time': restaurant.closing_time
    }

    menu = Food.query.filter(Food.restaurant_id == restaurant_id).all()

    return restaurant_info, menu


