#!/usr/bin/env python

import requests
import re
import urlparse
from bs4 import BeautifulSoup
import random
from io import open
import sys
import optparse


# setting the system default encoding as utf-8 at the start of the script, so that all strings are encoded using that.
reload(sys)
sys.setdefaultencoding('utf-8')

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-s", "--source", dest="source", default=True, help="Source to start the scraper for example you can use http://torlinkbgs6aabns.onion ")

    (options, arguments) = parser.parse_args()
    if not options.source:
        parser.error("(x) Please specify an Source, use --help for more info.")
    return options

def get_fake_user_agent():
    user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36']
    return random.choice(user_agents)

headers = {}
def get_response(url):
    try:
        headers['User-agent'] = get_fake_user_agent()
        session.cookies.clear()
        response = session.get(url, headers=headers)
        return response
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        return ""

def extract_links_from(response):
    return re.findall('(?:href=")(.*?)"', response.content)


dark_data = open("dark_data.csv", mode = "wb")
def write_file(link, title, text, mail):
    # Delimited files with a user-specified delimiter " ###### " because the result have a lot of ','
    dark_data.write(link + " ###### " + title + " ###### " + text + "\n")

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
    return title, text, mails


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
            title, text, mail = get_data(response)
            write_file(link, title, text, mail)
            print(title)
            print(link)
            if mail:
                print("[+] Find Email ------> " + str(mail))
            crawl(link)


session = requests.session()
session.proxies = {}
session.proxies['http'] = 'socks5h://localhost:9150'
session.proxies['https'] = 'socks5h://localhost:9150'

# source = "http://torlinkbgs6aabns.onion/"
options = get_arguments()
crawl(options.source)