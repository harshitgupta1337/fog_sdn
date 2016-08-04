#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from functools import partial

def myNetwork():
    
    switch = partial( OVSKernelSwitch, protocols='OpenFlow10' )
    net = Mininet( topo=None,
                   build=False,
                   switch=switch)

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    
    S1 = net.addSwitch('S1',dpid='01')
    S2 = net.addSwitch('S2',dpid ='02')

    info( '*** Add hosts\n')

    h1 = net.addHost('h1', cls=Host);
    h2 = net.addHost('h2', cls=Host);

    info( '*** Add links\n')
    net.addLink(S1, h1)
    net.addLink(S1, S2)
    net.addLink(S2, h2)
    
    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('S2').start([c0])
    net.get('S1').start([c0])

    info( '*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

