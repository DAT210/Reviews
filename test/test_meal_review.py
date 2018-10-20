import unittest
import random
import reviews.review as review
import reviews.db as dbb
from flask import Flask, current_app

testcases = {
	'test_get_pluss_3': {
		'input': 3,
		'want': 3
	},
	'test_get_pluss_5': {
		'input': 5,
		'want': 5
	},
	'test_get_pluss_8': {
		'input': 2,
		'want': 2
	},
	'test_get_pluss_13': {
		'input': 1,
		'want': 1
	},
	'test_get_pluss_21': {
		'input': 4,
		'want': 4
	},
	'test_get_pluss_34': {
		'input': 0,
		'want': 0
	},
	'test_get_pluss_multi': {
		'input': (3, 5, 3, 3, 4, 2, 2),
		'want': 3.1
	},
	'test_get_pluss_multi2': {
		'input': (3, 5, 5, 3, 4, 2, 3),
		'want': (3, 4, 4.3, 4, 4, 3.7, 3.6)
	},
	'test_get_pluss_multi3': {
		'input': (4, 5, 2, 3, 6, 0, 3),
		'want': 3.4
	},
	'test_get_pluss_multi4': {
		'input': (3, 6, 2, 0, 1, 5, 3),
		'want': (3, 3, 2.5, 2.5, 2, round(2.75,1), 2.8)
	},
	'test_add_remove_1': {
		'input': ('test_01_01', 'test_01_02', 'test_01_03', 'test_01_04'),
		'want': (0, None, 0, None)
	}
}

app = Flask(__name__)
app.app_context()

def build_app():
	with app.app_context():
		build_db()

def build_db():
	db = dbb.get_db()
	cursor = db.cursor()
	try:
		with current_app.open_resource('build_test_db.sql') as f:
			statements = f.read().decode('utf8')
			for statement in statements.split(';'):
				cursor.execute(statement)
		db.commit()
	except dbb.mysql.connector.Error as err:
		print(f"Error_testDBbuild: {err}")
	finally:
		cursor.close()
	dbb.DB_DATABASE = "meal_testdb"
	dbb.DB_USER="root"
	dbb.DB_PSWRD="root"

class TestGet(unittest.TestCase):
	initialized = False
	
	def setUp(self):
		if not self.initialized:
			print(f"\nInitializing Testing...")
			build_app()
			self.__class__.initialized = True

	def test_get_pluss_3(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0203', review=testcases[key]['input'])
			ok = review.get(id='m_fs0203')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_5(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0205', review=testcases[key]['input'])
			ok = review.get(id='m_fs0205')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_8(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0208', review=testcases[key]['input'])
			ok = review.get(id='m_fs0208')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_13(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0213', review=testcases[key]['input'])
			ok = review.get(id='m_fs0213')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_21(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0221', review=testcases[key]['input'])
			ok = review.get(id='m_fs0221')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_34(self):
		key = str(self)
		key,_ = key.split()
		with app.app_context():
			review.set(id='m_fs0234', review=testcases[key]['input'])
			ok = review.get(id='m_fs0234')
			self.assertEqual(testcases[key]['want'], ok, msg="Success!")

	def test_get_pluss_multi(self):
		key = str(self)
		key,_ = key.split()
		want = testcases[key]['want']
		for i in testcases[key]['input']:
			with app.app_context():
				review.set(id='m_fs0214', review=i)
		
		with app.app_context():
			ok = review.get(id='m_fs0214')
			self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")

	def test_get_pluss_multi2(self):
		key = str(self)
		key,_ = key.split()
		index = 0
		for i in testcases[key]['input']:
			x = testcases[key]['want'][index]
			index += 1
			with app.app_context():
				review.set(id='m_fs02m2', review=i)
				ok = review.get(id='m_fs02m2')
				with self.subTest(i=i):
					self.assertEqual(x, ok, msg=f"For {key} wanted {x} got {ok}")
	
	def test_get_pluss_multi3(self):
		key = str(self)
		key,_ = key.split()
		want = testcases[key]['want']
		for i in testcases[key]['input']:
			with app.app_context():
				review.set(id='m_fs02m3', review=i)
		
		with app.app_context():
			ok = review.get(id='m_fs02m3')
			self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")

	def test_get_pluss_multi4(self):
		key = str(self)
		key,_ = key.split()
		index = 0
		for i in testcases[key]['input']:
			x = testcases[key]['want'][index]
			index += 1
			with app.app_context():
				review.set(id='m_fs02m4', review=i)
				ok = review.get(id='m_fs02m4')
				with self.subTest(i=i):
					self.assertEqual(x, ok, msg=f"For {key} wanted {x} got {ok}")

class TestAddRemove(unittest.TestCase):
	initialized = False
	
	def setUp(self):
		if not self.initialized:
			print(f"\nInitializing Testing...")
			build_app()
			self.__class__.initialized = True

	def test_add_remove_1(self):
		key,_ = str(self).split()
		with app.app_context():
			for add in testcases[key]['input']:
				review.add(add)
			test = testcases[key]['input'][2]
			want = testcases[key]['want'][0]
			ok = review.get(test)
			with self.subTest(test=1):
				self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")
			review.remove(test)
			ok = review.get(test)
			want = testcases[key]['want'][1]
			with self.subTest(test=2):
				self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")
			want = testcases[key]['want'][2]
			test = testcases[key]['input'][3]
			ok = review.get(test)
			with self.subTest(test=3):
				self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")
			want = testcases[key]['want'][3]
			review.remove(test)
			ok = review.get(test)
			with self.subTest(test=4):
				self.assertEqual(want, ok, msg=f"For {key} wanted {want} got {ok}")

if __name__ == '__main__':
	unittest.main()