#!/usr/bin/env python
#@TODO: create optparce to target url

import requests
import time
import sys

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "docdok.health"

with open("wordlists/subdomains-wodlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        response = request(test_url)
        print("\r " + test_url + "         "),
        sys.stdout.flush()
        if response:
            print("[+] I found a subdomain")

with open("wordlists/files-and-dirs-wordlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = target_url + "/" + word
        response = request(test_url)
        print("\r " + test_url + "         "),
        sys.stdout.flush()
        if response:
            print("[+] I found a url")