from . import bp as app
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html.j2', title='Home')

@app.route('/about')
def about():
    return render_template('about.html.j2', title='About')
