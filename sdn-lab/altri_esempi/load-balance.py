# Implementazione openflow di un load balancer
#
# Si richiede l'uso della topologia
# load-balance-topology.py
#
# h1 -- s1 -- s3 -- s2 -- h2
#         \      /
#          \ s4 /
#
# FIXME: implementare host multipli

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.topology.api import get_all_host
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet, ether_types
from ryu.lib.packet import arp


class PolimiSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def add_flow_if_to_if(self,datapath,port_in,port_out):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(in_port=port_in)
        actions = [ parser.OFPActionOutput(port_out) ]
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=1,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    def add_flow_if_to_group(self,datapath,port_in,port_out_list):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        group_id = 1

        buckets = []
        for port_out in port_out_list:
            actions = [ parser.OFPActionOutput(port_out) ]
            buckets.append(
                parser.OFPBucket(
                    weight=1,
                    actions=actions
                )
            )
        req = parser.OFPGroupMod(
            datapath,
            ofproto.OFPGC_ADD,
            ofproto.OFPGT_SELECT,
            group_id,
            buckets)
        datapath.send_msg(req)

        match = parser.OFPMatch(in_port=port_in)
        actions = [ parser.OFPActionGroup(1) ]
        # actions = [ parser.OFPActionOutput(port_out_list[1]) ]
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=1,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath

        if datapath.id == 1 or datapath.id == 2:
            self.add_flow_if_to_group(datapath,1,[2, 3])
            self.add_flow_if_to_if(datapath,2,1)
            self.add_flow_if_to_if(datapath,3,1)
            return

        if datapath.id == 3 or datapath.id == 4:
            self.add_flow_if_to_if(datapath,1,2)
            self.add_flow_if_to_if(datapath,2,1)
            return
