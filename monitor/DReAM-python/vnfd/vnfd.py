from state.state import State

class Vnfd(object):
	"""docstring for Vnfd"""
	def __init__(self, name, vnfd_id):
		self.name = name
		self.vnfd_id = vnfd_id
		self.provider = ""
		self.description = ""
		self.version = ""
		self.maxSizeList = 2
		self.stateList = []

	def insertState(self, value):
		tempState = State(value)
		if(len(self.stateList)<=self.maxSizeList):
			self.stateList.append(tempState)
		else:
			self.stateList.pop(0)
			self.stateList.append(tempState)
		return

	def getLastNState(self, n):
		if len(self.stateList) >= n:
			return self.stateList[-n]
		else: 
			return ""




	



		