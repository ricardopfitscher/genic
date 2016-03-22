#!/bin/sh

curl -H "Content-Type: application/json" -X POST --data-binary @diagnoser/MonitoringParameter/cpu_usage http://143.54.12.174:9999/api/parameters
curl -H "Content-Type: application/json" -X POST --data-binary @diagnoser/MonitoringParameter/steal_usage http://143.54.12.174:9999/api/parameters


curl -H "Content-Type: application/json" -X POST --data-binary @diagnoser/DiagnosticModels/CPU_FULL http://143.54.12.174:9999/api/diagnostics

curl -H "Content-Type: application/json" -X POST -d '{"name": "Agent","id":1, "manager":"localhost"}' http://143.54.12.174:9999/api/agentd

curl -H "Content-Type: application/json" -X POST -d '{"name": "VNF1","id":1}' http://143.54.12.174:9999/api/vnfs

curl http://143.54.12.174:9999/api/diagnoserInterface/start_monitors

curl http://143.54.12.174:9999/api/diagnoserInterface/start_diagnoser/VNF1/CPU_FULL

curl http://143.54.12.174:9999/api/diagnoserInterface/start_log




