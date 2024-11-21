import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from .config import Config
from twilio.rest import Client

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db = SQLAlchemy()
db.init_app(app)

# set up twillio
twilio_client = Client(Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
twilio_content_sid = Config.TWILIO_CONTENT_SID
twilio_phone = Config.TWILIO_PHONE
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Import routes
from app import routes  # noqa: F401, E402

def create_delete_event():
    """Create MySQL Event to delete expired codes"""

    sql = """
    CREATE EVENT IF NOT EXISTS delete_expired_codes
    ON SCHEDULE EVERY 5 MINUTE
    DO 
    DELETE FROM temporary_codes WHERE expires_at < NOW();
    """
    with app.app_context():
        db.session.execute(text(sql))  # Directly pass the SQL string
        db.session.commit()


@app.before_request
def setup():
    create_delete_event()
    
    