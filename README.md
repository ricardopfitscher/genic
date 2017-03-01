# GENIC - Guiltiness idENtification In NFV Chains 
Who is Guilty?

**Directories**

*monitor* includes the current guiltiness monitor implementation

*monitor/python* contains a monitor writed in python 

*monitor/DReAM-python* an implementation of DReAM's monitoring agent with REST web service

*results* will include the experimental results

**DReAM Python API**

* ip:9999 - Visual interface
* || /api/agentd - GET or POST agent information
	* JSON Example: {"name": "Agent","id":1, "manager":"localhost", "manager_port":8765, "stateInterval":1}
* || /api/diagnostics/[name] - GET, DELETE or POST Diagnostic models
	* GET - allows requesting the diagnostics by name or, if the name is empty, show all
	* DELETE - delete the 'name' diagnostic model
	* POST - update or set a diagnostic model
	* JSON Example: {"function": ["average", "average", "average", "average"], "name": "CPU_FULL", "interval": 1, "monParList": ["cpu_usage", "cpu_usage", "steal_usage", "cpu_usage"], "window": 5, "result": ["normal", "sub", "sub", "over"], "lastResult": "over", "conditionals": [["<80", ">=30"], [">=80"], [">=5"], ["<30"]]}

* || /api/parameters/[name] - GET, DELETE or POST monitoring parameters
	* GET - allows requesting the monitoring parameters by name or, if the name is empty, show all
	* DELETE - delete the 'name' monitoring parameter
	* POST - update or set a diagnostic model
	* JSON Example: {"description": "", "window": 50, "terminalCommand": "mpstat 1 1 | tail -n 1 |  awk {' print 100-$12 '}", "values": [7.0, 5.0, 12.0, 1.0, 4.0, 3.0, 1.0, 3.0, 2.0, 3.0, 3.0, 8.0, 6.0, 5.0, 2.0, 3.0, 2.0, 7.0, 9.0, 3.0, 9.0], "type": "", "name": "cpu_usage"}
	* OBS.: you should not fill the 'values' field in POST operation

* || /api/vnfs/[name] - GET, DELETE or POST vnfs information
	* GET - allows requesting the vnfs information by name or, if the name is empty, show all
	* DELETE - delete the 'name' vnf
	* POST - update or set the vnf information

* || /api/diagnoserInterface/start_monitors - start the monitoring deamon for all monitoring parameters
* || /api/diagnoserInterface/start_diagnoser/element/diagnostic - start the diagnostic model 'diagnostic' for the monitored element 'element'
	* Example: http://143.54.12.174:9999/api/diagnoserInterface/start_diagnoser/VNF1/CPU_FULL

* || /api/diagnoserInterface/stop - stop the monitors and diagnosers

* || /api/diagnoserInterface/start_log - log the monitoring parameters and diagnostic values inside the monitoring agent

* || /api/diagnoserInterface/stop_log - stop loging


