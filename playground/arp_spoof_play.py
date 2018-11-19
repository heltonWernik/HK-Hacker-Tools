   
import scapy.all as scapy

# packet = scapy.ARP(op=2, pdst="192.168.252.98" , hwdst="00:0c:29:c5:7c:d6", psrc="192.168.252.1")
# print(packet.show())
# print(packet.summary())

#   network sudo python arp_spoof_test.py
# ###[ ARP ]###
#   hwtype    = 0x1
#   ptype     = 0x800
#   hwlen     = 6
#   plen      = 4
#   op        = is-at
#   hwsrc     = 60:f8:1d:b3:f2:7a
#   psrc      = 192.168.252.1
#   hwdst     = 00:0c:29:c5:7c:d6
#   pdst      = 192.168.252.98

# None
# ARP is at 60:f8:1d:b3:f2:7a says 192.168.252.1

# def scan(ip):
#    arp_request = scapy.ARP()
#    arp_request.pdst=ip
#    print(arp_request.summary())

# scan("192.168.252.0/24")

# -> ARP who has Net('192.168.252.0/24') says 192.168.252.63