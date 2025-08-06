from flask import redirect,request,render_template,url_for,flash,abort, jsonify
from . import restaurant
from app.models import *
from  .forms import UpdateItemForm, ResetPasswordForm, RestaurantForm, MenuItemForm
from .services import *
from flask_login import login_required, current_user


@restaurant.route('/')
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def home():
    # Show all restaurants owned by the current user
    restaurants = Restaurant.query.filter_by(user_id=current_user.id).all()
    # Add location for each restaurant (from Address)
    for r in restaurants:
        address = Address.query.filter_by(user_id=r.user_id).first()
        r.location = address.location if address else 'N/A'
    return render_template('restaurant/dashboard.html', restaurants=restaurants)


@restaurant.route('/view_orders') 
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def view_orders():
    # Show all orders for all restaurants owned by the current user
    restaurants = Restaurant.query.filter_by(user_id=current_user.id).all()
    restaurant_ids = [r.id for r in restaurants]
    orders = OrderList.query.filter(OrderList.restaurant_id.in_(restaurant_ids)).order_by(OrderList.order_time.desc()).all()
    # For search/filter, get all restaurant names
    restaurant_map = {r.id: r.name for r in restaurants}
    return render_template('restaurant/order_history.html', all_orders=orders, restaurant_map=restaurant_map, restaurants=restaurants, show_all=True)





@restaurant.route('order_detail/<int:order_id>')
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def order_detail(order_id):
    order_details,customer_id = get_order_details(order_id)
    order_data=[]
    for items in order_details:
        order_data.append(
            {
                "food": Food.query.get(items.food_id).name,
                "quantity": items.quantity,
                "price": Food.query.get(items.food_id).price
            }
        )
    return render_template('restaurant/order_detail.html',customer_id = customer_id, order_details=order_data,total_price = OrderList.query.get(order_id).total_price)


@restaurant.route('/view_menu')
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def view_menu():
    form = UpdateItemForm()
    restaurant_id = get_restaurant_id_by_user_id(current_user.id)
    menu = get_menu_for_restaurant(restaurant_id = restaurant_id)
    mostly_ordered = get_mostly_ordered_items(restaurant_id = restaurant_id)
    
    for item in menu :
        print(item['id'], item['id'] in [i.id for i in mostly_ordered])

    cuisine_list = [i.name for i in Cuisine.query.all()]
    return render_template("restaurant/menu.html", menu=menu,
                           form =form,
                           mostly_ordered = mostly_ordered,
                           cuisine_list = cuisine_list)



@restaurant.route("/add_dish/" , methods = ['POST','GET'])
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def add_dish() :
    form = UpdateItemForm()
    if request.method == 'POST' :
        if form.validate_on_submit():
            food_name = form.data.get('food_name')
            cuisine_name = form.data.get('cuisine_name')
            category = form.data.get('category')
            price = form.data.get("price")
            restaurant_id = get_restaurant_id_by_user_id(current_user.id)
            add_dish_to_menu(restaurant_id = restaurant_id,
                            food_name = food_name,
                            price = price,
                            cuisine_name = cuisine_name,
                            category = category)
            return redirect(url_for('restaurant.home'))
            
    else :
        return redirect(url_for('restaurant.add_dish'),form = form)
    

    return redirect(url_for('restaurant.view_menu'))

@restaurant.route("/remove_dish")
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def remove_dish():
    food_id = request.args.get('food_id')
    if not food_id:
        flash("Food ID not provided", "danger")
        return redirect(url_for('restaurant.view_menu'))
    success,message = remove_dish_from_menu(food_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('restaurant.view_menu'))


@restaurant.route("/mark_order_as_delivered")
@dont_allow_non_restaurants 
@login_required
@check_transaction_complete
def mark_order_as_delivered():
    print("mark_order_delivered")
    order_id = request.args.get('order_id')
    # food_id = request.args.get('food_id')
    if not order_id :
        
        flash("Order ID not provided", "danger")
        return redirect(url_for('restaurant.view_orders'))
    print("executing")
    success,message = mark_order_delivered(order_id)
    if success:
        flash(message, "success")
    else:
        flash(message, "danger")
    
    return redirect(url_for('restaurant.view_orders'))

@restaurant.route("/update_menu" , methods = ['POST'])
@dont_allow_non_restaurants
@login_required
# @check_transaction_complete
def update_menu():
    restaurant_id = get_restaurant_id_by_user_id(current_user.id)
    for key, value in request.form.items():
        print("key :",key)
        if key.startswith("food_name"):  # Extract the item ID from the key
            item_id = key.split("_")[-1]  # Extract ID from field name (e.g., food_name_5)
            food = Food.query.get(item_id)
            if food:
                food.name = request.form.get(f"food_name_{item_id}").capitalize()
                food.price = request.form.get(f"price_{item_id}")
                new_cuisine = request.form.get(f"cuisine_{item_id}").capitalize()
                existing_cuisine = Cuisine.query.filter(Cuisine.name == new_cuisine).first()

                if existing_cuisine :
                    food.cuisine_id = existing_cuisine.id

                else: 
                    flash("Mentioned cuisine is currently not supported" , "danger")
                food.category = request.form.get(f"category_{item_id}").capitalize()
                db.session.commit()

            else :
                print("doesn't exists")
                print(request.form.get(f'cuisine'))
                add_dish_to_menu(food_name = request.form.get(f"food_name"),
                                 price = request.form.get(f"price"),
                                 cuisine_name = request.form.get(f"cuisine"),
                                 category = request.form.get(f"category"),
                                 restaurant_id = restaurant_id
                                 )
    
    flash("Menu updated successfully!", "success")
    return redirect(url_for('restaurant.view_menu'))




@restaurant.route("/make_dish_of_the_day")
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def make_dish_of_the_day() :
    food_id = request.args.get(food_id)

@restaurant.route('/view_profile', methods=['GET'])
@dont_allow_non_restaurants
@login_required
def view_profile():
    """Show owner info and all their restaurants"""
    user = current_user
    restaurants = Restaurant.query.filter_by(user_id=user.id).all()
    return render_template('restaurant/view_profile.html', user=user, restaurants=restaurants)

@restaurant.route('/reset_password', methods=['GET', 'POST'])
@dont_allow_non_restaurants
@login_required
@check_transaction_complete
def reset_password():
    """Allow restaurant owner to reset their password (no email required)"""
    form = ResetPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Since the user is already logged in, use current_user directly
        user = current_user
        if not user:
            flash('User not found.', 'danger')
            return render_template('restaurant/reset_password.html', form=form)
        
        old_password = form.old_password.data
        new_password = form.new_password.data
        
        try:
            if not user.check_password(old_password):
                flash('Old password is incorrect.', 'danger')
                return render_template('restaurant/reset_password.html', form=form)
            
            user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'success')
            return redirect(url_for('restaurant.view_profile'))
            
        except Exception as e:
            print(f"Error updating password: {e}")
            db.session.rollback()
            flash('An error occurred while updating password. Please try again.', 'danger')
            return render_template('restaurant/reset_password.html', form=form)
            
    return render_template('restaurant/reset_password.html', form=form)

@restaurant.route('/restaurant/add', methods=['GET', 'POST'])
@dont_allow_non_restaurants
@login_required
def add_restaurant():
    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(
            user_id=current_user.id,
            name=form.name.data,
            description=form.description.data,
            image_url=form.image_url.data or None,
            opening_time=form.opening_time.data,
            closing_time=form.closing_time.data,
            rating=None
        )
        db.session.add(restaurant)
        db.session.commit()
        # Add address
        address = Address(user_id=current_user.id, full_address=form.location.data, city="", location=form.location.data)
        db.session.add(address)
        db.session.commit()
        flash('Restaurant added successfully!', 'success')
        return redirect(url_for('restaurant.home'))
    return render_template('restaurant/restaurant_form.html', form=form, restaurant=None)

@restaurant.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
@dont_allow_non_restaurants
@login_required
def edit_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    form = RestaurantForm(obj=restaurant)
    address = Address.query.filter_by(user_id=restaurant.user_id).first()
    if form.validate_on_submit():
        restaurant.name = form.name.data
        restaurant.description = form.description.data
        restaurant.image_url = form.image_url.data or None
        restaurant.opening_time = form.opening_time.data
        restaurant.closing_time = form.closing_time.data
        if address:
            address.location = form.location.data
        else:
            address = Address(user_id=restaurant.user_id, full_address=form.location.data, city="", location=form.location.data)
            db.session.add(address)
        db.session.commit()
        flash('Restaurant updated successfully!', 'success')
        return redirect(url_for('restaurant.restaurant_detail', restaurant_id=restaurant.id))
    if request.method == 'GET' and address:
        form.location.data = address.location
    return render_template('restaurant/restaurant_form.html', form=form, restaurant=restaurant)

@restaurant.route('/restaurant/<int:restaurant_id>')
@dont_allow_non_restaurants
@login_required
def restaurant_detail(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    address = Address.query.filter_by(user_id=restaurant.user_id).first()
    restaurant.location = address.location if address else 'N/A'
    # Fetch reviews and ratings
    rest_reviews = RestaurantReview.query.filter_by(restaurant_id=restaurant_id).all()
    avg_rest_rating = round(sum([r.rating for r in rest_reviews])/len(rest_reviews), 1) if rest_reviews else None
    # Fetch menu and dish reviews
    menu = Food.query.filter_by(restaurant_id=restaurant_id).all()
    menu_items = []
    for item in menu:
        dish_reviews = DishReview.query.filter_by(food_id=item.id).all()
        avg_dish_rating = round(sum([r.rating for r in dish_reviews])/len(dish_reviews), 1) if dish_reviews else None
        menu_items.append({
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'cuisine': item.cuisine_id,
            'category': item.category,
            'is_special': getattr(item, 'is_special', False),
            'is_deal_of_day': getattr(item, 'is_deal_of_day', False),
            'dish_reviews': dish_reviews,
            'avg_dish_rating': avg_dish_rating
        })
    return render_template('restaurant/restaurant_detail.html', restaurant=restaurant, rest_reviews=rest_reviews, avg_rest_rating=avg_rest_rating, menu=menu_items)

@restaurant.route('/restaurant/<int:restaurant_id>/orders')
@dont_allow_non_restaurants
@login_required
def view_orders_for_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    orders = OrderList.query.filter_by(restaurant_id=restaurant_id).order_by(OrderList.order_time.desc()).all()
    return render_template('restaurant/order_history.html', restaurant=restaurant, all_orders=orders)

@restaurant.route('/restaurant/<int:restaurant_id>/menu')
@dont_allow_non_restaurants
@login_required
def view_menu_for_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    menu = Food.query.filter_by(restaurant_id=restaurant_id).all()
    from datetime import datetime
    today = datetime.now().date()
    # Get food ids ordered more than 5 times today for this restaurant
    mostly_ordered_query = db.session.query(
        Food.id, db.func.count(OrderDetail.id).label('count')
    ).join(OrderDetail, Food.id == OrderDetail.food_id) \
    .join(OrderList, OrderList.id == OrderDetail.order_id) \
    .filter(db.func.date(OrderList.order_time) == today, Food.restaurant_id == restaurant_id) \
    .group_by(Food.id) \
    .having(db.func.count(OrderDetail.id) > 5) \
    .all()
    mostly_ordered_ids = {item.id for item in mostly_ordered_query}
    return render_template('restaurant/menu.html', restaurant=restaurant, menu=menu, mostly_ordered_ids=mostly_ordered_ids)

@restaurant.route('/restaurant/<int:restaurant_id>/menu/add', methods=['GET', 'POST'])
@dont_allow_non_restaurants
@login_required
def add_menu_item(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    form = MenuItemForm()
    form.cuisine_id.choices = [(c.id, c.name) for c in Cuisine.query.all()]
    if form.validate_on_submit():
        food = Food(
            restaurant_id=restaurant_id,
            name=form.name.data,
            price=form.price.data,
            cuisine_id=form.cuisine_id.data,
            category=form.category.data,
            is_special=bool(form.is_special.data),
            is_deal_of_day=bool(form.is_deal_of_day.data)
        )
        db.session.add(food)
        db.session.commit()
        flash('Menu item added!', 'success')
        return redirect(url_for('restaurant.view_menu_for_restaurant', restaurant_id=restaurant_id))
    return render_template('restaurant/menu_item_form.html', form=form, restaurant=restaurant, food=None)

@restaurant.route('/restaurant/<int:restaurant_id>/menu/<int:food_id>/edit', methods=['GET', 'POST'])
@dont_allow_non_restaurants
@login_required
def edit_menu_item(restaurant_id, food_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    food = Food.query.get_or_404(food_id)
    form = MenuItemForm(obj=food)
    form.cuisine_id.choices = [(c.id, c.name) for c in Cuisine.query.all()]
    if form.validate_on_submit():
        food.name = form.name.data
        food.price = form.price.data
        food.cuisine_id = form.cuisine_id.data
        food.category = form.category.data
        food.is_special = bool(form.is_special.data)
        food.is_deal_of_day = bool(form.is_deal_of_day.data)
        db.session.commit()
        flash('Menu item updated!', 'success')
        return redirect(url_for('restaurant.view_menu_for_restaurant', restaurant_id=restaurant_id))
    return render_template('restaurant/menu_item_form.html', form=form, restaurant=restaurant, food=food)

@restaurant.route('/restaurant/<int:restaurant_id>/menu/<int:food_id>/delete')
@dont_allow_non_restaurants
@login_required
def delete_menu_item(restaurant_id, food_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    if restaurant.user_id != current_user.id:
        abort(403)
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('Menu item deleted!', 'success')
    return redirect(url_for('restaurant.view_menu_for_restaurant', restaurant_id=restaurant_id))

