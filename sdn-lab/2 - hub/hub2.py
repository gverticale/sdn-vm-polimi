# Implementazione openflow di un hub tramite controller
#
# In ogni switch viene caricata un'unica regola
# di default (table miss) con azione di invio al controller
# dell'intero pacchetto. Il controller risponde con una
# packet out con azione flood
#
# NOTA: OpenVSwitch ignora l'opzione OFPCML_NO_BUFFER
# nelle regole table miss (priorita' 0); pertanto,
# carichiamo una regola con priorita' 1 

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

class PolimiHub(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

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

    # Registriamo un handler dell'evento Packet In
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Per come abbiamo scritto le regole nello switch
        # i pacchetti non devono essere bufferizzati allo switch
        assert msg.buffer_id == ofproto.OFP_NO_BUFFER      
        
        # Recuperiamo dai metadati del pacchetto
        # la porta di ingresso allo switch
        in_port = msg.match['in_port']

        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_FLOOD
            )
        ]

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)
