
# Imports:
from flask import g, current_app
from flask.cli import with_appcontext
import mysql.connector
import click

DB_HOST="mysql"
DB_USER="exerian"
DB_PSWRD="root"
DB_DATABASE="reviews_db"

def get_db(main_db=DB_DATABASE, active_db=True):
	if not active_db:
			main_db = ""
	if not hasattr(g, '_database'):
		g._database = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PSWRD)
	return g._database

def teardown_db(error):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def init_db():
	db = get_db(active_db=False)
	cursor = db.cursor()
	try:
		with current_app.open_resource('database.sql') as f:
			statements = f.read().decode('utf8')
			for statement in statements.split(';'):
				cursor.execute(statement)
		db.commit()
	except mysql.connector.Error as err:
		print(f"Error_testDBbuild: {err}")
	finally:
		cursor.close()

@click.command('init-db')
@with_appcontext
def init_db_command():
	click.echo("Initialize Database")
	init_db()


def init_app(app):
	app.teardown_appcontext(teardown_db)
	app.cli.add_command(init_db_command)