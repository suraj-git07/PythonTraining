from app import create_app
from app.models import db

# Create an instance of the Flask app using the factory pattern
app = create_app()

# Use the app's context to initialize or access app-specific features
# This ensures db.create_all() knows which app it's working with
with app.app_context():
    # Create all tables defined in models.py 
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)  
