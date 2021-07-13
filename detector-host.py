#coding:utf-8
"""
author: nejidev
github: https://github.com/nejidev

python3
pip install urllib3

example:
1, pre config ip parse file
curl https://api.github.com/meta -o githubip.txt
2, add detector 
https_detector("https://github.com", "githubip.txt")
3, run adminirstor or root python3 detector-host.py
"""

import os
import sys
import re
from urllib3.util import connection
from urllib3 import connectionpool

_orig_create_connection = connection.create_connection
ip_list = []
ip_index = 0

def patched_create_connection(address, *args, **kwargs):
	host, port = address
	global ip_list
	global ip_index

	hostname = ip_list[ip_index]
	ip_index += 1
	
	print(hostname)
	return _orig_create_connection((hostname, port), *args, **kwargs)

def parse_ip_file(file):
	f = open(file)
	content = f.read()
	f.close()
	return re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", content)

def https_detector(url, parse_file):
	global ip_list
	global ip_index

	ip_index = 0
	ip_list = parse_ip_file(parse_file)

	for i in range(0, len(ip_list)):
		connection.create_connection = patched_create_connection
		conn = connectionpool.connection_from_url(url)
		resp = conn.request('GET', url)
		print(resp.data)

"""
run https_detector
"""
https_detector("https://github.com", "githubip.txt")
