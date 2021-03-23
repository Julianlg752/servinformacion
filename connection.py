import mysql.connector
import sys
from os import environ


def connection():
    mydb = mysql.connector.connect(
        host=val("HOSTNAME"),
        database=val("DBNAME"),
        user=val("DBUSER"),
        password=val("DBPASS"),
        port=val("DBPORT")
    )
    return mydb


def val(key):
    if environ.get(key) is not None:
        return environ.get(key)
    else:
        print("Missing key: ", key)
        sys.exit()
