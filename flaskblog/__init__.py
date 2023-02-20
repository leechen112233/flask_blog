from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2ecf156c9f1a38634e9da387fba6bab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #this is the relevant path from the current file
db = SQLAlchemy(app) #an sqlalchemy database instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) #add some functionalities to the backend, and it will handle the login session
login_manager.login_view = 'login' #this sets the view that the user will be redirected to if they try to access a protected page without being logged in.
login_manager.login_message_category = 'info'

from flaskblog import routes
