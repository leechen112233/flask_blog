from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegisterForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user

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
        hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # this is to hash the password and convert the bytes password into a regular string
        user = User(username=form.username.data, email=form.email.data, password =hased_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login failed, please check email and password ', 'danger')
    return render_template('login.html', title='login', form=form)
