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
twilio_phone = Config.TWILIO_PHONE

twilio_service_sid = Config.TWILIO_SERVICE_SID  # This should be in your config if you already have a service SID

# If you don't have a pre-created Verify service, you can create one dynamically (optional)
if not twilio_service_sid:
    service = twilio_client.verify.services.create(
        friendly_name='Your Service Name'
    )
    twilio_service_sid = service.sid
    app.config['TWILIO_SERVICE_SID'] = twilio_service_sid 


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
    
    