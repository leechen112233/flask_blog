from flask import Flask
from flask import render_template, url_for, flash, redirect
from forms import RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c2ecf156c9f1a38634e9da387fba6bab'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #this is the relevant path from the current file
db = SQLAlchemy(app) #an sqlalchemy database instance

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True )
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', back_populates='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship('User', back_populates='posts', lazy=True)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}',')"

posts = [
    {
        'author':'li chen',
        'title':'blog post1',
        'content': ' first post content',
        'date_posted':'Feb 16 2023'
    },
{
        'author':'Fang Yiting',
        'title':'blog post2',
        'content': ' wo shi da sha zi',
        'date_posted':'Feb 17 2023'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='about')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'chen@okos.ca' and form.password.data == '1234':
            flash('You have logged in ', 'success')
            return redirect(url_for('home'))
        else:
            flash('failed ', 'danger')
    return render_template('login.html', title='login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
