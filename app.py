from secrets import token_urlsafe
import json

from flask import Flask, request, jsonify, abort, render_template
from twilio.rest import Client
import requests
import base64
from db import sqlite_handler as sql
import app_cfg

STATION_LOC = [32.009719, 34.7631017]



def send_sms(message, receiver_phone):
    """
    This function receives a message and receiver phone, and sends SMS using twilio services.
    :param message: Message to be sent (str)
    :param receiver_phone: Receiver's phone (str)
    :return: SMS id if successfully sent, or error message if failed
    """
    try:
        client = Client(app_cfg.ACCOUNT_SID, app_cfg.AUTH_TOKEN)

        message = client.messages \
            .create(
            body=message,
            from_=app_cfg.SENDER_PHONE,
            to=receiver_phone
        )
        return message.sid
    except:
        return 'An error ocurred, message was not sent. Please re-send or contact your system administrator.'


# send_sms("fuck yuval", "+972546488261")




# Windows: set FLASK_APP=./backend/app.py
# Linux: export FLASK_APP=./backend/app.py
# flask run


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
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={str(STATION_LOC[0])},{str(STATION_LOC[1])}&destinations={str(reporter_lat)},{str(reporter_lon)}&key={app_cfg.GOOGLE_KEY}&mode=driving&traffic_model=best_guess&departure_time=now'
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
@app.route("/")
def hello():

    # data = request.get_json(force=True)

    # token = request.args['token']
    # print(token)
    return render_template('./user/index.html')

@app.route('/forces/home')
def forces_home():
    return render_template('./forces/index.html', GOOGLE_API_KEY=app_cfg.GOOGLE_KEY)

@app.route('/forces/get_event_data')
def get_event_data():
    token = request.args['token']
    print(token)
    my_event_data = sql.get_all_from_token(token)
    # html = ''
    # for key, value in my_event_data.items():
    #     # if key != 'medias':
    #     #     html += f'<div>{key}: {value}</div><br>'
    #     print(f'{key}: {value}')
    # html += '<div>'
    # for media in my_event_data['medias']:
    #     html += f'<img src="{media}" />'
    # html += '</div>'
    return json.dumps(my_event_data)
    # return html

@app.route('/user_response/', methods=['POST'])
def user_response():
    content = request.json
    # content['img'] = content['img'].split(',')[1]
    img = content['img']
    lat = content['lat']
    lon = content['lon']
    wind_speed = content['windSpeed']
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', content['token'])
    token = content['token']
    sql.update_incident(lat, lon, wind_speed, token)
    sql.add_media(img, token)
    return 'Thank you!'


@app.route('/admin')
def admin_form():
    return render_template('./admin/index.html')


events = []


@app.route('/send_new_event', methods=['POST'])
def send_new_event():
    global events
    # token = token_urlsafe()
    token = 'Yt-03UGyIbGAOeeOVRhYw-KS0AQZmi6ZVIVvN_G3aMR'
    event = {'token': token, 'life_threat': request.form.get('isLifeThreat'),
             'address1': request.form.get('address'), 'address2': request.form.get('address2'),
             'free_text': request.form.get('textarea'), 'phone_number': request.form.get('phoneNumber'),
             'category': request.form.get('customRadio')}
    events.append(event)
    print('>>>>>>>>', event)

    sql.new_call(event['phone_number'], event['category'], event['life_threat'], event['address1'], event['address2'],
                 event['free_text'], event['token'])

    send_sms(f"{app_cfg.url}:{app_cfg.port}/?token={event['token']}", event['phone_number'])
    return '<a href=' + f"http://{app_cfg.url}:{app_cfg.port}/?token={event['token']}" + '>' + f"http://{app_cfg.url}:{app_cfg.port}/?token={event['token']}" + '</a>'


if __name__ == '__main__':
    # print(send_sms('Hello world!', app_cfg.DEFAULT_RECIPIENT))
    app.run(debug=True)