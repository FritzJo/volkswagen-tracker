import sqlite3
from sqlite3 import Error
import datetime


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def add_entry(data):
    database = r"volkswagen.db"
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS volkswagen (
                                    id integer PRIMARY KEY,
                                    date text NOT NULL,
                                    mileage integer,
                                    range integer,
                                    chargeStatus integer,
                                    batteryPercentage integer,
                                ); """

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_projects_table)
    else:
        print("Error! cannot create the database connection.")

    sql = ''' INSERT INTO volkswagen(date,mileage,range,chargeStatus,batteryPercentage)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data[0], data[1], data[2], data[3], data[4])
    return cur.lastrowid
