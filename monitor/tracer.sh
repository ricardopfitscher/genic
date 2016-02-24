#!/bin/sh


while [ 1 ]
do
	echo net:* >> /sys/kernel/debug/tracing/set_event
	echo "name == eth0" > /sys/kernel/debug/tracing/events/net/filter 
	echo 1 > /sys/kernel/debug/tracing/tracing_on
	sleep 1
	queue=`cat /sys/kernel/debug/tracing/trace | grep net_dev_queue | sed 's/len=//' | awk '{Queue += $8; } END {  print Queue }'` 
	xmi=`cat /sys/kernel/debug/tracing/trace | grep net_dev_xmit | sed 's/len=//' | awk '{Queue += $8; } END {  print Queue }'`
	result=`expr $queue - $xmi`
	echo $result >> log/kernel-queue
	#sleep 1
	echo 0 > /sys/kernel/debug/tracing/tracing_on
	echo "" > /sys/kernel/debug/tracing/trace
done
