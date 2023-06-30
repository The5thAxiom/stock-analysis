import os
import pickle
import base64

from io import BytesIO
from datetime import datetime
from matplotlib.figure import Figure

from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

from models.lstm import get_20_days_n_preds

app = Flask(__name__)

app.config['SQLALCHEMY_DATABSE_URI'] = os.environ.get('SQLALCHEMY_DATABSE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

stock_names = []
with open('./stock_names.pickle', 'rb') as pkl:
    stock_names = pickle.load(pkl)

@app.route('/')
def index():
    return render_template('index.html', **{
        'stock_names': stock_names
    })

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/license')
def license():
    return render_template('license.html')

@app.route('/search')
def search():
    query = request.args.get('q')
    is_valid_stock = query in stock_names
    if query is None:
        return render_template('search.html', **{
            'stock_names': stock_names
        })
    elif is_valid_stock:
        return redirect(f'/stock/{query}')
    else:
        return render_template('search.html', **{
            'stock_names': stock_names,
            'error': f'{query} is not a valid stock symbol'
        })

@app.route('/stock/<name>')
def stock(name):
    # predictions graph
    stock_data = get_20_days_n_preds(name, n=10)

    fig = Figure()
    ax = fig.subplots()
    ax.set_title('Closing Price Predictions')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Close Price USD ($)', fontsize=18)
    ax.plot(stock_data)
    ax.axvline(x = datetime.today(), color='r')
    ax.legend(['Closing Price', 'Predictions'], loc='lower left')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    return render_template('stock.html', **{
        'name': name,
        'stock_names': stock_names,
        'close_graph_data': data
    })
