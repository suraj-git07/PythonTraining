from flask import Flask
from flask_login import LoginManager
from app.models import db, User

def create_app():
    # Create Flask application instance
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = 'supersecretkey'  # Used for sessions and security (e.g., CSRF protection)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'  # Database location
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary signals

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Initialize Flask-Login for user session management
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Redirect users to this route if they're not logged in
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Define how to load a user from the database
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints for modular routing
    from app.routes.auth import auth_bp      # Handles authentication (login, signup)
    from app.routes.tasks import tasks_bp    # Handles main task-related routes

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Auth routes start with /auth
    app.register_blueprint(tasks_bp, url_prefix='/')     

    return app  # Return the fully configured app
