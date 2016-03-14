from diagnoser.diagnoser import *
from agentd.agentd import *
#from nsd.nsd import *
from state.state import *
from vnfd.vnfd import Vnfd
import threading
import time

m = MonitoringParameter()
m.from_JSON('cpu_usage')
diag = DiagnosticModel()
diag.from_JSON('CPU')
d = Diagnoser()
d.addMonitoringParameter(m)
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

