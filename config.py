import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # MySQL database configuration
    DB_USERNAME = os.environ.get('DB_USERNAME', 'turf_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'turf_password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'turf_time')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # Email Configuration - Updated for more reliable delivery
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))  # Changed to 465 for SSL
    MAIL_USE_TLS = False  # Disabled TLS
    MAIL_USE_SSL = True   # Enabled SSL instead (more reliable with Gmail)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'turftime4@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'fggdasmdjpqezrwc')  # App password for Gmail
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'Turf Time <turftime4@gmail.com>')
    
    # Additional email settings for debugging
    MAIL_DEBUG = os.environ.get('MAIL_DEBUG', 'True').lower() == 'true'
    MAIL_MAX_EMAILS = int(os.environ.get('MAIL_MAX_EMAILS', 3))
    MAIL_SUPPRESS_SEND = False  # Make sure emails are actually sent