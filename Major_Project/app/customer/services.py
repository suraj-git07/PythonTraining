"""Database services and other functionalities"""

from app.models import *
from app import db
from .helper import *
from collections import Counter, defaultdict
from flask_login import current_user
from functools import wraps
from flask import jsonify, redirect, url_for, flash, request
from sqlalchemy.sql import func, desc
from sqlalchemy import or_
from datetime import datetime, timedelta


def dont_allow_non_customers(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            # Always check authentication first
            if not current_user.is_authenticated:
                print("User not authenticated, redirecting to login with next URL")
                next_url = request.url  # Save the current URL
                return redirect(url_for('auth.login', next=next_url))
            
            print(f"Checking access for user {current_user.id} with code {current_user.code}")
            
            # If admin, allow access
            if current_user.code == '0':
                print("Admin access granted")
                return function(*args, **kwargs)
                
            # If not a customer, deny access
            if current_user.code != '1':
                print("User is not a customer or admin")
                flash('Access denied. This area is for customers only.', 'danger')
                return redirect(url_for('auth.logout'))
            
            # For customers, verify customer record exists
            customer = Customer.query.filter_by(user_id=current_user.id).first()
            print(f"Customer record found: {customer is not None}")
            if not customer:
                flash('Customer profile not found. Please contact support.', 'danger')
                return redirect(url_for('auth.logout'))
            
            print("Access granted, proceeding to view")
            return function(*args, **kwargs)
            
        except Exception as e:
            print(f"Error in dont_allow_non_customers: {str(e)}")
            db.session.rollback()  # Roll back any failed transaction
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('auth.logout'))
            
    return wrapper


def get_customer_id_from_user_id(user_id):
    try:
        print(f"Getting customer_id for user_id: {user_id}")
        customer = Customer.query.filter_by(user_id=user_id).first()
        if not customer:
            print(f"No customer found for user_id: {user_id}")
            return None
        print(f"Found customer_id: {customer.id}")
        return customer.id
    except Exception as e:
        print(f"Error in get_customer_id_from_user_id: {str(e)}")
        return None


def get_restaurant_list(customer_id, locations=None, min_rating=None, cuisines=None, name_filter=None, min_price=None):
    """Get list of restaurants based on filters"""
    try:
        print(f"Filtering restaurants with: locations={locations}, rating={min_rating}, cuisines={cuisines}, search={name_filter}, price={min_price}")
        
        # Start with base query
        query = Restaurant.query
        
        # Always join with Address for location info
        query = query.join(Address, Restaurant.user_id == Address.user_id)
        
        # Apply location filter first (most restrictive)
        if locations and len(locations) > 0:
            query = query.filter(Address.location.in_(locations))
            print(f"Applied location filter: {locations}")

        # Apply rating filter
        if min_rating:
            try:
                min_rating_val = float(min_rating)
                query = query.filter(Restaurant.rating >= min_rating_val)
                print(f"Applied rating filter: >= {min_rating_val}")
            except (ValueError, TypeError):
                print(f"Invalid rating value: {min_rating}")

        # Apply cuisine filter
        if cuisines and len(cuisines) > 0:
            # Use subquery to find restaurants that serve ANY of the selected cuisines
            cuisine_subquery = db.session.query(Food.restaurant_id).join(
                Cuisine, Food.cuisine_id == Cuisine.id
            ).filter(
                Cuisine.name.in_(cuisines)
            ).distinct().subquery()
            
            query = query.filter(Restaurant.id.in_(db.session.query(cuisine_subquery.c.restaurant_id)))
            print(f"Applied cuisine filter: {cuisines}")

        # Apply price filter
        if min_price is not None and min_price != '':
            try:
                min_price_val = float(min_price)
                # Find restaurants that have at least one item at or above the minimum price
                price_subquery = db.session.query(Food.restaurant_id).filter(
                    Food.price >= min_price_val
                ).distinct().subquery()
                
                query = query.filter(Restaurant.id.in_(db.session.query(price_subquery.c.restaurant_id)))
                print(f"Applied price filter: >= {min_price_val}")
            except (ValueError, TypeError):
                print(f"Invalid price value: {min_price}")

        # Apply search filter
        if name_filter and name_filter.strip():
            search_term = f"%{name_filter.strip()}%"
            
            # Create search conditions
            search_conditions = [
                Restaurant.name.ilike(search_term),
                Address.location.ilike(search_term)
            ]
            
            # Add cuisine search if not already filtering by specific cuisines
            if not cuisines or len(cuisines) == 0:
                cuisine_search_subquery = db.session.query(Food.restaurant_id).join(
                    Cuisine, Food.cuisine_id == Cuisine.id
                ).filter(
                    Cuisine.name.ilike(search_term)
                ).distinct().subquery()
                
                search_conditions.append(
                    Restaurant.id.in_(db.session.query(cuisine_search_subquery.c.restaurant_id))
                )
            
            query = query.filter(or_(*search_conditions))
            print(f"Applied search filter: {name_filter}")

        # Get distinct restaurants
        all_restaurants = query.distinct().all()
        print(f"Found {len(all_restaurants)} restaurants after filtering")
        
        if not all_restaurants:
            print("No restaurants found matching criteria")
            return []
            
        # Sort by favorites
        try:
            favourite_restaurant_objects = get_favourite_restaurants(customer_id)
            favourite_ids = {r.id for r in favourite_restaurant_objects}
            favourite_restaurants = [r for r in all_restaurants if r.id in favourite_ids]
            other_restaurants = [r for r in all_restaurants if r.id not in favourite_ids]
            
            result = favourite_restaurants + other_restaurants
            print(f"Returning {len(result)} restaurants ({len(favourite_restaurants)} favorites, {len(other_restaurants)} others)")
            return result
        except Exception as e:
            print(f"Error sorting by favorites: {e}")
            return all_restaurants
        
    except Exception as e:
        print(f"Error in get_restaurant_list: {str(e)}")
        import traceback
        traceback.print_exc()
        return []


def get_cuisines_for_restaurant(restaurant_id):
    """
    Retrieves the cuisines available for a specific restaurant.
    """
    cuisines = Cuisine.query.join(Food, Food.cuisine_id == Cuisine.id).join(
        Restaurant, Restaurant.id == Food.restaurant_id).filter(Restaurant.id == restaurant_id).all()

    return cuisines


def add_to_cart(food_id, customer_id):

    cart_item = Cart.query.filter(
        Cart.food_id == food_id, Cart.customer_id == customer_id).first()

    if cart_item:
        cart_item.quantity += 1
        db.session.commit()
        return True, "+1"
    else:
        cart_item = Cart(food_id=food_id, quantity=1, customer_id=customer_id)
        db.session.add(cart_item)
        db.session.commit()
        return True, "Item added to cart"


def remove_from_cart(food_id, customer_id):

    cart_item = Cart.query.filter(
        Cart.food_id == food_id, Cart.customer_id == customer_id).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

        return True, "removed item from cart"

    else:
        return False, "No matching item found in cart"


def subtract_from_cart(food_id, customer_id):

    cart_item = Cart.query.filter(
        Cart.food_id == food_id, Cart.customer_id == customer_id).first()

    if cart_item:

        if cart_item.quantity <= 1:
            return remove_from_cart(food_id=food_id, customer_id=customer_id)

        else:
            cart_item.quantity -= 1
            db.session.commit()
            return True, "-1"

    else:

        return False, "No matching item found in cart"


def get_cart_items(customer_id):
    cart_by_restaurant = split_cart_by_restaurant(customer_id)
    cart_items = Cart.query.filter_by(customer_id=customer_id).all()
    return cart_items


def clear_cart_for_customer(customer_id):
    cart_items = Cart.query.filter_by(customer_id=customer_id).all()
    for item in cart_items:
        db.session.delete(item)
    db.session.commit()
    return True, "Cart cleared successfully"


def split_cart_by_restaurant(customer_id):
    """
    Splits the cart items by restaurant and returns a dictionary with restaurant IDs as keys.
    Each value is a list of dictionaries containing 'cart', 'food', and 'restaurant' objects.
    """
    try:
        print(f"Splitting cart for customer_id: {customer_id}")
        
        # First get all cart items for this customer
        cart_items = Cart.query.filter_by(customer_id=customer_id).all()
        print(f"Found {len(cart_items)} cart items")

        if not cart_items:
            return False, "No items in the cart."

        # Group cart items by restaurant
        cart_by_restaurant = defaultdict(list)

        for cart_item in cart_items:
            # Get the food item
            food = Food.query.get(cart_item.food_id)
            if not food:
                print(f"Food item with id {cart_item.food_id} not found")
                continue
                
            # Get the restaurant
            restaurant = Restaurant.query.get(food.restaurant_id)
            if not restaurant:
                print(f"Restaurant with id {food.restaurant_id} not found")
                continue
                
            print(f"Processing item: {food.name} from {restaurant.name}")
            cart_by_restaurant[restaurant].append({
                'cart': cart_item,
                'food': food,
                'restaurant': restaurant
            })

        print(f"Grouped into {len(cart_by_restaurant)} restaurants")
        return True, cart_by_restaurant
        
    except Exception as e:
        print(f"Error in split_cart_by_restaurant: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, f"Error loading cart: {str(e)}"


def clear_cart_for_restaurant(customer_id, restaurant_id):
    """
    Clears the cart for a specific restaurant for a customer.
    """
    success, cart_by_restaurant = split_cart_by_restaurant(customer_id)
    if not success:
        return False, "No items in the cart."
    for dic_items in cart_by_restaurant[Restaurant.query.get(restaurant_id)]:

        cart_item = dic_items['cart']
        db.session.delete(cart_item)
    db.session.commit()

    return True, "Cart cleared successfully"


def clear_cart_for_all_restaurants(customer_id):
    cart = Cart.query.filter_by(customer_id=customer_id).all()
    for item in cart:
        db.session.delete(item)
    db.session.commit()

    return True, "Cart cleared successfully"


def place_order(customer_id):
    """
    Places an order for a customer by transferring cart items to the order table.
    Returns (bool, message) indicating success or failure.
    """
    success, cart_by_restaurants = split_cart_by_restaurant(customer_id)
    if not success:
        return False, "No items in the cart."
    cart_items = Cart.query.filter_by(customer_id=customer_id).all()

    print(cart_by_restaurants)

    for restaurant, items in cart_by_restaurants.items():
        rest_price = 0
        for item in items:
            rest_price += item['food'].price * item['cart'].quantity
        order = OrderList(customer_id=customer_id,
                          restaurant_id=restaurant.id, total_price=rest_price, status='p')
        db.session.add(order)
        db.session.flush()  # Ensure order ID is generated before using it

        order_details = [OrderDetail(
            order_id=order.id, food_id=item['food'].id, quantity=item['cart'].quantity) for item in items]

        db.session.add_all(order_details)

    # Create order details

    # Remove cart items after placing order
    Cart.query.filter_by(customer_id=customer_id).delete()

    
    db.session.commit()
    return True, "Order placed successfully!"


def cancel_order_by_customer(order_id, customer_id):
    """
    Cancels an order by setting its status to 'c' (cancelled).
    Returns True if successful, False otherwise.
    """
    order = OrderList.query.get(order_id)
    if not order or order.customer_id != customer_id:
        return False, "could not find the order"  # Order not found

    order.status = 'c'
    db.session.commit()
    return True, "cancelled the order succesfully"  # Successfully cancelled





def get_order_headers_for_customer(customer_id):
    pending_orders = OrderList.query.filter_by(
        customer_id=customer_id, status='p').order_by(desc(OrderList.id)).all()
    delivered_orders = OrderList.query.filter_by(
        customer_id=customer_id, status='d').order_by(desc(OrderList.id)).all()
    cancelled_orders = OrderList.query.filter_by(
        customer_id=customer_id, status='c').order_by(desc(OrderList.id)).all()
    all_orders = pending_orders + delivered_orders + cancelled_orders

    return pending_orders, delivered_orders, cancelled_orders, all_orders


def get_order_details(order_id):
    order_details = OrderDetail.query.filter_by(order_id=order_id).all()
    return order_details


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

    menu = Food.query.filter(Food.restaurant_id == restaurant_id)

    return restaurant_info, menu



def get_location_by_restaurant_id(restaurant_id):
    address = Address.query.join(Restaurant, Address.user_id == Restaurant.user_id) \
                           .filter(Restaurant.id == restaurant_id).first()
    # Avoids error if no address exists
    return address.location if address else "Unknown"


def get_restaurants_by_cuisine(cuisine_name):
    cuisine_id = Cuisine.query.filter(Cuisine.name == cuisine_name)
    restaurants = Restaurant.join(Food, Food.restaurant_id == Restaurant.id).Filter(
        Food.cuisine_id == cuisine_id
    )

    restaurants = restaurants.all()

    return restaurants


def get_order_count_for_customer(restaurant_id):
    orders_for_customer = OrderList.query.join(OrderDetail, OrderDetail.order_id == OrderList.id).join(
        Food, OrderDetail.food_id == Food.id).join(
            Restaurant, Restaurant.id == Food.restaurant_id
    )

    pending_order_counts = orders_for_customer.filter(
        OrderList.status == 'p').count()
    cancelled_order_counts = orders_for_customer.filter(
        OrderList.status == 'c').count()
    delivered_order_counts = orders_for_customer.filter(
        OrderList.status == 'd').count()

    total_order_counts = pending_order_counts + \
        cancelled_order_counts + delivered_order_counts

    return pending_order_counts, cancelled_order_counts, delivered_order_counts, total_order_counts


def get_restaurant_open_and_close_time(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)

    if restaurant:
        if datetime.now().time() > restaurant.opening_time and datetime.now().time() < restaurant.closing_time:
            return True, restaurant.opening_time, restaurant.closing_time
        return False, restaurant.opening_time, restaurant.closing_time
    else:
        return None, None, None


def get_customer_profile(customer_id):
    orders = get_order_headers_for_customer(customer_id)

    customer_profile = {}
    user = User.query.filter(
        User.id == Customer.query.get(customer_id).user_id).first()
    customer_profile['name'] = Customer.query.get(customer_id).name
    customer_profile['email'] = User.query.get(
        Customer.query.get(customer_id).user_id).email
    customer_profile['address'] = Address.query.filter(
        Address.user_id == user.id).first()
    customer_profile['orders'] = orders
    customer_profile['order_count'] = len(orders)
    customer_profile['phone'] = User.query.get(
        Customer.query.get(customer_id).user_id).phone

    return customer_profile


def update_customer_profile(customer_id, name, phone, email, address):
    try:
        user = User.query.filter(
            User.id == Customer.query.get(customer_id).user_id).first()
        print("starting update")
        if not user:

            return False, "User not found"
        if not address:

            return False, "Please enter address"
        if not name:

            return False, "Please enter name"
        if not phone:

            return False, "Please enter phone number"
        if not email:

            return False, "Please enter email"
        if not is_valid_email(email):

            return False, "Please enter valid email"
        if not is_valid_phone(phone):

            return False, "Please enter valid phone number"
        
        customer_id = get_customer_id_from_user_id(user.id)
        customer = Customer.query.get(customer_id)
        customer.name = name
        user.phone = phone
        user.email = email
        address_obj = Address.query.filter(
            Address.user_id == user.id).first()
        address_obj.full_address = address

        db.session.commit()
        print("successfull in updatiion")

        return True, "Profile updated successfully"

    except Exception as e:
        print("error in updating profile", e)
        db.session.rollback()
        return False, "unable to update the profile, please try again later"


def add_restaurant_to_favourite(restaurant_id, customer_id):
    """
    Adds a restaurant to the customer's favourites.
    """
    print(restaurant_id,Restaurant.query.get(restaurant_id).name)
    fav_obj = FavouriteRestaurant(
        customer_id=customer_id, restaurant_id=restaurant_id, mode='m')
    db.session.add(fav_obj)
    db.session.commit()

    return True, "Restaurant added to favourites"


def remove_restaurant_from_favourite(restaurant_id, customer_id):
    """
    Removes a restaurant from the customer's favourites.
    """
    fav_obj = FavouriteRestaurant.query.filter(
        FavouriteRestaurant.customer_id == customer_id,
        FavouriteRestaurant.restaurant_id == restaurant_id).first()
    if not fav_obj:
        return False, "restaurant not found in favourites"

    db.session.delete(fav_obj)
    db.session.commit()

    return True, "Restaurant removed from favourites"


def add_food_to_favourite(food_id, customer_id):
    """
    Adds a Food item to the customer's favourites.
    """
    fav_obj = FavouriteFood(customer_id=customer_id, food_id=food_id, mode='m')
    db.session.add(fav_obj)
    db.session.commit()

    return True, "Food added to favourites"


def remove_food_from_favourite(food_id, customer_id):
    fav_obj = FavouriteFood.query.filter(
        FavouriteFood.customer_id == customer_id,
        FavouriteFood.food_id == food_id).first()
    if not fav_obj:
        return False, "Food not found in favourites"

    db.session.delete(fav_obj)
    db.session.commit()

    return True, "Food removed from favourite"


def get_favourite_foods(customer_id):
    fav_foods = FavouriteFood.query.filter(
        FavouriteFood.customer_id == customer_id).all()
    food_ids = [fav.food_id for fav in fav_foods]
    foods = Food.query.filter(
        Food.id.in_(food_ids)).all()
    food_ids = set([food.id for food in foods])
    return food_ids


def is_favourite_food(food_id, customer_id):
    """
    Checks if a restaurant is a favourite of the customer.
    """
    fav_obj = FavouriteFood.query.filter(
        FavouriteFood.customer_id == customer_id,
        FavouriteFood.food_id == food_id).first()
    return fav_obj is not None


def add_cuisine_to_favourite(cuisine_id, customer_id):
    """
    Adds a cuisine to the customer's favourites.
    """
    fav_obj = FavouriteCuisine(
        customer_id=customer_id, cuisine_id=cuisine_id)
    db.session.add(fav_obj)
    db.session.commit()

    return True, "Cuisine added to favourites"


def remove_cuisine_from_favourite(cuisine_id, customer_id):
    """
    Removes a cuisine from the customer's favourites.
    """
    fav_obj = FavouriteCuisine.query.filter(
        FavouriteCuisine.customer_id == customer_id,
        FavouriteCuisine.cuisine_id == cuisine_id).first()
    if not fav_obj:
        return False, "cuisine not found in favourites"

    db.session.delete(fav_obj)
    db.session.commit()

    return True, "Cuisine removed from favourites"


def get_favourite_restaurants(customer_id):
    """
    Retrieves the customer's favourite restaurants.
    """
    fav_restaurants = FavouriteRestaurant.query.filter(
        FavouriteRestaurant.customer_id == customer_id).all()

    restaurant_ids = [i.restaurant_id for i in fav_restaurants]
    
    restaurants = Restaurant.query.filter(
        Restaurant.id.in_(restaurant_ids)).all()
    
    return restaurants


def is_favourite_restaurant(restaurant_id, customer_id):
    """
    Checks if a restaurant is a favourite of the customer.
    """
    fav_obj = FavouriteRestaurant.query.filter(
        FavouriteRestaurant.customer_id == customer_id,
        FavouriteRestaurant.restaurant_id == restaurant_id).first()
    return fav_obj is not None


def automatically_get_favourite_Restaurant(customer_id):
    """
    restaurants from which customer ordered >= 2 times in previous month
    """

    restaurants = Restaurant.query.join(OrderList, OrderList.restaurant_id == Restaurant.id).join(
        Customer, Customer.id == OrderList.customer_id).filter(OrderList.order_time + timedelta(days=30)).group_by(
            Restaurant.id).having(func.count(OrderList.id) >= 2).all()

    for restaurant in restaurants:
        fav_obj = FavouriteRestaurant(
            customer_id=customer_id, restaurant_id=restaurant.id, mode='a')
        db.session.add(fav_obj)
        db.session.commit()

    return restaurants
