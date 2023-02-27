import os
class Config:
    SECRET_KEY = os.environ.get('FLASK_BLOG_APP_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_BLOG_APP_SQLALCHEMY_DATABASE_URI') # this is the relevant path from the current file
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')