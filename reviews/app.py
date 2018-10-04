import os

from flask import Flask

test_config = None

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(SECRET_KEY='dev',
	DB_HOST = '127.0.0.1',
	DB_USER = 'root',
	DB_PSWRD = 'root',
	DB_DATABASE='meal_db',
	)

if test_config is None:
	app.config.from_pyfile('config.py', silent=True)
else:
	app.config.from_mapping(test_config)
try:
	os.makedirs(app.instance_path)
except OSError:
	pass

@app.route('/hello')
def hello():
	return 'Hello, World!'

from reviews import db
db.init_app(app)

from reviews import api
app.register_blueprint(api.bp)

if __name__ == '__main__':
    app.run()
