import sqlite3
import tables

DATABASE = '../data/stayin_alive.db'


def create_table(database, table):
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute(table)
    con.close()


def create_tables(database):
    for table in tables.tables:
        create_table(database, table)


if __name__ == '__main__':
    create_tables(DATABASE)