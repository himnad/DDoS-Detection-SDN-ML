from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
from datetime import datetime
from ryu.app import simple_switch_13 as switch


class CollectTrainingStatsApp(switch.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(CollectTrainingStatsApp, self).__init__(*args, **kwargs)
        self.datapaths = {}
        self.monitor_thread = hub.spawn(self.monitor)

        file0 = open("FlowStatsfile.csv", "w")
        file0.write(
            "timestamp,datapath_id,flow_id,ip_src,tp_src,ip_dst,tp_dst,"
            "ip_proto,icmp_code,icmp_type,flow_duration_sec,flow_duration_nsec,"
            "idle_timeout,hard_timeout,flags,packet_count,byte_count,"
            "pps,ppns,bps,bpns,label\n"
        )
        file0.close()

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath

        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.datapaths[datapath.id] = datapath

        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]

    def monitor(self):
        while True:
            for dp in self.datapaths.values():
                self.request_stats(dp)
            hub.sleep(5)

    def request_stats(self, datapath):
        parser = datapath.ofproto_parser
        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):

        timestamp = datetime.now().timestamp()
        file0 = open("FlowStatsfile.csv", "a+")

        for stat in ev.msg.body:

            ip_src = stat.match.get('ipv4_src', '0')
            ip_dst = stat.match.get('ipv4_dst', '0')
            ip_proto = stat.match.get('ip_proto', 0)

            tp_src = 0
            tp_dst = 0
            icmp_code = -1
            icmp_type = -1

            if ip_proto == 1:
                icmp_code = stat.match.get('icmpv4_code', -1)
                icmp_type = stat.match.get('icmpv4_type', -1)

            elif ip_proto == 6:
                tp_src = stat.match.get('tcp_src', 0)
                tp_dst = stat.match.get('tcp_dst', 0)

            elif ip_proto == 17:
                tp_src = stat.match.get('udp_src', 0)
                tp_dst = stat.match.get('udp_dst', 0)

            flow_id = str(ip_src) + str(tp_src) + str(ip_dst) + str(tp_dst) + str(ip_proto)

            try:
                pps = stat.packet_count / stat.duration_sec if stat.duration_sec > 0 else 0
                ppns = stat.packet_count / stat.duration_nsec if stat.duration_nsec > 0 else 0
            except:
                pps = 0
                ppns = 0

            try:
                bps = stat.byte_count / stat.duration_sec if stat.duration_sec > 0 else 0
                bpns = stat.byte_count / stat.duration_nsec if stat.duration_nsec > 0 else 0
            except:
                bps = 0
                bpns = 0

            # 🔥 LABELING (optimized for VM)
            if pps > 20:
                label = 1   # DDoS
            else:
                label = 0   # Normal

            file0.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                timestamp,
                ev.msg.datapath.id,
                flow_id,
                ip_src,
                tp_src,
                ip_dst,
                tp_dst,
                ip_proto,
                icmp_code,
                icmp_type,
                stat.duration_sec,
                stat.duration_nsec,
                stat.idle_timeout,
                stat.hard_timeout,
                stat.flags,
                stat.packet_count,
                stat.byte_count,
                pps,
                ppns,
                bps,
                bpns,
                label
            ))

        file0.close()