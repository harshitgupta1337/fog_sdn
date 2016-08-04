# This is the controller file, written in POX
# 

from pox.core			import core
from pox.lib.revent		import *
from pox.lib.util		import dpidToStr
from pox.lib.addresses	import IPAddr, EthAddr

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

HARD_TIMEOUT = 30
IDLE_TIMEOUT = 30

class LearningSwitch (EventMixin):

	def __init__ (self, connection):
		# Initiates a switch to which we'll be adding L2 learning capabilities
		self.macToPort = {}
		self.connection= connection
		self.listenTo(connection)

	def _handle_PacketIn (self, event):

		# parsing the input packet
		packet = event.parse()

		# updating out mac to port mapping
		self.macToPort[packet.src] = event.port

		if packet.type == packet.LLDP_TYPE or packet.type == 0x86DD:
			# Drop LLDP packets 
			# Drop IPv6 packets
			# Send of command without actions

			#log.debug("Port type is LLDP or IPv6 -- dropping")
			msg	= of.ofp_packet_out()
			msg.buffer_id = event.ofp.buffer_id
			msg.in_port = event.port
			self.connection.send(msg)

			return

		if packet.dst not in self.macToPort: 
			# does not know out port
			# flood the packet
			# this is an ARP request/reply packet which is arriving to the switch for the first time
			
			#log.debug("Port for %s unknown -- flooding" % (packet.dst))
			msg = of.ofp_packet_out()
			msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
			msg.buffer_id = event.ofp.buffer_id
			msg.in_port = event.port
			self.connection.send(msg)

		else:
			# The outport is known
			# Thus, we can create a open flow rule
			# installing Flow
			outport = self.macToPort[packet.dst]

			# creating openflow message
			msg = of.ofp_flow_mod()
			msg.match.dl_src = packet.src
			msg.match.dl_dst = packet.dst
			msg.idle_timeout = IDLE_TIMEOUT
			msg.hard_timeout = HARD_TIMEOUT
			msg.buffer_id = event.ofp.buffer_id

			if packet.type == packet.IP_TYPE:

				# extracting ipv4 payload from the ethernet part 
				ip_part = packet.find('ipv4')

				#log.debug("installing flow for %s.%i -> %s.%i" % (packet.src, event.port, packet.dst, outport))

				# if packet is coming from 10.0.0.3, give it queue 1 (mentioned in the topo file)
				if ip_part.srcip == '10.0.0.3' or ip_part.srcip == '10.0.0.4':
					log.debug("-------QUEUE 3--------");
					msg.actions.append(of.ofp_action_enqueue(port = outport, queue_id = 3))
					self.connection.send(msg)

					return

			if outport == event.port:
				#log.warning("Same port for packet from %s -> %s on %s.  Drop." % (packet.src, packet.dst, outport), dpidToStr(event.dpid))
				return
			
			# For any other traffic, full bandwidth can be used (queue 0)

			log.debug("installing flow for %s.%i -> %s.%i" % (packet.src, event.port, packet.dst, outport))
			log.debug("-------QUEUE 0--------");						
			msg.actions.append(of.ofp_action_enqueue(port = outport, queue_id = 0))
			self.connection.send(msg)


class learning_switch (EventMixin):

	def __init__(self):
		self.listenTo(core.openflow)

	def _handle_ConnectionUp (self, event):
		log.debug("Connection %s" % (event.connection,))
		LearningSwitch(event.connection)

def launch ():
	core.registerNew(learning_switch)
