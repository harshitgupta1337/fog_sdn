# fog_sdn

Experimentation for Software Defined Fog

# htb_implement
Implementation of hierarchical token buckets in POX. This code just shows how to setup a simple token bucket in a topology.
Two files are required for this. The file in `in_mininet` is used to setup the topology. The file in `in_pox` contains the controller.

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

