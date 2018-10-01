#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC addres")
    parser.add_option("-m", "--mac", dest="new_mac", help="New Mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("(x) Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("(x) Please specify a new MAC, use --help for more info.")
    return options

def change_mac(interface, new_mac):
    print("(o) Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("(x) Could not read MAC address.") 


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("current MAC = " + str(current_mac))
change_mac(options.interface, options.new_mac)

current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("(o) MAC address was successfully changed to " + current_mac)
else:
    print("(x) MAC address did not get changed.")


# get interfaces:
# ifconfig | expand | cut -c1-8 | uniq -u | awk -F: '{print $1;}'

# create random MAC:
# import random

# # The first line is defined for specified vendor
# mac = [ 0x00, 0x24, 0x81,
#     random.randint(0x00, 0x7f),
#     random.randint(0x00, 0xff),
#     random.randint(0x00, 0xff) ]

# print ':'.join(map(lambda x: "%02x" % x, mac))