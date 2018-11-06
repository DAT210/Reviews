'''Custom exceptions for the Reviews API'''

from flask import jsonify


class APIError(Exception):
	"""Exception class for API error handling."""
	status_code = 404

	def __init__(self, message, status_code=None, type=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.type = type

	def msg(self):
		"""Returns the message of the error."""
		return self.message

	def code(self):
		"""Returns the status code of the error."""
		return self.status_code

	def t(self):
		"""Returns the type of error."""
		return self.type

	def json(self):
		"""Returns a dictionary in the format: \n
		{ 'error': {
			'code': status_code,
			'message': message,
			'type': type
			}
		}
		"""
		return jsonify({
			'status': 'error',
			'data': {
				'error': {
					'code': self.status_code,
					'message': self.message,
					'type': self.type
				}
			}
		})


class APIFail(Exception):
	"""Exception class for API error handling."""
	status_code = 404

	def __init__(self, message, status_code=None, type=None):
		Exception.__init__(self)
		self.message = message
		if status_code is not None:
			self.status_code = status_code
		self.type = type

	def msg(self):
		"""Returns the message of the error."""
		return self.message

	def code(self):
		"""Returns the status code of the error."""
		return self.status_code

	def t(self):
		"""Returns the type of error."""
		return self.type

	def json(self):
		"""Returns a dictionary in the format: \n
		{ 'error': {
			'code': status_code,
			'message': message,
			'type': type
			}
		}
		"""
		return jsonify({
			'status': 'error',
			'data': {
				'error': {
					'code': self.status_code,
					'message': self.message,
					'type': self.type
				}
			}
		})
