from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2ecf156c9f1a38634e9da387fba6bab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #this is the relevant path from the current file
db = SQLAlchemy(app) #an sqlalchemy database instance

from flaskblog import routes
