from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User

# Define a blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)

# ----------------------------
# Login Route
# ----------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    - If the user is already logged in, redirect to the task page.
    - On POST: Validate username and password.
    - If valid, log in the user and redirect to tasks page.
    - If invalid, flash an error message.
    - On GET: Render the login form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    
    return render_template('login.html')

# ----------------------------
# Register Route
# ----------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    - If already logged in, redirect to tasks.
    - On POST: Validate form input (required fields, password match, length, uniqueness).
    - If validation passes, create new user and store in DB.
    - On success, redirect to login page with a flash message.
    - On GET: Show the registration form.
    """
    if current_user.is_authenticated:
        return redirect(url_for('tasks.view_tasks'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic form validations
        if not username or not email or not password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html')
        
        # Uniqueness checks
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different email.', 'danger')
            return render_template('register.html')
        
        # Create and store the new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# ----------------------------
# Logout Route
# ----------------------------
@auth_bp.route('/logout')
@login_required
def logout():
    """
    Logs out the current user and redirects to the login page.
    Only accessible if user is logged in.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
