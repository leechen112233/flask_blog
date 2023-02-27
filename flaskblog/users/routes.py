from flask import Blueprint, render_template, url_for, flash, redirect, request
from flaskblog.users.forms import RegisterForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from flaskblog.models import User, Post
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # this is to hash the password and convert the bytes password into a regular string
        user = User(username=form.username.data, email=form.email.data, password =hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='register', form=form)

@users.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login failed, please check email and password ', 'danger')
    return render_template('login.html', title='login', form=form)

@users.route("/logout", methods = ['GET'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for("main.home"))

@users.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successfully', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET': # this is to populate the form from the current_user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int) # set default value to 1, and type is integer
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.id.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

@users.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    # make sure this user is logged out before reset password
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("There is no such email exists", 'error')
            return
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", 'success')
        return redirect(url_for("users.login"))
    return render_template('reset_request.html', title="Reset Password", form=form)

@users.route("/reset_password/<string:token>", methods = ['GET', 'POST'])
def reset_token(token):
    # make sure this user is logged out before reset password
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    user = User.verify_reset_token(token)

    if user is None:
        flash("This token is invalid or expired!", 'warning')
        return redirect(url_for("users.reset_request"))
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                'utf-8')  # this is to hash the password and convert the bytes password into a regular string
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated', 'success')
            return redirect(url_for('users.login'))
    return render_template('reset_token.html', title="Reset Password", form=form)