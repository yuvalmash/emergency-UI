# Windows: set FLASK_APP=./backend/app.py
# Linux: export FLASK_APP=./backend/app.py

from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Stayin' Alive API"


@app.route('/test/get_length/<my_var>')
def length(my_var):
    return f'{len(my_var)}'


@app.route('/test/get_length/')
def return_0():
    return f'0'


@app.route('/test/show_param/')
def show_param():
    args = request.args
    ret = ''
    for (key, value) in args.items():
        ret += f'{key}: {value}<br>'
    return ret