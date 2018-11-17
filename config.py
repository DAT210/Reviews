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
		'database': 'reviews_db',
		'user': os.environ.get('DB_USER'),
		'password': os.environ.get('DB_PSWRD')
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
		'database': None,
		'user': os.environ.get('DB_TEST_USER'),
		'password': os.environ.get('DB_TEST_PSWRD')
	}


class LocalConfig(DevelopmentConfig):
	DB_CONFIG = {
		'host': 'localhost',
		'port': 3306,
		'database': 'reviews_db',
		'user': os.environ.get('DB_LOCAL_USER'),
		'password': os.environ.get('DB_LOCAL_PSWRD')
	}


class ProductionConfig(Config):
	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

		import logging
		from logging.handlers import HTTPHandler
		# TODO: Add logging handler to admin site if wanted.


class DockerConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.INFO)
		app.logger.addHandler(file_handler)


class AzureConfig(ProductionConfig):
	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'docker': DockerConfig,
	'azure': AzureConfig,
	'local': LocalConfig,

	'default': DevelopmentConfig
}
