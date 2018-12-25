# !/usr/bin/python
# This is a antivirus I create with python using Virus Total API, unfortunately The Virus Total Public API is limited to 4 requests per minute.
# You need to put your virus total api_key in line 14 it's free
# for tests pourpose you can check for malicius hash, change the line 30 -> return hasher.hexdigest() for this: return "52d3df0ed60c46f336c131bf2ca454f73bafdc4b04dfa2aea80746f5ba9e6d1c"
import os
import requests
import hashlib

import time
import sys

def scan(hash_str):
   url = 'https://www.virustotal.com/vtapi/v2/file/report'
   api_key = "your apikey"
   params = {'apikey': api_key, 'resource': hash_str}
   response = requests.get(url, params=params)
   if "204" in str(response):
      print("\nThe Virus Total Public API is limited to 4 requests per minute.")
      exit()
   return response.json()

def get_hash(file_path):
   BLOCKSIZE = 65536
   hasher = hashlib.sha256()
   with open(file_path, 'rb') as afile:
      buf = afile.read(BLOCKSIZE)
      while len(buf) > 0:
         hasher.update(buf)
         buf = afile.read(BLOCKSIZE)
   return hasher.hexdigest()

def get_virus_total_response_list(path):
   result_list = []
   for root, dirs, files in os.walk(path):
      for f in files:
         current_file = os.path.join(root,f)
         hash_str = get_hash(current_file)
         vt_response = scan(hash_str)

         print("\r[+] scanning " + current_file),
         sys.stdout.flush()
         time.sleep(2)

         if vt_response["response_code"]:
            result = {}
            result["file"] = current_file
            result["result"] = vt_response
            result_list.append(result)
            return result_list
      

vt_result = get_virus_total_response_list(raw_input("Enter a path do you want to scanner\n"))
# /Users/heltonwernik/test_dir

for dic in vt_result:
   positive_anti_virus_list = []
   result = dic["result"]
   if result["positives"] > 0:
      scans = result["scans"]
      for scan, result in scans.items():
         if result["detected"]:
            positive_anti_virus_list.append(scan)
      print("Detected virus in:\n" + 15 * "-" + dic["file"] + 15 * "-" + "\nby this Anti_virus services: " + ", ".join(positive_anti_virus_list))
   else:
      print("All clear, you can sleep peacefully today.")
