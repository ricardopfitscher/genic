import datetime
import psutil
import time
import threading
import subprocess
import sys
import cherrypy
import json
DEBUG = True

frontpage = """<html>
	<head></head>
		<body>


			"""

g = 0
m = 0

class Guiltiness():
	def __init__(self,c1,c2,c3,c4):
		self.c1=c1
		self.c2=c2
		self.c3=c3
		self.c4=c4
		self.U = 0
		self.A = 0
		self.Qu = 0
		self.Q = 0
		self.guiltiness = 0.0
		self.timestamp = datetime.datetime.now()
		 

	def computeGuiltiness(self):
		self.guiltiness = self.c1*(1/(1-self.U)) + self.c2*self.A + self.c3*(1/(1-self.Qu)) - self.c4*(self.A/(1+self.Q))
		self.timestamp = datetime.datetime.now()

	def show(self):
		with open('guiltiness.log.dat', 'a') as outfile:
								outfile.write('%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\n' % ( str(self.timestamp) , self.guiltiness , self.U, self.A, self.Q, self.Qu))


	def update_coeff(c1,c2,c3,c4):
		self.c1=c1
		self.c2=c2
		self.c3=c3
		self.c4=c4


class Monitor():
	def __init__(self, iface):
		global g
		self.stop_flag = True
		self.window = 30
		self.threshold = 20.0
		self.queueSize = 1500000
		self.cpuTimeSeries = []
		self.queueTimeSeries = []
		self.gList = {'timestamp':[],'guiltiness':[],'U':[],'A':[],'Q':[],'Qu':[]}
		self.interface = iface

	def computeActive(self):
		count=0
		for value in self.cpuTimeSeries:
			if value >= self.threshold:
				count += 1
		return (count/float(len(self.cpuTimeSeries)))

	def computeAverage(self, metric):
		if metric == 'cpu':
			return sum(self.cpuTimeSeries)/float(len(self.cpuTimeSeries))
		if metric == 'queue':
			return sum(self.queueTimeSeries)/float(len(self.queueTimeSeries))

	def computeQueueUsage(self):
		return self.computeAverage('queue')/self.queueSize

	def runMonitor(self):
		count = 0
		while not self.stop_flag:
			#g = Guiltiness(0.1,1,0.001,0.9)
			cpuTemp = psutil.cpu_percent()
			queueTemp = "tc -s -d qdisc show dev "+ self.interface +" | grep backlog | awk {' print $2 '} | sed \'s/b//\'"
			proc=subprocess.Popen(queueTemp, shell=True, stdout=subprocess.PIPE, )
			queueTemp=float(proc.communicate()[0])
			
			if len(self.cpuTimeSeries) < self.window:
				self.cpuTimeSeries.append(cpuTemp)
				self.queueTimeSeries.append(queueTemp)
			else:
				self.cpuTimeSeries.pop(0)
				self.queueTimeSeries.pop(0)
				self.cpuTimeSeries.append(cpuTemp)
				self.queueTimeSeries.append(queueTemp)

			g.U = self.computeAverage('cpu')/100.0
			g.A = self.computeActive()
			g.Q = self.computeAverage('queue')
			g.Qu = self.computeQueueUsage()
			g.computeGuiltiness()
			self.gList['guiltiness'].append(g.guiltiness)
			self.gList['U'].append(g.U)
			self.gList['A'].append(g.A)
			self.gList['Q'].append(g.Q)
			self.gList['Qu'].append(g.Qu)
			self.gList['timestamp'].append(str(g.timestamp))
			g.show()
			time.sleep(1)

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


class Data():
	global g
	global m
	exposed = True
	# Retornar o conjunto de metricas armazenadas (gList)
	@cherrypy.tools.json_out()
	def GET(self): 
		if m != 0:
			if DEBUG: print "webserver output:", m.gList
			returnData = m.gList
		else:
			returnData = 'Ok'
		return returnData

	#curl -H "Content-Type: application/json" -X POST -d '{"c1":0.01, "c2":0.9, "c3":0.001, "c4":0.8}' http://143.54.12.174:9999/api/data
	@cherrypy.tools.json_in()
	def POST(self):
		data = cherrypy.request.json
		inputData = '{"c1":0.01, "c2":0.9, "c3":0.001, "c4":0.8}'
		inputData = data
		if DEBUG: print "webserver inputed data:", inputData
		g.update_coeff(inputData['c1'],inputData['c2'],inputData['c3'],inputData['c4'])


class AgentInterface(object):


	@cherrypy.expose
	def index(self):
		return frontpage+"</body></html>"

	@cherrypy.expose
	def stop(self):
		try:
			global m
			m.stop_flag=True
			#add_data(list(name))
			return 'Ok'
		except:
			return 'Error'
	
	@cherrypy.expose
	def resume(self):
		try:
			global m
			m.stop_flag=False
			#add_data(list(name))
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def start(self):
		try:
			global m
			m.stop_flag=False
			with open('guiltiness.log.dat', 'w') as outfile:
				outfile.write('time\tguiltiness\tusage\tactive\tqueue\tqueueUsage\n')
			monitorThread = threading.Thread(target=m.runMonitor)
			monitorThread.start()
			#add_data(list(name))
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def init(self):
		try:
			global g
			global m
			g = Guiltiness(float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))
			m = Monitor(sys.argv[1])
			#add_data(list(name))
			return 'Ok'
		except:
			return 'Error'




if __name__ == '__main__':
	if len(sys.argv) < 7:
		print "call: python monitor.py interface-name c1 c2 c3 c4 time_to_run"
	else:
		try:
				conf = {
				'/': {'tools.sessions.on': True}
				}
				cherrypy.tree.mount(
		    		Data(), '/api/data',
					{'/':
						{'request.dispatch': cherrypy.dispatch.MethodDispatcher(),'tools.CORS.on': True}
					}
				)

				#time.sleep(int(sys.argv[6]))
				#m.stop_flag=True
				cherrypy.tree.mount(AgentInterface(), '/', conf)
				cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
				cherrypy.config.update({'server.socket_host': '143.54.12.174','server.socket_port': 9999}) 
				cherrypy.engine.start()
				cherrypy.engine.block()

		except:
				print '\nerror in starting monitor'
	
