from . import bp as app
from app.blueprints.blog.models import User
from app import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html.j2', title='Login')

    email = request.form['inputEmail']
    password = request.form['inputPassword']
    next_url = request.form['next']

    user = User.query.filter_by(email=email).first()

    if user is None:
       flask(f'No user with email {email} found.', 'danger')
    elif user.check_password(password):
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        if next_url:
            return redirect(next_url)
        return redirect(url_for('main.home'))
    else:
        flash('Invalid credentials.', 'danger')

    return render_template('login.html.j2', title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html.j2', title='Register')

    email = request.form['inputEmail']
    username = request.form['inputUsername']
    password = request.form['inputPassword']
    confirm_password = request.form['inputConfirmPassword']
    first_name = request.form['inputFirstName']
    last_name = request.form['inputLastName']

    check_user = User.query.filter_by(email=email).first()

    if check_user is not None:
        flash(f'User with email {email} already exists.', 'danger')
    elif password != confirm_password:
        flash('Passwords do not match.', 'danger')
    else:
        try:
            new_user = User(email=email, username=username, password=password, first_name=first_name, last_name=last_name)
            new_user.hash_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Welcome, {username}!', 'success')
            return redirect(url_for('auth.login'))
        except:
            flash('Something went wrong. Please try again.', 'danger')

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

@app.route('reset_password', methods=['GET', 'POST'])
@login_required
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html.j2', title='Reset Password')

    old_password = request.form['inputOldPassword']
    new_password = request.form['inputNewPassword']
    confirm_new_password = request.form['inputConfirmNewPassword']

    if new_password != confirm_new_password:
        flash('Passwords do not match.', 'danger')
    elif not current_user.check_password(old_password):
        flash('Old password is incorrect.', 'danger')
    else:
        current_user.hash_password(new_password)
        db.session.add(current_user)
        db.session.commit()
        flash('Password has been updated.', 'success')

        return redirect(url_for('auth.login'))
