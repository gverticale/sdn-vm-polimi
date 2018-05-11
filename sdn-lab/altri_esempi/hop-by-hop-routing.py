# Implementazione openflow di hop-by-hop routing
# usando la mappa della rete trovata con topology discovery
#
# Si richiede l'uso del topology discovery
# ryu-manager --observe-links
#
# Nella versione attuale richiede risoluzione arp gia' fatta
# invocare mininet con
# mn --arp

# FIXME: bug con topologia ad albero

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.topology import event, switches
from ryu.topology.api import get_all_switch, get_all_link, get_host
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ether_types
from ryu.lib.packet import ipv4
import networkx as nx


class PolimiSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # table miss, mando il pacchetto al controllore
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                128
            )
        ]
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=0,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    # trova switch destinazione e porta dello switch
    def find_destination_switch(self,ip_address):
        switch_list = get_all_switch(self)
        for switch in switch_list:
            host_list = get_host(self, switch.dp.id)
            for host in host_list:
                if ip_address in host.ipv4:
                    return (switch, host.port.port_no)
        return ( None, None )

    def find_next_hop_to_destination(self,source_id,destination_id):
        link_list = get_all_link(self)
        net = nx.DiGraph()
        for link in link_list:
            net.add_edge(link.src.dpid, link.dst.dpid, port=link.src.port_no)

        path = nx.shortest_path(
            net,
            source_id,
            destination_id
        )

        first_link = net[ path[0] ][ path[1] ]

        return first_link['port']

    def add_flow_to_switch(self,datapath,ip_address,port_no,buffer_id):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(
            eth_type=ether_types.ETH_TYPE_IP,
            ipv4_dst=ip_address
            )
        actions = [ parser.OFPActionOutput(port_no) ]
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=2,
            match=match,
            instructions=inst,
            buffer_id=buffer_id
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):

        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)
        pkt_ip = pkt.get_protocol(ipv4.ipv4)

        # ignora pacchetti non IPv4 (es. ARP, LLDP)
        if pkt_ip is None:
            return

        # trova switch destinazione
        ( switch, port_no ) = self.find_destination_switch(pkt_ip.dst);

        # host non trovato
        if switch is None:
            # print "DP: ", datapath.id, "Host not found: ", pkt_ip.dst
            return

        # da usare se l'host e' direttamente collegato
        output_port = port_no

        # host non direttamente collegato
        if switch.dp.id != datapath.id:
            output_port = self.find_next_hop_to_destination(datapath.id,switch.dp.id);

        # print "DP: ", datapath.id, "Host: ", pkt_ip.dst, "Port: ", output_port

        # aggiungi la regola
        self.add_flow_to_switch(
            datapath,
            pkt_ip.dst,
            output_port,
            msg.buffer_id
            )

        return
