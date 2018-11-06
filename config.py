import os
from dotenv import load_dotenv, find_dotenv

secret = None


class Config:
	load_dotenv(find_dotenv())
	SECRET_KEY = (
		secret or os.environ.get('SECRET_KEY', 'top_secret_key').encode('latin'))
	APP_NAME = 'Review API'
	DB_CONFIG = {
		'host': 'dbserver',
		'port': 3306,
		'db': 'reviews_db',
		'user': os.environ.get('DB_USER'),
		'pswrd': os.environ.get('DB_PSWRD')
	}

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True


class TestingConfig(Config):
	TESTING = True
	DB_CONFIG = {
		'host': 'localhost',
		'port': 3306,
		'db': None,
		'user': os.environ.get('DB_TEST_USER'),
		'pswrd': os.environ.get('DB_TEST_PSWRD')
	}


class LocalConfig(DevelopmentConfig):
	DB_CONFIG = {
		'host': 'localhost',
		'port': 3306,
		'db': 'reviews_db',
		'user': '<set_to_whatever>',
		'pswrd': '<set_to_whatever>'
	}


class ProductionConfig(Config):
	@classmethod
	def init_app(app):
		Config.init_app(app)

		import logging
		from logging.handlers import HTTPHandler
		# TODO: Add logging handler to admin site if wanted.


class DockerConfig(ProductionConfig):
	@classmethod
	def init_app(app):
		ProductionConfig.init_app(app)

		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
