'''The database portion of the review application'''

# Imports:
from flask import (
	g, current_app
)
import click
from flask.cli import with_appcontext
import mysql.connector


def get_db():
	"""Makes an unique connection for each context to the database of the\
	application, reuses it if it's called again."""

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


@click.command('init-db')
@click.option(
	'--host', default='localhost',
	help="The host address of the database, default=localhost"
)
@click.option(
	'--user', default='root',
	help="Set database user to be used, default=root"
)
@click.option(
	'--pswrd', default='root',
	help="Set database password to be used, default=root"
)
@with_appcontext
def build_db(host, user, pswrd):
	config = {
		'host': host,
		'db': None,
		'user': user,
		'pswrd': pswrd
	}
	click.echo(f"Database initializing @{config['host']}...")
	current_app.config['DB_CONFIG'].update(config)

	db = get_db()
	cursor = db.cursor(buffered=True)

	try:
		with current_app.open_resource('../db/init.sql') as f:
			statements = f.read().decode('utf8')
			for statement in statements.split(';'):
				cursor.execute(statement)
		db.commit()
	except mysql.connector.Error as err:
		click.echo('Failed initializing database.')
		click.echo(str(err), err=True)
	finally:
		cursor.close()
		current_app.config['DB_CONFIG'].update({'db': 'reviews_db'})
		click.echo('Database initialized!')
