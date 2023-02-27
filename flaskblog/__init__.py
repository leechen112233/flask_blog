from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app) #an sqlalchemy database instance
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) #add some functionalities to the backend, and it will handle the login session
login_manager.login_view = 'users.login' #this sets the view that the user will be redirected to if they try to access a protected page without being logged in.
login_manager.login_message_category = 'info'
mail = Mail(app)


from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)

