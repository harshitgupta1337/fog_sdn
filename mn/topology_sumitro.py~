# . : ABOUT : .
# 
# This file creates a basic butterfly topology
# 
# h1             h3
#     s1 --- s2  h4 
# h2             h5
#
# h2 and h2 are connected to s1
# h3, h4 and h5 are connected to s2
# 
# There is a heirarchical token bucket (htb) inbetween s1 and h2
# which has three queues
# > 6
# > 4
# > Full
#  
# If you want to modify the queue values,
# modify the 'values' variable present in the main() function

from mininet.topo import Topo
from mininet.net  import Mininet
from mininet.cli  import CLI
from mininet.link import TCLink
from mininet.node import RemoteController
from functools 	  import partial

import subprocess as sp

class MyTopo(Topo):
	def build(self, _max_bw):
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		h5 = self.addHost('h5')

		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')

		self.addLink(h1,s1)
		self.addLink(h2,s1)
		self.addLink(h3,s2)
		self.addLink(h4,s2)
		self.addLink(h5,s2)

		self.addLink(s1,s2)

def main():

	# All b/w are in megabits
	max_bw = 1000

	# B/w of queue 1 and queue 2
	values = [600,400]

	topo = MyTopo(max_bw)

	net = Mininet(topo, link = TCLink, controller = partial(RemoteController, ip = '127.0.0.1', port = 6633))
	
	net.start()

	# Queue set in between h1 and s1
	cmd = 'ovs-vsctl -- set Port s2-eth4 qos=@newqos -- \
		--id=@newqos create QoS type=linux-htb other-config:max-rate=1000000000 queues=0=@q0,1=@q1,2=@q2 -- \
		--id=@q0 create Queue other-config:min-rate=%d other-config:max-rate=%d -- \
		--id=@q1 create Queue other-config:min-rate=%d other-config:max-rate=%d -- \
		--id=@q2 create Queue other-config:min-rate=%d other-config:max-rate=%d' % \
		(max_bw * 10**6, max_bw * 10**6, \
		values[0] * 10**6, values[0] * 10**6, \
		values[1] * 10**6, values[1] * 10**6)

	sp.call(cmd, shell = True)
	
	CLI(net)
	net.stop()

if __name__ == '__main__':
	main()
