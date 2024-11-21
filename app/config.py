# import os

# class Config:
#     SECRET_KEY = os.environ.get("SECRET_KEY")
#     DB_USER = os.environ.get("DB_USER")
#     DB_PASSWORD = os.environ.get("DB_PASSWORD")
#     DB_HOST = os.environ.get("DB_HOST")
#     DB_NAME = os.environ.get("DB_HOST", "mfa_demo")
#     SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "localhost")  # Provide a default value if necessary
    DB_NAME = os.getenv("DB_NAME", "mfa_demo")   # Corrected DB_NAME to use DB_NAME environment variable
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/mfa_demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SECRET_KEY = os.environ.get('SECRET_KEY')

    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE = os.getenv("TWILIO_PHONE")
    # TWILIO_SERVICE_SID= os.getenv("TWILIO_SERVICE_SID")
    TWILIO_CONTENT_SID = os.getenv("TWILIO_CONTENT_SID")