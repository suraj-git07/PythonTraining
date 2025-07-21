from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize the SQLAlchemy ORM object
db = SQLAlchemy()

# User model definition
class User(UserMixin, db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='user', lazy=True, cascade='all, delete-orphan')

    # Hash and set the user's password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    # Verify the password against the hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

# Task model definition
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign key: links task to its owning user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Returns a CSS class name based on how urgent the task is
    def get_priority_class(self):
        if not self.due_date:
            return 'normal'
        
        from datetime import date
        today = date.today()
        days_until_due = (self.due_date - today).days

        if days_until_due < 0:
            return 'overdue'
        elif days_until_due == 0:
            return 'due-today'
        elif days_until_due <= 3:
            return 'due-soon'
        else:
            return 'normal'
    