#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import sys

if(len(sys.argv) != 3):
	exit(1)

toUserName = sys.argv[1]
message = sys.argv[2]

port = 8888
#host = '123.206.176.165'
host = '139.199.77.204'




def post_log(whoami, loginfo):
	# print('ok')
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(whoami.encode() + b'-QAQ-' + loginfo.encode(), (host,8888))
		exit(0)
	except Exception as _Eall:
		print(str(_Eall))
		exit(1)
	# print('ok')

if __name__ == '__main__':
	post_log(toUserName, message)
