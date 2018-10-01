
# Imports:
from flask import g
import mysql.connector

DB_HOST="127.0.0.1"
DB_USER="root"
DB_PSWRD="root"
DB_DATABASE="group3_db"

def get_db():
    if not hasattr(g, '_database'):
        g._database = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PSWRD, database=DB_DATABASE)
    return g._database

def teardown_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()