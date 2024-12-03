import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from .config import Config
from twilio.rest import Client
from flask_wtf.csrf import CSRFProtect

# Initialize the database
db = SQLAlchemy()
csrf = CSRFProtect()

# Set up Twilio client (initialization will happen in create_app)
twilio_client = None
twilio_content_sid = None
twilio_phone = None

# Set up logging (initialization will happen in create_app)
logger = None

def create_app(config_class=Config):
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Enable CSRF protection
    csrf.init_app(app)

    # Initialize the database with the app
    db.init_app(app)

    # Set up Twilio client
    global twilio_client, twilio_content_sid, twilio_phone
    twilio_client = Client(config_class.TWILIO_ACCOUNT_SID, config_class.TWILIO_AUTH_TOKEN)
    twilio_content_sid = config_class.TWILIO_CONTENT_SID
    twilio_phone = config_class.TWILIO_PHONE

    # Set up logging
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s: %(message)s')
    global logger
    logger = logging.getLogger(__name__)

    # Register the before_request function for cleanup tasks (like deleting expired codes)
    @app.before_request
    def setup():
        create_delete_event(app)

    # Import and register routes blueprint to avoid circular imports
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app

def create_delete_event(app):
    """Create MySQL Event to delete expired codes."""
    sql = """
    CREATE EVENT IF NOT EXISTS delete_expired_codes
    ON SCHEDULE EVERY 5 MINUTE
    DO 
    DELETE FROM temporary_codes WHERE expires_at < NOW();
    """
    with app.app_context():
        db.session.execute(text(sql))  # Directly pass the SQL string
        db.session.commit()