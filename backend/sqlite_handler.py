import sqlite3
import sqlite_conf as cfg

DATABASE = '../data/stayin_alive.db'


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
    query(DATABASE, cfg.insert_queries['users'], ['+972587030277'])
    query(DATABASE, cfg.insert_queries['incidents'], ['32.053016', ' 34.772589', 'fire'])
    query(DATABASE, cfg.insert_queries['media'], ['./backend/streetview/gsv_0.jpg', 1])
    query(DATABASE, cfg.insert_queries['incident_user'], [1, 1, 'someUniqueToken'])
    print(query(DATABASE, 'SELECT * FROM media LIMIT 5'))
    print(query(DATABASE, 'SELECT * FROM users LIMIT 5'))
    print(query(DATABASE, 'SELECT * FROM incidents LIMIT 5'))
    print(query(DATABASE, 'SELECT * FROM incident_user LIMIT 5'))
