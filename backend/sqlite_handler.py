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


if __name__ == '__main__':
    create_tables(DATABASE)

    user_id = insert(DATABASE, cfg.insert_queries['users'], ['+972587030277'])
    incident_id = insert(DATABASE, cfg.insert_queries['incidents'], ['NULL', 'NULL', 'fire'])
    media_id = insert(DATABASE, cfg.insert_queries['media'], ['./backend/streetview/gsv_0.jpg', 1])

    token = token_urlsafe()
    iu_id = query(DATABASE, cfg.insert_queries['incident_user'], [incident_id, user_id, token])

    print(query(DATABASE, 'SELECT * FROM incidents')[-1])
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    print(incident_id)
    insert(DATABASE, cfg.update_queries['incidents'], ['32.053016', '34.772589', 'fire', incident_id])
    print(query(DATABASE, 'SELECT * FROM incidents')[-1])

    user_id = insert(DATABASE, cfg.insert_queries['users'], ['+33630643415'])
    incident_id = insert(DATABASE, cfg.insert_queries['incidents'], ['NULL', 'NULL', 'water'])
    media_id = insert(DATABASE, cfg.insert_queries['media'], ['./backend/streetview/blablabla.jpg', 1])

    token = token_urlsafe()
    iu_id = insert(DATABASE, cfg.insert_queries['incident_user'], [incident_id, user_id, token])

    print(query(DATABASE, 'SELECT * FROM incidents')[-1])
    incident_id = query(DATABASE, cfg.queries['id_from_token'], [token])[0][0]
    print(incident_id)
    query(DATABASE, cfg.update_queries['incidents'], ['30', '72', 'water', incident_id])
    print(query(DATABASE, 'SELECT * FROM incidents')[-1])

    # print(query(DATABASE, 'SELECT * FROM media')[-1])
    # print(query(DATABASE, 'SELECT * FROM users')[-1])
    # print(query(DATABASE, 'SELECT * FROM incidents')[-1])
    # print(query(DATABASE, 'SELECT * FROM incident_user')[-1])

    qry = """SELECT incidents.id, incidents.lat, incidents.lon, incidents.category, incident_user.key, users.phone_number
                 FROM incidents
                 JOIN incident_user
                    ON incidents.id == incident_user.incident_id
                 JOIN users
                    ON users.id == incident_user.user_id
          """
    [print(r) for r in query(DATABASE, qry)]
