import os
from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABSE_URI'] = os.environ.get('SQLALCHEMY_DATABSE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/license')
def license():
    return render_template('license.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/stock/<name>')
def stock(name):
    query = request.args.get('q')
    # find the correct stock from the search term here
    # perform stock analysis here
    return render_template('stock.html', **{
        'name': name
    })
