# Implementazione openflow di un hub
#
# In ogni switch viene caricata un'unica regola
# di default (table miss) con azione flooding

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3

# Classe principale, derivata da RyuApp
class PolimiHub(app_manager.RyuApp):
    # usiamo openflow 1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Registriamo un handler dell'evento Switch Features
    # Il messaggio Switch Features e' inviato dallo switch
    # quando si registra al controllore
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # Definizione della regola di default
        # priorita' 0
        # match di tutti i pacchetti
        # azione FLOOD
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]
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
