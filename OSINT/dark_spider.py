#!/usr/bin/env python
# Spider that find .onion urls in the dark web and test if its up
# To run you need to open TOR browser
# Put in target_url line 66 .onion index you know and the spider go to all links and links inside this links and create a database of links, title, text and emails

import requests
import re
import urlparse
from bs4 import BeautifulSoup

def get_response(url):
    try:
        response = session.get(url, headers=headers)
        return response
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return ""

def extract_links_from(response):
    return re.findall('(?:href=")(.*?)"', response.content)

title_list = []
emails = []
texts = []
def get_data(response):
    soup = BeautifulSoup(response.text, features="html.parser")
    title = soup.title.string
    title_list.append(title)
    text = soup.text
    texts.append(text)
    mails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    emails.append(mails)
    return title, mails


target_links = []

def crawl(url):
    response = get_response(url)
    href_links = extract_links_from(response)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if ".onion" in link and link not in target_links:
            target_links.append(link)
            title, mail = get_data(response)
            print(title)
            print(link)
            if mail:
                print("[+] Find Email ------> " + str(mail))
            crawl(link)


session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9150'
session.proxies['https'] = 'socks5h://localhost:9150'
headers = {}
headers['User-agent'] = "HotJava/1.1.2 FCS"


target_url = "http://torlinkbgs6aabns.onion/"
crawl(target_url)