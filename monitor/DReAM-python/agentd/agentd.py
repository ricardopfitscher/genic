import requests

class Agentd(object):
	"""docstring for ClassName"""
	def __init__(self, name, agent_id, manager=None):
		self.name = name
		self.agent_id = agent_id
		self.manager = manager
		self.localAddress = ""
		self.manager_port = 8765
		self.stateInterval = 1

	def sendMsgtoManager(self,message):
		string_temp = "http://%s:%s/vnfs/updateDiagnostic" % (self.manager,self.manager_port)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(string_temp,data=message,headers=headers)




		
