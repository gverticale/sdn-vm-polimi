# Implementazione openflow di un hub
#
# In ogni switch viene caricata un'unica regola
# con azione flooding

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls, CONFIG_DISPATCHER
from ryu.ofproto import ofproto_v1_3

# Classe principale, derivata da RyuApp
class PolimiHub(app_manager.RyuApp):

    # usiamo openflow 1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    # Registriamo un handler dell'evento Switch Features
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        # un datapath e' uno specifico switch openflow
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        ### Definizione della regola ###

        # match di tutti i pacchetti
        match = parser.OFPMatch()

        # lista di azioni
        # 1. azione FLOOD
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

        # lista di istruzioni
        # 1. esegui la lista di azioni immediatamente
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        # prepara un messaggio Modify-State
        # priorita' 1
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=1,
            match=match,
            instructions=inst
        )

        # invia allo switch
        datapath.send_msg(mod)
