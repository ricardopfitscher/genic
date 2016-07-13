from state.state import State
from vnfd.vnfd import Vnfd
import datetime
import requests
import json

class Nsd(object):
	"""docstring for Nsd"""
	def __init__(self, name=None, nsd_id=None):
		self.name = name
		self.id = nsd_id
		self.description = ""
		self.version = ""
		self.neighborhood = []
		self.maxSizeList = 2
		self.stateList = []


	def setNeighborhood(self, vnf_fg):
		for vnf in vnf_fg.split():
			self.neighborhood.append(vnf)
			#string_temp = "http://%s:9999/api/agentd/" % (vnf)
			#r = requests.get(string_temp)
			#print r.json

	def getMonitoringTarget(self,localAdress):
		timestamp = datetime.datetime.now()
		size = self.neighborhood.size()
		mypos = self.neighborhood.index(localAdress)
		gid = mypos+timestamp%size + 1
		if(gid > size):
			gid -= size
		if gid == mypos:
			gid += 1
		return self.neighborhood[gid]

