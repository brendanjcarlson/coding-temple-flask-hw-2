from . import bp as app
from flask import render_template, request, redirect, url_for, flash, request, session
from app import db
from app.blueprints.blog.models import User, Post, Comment, Car
from flask_login import current_user, login_required


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    cars = Car.query.all()
    if request.method == 'GET':
        return render_template('home.html.j2', title='Home', cars=cars, user=current_user)
    else:
        make = request.form['inputMake'].strip()
        model = request.form['inputModel'].strip()
        year = request.form['inputYear'].strip()
        color = request.form['inputColor'].strip()
        price = request.form['inputPrice'].strip()
        new_car = Car(make=make, model=model, year=year, color=color, price=price, user_id=current_user)
        db.session.add(new_car)
        db.session.commit()
        flash(f'Car added!', 'success')
        return redirect(url_for('main.home', title='Home', cars=cars))

@app.route('/about')
def about():
    return render_template('about.html.j2', title='About')