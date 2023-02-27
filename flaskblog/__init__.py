from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


app = Flask(__name__)
db = SQLAlchemy(app) #an sqlalchemy database instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) #add some functionalities to the backend, and it will handle the login session
login_manager.login_view = 'login' #this sets the view that the user will be redirected to if they try to access a protected page without being logged in.
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
mail = Mail(app)


from flaskblog import routes
