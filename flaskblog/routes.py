from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegisterForm, LoginForm
from flaskblog.models import User, Post
from flaskblog import app

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
