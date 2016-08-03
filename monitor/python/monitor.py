import datetime
import psutil
import time
import threading
import subprocess
import sys

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
	def __init__(self, iface, g):
		self.stop_flag = True
		self.window = 30
		self.threshold = 20.0
		self.queueSize = 1500000
		self.cpuTimeSeries = []
		self.queueTimeSeries = []
		self.gList =[]
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
			#self.gList.append(g)
			g.show()
			time.sleep(1)


if __name__ == '__main__':
	if len(sys.argv) < 7:
		print "call: python monitor.py interface-name c1 c2 c3 c4 time_to_run"
	else:
		g = Guiltiness(float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]))
		m = Monitor(sys.argv[1],g)
	try:
			m.stop_flag=False
			with open('guiltiness.log.dat', 'w') as outfile:
								outfile.write('time\tguiltiness\tusage\tactive\tqueue\tqueueUsage\n')
			monitorThread = threading.Thread(target=m.runMonitor)
			monitorThread.start()
			time.sleep(int(sys.argv[6]))
			m.stop_flag=True

	except:
			print 'error in starting monitor'
	
