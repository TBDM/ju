#!/usr/bin/env python
#coding:utf-8

import socket
import time

port = 8888
host = '139.199.77.204'

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(b"Hello, tbdm", (host,port))