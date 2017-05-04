#!/usr/bin/env python
#coding:utf-8

import socket
import time

port = 8888
#host = '123.206.176.165'
host = '139.199.77.204'

def post_log(whoami, loginfo):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(whoami.encode() + b'-QAQ-' + loginfo.encode(), (host,8888))
	except Exception as _Eall:
		print(str(_Eall))
