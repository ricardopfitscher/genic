#!/sbin/bash
#Run as sudo
#$1 is time for monitoring
#$2 is iteration
#$3 is subscribers

#apt-get install sysstat
#apt-get install perf-tools-unstable
sar -A 1 $1 >> output-sarAll-$3-$2.dat &
#cachestat >> output-cache.dat &
mpstat 1 $1 >> output-mpstat-$3-$2.dat &
iostat 1 $1 >> output-iostat-$3-$2.dat &
ifstat 1 $1 >> output-ifstat-$3-$2.dat &
sar -r 1 $1 >> output-sarMem-$3-$2.dat &  
typeset -i i
for ((i=1;i<=$1;++i))
do 
	tc -s -d qdisc show  | grep backlog >> output-tc-$3-$2.dat
	#ethtool -S eth0 | grep dropp >> output-ethDropp.dat
	ifconfig eth0 | grep dropp >> output-ethDropp-$3-$2.dat
	ping 143.54.12.69 -c 1 >> output-pingDNS-$3-$2.dat &
	ping 143.54.12.140 -c 1 >> output-pingHomer-$3-$2.dat &
	ping 143.54.12.74 -c 1 >> output-pingVellum-$3-$2.dat &
	ping 143.54.12.78 -c 1 >> output-pingDime-$3-$2.dat &
	ping 143.54.12.57 -c 1 >> output-pingSprout-$3-$2.dat &
	ping 143.54.12.99 -c 1 >> output-pingBono-$3-$2.dat &
	ping 143.54.12.221 -c 1 >> output-pingEllis-$3-$2.dat
	echo $i
	sleep 1
done

pkill -f cachestat



