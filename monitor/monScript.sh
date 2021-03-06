#!/sbin/bash
#Run as sudo

#$1 is the vnf netwok rate
#$2 is the vnt type
#$3 is the iteration
#$4 is time for monitoring
#$5 is the call rate

#apt-get install sysstat
#apt-get install perf-tools-unstable
#sar -A 1 $4 >> output-sarAll-$1-$2-$3-$5.dat &
#./cachestat >> output-cache-$1-$2-$3-$5.dat &
mpstat 1 $4 >> output-mpstat-$1-$2-$3-$5.dat &
iostat 1 $4 >> output-iostat-$1-$2-$3-$5.dat &
ifstat 1 $4 >> output-ifstat-$1-$2-$3-$5.dat &
sar -r 1 $4 >> output-sarMem-$1-$2-$3-$5.dat &

typeset -i i
for ((i=1;i<=$4;++i))
do
	tc -s -d qdisc show dev eth0 |grep backlog >> output-tc-$1-$2-$3-$5.dat
	ethtool -S eth0 | grep dropp >> output-ethDropp-$1-$2-$3-$5.dat
	ifconfig eth0 | grep dropp >> output-ethDropp2-$1-$2-$3-$5.dat
	#For cpu monitoring in docker containers, please uncomment the following idented lines:
		prevTotA=($(cat /sys/fs/cgroup/cpuacct/cpuacct.usage))
		memUsage=($(cat /sys/fs/cgroup/memory/memory.usage_in_bytes))
		percentM=($(awk "BEGIN {print 100*($memUsage)/(64*(2^30))}"))
		cat /sys/fs/cgroup/blkio/blkio.io_serviced | grep Total | cut -d ' ' -f 2  >> output-dockerIOserviced-$1-$2-$3-$5.dat
		cat /sys/fs/cgroup/blkio/blkio.io_queued | grep Total | cut -d ' ' -f 2 >> output-dockerIOqueued-$1-$2-$3-$5.dat
		echo $percentM >> output-dockerMem-$1-$2-$3-$5.dat
		sleep 1
		TotA=($(cat /sys/fs/cgroup/cpuacct/cpuacct.usage))
		percentCPU=($(awk "BEGIN {print ($TotA-$prevTotA)/10000000}"))
		echo $percentCPU >> output-dockerCPU-$1-$2-$3-$5.dat
	#echo $i
	#sleep 1
done
pkill -f cachestat
