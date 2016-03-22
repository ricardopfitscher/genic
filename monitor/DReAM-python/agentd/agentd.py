class Agentd(object):
	"""docstring for ClassName"""
	def __init__(self, name, agent_id, manager):
		self.name = name
		self.agent_id = agent_id
		self.manager = manager
		self.stateInterval = 1

	def sendMsgtoManager(self,message):
		print message



		
