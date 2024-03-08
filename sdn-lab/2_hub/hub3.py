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

        # In base al datapath identifichiamo lo switch
        if datapath.id == 1:
            # switch 1
            # definiamo la regola di match per il primo switch
            match = parser.OFPMatch(eth_dst='00:00:00:00:00:01')

            # In questo esempio statico, sappiamo che la porta 1 dello
            # switch e' sempre connessa all'host che abbiamo specificato
            actions = [parser.OFPActionOutput(1)]
        elif datapath.id == 2:
            # switch 2
            # definiamo la regola di match per il secondo switch
            match = parser.OFPMatch(eth_dst='00:00:00:00:00:02')
            # In questo esempio statico, sappiamo che la porta 1 dello
            # switch e' sempre connessa all'host che abbiamo specificato
            actions = [parser.OFPActionOutput(1)]
        elif datapath.id == 3:
            # switch 3
            # definiamo la regola di match per il terzo switch
            match = parser.OFPMatch(eth_dst='00:00:00:00:00:03')
            # In questo esempio statico, sappiamo che la porta 1 dello
            # switch e' sempre connessa all'host che abbiamo specificato
            actions = [parser.OFPActionOutput(1)]
        else:
            # switch sconosciuto
            self.logger.error(f"Switch {datapath.id} sconosciuto")
            return
            
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
            instructions=inst
        )

        datapath.send_msg(mod)
        

        ### Definizione della regola di default ###
        match_broadcast = parser.OFPMatch()

        # lista di azioni
        actions = [parser.OFPActionOutput(ofproto.OFPP_FLOOD)]

        # lista di istruzioni
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        # prepara un messaggio Modify-State
        # priorita' 0, in quanto e' la regola di default
        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=0,
            match=match_broadcast,
            instructions=inst
        )

        # invia allo switch
        datapath.send_msg(mod)
