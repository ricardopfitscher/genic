#!/sbin/bash
#Run as sudo
#$1 is time for monitoring

#apt-get install sysstat
#apt-get install perf-tools-unstable
sar -A 1 $1 >> output-sarAll.dat &
#cachestat >> output-cache.dat &
mpstat 1 $1 >> output-mpstat.dat &
iostat 1 $1 >> output-iostat.dat &
ifstat 1 $1 >> output-ifstat.dat &
sar -r 1 $1 >> output-sarMem.dat &  
typeset -i i
for ((i=1;i<=$1;++i))
do 
	tc -s -d qdisc show  | grep backlog >> output-tc.dat
	#ethtool -S eth0 | grep dropp >> output-ethDropp.dat
	ifconfig eth0 | grep dropp >> output-ethDropp.dat
	ping 143.54.12.69 -c 1 >> output-pingDNS.dat &
	ping 143.54.12.140 -c 1 >> output-pingHomer.dat &
	ping 143.54.12.74 -c 1 >> output-pingVellum.dat &
	ping 143.54.12.78 -c 1 >> output-pingDime.dat &
	ping 143.54.12.57 -c 1 >> output-pingSprout.dat &
	ping 143.54.12.99 -c 1 >> output-pingBono.dat &
	ping 143.54.12.221 -c 1 >> output-pingEllis.dat
	echo $i
	sleep 1
done

pkill -f cachestat



