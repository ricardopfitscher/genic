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


**Reporting**

24/02/2016 - In forwarding chains, the kernel queues are not filled, in this case we measure the queues through backlog from tc qdisc.

**Evaluation Scenarios**

*Stratos*: The NFV chain is composed by two VNFs, a Firewall and a DPI. Both the VNFs have two adjustable resources, network and CPU. We run all the combinations for the following capacities.

| **Network (Mbps)** | **CPU (cap)** |
| :------------: | :-------: |
| 1		 | -         |
| 10		 | 10        |
| 100		 | 100       |

We apply the same workload generator that the authors from STRATOS used. Two clients request a 32KB file with an initial 10000 requests by second, the rate increases by 10000 every 60 seconds up to 50000. 

*Gnuradio*: 


*Mixed*: This scenario is similar to Stratos, with the same VNFs. In this case, the workload is composed by three different clients, the RUBiS that simulates a HTTP e-commerce client, the ffmpeg that represents a 30 Mbps video stream demand, and finally, the Iperf that runs a5 Mbps UDP traffic.  


