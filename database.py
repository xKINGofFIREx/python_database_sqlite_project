import sqlite3

sqlite_connection = sqlite3.connect('Popular_russian_writers')


def connect_db():
    try:
        cursor = sqlite_connection.cursor()
        print("Database created and Successfully Connected to SQLite")

        sqlite_select_query = "select sqlite_version();"
        cursor.execute(sqlite_select_query)
        record = cursor.fetchall()
        print("SQLite Database Version is: ", record)
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)


def disconnect_db():
    if sqlite_connection:
        sqlite_connection.close()
        print("The SQLite connection is closed")
