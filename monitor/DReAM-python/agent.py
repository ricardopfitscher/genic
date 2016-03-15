from diagnoser.diagnoser import *
from agentd.agentd import *
#from nsd.nsd import *
from state.state import *
from vnfd.vnfd import Vnfd
import threading
import time

m = MonitoringParameter()
m.from_JSON('cpu_usage')

m2 = MonitoringParameter()
m2.from_JSON('steal_usage')

diag = DiagnosticModel()
diag.name='CPU_FULL'

file = open('diagnoser/DiagnosticModels/example.string','r')
diag_text = file.read()

#diag.from_JSON('CPU_FULL')

diag.from_string(diag_text)

d = Diagnoser()
d.addMonitoringParameter(m)
d.addMonitoringParameter(m2)

vnf1 = Vnfd('local',1)
agent = Agentd('home',1,'localhost')

monitoredElements = []
monitoredElements.append(vnf1)

monitor = threading.Thread(target=d.runAllMonitors)
monitor.start()

diagRunner = threading.Thread(target=d.runDiagnoser, args=(diag,vnf1))
diagRunner.start()

stateVerifyer = threading.Thread(target=agent.verifyStateChange, args=(monitoredElements,))
stateVerifyer.start()

monitor.join()
diagRunner.join()
stateVerifyer.join()

