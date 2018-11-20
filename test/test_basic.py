
from flask import current_app
from reviews import create_app
import unittest


class TestBasic(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.app = create_app('testing')
		cls.app_context = cls.app.app_context()

	def setUp(self):
		pass

	def test_app_exists(self):
		"""Is the app created?"""
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		"""Is configuration set for testing?"""
		with self.app_context:
			self.assertTrue(current_app.config['TESTING'])

	def tearDown(self):
		pass

	@classmethod
	def tearDownClass(cls):
		pass
