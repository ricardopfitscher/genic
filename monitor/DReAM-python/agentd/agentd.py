import time
import json

class Result(object):
	def __init__(self,element_param,element_id,element_state,element_time):
		self.element_param = element_param
		self.element_id = element_id
		self.element_state = element_state
		self.element_time = element_time



class Agentd(object):
	"""docstring for ClassName"""
	def __init__(self, name, agent_id, manager):
		self.name = name
		self.agent_id = agent_id
		self.manager = manager
		self.stateInterval = 1

	def sendMsgtoManager(self,message):
		print message

	def verifyStateChange(self,elementList):
		while True:
			for element in elementList:
				current = element.getLastNState(1)
				last = element.getLastNState(2)
				if current != "" and last != "":
					if current.getState() != last.getState():
						obj = Result('cpu_usage',element.vnfd_id,current.getState(),str(current.getTimestamp()))
						self.sendMsgtoManager(json.dumps(obj.__dict__))
			time.sleep(self.stateInterval)

		