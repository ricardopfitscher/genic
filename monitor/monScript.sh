#!/sbin/bash
#Run as sudo
#$1 is time for monitoring

#apt-get install sysstat
#apt-get install perf-tools-unstable
sar -A 1 $1 >> output-sarAll.dat &
cachestat >> output-cache.dat &
mpstat 1 $1 >> output-mpstat.dat &
iostat 1 $1 >> output-iostat.dat &
ifstat 1 $1 >> output-ifstat.dat &
sar -r 1 $1 >> output-sarMem.dat &
typeset -i i
for ((i=1;i<=$1;++i))
do 
	tc -s -d qdisc show  | grep backlog >> output-tc.dat
	ethtool -S eth0 | grep dropp >> output-ethDropp.dat
	echo $i
	sleep 1
done

pkill -f cachestat



