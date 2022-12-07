from app import app, db
from flask import render_template
from app.models import User, Post, Comment, Car


@app.route('/')
def home():
    return render_template('home.html.j2', title='Home')

@app.route('/about')
def about():
    return render_template('about.html.j2', title='About')

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html.j2', title='Users', users=users)

@app.route('/user/<string:username>')
def display_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('profile.html.j2', title=user.username ,user=user, posts=posts)

@app.route('/post/<int:post_id>')
def display_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html.j2', title=f"Post {post.title}", post=post, comments=comments)