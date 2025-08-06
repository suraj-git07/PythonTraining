"""routes for customer side"""

from flask import redirect, request, render_template, url_for, flash, abort, session, jsonify
from . import customer
from .services import *
from .helper import get_all_locations, get_all_cuisines, is_valid_phone, is_valid_email
from app.models import Address, Cart, Customer, Food, OrderList, User, Restaurant, db, FavouriteRestaurant 
from flask_login import login_required, current_user
from .forms import *  
from app.models import DishReview, RestaurantReview
from app.extensions import csrf



@customer.route('/')
@check_transaction_complete
@dont_allow_non_customers
@login_required
def home():
    """ redirect to view_restaurants page """
    return redirect(url_for('customer.view_restaurants'))



@customer.route('/view_restaurants')
@dont_allow_non_customers
@login_required
@check_transaction_complete
def view_restaurants():
    """
    view the list of restaurants matching the filters
    """
    try:
        customer_id = get_customer_id_from_user_id(current_user.id)
        
        if customer_id is None:
            flash('Customer profile not found. Please contact support.', 'danger')
            return redirect(url_for('auth.logout'))
        
        # Get filter parameters
        args = request.args
        locations = args.getlist('location')
        min_rating = args.get('min_rating')
        cuisines = args.getlist('cuisine')
        name_filter = args.get('name_filter')
        min_price = args.get('min_price', type=float)
        # Get all restaurants first
        restaurants = get_restaurant_list(customer_id) if not any([locations, min_rating, cuisines, name_filter, min_price]) else \
                     get_restaurant_list(
                        customer_id=customer_id,
                        min_rating=min_rating,
                        locations=locations,
                        cuisines=cuisines,
                        name_filter=name_filter,
                        min_price=min_price
                     )
        
        
        try:
            # Prepare restaurant data for template
            restaurant_data = []
            for restaurant in restaurants:
                restaurant_data.append({
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "rating": restaurant.rating,
                    "image_url": restaurant.image_url,
                    "location": get_location_by_restaurant_id(restaurant.id),
                    "open_status": get_restaurant_open_and_close_time(restaurant.id),
                    "is_favorite": is_favourite_restaurant(restaurant.id, customer_id),
                })
            
            all_locations = get_all_locations()
            print(f"Found {len(all_locations)} locations")
            
            all_cuisines = get_all_cuisines()
            print(f"Found {len(all_cuisines)} cuisines")
            
            search_form = SearchForm()
            
            return render_template(
                "customer/view_restaurants.html",
                customer_id=customer_id,
                restaurants=restaurant_data,
                locations=all_locations,
                cuisines=all_cuisines,
                search_form=search_form,
                is_favourite_restaurant=is_favourite_restaurant,
                selected_filters={
                    'locations': locations,
                    'min_rating': min_rating,
                    'cuisines': cuisines,
                    'name': name_filter,
                    'min_price': min_price,
                }
            )
            
        except Exception as e:
            flash("Error loading restaurant data. Please try again.", "error")
            return render_template(
                "customer/view_restaurants.html",
                customer_id=customer_id,
                restaurants=[],
                locations=[],
                cuisines=[],
                search_form=SearchForm(),
                is_favourite_restaurant=lambda x, y: False,
                selected_filters={}
            )
        
    except Exception as e:
        flash("An error occurred while loading restaurants. Please try again.", "error")
        return redirect(url_for('auth.login'))
    

@customer.route('/update_cart', methods=['POST', 'GET'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def update_cart():
    """ add/subtract/remove items from the cart"""
    args = request.args
    food_id = args.get('food_id', None)
    # customer_id = args.get('customer_id', None)
    customer_id = get_customer_id_from_user_id(current_user.id)
    restaurant_id = Food.query.get(food_id).restaurant_id
    action = args.get("action")

    if action == "add":
        success, message = add_to_cart(
            food_id=food_id, customer_id=customer_id)

    elif action == "subtract":
        success, message = subtract_from_cart(
            food_id=food_id, customer_id=customer_id)

    else:
        success, message = remove_from_cart(
            food_id=food_id, customer_id=customer_id)

    flash(message, 'success' if success else 'danger')
    print("cart", Cart.query.count())

    return redirect(url_for('customer.view_restaurant', restaurant_id=restaurant_id))


@customer.route('/view_cart')
@dont_allow_non_customers
@login_required
def view_cart():
    """view the cart"""
    try:
        customer_id = get_customer_id_from_user_id(current_user.id)
        if not customer_id:
            flash('Customer profile not found. Please contact support.', 'danger')
            return redirect(url_for('customer.home'))
        
        success, cart_by_restaurants = split_cart_by_restaurant(customer_id)
        print(f"Cart split result - Success: {success}")
        
        if not success:
            # If it's just an empty cart, show the empty cart template
            if "No items in the cart" in str(cart_by_restaurants):
                return render_template('customer/cart.html', cart_by_restaurants={})
            else:
                # If it's an actual error, show the error
                flash(f'Cart loading error: {cart_by_restaurants}', 'danger')
                return redirect(url_for('customer.view_restaurants'))

        return render_template('customer/cart.html', cart_by_restaurants=cart_by_restaurants)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        flash(f'An error occurred while loading your cart: {str(e)}', 'danger')
        return redirect(url_for('customer.view_restaurants'))


@customer.route('/clear_cart')
@check_transaction_complete
@dont_allow_non_customers
@login_required
def clear_cart():
    """clear the cart for a customer"""
    customer_id = get_customer_id_from_user_id(current_user.id)
    restaurant_id = request.args.get('restaurant_id', None)
    if restaurant_id:
        success, message = clear_cart_for_restaurant(
            customer_id=customer_id, restaurant_id=restaurant_id)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('customer.view_restaurant', restaurant_id=restaurant_id))
    else:
        success, message = clear_cart_for_all_restaurants(
            customer_id=customer_id)
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('customer.view_restaurants'))


@customer.route('/order', methods=['POST', 'GET'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def order():
    """place the order based on cart"""
    customer_id = get_customer_id_from_user_id(current_user.id)
    success, message = place_order(customer_id)

    flash(message, 'success' if success else 'danger')

    # BUILD THE FUNCTION : add_dish_to_restaurant_history()
    return redirect(url_for('customer.view_order_history'))


@customer.route('/view_order_history')
@check_transaction_complete
@dont_allow_non_customers
@login_required
def view_order_history():
    """ returns order headers (orderList) for a customer """
    try:
        customer_id = get_customer_id_from_user_id(current_user.id)
        pending_orders, delivered_orders, cancelled_orders, all_orders = get_order_headers_for_customer(customer_id)
        
        # Handle search functionality
        search_term = request.args.get('order_restaurant', '').strip()
        if search_term:
            # Filter orders by restaurant name
            filtered_orders = []
            for order in all_orders:
                try:
                    restaurant = Restaurant.query.get(order.restaurant_id)
                    if restaurant and search_term.lower() in restaurant.name.lower():
                        filtered_orders.append(order)
                except Exception as e:
                    print(f"Error filtering order {order.id}: {e}")
                    continue
            all_orders = filtered_orders
        
        return render_template('customer/order_history.html',
                               pending_orders=pending_orders,
                               delivered_orders=delivered_orders,
                               cancelled_orders=cancelled_orders,
                               all_orders=all_orders,
                               Restaurant=Restaurant)
    except Exception as e:
        print(f"Error in view_order_history: {e}")
        flash('Unable to load order history. Please try again.', 'danger')
        return redirect(url_for('customer.view_restaurants'))


@customer.route('/order_detail/<int:order_id>', methods=['GET', 'POST'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def order_detail(order_id):
    """ view the details of a order and allow review submission if delivered """
    order = OrderList.query.get(order_id)
    order_details = OrderDetail.query.filter_by(order_id=order_id).all()
    
    # Create combined order items with food information
    order_items = []
    for detail in order_details:
        food = Food.query.get(detail.food_id)
        if food:
            order_items.append({
                'food_name': food.name,
                'quantity': detail.quantity,
                'price': food.price,
                'food_id': food.id
            })
    
    customer_id = get_customer_id_from_user_id(current_user.id)
    food_items = [Food.query.get(od.food_id) for od in order_details]
    dish_review_forms = []
    dish_reviews = {}
    for food in food_items:
        # Check if review already exists for this dish in this order
        existing_review = DishReview.query.filter_by(order_id=order_id, food_id=food.id, customer_id=customer_id).first()
        form = DishReviewForm(prefix=f'dish_{food.id}')
        if form.validate_on_submit() and not existing_review:
            new_review = DishReview(
                customer_id=customer_id,
                food_id=food.id,
                order_id=order_id,
                rating=form.rating.data,
                review=form.review.data
            )
            db.session.add(new_review)
            db.session.commit()
            flash(f'Review submitted for {food.name}', 'success')
        dish_review_forms.append((food, form, existing_review))
        dish_reviews[food.id] = existing_review

    # Restaurant review
    rest_review_form = RestaurantReviewForm(prefix='rest')
    existing_rest_review = RestaurantReview.query.filter_by(order_id=order_id, restaurant_id=order.restaurant_id, customer_id=customer_id).first()
    if rest_review_form.validate_on_submit() and not existing_rest_review:
        new_rest_review = RestaurantReview(
            customer_id=customer_id,
            restaurant_id=order.restaurant_id,
            order_id=order_id,
            rating=rest_review_form.rating.data,
            review=rest_review_form.review.data
        )
        db.session.add(new_rest_review)
        db.session.commit()
        flash('Restaurant review submitted!', 'success')

    return render_template('customer/order_detail.html', order=order, order_items=order_items, food_items=food_items, dish_review_forms=dish_review_forms, dish_reviews=dish_reviews, rest_review_form=rest_review_form, existing_rest_review=existing_rest_review, total_price=order.total_price)


@customer.route('/order/cancel')
@check_transaction_complete
@dont_allow_non_customers
@login_required
def cancel_order():
    """ cancel a pending order"""
    customer_id = get_customer_id_from_user_id(current_user.id)
    order_id = request.args.get('order_id', None)
    if not order_id:
        flash('Order ID not found', 'danger')
        return redirect(url_for('customer.view_order_history'))

    success, message = cancel_order_by_customer(order_id, customer_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('customer.view_order_history'))


@customer.route('/view_restaurant')
@dont_allow_non_customers
@login_required
# @check_transaction_complete
def view_restaurant():
    """ view details of a restaurant with menu and show reviews/ratings """
    restaurant_id = request.args.get('restaurant_id')
    customer_id = get_customer_id_from_user_id(current_user.id)
    try:
        restaurant, menu = get_restaurant_details(restaurant_id)
    except:
        return "error", abort(401)
    if not restaurant:
        flash("Restaurant not found", "danger")
        return redirect(url_for('customer.home'))
    cuisines = get_cuisines_for_restaurant(restaurant_id)
    menu = menu.order_by(Food.category).all()
    menu_items = []
    for item in menu:
        cart_item = Cart.query.filter(
            Cart.food_id == item.id, Cart.customer_id == customer_id).first()
        # Get dish reviews and average rating
        dish_reviews = DishReview.query.filter_by(food_id=item.id).all()
        avg_dish_rating = round(sum([r.rating for r in dish_reviews])/len(dish_reviews), 1) if dish_reviews else None
        menu_items.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'cuisine': item.cuisine_id,
            'category': item.category,
            'quantity': cart_item.quantity if cart_item else 0,
            'is_special': getattr(item, 'is_special', False),
            'is_deal_of_day': getattr(item, 'is_deal_of_day', False),
            'dish_reviews': dish_reviews,
            'avg_dish_rating': avg_dish_rating
        })
    # Restaurant reviews and average
    rest_reviews = RestaurantReview.query.filter_by(restaurant_id=restaurant_id).all()
    avg_rest_rating = round(sum([r.rating for r in rest_reviews])/len(rest_reviews), 1) if rest_reviews else None
    return render_template('customer/restaurant_detail.html', restaurant=restaurant,
                           menu=menu_items,
                           cuisines=cuisines,
                           customer_id=customer_id,
                           restaurant_id=restaurant_id,
                           is_favourite_food=is_favourite_food,
                           Food=Food,
                           rest_reviews=rest_reviews,
                           avg_rest_rating=avg_rest_rating
                           )



@customer.route('/view_profile', methods=['GET', 'POST'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def view_profile():
    """view and update the profile"""
    form = UpdateProfileForm()
    if request.method == 'GET':
        customer_id = get_customer_id_from_user_id(current_user.id)
        customer_profile = get_customer_profile(customer_id)
        return render_template('customer/view_profile.html',
                               customer_profile=customer_profile,
                               customer_id=customer_id,
                               form=form)
    else:
        customer_id = get_customer_id_from_user_id(current_user.id)
        name = request.form.get('name')
        phone = form.data.get('phone')
        address = form.data.get('address')
        email = form.data.get('email')
        success, message = update_customer_profile(customer_id, name=name, email=email,
                                                   phone=phone, address=address)
        print("name :", name)
        print("updated")
        flash(message, 'success' if success else 'danger')
        return redirect(url_for('customer.view_profile'))


@customer.route('/apply_name_filter', methods=['POST', 'GET'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def apply_name_filter():
    """ apply name filter to restaurant list """
    search_form = SearchForm()
    if request.method == 'POST':
        name_filter = search_form.name_filter.data

        if name_filter:
            return redirect(url_for('customer.view_restaurants', name_filter=name_filter))

        return redirect(url_for('customer.view_restaurants'))
    else:
        return redirect(url_for('customer.view_restaurants'), search_form=search_form)


@customer.route("add_favourite_restaurant")
@check_transaction_complete
@dont_allow_non_customers
@login_required
def add_favourite_restaurant():
    """add a restaurant to favourites"""
    restaurant_id = request.args.get('restaurant_id')
    customer_id = get_customer_id_from_user_id(current_user.id)
    print(restaurant_id,Restaurant.query.get(restaurant_id).name,"rest-id added to fAV")
    success, message = add_restaurant_to_favourite(customer_id=customer_id,
                                                   restaurant_id=restaurant_id)
    flash(message, 'success' if success else 'danger')

    locations = session.get('locations', [])
    min_rating = session.get('min_rating', None)
    cuisines = session.get('cuisines', [])
    name_filter = session.get('name_filter', None)

    return redirect(url_for('customer.view_restaurants',location = locations,
                            min_rating=min_rating,
                            cuisine=cuisines,
                            name_filter=name_filter))


@customer.route("remove_favourite_restaurant")
@check_transaction_complete
@dont_allow_non_customers
@login_required
def remove_favourite_restaurant():
    """remove a restaurant from favourites"""
    restaurant_id = request.args.get('restaurant_id')
    customer_id = get_customer_id_from_user_id(current_user.id)
    success, message = remove_restaurant_from_favourite(customer_id=customer_id,
                                                        restaurant_id=restaurant_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('customer.view_restaurants'))


@customer.route("set_favourite_food")
@check_transaction_complete
@dont_allow_non_customers
@login_required
def set_favourite_food():
    """add a food item to favourites"""
    print("here")
    restaurant_id = request.args.get('restaurant_id')
    customer_id = get_customer_id_from_user_id(current_user.id)
    food_id = request.args.get('food_id')
    success,message = add_food_to_favourite(customer_id= customer_id,
                                            food_id= food_id
                                            )
    if success :
        flash(message , 'success' if success else 'danger')
    # print("redirecting")
    return redirect(url_for('customer.view_restaurant',restaurant_id = restaurant_id))

@customer.route("remove_favourite_food")
@check_transaction_complete
@dont_allow_non_customers
@login_required
def remove_favourite_food() :
    """remove a food item from favourites"""
    restaurant_id = request.args.get('restaurant_id')
    food_id = request.args.get('food_id')
    customer_id = get_customer_id_from_user_id(current_user.id)
    success, message = remove_food_from_favourite(customer_id=customer_id,
                                                        food_id=food_id)
    flash(message, 'success' if success else 'danger')
    return redirect(url_for('customer.view_restaurant',restaurant_id = restaurant_id))



@customer.route("auto_set_fav_rest")
@check_transaction_complete
@dont_allow_non_customers
@login_required
def auto_set_fav_rest() :
    """used for development purposes, currently not included in app"""
    customer_id = request.args.get('customer_id')
    print(automatically_set_favourite_Restaurant(customer_id))

    return redirect(url_for('customer.view_restaurants'))

@customer.route('/reset_password', methods=['GET', 'POST'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def reset_password():
    """Allow customer to reset their password (no email required)"""
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Since the user is already logged in, use current_user directly
        user = current_user
        if not user:
            flash('User not found.', 'danger')
            return render_template('customer/reset_password.html', form=form)
        
        old_password = form.old_password.data
        new_password = form.new_password.data
        
        try:
            if not user.check_password(old_password):
                flash('Old password is incorrect.', 'danger')
                return render_template('customer/reset_password.html', form=form)
            
            user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('customer.view_profile'))
            
        except Exception as e:
            print(f"Error updating password: {e}")
            db.session.rollback()
            flash('An error occurred while updating password. Please try again.', 'danger')
            return render_template('customer/reset_password.html', form=form)
            
    return render_template('customer/reset_password.html', form=form)


@customer.route('/mostly_ordered')
@check_transaction_complete
@dont_allow_non_customers
@login_required
def mostly_ordered():
    from datetime import datetime
    customer_id = get_customer_id_from_user_id(current_user.id)
    # Query for items ordered by this user more than 3 times in total
    my_fav_query = db.session.query(
        Food.id, Food.name, Food.price, Food.restaurant_id, db.func.count(OrderDetail.id).label('count')
    ).join(OrderDetail, Food.id == OrderDetail.food_id)\
    .join(OrderList, OrderList.id == OrderDetail.order_id)\
    .filter(OrderList.customer_id == customer_id)\
    .group_by(Food.id)\
    .having(db.func.count(OrderDetail.id) > 3)\
    .all()
    # Also include manually favourited foods
    manual_favs = db.session.query(Food.id, Food.name, Food.price, Food.restaurant_id).join(FavouriteFood, Food.id == FavouriteFood.food_id)\
        .filter(FavouriteFood.customer_id == customer_id).all()
    # Merge both sets, avoid duplicates
    fav_ids = set()
    mostly_ordered_items = []
    for item in my_fav_query:
        rest = Restaurant.query.get(item.restaurant_id)
        mostly_ordered_items.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'restaurant_name': rest.name if rest else '',
            'count': item.count
        })
        fav_ids.add(item.id)
    for item in manual_favs:
        if item.id not in fav_ids:
            rest = Restaurant.query.get(item.restaurant_id)
            mostly_ordered_items.append({
                'id': item.id,
                'name': item.name,
                'price': item.price,
                'restaurant_name': rest.name if rest else '',
                'count': '★'  # Mark as manual favourite
            })
    # Get user's favourite restaurants
    favourite_restaurants = get_favourite_restaurants(customer_id)
    return render_template('customer/mostly_ordered.html', mostly_ordered_items=mostly_ordered_items, favourite_restaurants=favourite_restaurants)

# Alternative cart route for testing
@customer.route('/cart')
# @check_transaction_complete  # Temporarily disabled for debugging
@dont_allow_non_customers  
@login_required
def cart():
    """Alternative cart route"""
    return redirect(url_for('customer.view_cart'))

@customer.route('/cart/update', methods=['POST', 'GET'])
@check_transaction_complete
@dont_allow_non_customers
@login_required
def cart_update():
    """ add/subtract/remove items from the cart and return to cart page"""
    args = request.args
    food_id = args.get('food_id', None)
    customer_id = get_customer_id_from_user_id(current_user.id)
    action = args.get("action")

    if not food_id:
        flash('Invalid food item selected.', 'danger')
        return redirect(url_for('customer.view_cart'))

    if action == "add":
        success, message = add_to_cart(
            food_id=food_id, customer_id=customer_id)

    elif action == "subtract":
        success, message = subtract_from_cart(
            food_id=food_id, customer_id=customer_id)

    else:  # remove
        success, message = remove_from_cart(
            food_id=food_id, customer_id=customer_id)

    flash(message, 'success' if success else 'danger')
    print("cart", Cart.query.count())

    return redirect(url_for('customer.view_cart'))

@customer.route('/toggle_favorite_restaurant/<int:restaurant_id>', methods=['POST'])
@csrf.exempt  # Exempt from CSRF protection for AJAX requests
@login_required
def toggle_favorite_restaurant(restaurant_id):
    """Toggle restaurant as favorite/unfavorite"""
    try:
        # Check if user is a customer
        if current_user.code != '1':
            return jsonify({'success': False, 'message': 'Access denied'}), 403
            
        customer_id = get_customer_id_from_user_id(current_user.id)
        
        # Check if restaurant exists
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return jsonify({'success': False, 'message': 'Restaurant not found'}), 404
        
        # Check if already favorited
        favorite = FavouriteRestaurant.query.filter_by(
            customer_id=customer_id, 
            restaurant_id=restaurant_id
        ).first()
        
        if favorite:
            # Remove from favorites
            db.session.delete(favorite)
            db.session.commit()
            is_favorite = False
            message = f'{restaurant.name} removed from favorites'
        else:
            # Add to favorites
            new_favorite = FavouriteRestaurant(
                customer_id=customer_id,
                restaurant_id=restaurant_id,
                mode='m'  # manual
            )
            db.session.add(new_favorite)
            db.session.commit()
            is_favorite = True
            message = f'{restaurant.name} added to favorites'
        
        return jsonify({
            'success': True, 
            'is_favorite': is_favorite,
            'message': message
        })
        
    except Exception as e:
        print(f"Error toggling favorite: {e}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'An error occurred'}), 500
