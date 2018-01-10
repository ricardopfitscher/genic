#!/sbin/bash
#Run as sudo
#$1 is the vnf netwok rate
#$2 is the vnt type
#$3 is the iteration
#$4 is time for monitoring

#apt-get install sysstat
#apt-get install perf-tools-unstable
sar -A 1 $4 >> output-sarAll-$1-$2-$3.dat &
./cachestat >> output-cache-$1-$2-$3.dat &
mpstat 1 $4 >> output-mpstat-$1-$2-$3.dat &
iostat 1 $4 >> output-iostat-$1-$2-$3.dat &
ifstat 1 $4 >> output-ifstat-$1-$2-$3.dat &
sar -r 1 $4 >> output-sarMem-$1-$2-$3.dat &

typeset -i i
for ((i=1;i<=$4;++i))
do 
	tc -s -d qdisc show dev eth0 |grep backlog >> output-tc-$1-$2-$3.dat
	ethtool -S eth0 | grep dropp >> output-ethDropp-$1-$2-$3.dat
	ifconfig eth0 | grep dropp >> output-ethDropp2-$1-$2-$3.dat
	ping 143.54.12.55 -c 1 >> output-pingFW-$1-$2-$3.dat &
	ping 143.54.12.72 -c 1 >> output-pingDPI-$1-$2-$3.dat &
	ping 143.54.12.186 -c 1 >> output-pingIDS-$1-$2-$3.dat &
	echo $i
	sleep 1
done
pkill -f cachestat
