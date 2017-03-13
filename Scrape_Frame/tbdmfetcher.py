#!/usr/bin/env python
# -*- Python Ver: 3.6.0 -*-
# -*- coding: utf-8 -*-

#----------model import----------

import re
import os
import time
import urllib.request
import pickle

import pymongo

from tbdmSlack import tbdmSlack
from tbdmSetting import tbdmDatabase
from tbdmLogging import tbdmLogger

#----------model import----------


#----------global variables----------

tbdmDb = tbdmDatabase()
fetchlog = tbdmLogger("fetch", loglevel = 20).log # logging.DEBUG - 10, increase 10 for every level
redisCli = tbdmDb.tbdmRedis(addrOwner = 'xhuang', auth = True)
mongoCli = tbdmDb.tbdmMongo(addrOwner = 'xhuang', authDb = 'tbdm')
mongod = mongoCli.tbdm
slacker = tbdmSlack()

SLEEP_DURATION = 360 # This should be a const : )

#----------global variables----------


#----------class definition----------

#----------class definition----------


#----------function definition----------

def page():
	data = urllib.request.urlopen('https://ju.taobao.com/tg/forecast.htm').read().decode('gbk')
	list_num = re.search('<span class="sum"><em>1</em>/([0-9]*)</span>', data).group(1)
	return int(list_num)

def filtrate(db, num):
	data = urllib.request.urlopen('https://ju.taobao.com/tg/forecast.htm?page=' + str(num)).read().decode('gbk')
	item_num = 0
	item_list = re.findall('detail.ju.taobao.com/home.htm\?id=([0-9]*)&amp;item_id=([0-9]*)', data)
	bulk = db.juList.initialize_unordered_bulk_op()
	with redisCli.pipeline() as redisp:
		for item in item_list:
			if(not db.juList.find_one({'juID' : item[0]})):
				item_num += 1
				bulk.find({'juID' : item[0]}).upsert().update_one({'$setOnInsert' : {
					'juID' : item[0],
					'itemID' : item[1],
					'status' : 0,
					'score' : 0,
					'urlType' : 0
				}})
				# Task to be inserted into Redis queue on format: juid/itemid/next_time/status/url_type/fail
				taskinfo = ''.join((str(x) + '/' for x in item)) + '0/0/0/0/'
				# Redis.pipeline.zadd(zset_name, score, key)
				redisp.zadd('juList', 0, taskinfo)
		try:
			if(item_num > 0):
				bulk.execute()
				redisp.execute()
		except Exception as _Eall:
			fetchlog.error("Database error:" + str(_Eall))
			slacker.post_message("Database error:" + str(_Eall) + "\nData dumped with pickle. "
				"Do recovery ASAP.", channel = 'test')
			if not os.path.isdir('fetch_dump'):
				os.mkdir('fetch_dump')
			with open('fetch_dump/' + str(time.time()), 'ab+') as f:
				pickle.dump(item_list, f, 0)
			item_num = -1
		finally:
			return item_num

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
	while not os.path.isdir('stopFetch'):
		try:
			fetchlog.info("Fetch start")
			list_num = page()
			total_num = 0
			for num in range(1, list_num + 1):
				item_num = filtrate(mongod, num)
				total_num = total_num + item_num
				if(item_num > 0):
					fetchlog.info(str(item_num) + " items added on page " + str(num))
					slacker.post_message(str(item_num) + " items added on page " + str(num), channel = 'test')
				time.sleep(time.time()%5 + 5)
			fetchlog.info("Fetch end with " + str(total_num) + " items added, "
				"next fetch scheduled " + str(SLEEP_DURATION) + "s later")
			time.sleep(SLEEP_DURATION)
		except:
			pass
	fetchlog.info("Fetcher stopped on detecting flag.")
	slacker.post_message("Fetcher stopped on detecting flag.", channel = 'test')

#----------main function----------
