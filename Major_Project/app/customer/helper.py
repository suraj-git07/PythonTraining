"""helper functions used throughout the Blueprint"""
import re
from functools import wraps
from flask import flash, request, redirect
from app.models import Address, Cuisine, Restaurant, User
from sqlalchemy import distinct

def check_transaction_complete(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            flash('Could not complete the action. Please try again later.', 'danger')
            print(f"Transaction Error: {e}")
            return redirect(request.referrer or '/')  # Fallback to home if no referrer
    return wrapper


def is_valid_email(email):
    """
    Validate the email address format.
    """
    # Regular expression for validating an Email
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    if re.match(regex, email):
        return True
    else:
        return False
    
def is_valid_phone(phone):
    """
    Validate the phone number format.
    """
    # Regular expression for validating a phone number
    regex = r'^\+?[1-9]\d{9,14}$'
    
    if re.match(regex, phone):
        return True
    else:
        return False


def get_all_locations():
    """Get all unique locations from the addresses table"""
    try:
        # Join with Restaurant to only get locations where there are active restaurants
        locations = Address.query.join(
            User, Address.user_id == User.id
        ).join(
            Restaurant, Restaurant.user_id == User.id
        ).with_entities(
            distinct(Address.location)
        ).all()
        
        # Extract location strings from tuples
        return [loc[0] for loc in locations if loc[0]]
    except Exception as e:
        print(f"Error getting locations: {str(e)}")
        return []

def get_all_cuisines():
    """Get all available cuisines"""
    try:
        cuisines = Cuisine.query.order_by(Cuisine.name).all()
        return cuisines
    except Exception as e:
        return []




