'''The database portion of the review application'''

# Imports:
from flask import (
	g, current_app
)
import mysql.connector

def get_db():
	"""Makes an unique connection for each context to the database of the application,\
	reuses it if it's called again."""
	if not hasattr(g, '_database'):
		g._database = mysql.connector.connect(
			host=current_app.config['DB_CONFIG']['host'], 
			user=current_app.config['DB_CONFIG']['user'],
			password=current_app.config['DB_CONFIG']['pswrd'],
			database=current_app.config['DB_CONFIG']['db'],
			port=current_app.config['DB_CONFIG']['port']
			)
	return g._database

def teardown_db(error):
	"""Closes the connection if this context connected to the database."""
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()