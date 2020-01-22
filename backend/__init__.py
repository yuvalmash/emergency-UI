from flask import Flask, request, jsonify, abort
from twilio.rest import Client

ACCOUNT_SID = 'AC5f1460f752c9e622a921b909e70dba6e'
AUTH_TOKEN = 'd7c0cbf61857b3cc1ed640febfb22dbf'
SENDER_PHONE = 'whatsapp:+14155238886'


def send_sms(message, receiver_phone):
    """
    This function receives a message and receiver phone, and sends SMS using twilio services.
    :param message: Message to be sent (str)
    :param receiver_phone: Receiver's phone (str)
    :return: SMS id if successfully sent, or error message if failed
    """
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)

        message = client.messages \
            .create(
                body=message,
                from_=SENDER_PHONE,
                to=receiver_phone
            )
        return message.sid
    except:
        return 'An error ocurred, message was not sent. Please re-send or contact your system administrator.'

# send_sms("fuck yuval", "+972546488261")


# export FLASK_APP=backend/__init__.py
# flask run

# Windows: set FLASK_APP=./backend/__init__.py
# Linux: export FLASK_APP=./backend/__init__.py


app = Flask(__name__)
tels = []
incidents = []


def getApp():
    return app


@app.route('/')
def hello_world():
    send_sms("fuck yuval", "+972546488261")
    return "Stayin' Alive API"


@app.route('/get_sms')
def show_sms():
    return jsonify(tels)


@app.route('/send_sms', methods=['POST'])
def create_sms():
    tel = {
        'tel': request.json['tel']
    }
    tels.append(tel)
    return jsonify({'tel': tel}), 201


@app.route('/send_event', methods=['POST'])
def send_event():
    print("got into post request")
    incident = {
        'lat': request.json['lat'],
        'lon': request.json['lon']
    }
    incidents.append(incident)
    return jsonify({'incident': incident}), 201


@app.route('/new_event', methods=['POST'])
def create_incident():
    incident = {
        'lat': request.json['lat'],
        'lon': request.json['lon']
    }
    incidents.append(incident)
    return jsonify(incident)


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
