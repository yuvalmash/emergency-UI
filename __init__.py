from flask import Flask, request, jsonify, abort, render_template
from twilio.rest import Client
import requests
import base64

ACCOUNT_SID = 'AC5f1460f752c9e622a921b909e70dba6e'
AUTH_TOKEN = 'd7c0cbf61857b3cc1ed640febfb22dbf'
SENDER_PHONE = '+972525835074'
STATION_LOC = [32.009719, 34.7631017]
GOOGLE_KEY = 'AIzaSyBgPmnoaTooWJdgcHor2jUeCMFRv40ekkA'
DEFAULT_RECIPIENT = '+972587030277'


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


# app = Flask(__name__, static_folder='../../frontend/', template_folder='../../frontend/')
app = Flask(__name__)
tels = []
incidents = []


def getApp():
    return app


#
# @app.route('/')
# def hello_world():
#     print(send_sms("hello world", DEFAULT_RECIPIENT))
#     return "Stayin' Alive API"


@app.route('/get_sms')
def show_sms():
    return jsonify(tels)


@app.route('/send_sms', methods=['POST'])
def create_sms():
    print("hello")
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


@app.route('/time_to_arrival')
def get_time_to_arrival(reporter_lat=32.051195, reporter_lon=34.755205):
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={str(STATION_LOC[0])},{str(STATION_LOC[1])}&destinations={str(reporter_lat)},{str(reporter_lon)}&key={GOOGLE_KEY}&mode=driving&traffic_model=best_guess&departure_time=now'
    r = requests.get(url)
    if r.status_code == 200:
        response = r.json()
        origin_address = response['origin_addresses'][0]
        dest_address = response['destination_addresses'][0]
        distance = response['rows'][0]['elements'][0]['distance']['text']
        time = response['rows'][0]['elements'][0]['duration_in_traffic']['text']
        return f'<b>Origin address:</b> {origin_address}<br><b>Destination address:</b> {dest_address}<br><b>Distance:</b> {distance}<br><b>Estimated time to arrival:</b> {time}'
    else:
        return 'Error retrieving data'


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


########################################################################################################################
@app.route("/<token>")
def hello(token):
    print(token)
    return render_template('./user/index.html')


@app.route('/user_response/', methods=['POST'])
def user_response():
    content = request.json
    content['img'] = content['img'].split(',')[1]
    img = content['img']
    lat = content['lat']
    lon = content['lon']
    print(img)
    print(lat)
    print(lon)
    img = base64.b64decode(img)
    with open('img.png', 'wb') as file:
        file.write(img)
    return img

events = []


@app.route('/send_new_event', methods=['POST'])
def send_new_event():
    global events
    event = {}
    event['isLifeThreat'] = request.form.get('isLifeThreat')
    event['address'] = request.form.get('address')
    event['address2'] = request.form.get('address2')
    event['textarea'] = request.form.get('textarea')
    event['phoneNumber'] = request.form.get('phoneNumber')
    event['category'] = request.form.get('customRadio')
    events.append(event)
    return str(events)


if __name__ == '__main__':
    print(send_sms('fuck yuval', DEFAULT_RECIPIENT))
    app.run(debug=True)
