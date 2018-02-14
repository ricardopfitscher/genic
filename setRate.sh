#!/bin/bash

# $1 is the amount of rate

tc qdisc del dev eth0 root
tc qdisc add dev eth0 handle 1: root htb default 11
tc class add dev eth0 parent 1: classid 1:1 htb rate $1
tc class add dev eth0 parent 1:1 classid 1:11 htb rate $1
