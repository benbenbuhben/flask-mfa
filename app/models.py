import uuid
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from . import db  # Import the db instance from the current package


def default_expires_at():
    return datetime.now() + timedelta(minutes=5)


def default_created_at():
    return datetime.now()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=default_created_at)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        """Set the password hash for the user."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        """Return a string representation of the User instance."""
        return f"<User {self.email}>"

    def valid_lastlogin(self):
        if self.last_login and datetime.now() - self.last_login <= timedelta(hours=1):
            return True
        else:
            return False

    def update_lastlogin(self):
        self.last_login = datetime.now()


class TemporaryCode(db.Model):
    __tablename__ = "temporary_codes"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=default_created_at)
    expires_at = db.Column(db.DateTime, nullable=False, default=default_expires_at)

    user = db.relationship(
        "User", backref="temporary_codes"
    )  # Referencing the User class
