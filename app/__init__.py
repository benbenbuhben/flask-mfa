from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy()
# Initialize the database with the app
db.init_app(app)

# Import routes
from app import routes  # noqa: F401, E402
