#!/usr/bin/env python
#@TODO: create optparce to target url

import requests

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = "google.com"

with open("subdomains-wodlist.txt", "r") as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        test_url = word + "." + target_url
        test_url2 = target_url + "/" + word
        response = request(test_url)
        if response:
            print("[+] I found a subdomain --> " + test_url)
        response2 = request(test_url2)
        if response2:
            print("[+] I found a subdomain --> " + test_url2)