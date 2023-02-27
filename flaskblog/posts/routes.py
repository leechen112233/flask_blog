from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog.posts.forms import PostForm
from flaskblog.models import Post
from flaskblog import db
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created successfully!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form)

@posts.route("/post/<int:post_id>", methods = ['GET', 'POST', 'PUT'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, legend='new_post')

@posts.route("/post/<int:post_id>/update", methods = ['GET', 'POST', 'PUT'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        # use the post's title and content for the update post page
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', title='Update Post', form=form, legend='Update_post')

@posts.route("/post/<int:post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted successfully!', 'success')
    return redirect(url_for('main.home'))





