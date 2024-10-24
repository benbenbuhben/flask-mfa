import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{DB_PASSWORD}@db/mfa_demo"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
