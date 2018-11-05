'''The review module'''

# Imports:
from flask import (
	Flask
)
from config import config
import os


def create_app(config_type='default'):
	"""Create and configure an instance of the Flask application."""
	app = Flask(__name__, instance_relative_config=True)

	# Add configurations:
	app.config.from_object(config[config_type])
	config[config_type].init_app(app)

	# Ensure the instance folder exists:
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
