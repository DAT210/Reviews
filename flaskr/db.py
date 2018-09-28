
# Imports:
from flask import g
import mysql.connector

DB_HOST="localhost"
DB_USER="root"
DB_PSWRD="root"
DB_DATABASE="review"

def get_db():
    if hasattr(g, '_database'):
        g._database = mysql.connector.connect(host=, user=, password=, database=)
    return g._database

def teardown_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()