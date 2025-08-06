
from functools import wraps
from flask import flash, request, redirect


def check_transaction_complete(func):
    """decorator to check whether a function executes without any unforseen erroror not\
        Used in routes.py"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            flash('Could not complete the action due to unexpected error', 'danger')
            # flash(f"Transaction Error: {e}",'danger')
            # Fallback to home if no referrer
            return redirect(request.referrer or '/')
    return wrapper
