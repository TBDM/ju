#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import tbdmConfig

def post_log(whoami, loginfo):
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(whoami.encode() + b'-QAQ-' + loginfo.encode(), (tbdmConfig.logHost, tbdmConfig.logPort))
	except Exception as _Eall:
		print(str(_Eall))
