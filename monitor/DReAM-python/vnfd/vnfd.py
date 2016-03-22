from state.state import State
import json

class Vnfd(object):
	"""docstring for Vnfd"""
	def __init__(self, name=None, vnfd_id=None):
		self.name = name
		self.id = vnfd_id
		self.provider = ""
		self.description = ""
		self.version = ""
		self.maxSizeList = 2
		self.stateList = []

	def insertState(self, value, diag):
		tempState = State(value,diag)
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

	def return_JSON(self):
		data=json.dumps(self.__dict__)
		return data




	



		