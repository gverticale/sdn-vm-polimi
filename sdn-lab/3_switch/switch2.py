from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types

# This implements a learning switch in the controller
# The switch sends all packets to the controller
# The controller implements the MAC table using a python dictionary
# If the MAC dst is known, add rule to the switch
class PsrSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(PsrSwitch, self).__init__(*args, **kwargs)
        self.mac_to_port = {}

    # execute at switch registration
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        self.mac_to_port[datapath.id] = {}

        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
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
            priority=1,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        assert eth is not None

        dst = eth.dst
        src = eth.src

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return

        self.mac_to_port[dpid][src] = in_port

        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
        else:
            out_port = ofproto.OFPP_FLOOD

#        self.logger.info("packet in %s %s %s %s %s", dpid, src, dst, in_port, out_port)

        actions = [
            parser.OFPActionOutput(out_port)
        ]

        assert msg.buffer_id == ofproto.OFP_NO_BUFFER

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)

        # if the output port is not FLOODING
        # install a new flow rule *for the next packets*
        if out_port != ofproto.OFPP_FLOOD:
        	# install a new flow rule
            match = parser.OFPMatch(
                eth_src=src,
                eth_dst=dst
            )
            inst = [
                parser.OFPInstructionActions(
                    ofproto.OFPIT_APPLY_ACTIONS,
                    actions
                )
            ]
            ofmsg = parser.OFPFlowMod(
                datapath=datapath,
                priority=10,
                match=match,
                instructions=inst,
            )
            datapath.send_msg(ofmsg)
