# !/bin/python
# coding:utf-8
import socket
import os
import threading
import pickle

import itchat
from itchat.content import *
# import requests

# def get_response(msg):
# 	key = 'ff61dcbd86f34a21bdb2f2a980014fb1'
# 	url = 'http://www.tuling123.com/openapi/api'


uin = ''
port = 8888

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
	global uin
	if (msg['isAt']):
		if (msg['Content'] == u'@TBDM Robot uin'):
			print(msg['Content'])
			if (uin == msg['FromUserName']):
				itchat.send(u'UIN is not changed. Thanks anyway!', msg['FromUserName'])
			else:
				uin = msg['FromUserName']
				itchat.send(u'UIN got! Thanks!', msg['FromUserName'])
				with open('TBDMUIN', 'wb') as f:
					pickle.dump(uin, f, 0)
	else:
		itchat.send('Really?')

	print(uin)

def send_log(msg):
	itchat.send(msg, uin)
# chatroomName = 'TBDM'
# itchat.get_chatrooms(update=True)
# chatrooms = itchat.search_chatrooms(name=chatroomName)

# if (chatrooms is None):
# 	pass
# else:
# 	chatroom = itchat.update_chatroom(chatroom[0])
# itchat.send('hello', toGroupName='TBDM')
def listen_log():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind(('', port))
		print('listening')
		while(True):
			data,addr = sock.recvfrom(1024)
			print(data.decode())
			send_log(data.decode())
	except Exception as _Eall:
		logbot.error(str(_Eall))

if __name__ == '__main__':
	logbot = tbdmLogger("logbot", loglevel = 30).log
	itchat.auto_login(enableCmdQR=2, hotReload=True)
	threads = []
	if os.path.exists("TBDMUIN"):
		with open('TBDMUIN', 'rb') as f:
			uin = pickle.load(f)
	try:
		t_itchat = threading.Thread(target=itchat.run,name = 'itchat')
		t_itchat.setDaemon(True)
		t_itchat.start()
		listen_log()
	except Exception as _Eall:
		logbot.error(str(_Eall))
		###