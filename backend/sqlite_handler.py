import sqlite3
import sqlite_conf as cfg
from secrets import token_urlsafe

DATABASE = '../data/stayin_alive.db'


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


def new_call(phone_number, category):
    user_id = insert(DATABASE, cfg.insert_queries['users'], [phone_number])
    incident_id = insert(DATABASE, cfg.insert_queries['incidents'], ['NULL', 'NULL', category])
    token = token_urlsafe()
    query(DATABASE, cfg.insert_queries['incident_user'], [incident_id, user_id, token])
    return token


def add_media(media, token):
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    insert(DATABASE, cfg.insert_queries['media'], [media, incident_id])


def update_incident(lat, lon, token):
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    insert(DATABASE, cfg.update_queries['incidents'], [lat, lon, incident_id])


if __name__ == '__main__':
    create_tables(DATABASE)

    token = new_call('+972587030277', 'fire')
    add_media('./backend/streetview/gsv_0.jpg', token)
    update_incident('32.053016', '34.772589', token)
    print(query(DATABASE, 'SELECT * FROM incidents')[-1])

    token = new_call('+33630643415', 'water')
    add_media('./backend/streetview/blablabla.jpg', token)
    update_incident('30', '72', token)
    print(query(DATABASE, 'SELECT * FROM incidents')[-1])

    qry = """SELECT incidents.id, incidents.lat, incidents.lon, incidents.category, incident_user.key, users.phone_number
                 FROM incidents
                 JOIN incident_user
                    ON incidents.id == incident_user.incident_id
                 JOIN users
                    ON users.id == incident_user.user_id
          """
    [print(r) for r in query(DATABASE, qry)]
