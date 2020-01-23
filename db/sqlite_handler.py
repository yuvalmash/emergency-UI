import sqlite3
import os
from secrets import token_urlsafe
import base64
import sys
if 'db' in sys.modules.keys():
    from . import sqlite_conf as cfg
else:
    import sqlite_conf as cfg
db_path = os.path.dirname(cfg.__file__)
DATABASE = os.path.join(db_path, 'stayin_alive.db')


def insert(database, qry, data=None):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if data is not None:
        cur.execute(qry, data)
        result = cur.lastrowid
    else:
        cur.execute(qry)
        result = cur.fetchall()
    con.commit()
    con.close()
    return result


def query(database, qry, data=None):
    con = sqlite3.connect(database)
    cur = con.cursor()
    if data is not None:
        cur.execute(qry, data)
    else:
        cur.execute(qry)
    result = cur.fetchall()
    con.commit()
    con.close()
    return result


def create_table(database, table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(table)
    con.commit()
    con.close()


def create_tables(database):
    for table in cfg.tables:
        create_table(database, table)


def new_call(phone_number, category, life_threat, address1, address2, free_text, token):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>', DATABASE)
    user_id = insert(DATABASE, cfg.insert_queries['users'], [phone_number])
    incident_id = insert(DATABASE, cfg.insert_queries['incidents'], [category, life_threat, address1, address2, free_text])
    query(DATABASE, cfg.insert_queries['incident_user'], [incident_id, user_id, token])


def add_media(media, token):
    # bmedia = base64.b64decode(media)
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    insert(DATABASE, cfg.insert_queries['media'], [media, incident_id])


def get_media(token):
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    medias = query(DATABASE, cfg.queries['get_media'], [incident_id])
    # medias = [base64.b64encode(bmedia[0]) for bmedia in bmedias]
    medias = [media[0] for media in medias]
    return medias


def get_incident_from_token(token):
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    [((lat, lon, wind_speed, category, life_threat, address1, address2, free_text, start_time))] = query(DATABASE, cfg.queries['get_incident_from_token'], [incident_id])
    return {'lat': lat, 'lon': lon, 'wind_speed': wind_speed, 'category': category, 'life_threat': life_threat,
            'address1': address1, 'address2': address2, 'free_text': free_text, 'start_time': start_time}


def get_all_from_token(token):
    result = get_incident_from_token(token)
    result['token'] = token
    result['medias'] = get_media(token)
    return result


def update_incident(lat, lon, wind_speed, token):
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    insert(DATABASE, cfg.update_queries['incidents'], [lat, lon, wind_speed, incident_id])


if __name__ == '__main__':
    create_tables(DATABASE)

    token = token_urlsafe()
    new_call('+972587030277', 'fire', True, 'Tel Aviv', 'Florentin', 'Some Free Text', token)
    add_media('Some Image base64 encoded', token)
    update_incident('32.053016', '34.772589', '15.0', token)
    print(query(DATABASE, 'SELECT * FROM incidents')[-1])

    qry = """SELECT incidents.id, incidents.lat, incidents.lon,
                    incidents.category, incident_user.token, 
                    users.phone_number
                 FROM incidents
                 JOIN incident_user
                    ON incidents.id == incident_user.incident_id
                 JOIN users
                    ON users.id == incident_user.user_id
          """
    # [print(r) for r in query(DATABASE, qry)]
    # for media in get_media('XtZQ40v-qpqYKDAxoToE1tN4ZLo45ATtK6sv4pZnT7s'):
    #     print(media)
    print(get_all_from_token('lk8wsnVLcnQoJ-YteGrlP7Vo-Yei9bC7HMbu3UYma5g'))
