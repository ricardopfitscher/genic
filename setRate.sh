#!/bin/bash

# $1 is the amount of rate

rate=$(echo "$1" | tr -dc '0-9')
burst=($(awk "BEGIN {print ($rate/10)*5000}"))
tc qdisc del dev eth0 root
tc qdisc add dev eth0 root tbf rate $1 latency 1ms burst $burst

#tc qdisc add dev eth0 handle 1: root htb default 11
#tc class add dev eth0 parent 1: classid 1:1 htb rate $1
#tc class add dev eth0 parent 1:1 classid 1:11 htb rate $1
