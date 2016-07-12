from diagnoser.diagnoser import *
from agentd.agentd import *
#from nsd.nsd import *
from state.state import *
from vnfd.vnfd import Vnfd
import threading
import time
import cherrypy


frontpage = """<html>
	<head></head>
	<meta http-equiv="refresh" content="40">
		<body>
			<form method="get" action="addMonitoringParameter">
				<input type="text" value="" name="name"/>
				<button type="submit">Add a parameter</button>
			</form>
			<form method="get" action="addDiagnosticModel">
				<input type="text" value="diagnostic name" name="name"/>
				<input type="text" value="file name" name="file"/>
				<button type="submit">Add a diagnostic model</button>
			</form>
			<form method="get" action="setAgentInformation">
				<input type="text" value="Agent name" name="name"/>
				<input type="text" value="Agent id" name="aid"/>
				<input type="text" value="localhost" name="manager"/>
				<input type="text" value="" name="stateInterval"/>
				<button type="submit">Set agent information</button>
			</form>
			<form method="get" action="addDiagnosticModelFromString">
				<input type="text" value="diagnostic name" name="name"/>
				<textarea value="" name="text" rows="4" cols="20"> </textarea>
				<button type="submit">Add a diagnostic model from string</button>
			</form>
			<form method="get" action="runMonitors">
				<button type="submit">Run all monitoring parameters</button>
			</form>
			<form method="get" action="startDiagnoser">
				<button type="submit">Start the diagnoser</button>
			</form>
			<form method="get" action="stopDiagnoser">
				<button type="submit">Stop diagnoser</button>
			</form>
			<table style=\"width:100%\"> 
				<caption>Active Monitoring Parameters</caption>
			"""

class AgentInfo:
	exposed = True
	
	@cherrypy.tools.json_out()
	def GET(self):
			return localAgent.__dict__

	#curl -H "Content-Type: application/json" -X POST -d '{"name": "Agent","id":1, "manager":"localhost"}' http://143.54.12.174:9999/api/agent
	@cherrypy.tools.json_in()
	def POST(self):
		global localAgent
		data = cherrypy.request.json
		tmp = Agentd('tmp',1,'tmp')
		tmp.__dict__ = data
		for key in tmp.__dict__:
			localAgent.__dict__[key]=tmp.__dict__[key]


		print localAgent.name

		


class Diagnostics:
	exposed = True

	def GET(self, name=None):
		names = {obj.name:obj for obj in diagnoserDeamon.DiagnosticModels}
		if name is None:
			l=[]
			for diags in diagnoserDeamon.DiagnosticModels:
				l.append(diags.return_JSON())
			return('Available Diagnostic Models \n: %s' % str(l) )
		elif name in names:
			return(names[name].return_JSON())
		else:
			return('No diagnostic model with name %s' % name)

	#curl -H "Content-Type: application/json" -X POST -d '{"function": ["average", "average", "average", "average"], "name": "CPU_FULL", "interval": 1, "monParList": ["cpu_usage", "cpu_usage", "steal_usage", "cpu_usage"], "window": 5, "result": ["normal", "sub", "sub", "over"], "conditionals": [["<80", ">=30"], [">=80"], [">=5"], ["<30"], []]}' http://143.54.12.174:9999/api/diagnostics
	@cherrypy.tools.json_in()
	def POST(self):
		data = cherrypy.request.json
		diag = DiagnosticModel()
		diag.__dict__ = data
		diag.to_JSON()
		diagnoserDeamon.DiagnosticModels.append(diag)

	def DELETE(self,name):
		names = {obj.name:obj for obj in diagnoserDeamon.DiagnosticModels}
		if name in names:
			diagnoserDeamon.DiagnosticModels.remove(names[name])
			return('Diagnostic model named %s has been deleted.' % name)
		else:
			return('There is no Diagnostic model named %s' % name)
		

class Parameters:
	exposed = True
	@cherrypy.tools.json_out()
	def GET(self, name=None):
		
		names = {obj.name:obj for obj in diagnoserDeamon.MonitoringParameters}
		if name is None:
			l=[]
			for parameter in diagnoserDeamon.MonitoringParameters:
				l.append(parameter.return_JSON())
			return l
		elif name in names:
			return(names[name].__dict__)
		else:
			return('No monitoring parameter with name %s' % name)

	#curl -H "Content-Type: application/json" -X POST --data-binary @diagnoser/MonitoringParameter/cpu_usage http://143.54.12.174:9999/api/parameters
	#curl -H "Content-Type: application/json" -X POST --data-binary @diagnoser/MonitoringParameter/steal_usage http://143.54.12.174:9999/api/parameters
	@cherrypy.tools.json_in()
	def POST(self):
		#TOTHINK: authentication:
		#attention is needed here, a terminal command can turn off the VNF
		data = cherrypy.request.json

		m = MonitoringParameter()
		m.__dict__ = data
		m.to_JSON()
		diagnoserDeamon.MonitoringParameters.append(m)

	def DELETE(self,name):
		names = {obj.name:obj for obj in diagnoserDeamon.MonitoringParameters}
		if name in names:
			diagnoserDeamon.MonitoringParameters.remove(names[name])
			return('Monitoring Parameter named %s has been deleted.' % name)
		else:
			return('There is no Monitoring Parameter named %s' % name)
		

class DiagnoserInterface:
	exposed = True
	def GET(self,action,element=None,diagnostic=None):
		#http://143.54.12.174:9999/api/diagnoserInterface/start_monitors
		if action == "start_monitors":
			try:
				diagnoserDeamon.stop_flag=False
				monitor = threading.Thread(target=diagnoserDeamon.runAllMonitors)
				monitor.start()
				return 'Ok'
			except:
				return 'Error'
		#http://143.54.12.174:9999/api/diagnoserInterface/start_diagnoser/VNF1/CPU_FULL
		elif action == "start_diagnoser":
			if element is not None and diagnostic is not None and localAgent is not None:
				choose_element = filter(lambda x: x.name==element, monitoredElements).pop()
				choose_diagnostic = filter(lambda x: x.name==diagnostic, diagnoserDeamon.DiagnosticModels).pop()
				try:
					diagnoserDeamon.stop_flag=False

					diagRunner = threading.Thread(target=diagnoserDeamon.runDiagnoser, args=(choose_diagnostic,choose_element))
					diagRunner.start()	
					
					stateVerifyer = threading.Thread(target=diagnoserDeamon.verifyStateChange, args=(localAgent,monitoredElements,))
					stateVerifyer.start()		
					return 'Ok'
				except:
					return 'Error'
			else:
				return "Without parameters"
		elif action == "stop":
			diagnoserDeamon.stop_flag=True
			return 'Ok'
		elif action == "start_log":
			diagnoserDeamon.store_log=True
			return 'Ok'
		elif action == "stop_log":
			diagnoserDeamon.store_log=False

		elif action == "last_state":
			if element is not None:
				choose_element = filter(lambda x: x.name==element, monitoredElements).pop()
				current=choose_element.getLastNState(1)
				obj = Result(current.diagnosticName,choose_element.id,current.getState(),str(current.getTimestamp()))
				return(json.dumps(obj.__dict__))

class VNFs:
	exposed = True

	def GET(self, name=None):
		#TODO: cut off the states from this answer
		names = {obj.name:obj for obj in monitoredElements}
		if name is None:
			l=[]
			for element in monitoredElements:
				l.append(element.return_JSON())
			return('Monitored VNFs \n: %s' % str(l) )
		elif name in names:

			return(names[name].return_JSON())
		else:
			return('No VNF with name %s' % name)
	
	#curl -H "Content-Type: application/json" -X POST -d '{"name": "VNF1","id":1}' http://143.54.12.174:9999/api/vnfs
	@cherrypy.tools.json_in()
	def POST(self):
		data = cherrypy.request.json
		v = Vnfd()
		temp = Vnfd()
		temp.__dict__ = data
		for key in temp.__dict__:
			v.__dict__[key]=temp.__dict__[key]


		monitoredElements.append(v)

	def DELETE(self,name):
		names = {obj.name:obj for obj in monitoredElements}
		if name in names:
			monitoredElements.remove(names[name])
			return('VNF named %s has been deleted.' % name)
		else:
			return('There is no VNF named %s' % name)


class AgentInterface(object):
	@cherrypy.expose
	def index(self):
		temp = ''
		for parameter in diagnoserDeamon.MonitoringParameters:
			temp+="<tr><td>"+parameter.name+"</td>"+"<td>"+str(parameter.values)+"</td>"+"</tr>"
		temp += "</table>"
		return frontpage+temp+"</body></html>"

	@cherrypy.expose
	def addMonitoringParameter(self, name):
		try:
			m = MonitoringParameter()
			m.from_JSON(name)
			diagnoserDeamon.addMonitoringParameter(m)
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def addDiagnosticModel(self, name, file):
		try:
			diag.name = name
			diag.from_JSON(file)
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def setAgentInformation(self,name,aid,manager,stateInterval=None):
		try:
			localAgent = Agentd(name,aid,manager)
			if stateInterval is not None:
				self.agent.stateInterval = stateInterval
			return 'Ok'
		except:
			return 'Error'



	@cherrypy.expose
	def addDiagnosticModelFromString(self,name,text):
		try:
			diag.name = name
			diag.from_string(text)
			return 'Ok'
		except:
			return 'Error'


	@cherrypy.expose
	def runMonitors(self):
		try:
			diagnoserDeamon.stop_flag=False
			monitor = threading.Thread(target=diagnoserDeamon.runAllMonitors)
			monitor.start()
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def stopDiagnoser(self):
		try:
			diagnoserDeamon.stop_flag=True
			return 'Ok'
		except:
			return 'Error'

	@cherrypy.expose
	def startDiagnoser(self):
		try:
			diagRunner = threading.Thread(target=diagnoserDeamon.runDiagnoser, args=(diag,vnf))
			diagRunner.start()
			stateVerifyer = threading.Thread(target=diagnoserDeamon.verifyStateChange, args=(agent,monitoredElements,))
			stateVerifyer.start()
			return 'Ok'
		except:
			return 'Error'
		

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
 


if __name__ == '__main__':
	conf = {
		'/': {
		'tools.sessions.on': True
		}
	}

	diagnoserDeamon = Diagnoser()
	monitoredElements = []
	localAgent = Agentd('tmp',1,'tmp')

	cherrypy.tree.mount(


    	AgentInfo(), '/api/agentd',
		{'/':
			{'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
		}
	)

	cherrypy.tree.mount(


    	Diagnostics(), '/api/diagnostics',
		{'/':
			{'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
		}
	)

	cherrypy.tree.mount(


    	Parameters(), '/api/parameters',
		{'/':
			{'request.dispatch': cherrypy.dispatch.MethodDispatcher(),'tools.CORS.on': True}
		}
	)

	cherrypy.tree.mount(


    	DiagnoserInterface(), '/api/diagnoserInterface',
		{'/':
			{'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
		}
	)

	cherrypy.tree.mount(


    	VNFs(), '/api/vnfs',
		{'/':
			{'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
		}
	)


	cherrypy.tree.mount(AgentInterface(), '/', conf)
	cherrypy.tools.CORS = cherrypy.Tool('before_handler', CORS)
	cherrypy.config.update({'server.socket_host': '143.54.12.174','server.socket_port': 9999}) 
	cherrypy.engine.start()
	cherrypy.engine.block()

