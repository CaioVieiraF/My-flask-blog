import json
# import os

# If you want to run the code on your machine,
# uncomment the import and the constants

with open('/etc/config.json') as f:
    config = json.load(f)


class Config:
    """docstring for Config."""

    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('GMAIL_USER')
    MAIL_PASSWORD = config.get('GMAIL_PASS')
    # MAIL_USERNAME = os.environ.get('GMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('GMAIL_PASS')
