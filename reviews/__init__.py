'''The review module'''

# Imports:
from flask import (
	Flask
)
from config import config
import os


def create_app(config_type='default'):
	"""
	Create and configure an instance of the Flask application.\n
	The :param config_type: sets the environment of the application, which
	defaults to 'development', the configuration modes are:
	\t'development' which runs the application in development mode.
	\t'production' which runs the application in production mode.
	\t'azure' which runs the application in production mode for azure.
	\t'docker' which runs the application in production mode for docker.
	\t'testing' which runs the application in testing mode.
	\t'local' which runs the application in development mode for localhost.
	"""
	app = Flask(__name__, instance_relative_config=True)

	# Add configurations:
	app.config.from_object(config[config_type])
	config[config_type].init_app(app)

	# Creates an instance folder.
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	# Set teardown context and click command for DB:
	from reviews import db
	app.teardown_appcontext(db.teardown_db)
	app.cli.add_command(db.build_db)

	# Register blueprints:
	from reviews import api
	app.register_blueprint(api.bp)

	return app
