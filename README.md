# fog_sdn

Experimentation for Software Defined Fog

## Prerequisites
* Mininet
* Pox

## How to execute the controller
* From inside the `mn` directory, run the following command
```
sudo python topology_sumitro.py
```
* From inside the `pox` directory, run the following command
```
sudo ./pox.py log.level --DEBUG forwarding.controller_sumitro
```

* For measuring bandwidth between hosts, use the `iperf` command
For measuring bandwidth of the path `h1 --> h2`
* Execute following command on `h2`
```
iperf -s -p 6000 -i 1
```
This command creates an Iperf server on `h2`.
* Execute following command on `h1`
```
iperf -c <h2-ip-addr> -p 7000 -t 30
```
This command starts an Iperf server on `h1`.
