"""Initialize the Customer blueprint"""
from flask import Blueprint

# Define the blueprint
customer = Blueprint("customer", __name__)

# Import routes (this ensures they are registered with the blueprint)
from . import routes