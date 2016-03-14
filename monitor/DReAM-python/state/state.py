import datetime

class State(object):
	"""docstring for State"""
	def __init__(self,value):
		self.value = value
		self.timestamp = datetime.datetime.now()

	def setState(self, value):
		self.value = value
		self.timestamp = datetime.datetime.now()

	def getState(self):
		return self.value

	def getTimestamp(self):
		return self.timestamp