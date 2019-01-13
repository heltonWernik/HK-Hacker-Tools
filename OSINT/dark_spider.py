#!/usr/bin/env python
# Spider that find .onion urls in the dark web and test if its up
# To run you need to open TOR browser
#TODO find email's and other information, Search something.

import requests
import re
import urlparse

target_links = []

def url_ok(url):
    try:
        r = session.head(url)
    except:
        return False
    return r.status_code == 200

def extract_links_from(url):
    response = session.get(url, headers=headers)
    return re.findall('(?:href=")(.*?)"', response.content)

def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if link not in target_links:
            if url_ok(link):
                target_links.append(link)
                print(link)
                crawl(link)


session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9150'
session.proxies['https'] = 'socks5h://localhost:9150'
headers = {}
headers['User-agent'] = "HotJava/1.1.2 FCS"


target_url = "http://wikitjerrta4qgz4.onion/"
crawl(target_url)