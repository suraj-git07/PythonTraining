import os
from flask import Flask,redirect,url_for
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import Config
import logging
from logging.handlers import RotatingFileHandler
# Import extensions from a separate file for better structure
from .extensions import db, login_manager, csrf

# Load environment variables
load_dotenv()

# Function to create the Flask app
def create_app(config_name='default'):
    app = Flask(__name__)
    # --- Logging Setup ---
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Optional: Console logging for dev
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Attach handlers
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    # ----------------------
    # Load configuration from config.py
    if config_name == 'testing':
        app.config.from_object("app.config.TestingConfig")
    else:
        app.config.from_object("app.config.Config")

    # Initialize Flask extensions
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Set login view for Flask-Login
    login_manager.login_view = "auth.login"

    # Initialize Flask-Migrate
    Migrate(app, db)

    # Register Blueprints
    from .auth import auth
    from .customer import customer
    from .restaurant import restaurant

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(customer, url_prefix="/customer")
    app.register_blueprint(restaurant, url_prefix="/restaurant")

    #add extension for do
    app.jinja_env.add_extension('jinja2.ext.do')

    # Create database tables if they don’t exist
    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return redirect(url_for('auth.login')) 
    
    return app
