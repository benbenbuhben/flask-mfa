from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the db instance from the current package

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Set the password hash for the user."""
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        """Return a string representation of the User instance."""
        return f'<User {self.email}>'
