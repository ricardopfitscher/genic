# GENIC - Guiltiness idENtification In NFV Chains 
Who is Guilty?

**Directories**

*monitor* includes the current monitor implementation 

*results* includes the experimental results

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


