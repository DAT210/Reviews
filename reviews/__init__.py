'''The review module'''

# Imports:
import os
from flask import Flask

def create_app(test_config=None, mode='dev'):
	"""Create and configure an instance of the Flask application."""
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		# a default secret that should be overridden by instance config
		SECRET_KEY='dev',
		DEBUG=True,
	)

	if test_config is None:
		# load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.update(test_config)

	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.route('/hello/')
	def hello():
		return f"Hello, World!"

	from reviews import db
	app.teardown_appcontext(db.teardown_db)
	app.cli.add_command(db.build_db)

	from reviews import api
	app.register_blueprint(api.bp)

	return app