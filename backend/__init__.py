from flask import Flask, request

# export FLASK_APP=backend/__init__.py

# Windows: set FLASK_APP=./backend/__init__.py
# Linux: export FLASK_APP=./backend/__init__.py


app = Flask(__name__)

tels = []


def getApp():
    return app


@app.route('/')
def hello_world():
    return "Stayin' Alive API"


@app.route('/send_sms', methods=['POST'])
def create_sms():
    tel = {
        'tel': request.json['tel'],
    }
    tels.append(tel)
    return jsonify({'tel': tel}), 201


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


if __name__ == '__main__':
    app.run(debug=True)
