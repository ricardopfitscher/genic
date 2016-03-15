import json
import threading
import time
import subprocess
import commands

class MonitoringParameter(object):
	"""docstring for Monitoring Parameter"""
	#TOTHINK: Each monitoring parameter has a state?
	def __init__(self):
		self.name = ""
		self.description = ""
		self.type = ""
		self.terminalCommand = "" 
		self.values = []
		#TOTHINK: self.stateList = []
		return

	def insertValue(self,value,window):
		if(len(self.values)<=window):
			self.values.append(value)
		else:
			self.values.pop(0)
			self.values.append(value)
		return

	def to_JSON(self):
		data=json.dumps(self.__dict__)
		with open('diagnoser/MonitoringParameter/'+self.name, 'w') as outfile:
			json.dump(self.__dict__, outfile)
	
	def from_JSON(self,name):
		with open('diagnoser/MonitoringParameter/'+name, 'r') as infile:
			self.__dict__ = json.load(infile)



# In the DiagnosticModel class we store the Diagnostic Information
# it includes the monitoring parameteres and the rules for each one
# also, it parses the human writed rules

class DiagnosticModel(object):
	def __init__(self):
		self.name = ""
		self.rule = "" # the human writed string
		self.interval = 0 # the time interval between measurements
		self.window = 0 # the window size for this diagnosis model
		self.function = [] # the calculated functions  
		self.monParList = [] # the monitoring parameter list
		self.conditionals = [[]] # list of conditionals used to determine the state
		self.result = [] # list of the related line results
		

	def from_JSON(self,name): # read the diagnosis model from a JSON
		with open('diagnoser/DiagnosticModels/'+name, 'r') as infile:
			self.__dict__ = json.load(infile)

	def to_JSON(self):
		data=json.dumps(self.__dict__)
		with open('diagnoser/DiagnosticModels/'+self.name, 'w') as outfile:
			json.dump(self.__dict__, outfile)

	def from_string(self,rule):
		self.rule = rule
		text = rule.split()
		word = 0
		cond = 0
		while text[word] != 'END':
			if text[word] == "FOREACH":
				word+=1
				self.interval = int(text[word])
			elif text[word] == "FROM":
				word+=1
				self.window= int(text[word])
			elif text[word] == "IF":
				self.conditionals.append([])# TOTHINK: WHEN ADD?
				word+=1
				self.function.append(text[word])
				word+=2
				self.monParList.append(text[word])
				word+=1
				while text[word] != "THEN":
					if text[word] == "IS" or text[word] == "AND":
						word+=1
						self.conditionals[cond].append(text[word])
					word+=1
				word+=1
				self.result.append(text[word])
				cond += 1
			word+=1
		self.to_JSON()


class Diagnoser(threading.Thread):
	"""docstring for Diagnoser"""
	def __init__(self):
		#self.arg = arg
		self.stop_flag = False
		self.maxWindow = 20
		self.defaultInterval = 1
		self.MonitoringParameters = []

	def stop(self):
		self.stop_flag = True

	def addMonitoringParameter(self,m):
		self.MonitoringParameters.append(m)

	def wheightedAverage(self,values,window):
		average=0
		counter=1
		cropedValues = values[-window:]
		n=len(cropedValues)
		somatory=n*(n+1)/2.0
		for val in cropedValues:
			average+=val*counter
			counter+=1
		return(average/somatory)

	def average(self,values,window):
		average=0
		counter=1
		cropedValues = values[-window:]
		for val in cropedValues:
			average+=val
			counter+=1
		return(average/counter)
	
	#runDiagnoser(diagnostic,ns=n)
	def runDiagnoser(self,diagnostic,vnf=None,ns=None):
		while not self.stop_flag:
		 	size = len(diagnostic.monParList)
			for i in range(0,size):
				parameter = diagnostic.monParList[i]
				try:
					choose = filter(lambda x: x.name==parameter, self.MonitoringParameters).pop()
					func = getattr(self,diagnostic.function[i])
					output = func(choose.values,diagnostic.window)
					tempCondition = True
					for cond in diagnostic.conditionals[i]:
						if not eval(str(output)+cond):
							tempCondition = False
					if tempCondition is True:
						if vnf is not None:
							vnf.insertState(diagnostic.result[i])
						if ns is not None:
							ns.insertState(diagnostic.result[i])
				except:
					print "empty values for ", parameter 
			time.sleep(diagnostic.interval)

	def runMonitor(self,diagnostic):
		while not self.stop_flag:
			for parameter in list(set(diagnostic.monParList)):
				choose = filter(lambda x: x.name==parameter, self.MonitoringParameters).pop()
				output = commands.getoutput(choose.terminalCommand).replace(",",".")
				choose.insertValue(float(output),diagnostic.window)
			time.sleep(diagnostic.interval)

	def runAllMonitors(self):
		while not self.stop_flag:
			for parameter in self.MonitoringParameters:
				output = commands.getoutput(parameter.terminalCommand).replace(",",".")
				parameter.insertValue(float(output),self.maxWindow)
			time.sleep(self.defaultInterval)






	







		











