from flask import Blueprint

# Define the blueprint
auth = Blueprint("auth", __name__)

# Import routes (this ensures they are registered with the blueprint)
from . import routes