"""
routes for auth
"""
from app.models import User, Customer
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from .forms import LoginForm
from . import auth
from werkzeug.security import check_password_hash


@auth.route('/')
def index():
    """
    Authenticated users go to their appropriate dashboard, 
    unauthenticated users go to login.
    """
    if current_user.is_authenticated:
        # Redirect authenticated users to their appropriate dashboard
        if current_user.code == '1':  # Customer
            return redirect(url_for('customer.view_restaurants'))
        elif current_user.code == '2':  # Restaurant
            return redirect(url_for('restaurant.home'))
        else:
            # Unknown user code, logout for safety
            return redirect(url_for('auth.logout'))
    
    # Redirect unauthenticated users to login
    return redirect(url_for('auth.login'))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next')  # Get the next URL if it exists
    
    if current_user.is_authenticated:
        # If there's a next URL and it's safe, use it
        if next_url:
            print(f"Redirecting to next URL: {next_url}")
            return redirect(next_url)
        # Otherwise redirect based on user type
        if current_user.code == '2':
            return redirect(url_for('restaurant.home'))
        elif current_user.code == '1':
            return redirect(url_for('customer.view_restaurants'))
        return redirect(url_for('auth.logout'))

    form = LoginForm()
    # Handle POST request
    if request.method == 'POST':
        try:
            # Validate form
            if not form.validate_on_submit():
                flash('Please check your input and try again.', 'danger')
                return render_template('auth/login.html', form=form)
            
            # Find user
            user = User.query.filter_by(email=form.email.data).first()
            if not user:
                flash('Invalid email or password.', 'danger')
                return render_template('auth/login.html', form=form)
            
            # Verify password
            if not check_password_hash(user.password, form.password.data):
                flash('Invalid email or password.', 'danger')
                return render_template('auth/login.html', form=form)            
            # For customers, verify customer record exists
            if user.code == '1':
                customer = Customer.query.filter_by(user_id=user.id).first()
                if not customer:
                    flash('Customer profile not found. Please contact support.', 'danger')
                    return render_template('auth/login.html', form=form)            
            # Login user
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            
            # Handle redirection
            if next_url:
                return redirect(next_url)
            # Default redirects based on user type
            if user.code == '2':
                return redirect(url_for('restaurant.home'))
            elif user.code == '1':
                return redirect(url_for('customer.view_restaurants'))
            else:
                flash('Invalid user type.', 'danger')
                return redirect(url_for('auth.logout'))
                
        except Exception as e:
            flash('An error occurred during login. Please try again.', 'danger')
            return render_template('auth/login.html', form=form)
    
    return render_template('auth/login.html', form=form)
        
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Logs out the user
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  # Redirect to login or homepage

