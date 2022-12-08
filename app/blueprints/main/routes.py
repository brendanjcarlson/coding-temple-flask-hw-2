from . import bp as app
from flask import render_template, request, redirect, url_for, flash, request, session
from app import db
from app.blueprints.blog.models import User, Post, Comment, Car


@app.route('/', methods=['GET', 'POST'])
def home():
    cars = Car.query.all()
    if request.method == 'POST':
        make = request.form['inputMake'].strip()
        model = request.form['inputModel'].strip()
        year = request.form['inputYear'].strip()
        color = request.form['inputColor'].strip()
        price = request.form['inputPrice'].strip()
        new_car = Car(make=make, model=model, year=year, color=color, price=price, user_id=2)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('main.home', title='Home', cars=cars))

    else:
        return render_template('home.html.j2', title='Home', cars=cars)

@app.route('/about')
def about():
    return render_template('about.html.j2', title='About')