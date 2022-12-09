from . import bp as app
from app import db
from .models import User, Post, Comment, Car
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_required


@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html.j2', title='Users', users=users)

@app.route('/user/<string:username>')
@login_required
def display_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html.j2', title=user.username ,user=user, posts=posts)

@app.route('/create_post', methods=['POST'])
@login_required
def create_post():
    title = request.form['inputTitle']
    body = request.form['inputBody']
    new_post = Post(title=title, body=body, user_id=current_user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(location=url_for('main.home'))

@app.route('/post/<int:post_id>')
@login_required
def display_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html.j2', title=f"Post {post.title}", post=post, comments=comments)