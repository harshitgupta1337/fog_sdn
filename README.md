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

