# !/usr/bin/env python
# -*- coding: utf-8 -*-


#----------model import----------

import re
import time
import urllib.request
import redis
import pymongo
from tbdmPrivacy import tbdmDatabase

#----------model import----------


#----------global variables----------

tbdmDb = tbdmDatabase()
redis0Client = tbdmDb.tbdmRedis(addrOwner = 'jbtan', connDb = 0, auth = True)
mongoClient = tbdmDb.tbdmMongo(addrOwner = 'jbtan')

#----------global variables----------


#----------class definition----------

#----------class definition----------


#----------function definition----------

def page():
	data = urllib.request.urlopen('https://ju.taobao.com/tg/forecast.htm').read().decode('gbk')
	list_num = re.search('<span class="sum"><em>1</em>/([0-9]*)</span>', data).group(1)
	return int(list_num)

def filtrate(mongoClient, redis0Client, num):
	juBulk = mongoClient.juList.ju.initialize_unordered_bulk_op()
	redisPipe = redis0Client.pipeline()
	data = urllib.request.urlopen('https://ju.taobao.com/tg/forecast.htm?page=' + str(num)).read().decode('gbk')
	'''
	f = open(str(num) + '.html', 'wb')
	f.write(data.encode('utf-8'))
	f.close()
	'''
	item_list = re.findall('detail.ju.taobao.com/home.htm\?id=([0-9]*)&amp;item_id=([0-9]*)', data)
	for item in item_list:
		juBulk.find({'ju_id' : item[0], 'item_id' : item[1]}).upsert().update_one(
			{'$setOnInsert' : {'schedule_time' : 0, 'status' : 0}})
		#redisPipeline.zadd(SortedSetName, Score, String containing juId/itemId/Status delimited by '/')
		redisPipe.zadd('juList', 0, item[0] + '/' + item[1] + '/' + '0')
		'''
		if(not juDb.ju.find_one({'ju_id' : item[0]})):
			item_num = item_num + 1
			juDb.ju.insert_one({
				'ju_id' : item[0],
				'item_id' : item[1],
			})
		'''
	try:
		mongoFeedback = juBulk.execute()
		item_num = mongoFeedback['nUpserted']
	except pymongo.errors.InvalidOperation as _Einvo:
		print('No ju-item found: ', _Einvo)
		item_num = 0
	except Exception as _Eall:
		#TODO: deal with other exceptions
		item_num = 0
		pass
	try:
		redisPipe.execute()
	except Exception as _Eall:
		#TODO: deal with exceptions
		pass
	return item_num

#----------function definition----------


#----------main function----------

print("[" + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + "*] " + "item start")
list_num = page()
total_num = 0
# print('totally ' + str(list_num) + ' pages')

for num in range(1, list_num + 1):
	item_num = filtrate(mongoClient, redis0Client, num)
	total_num = total_num + item_num
	print("[" + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + str(num) + "] " + str(item_num) + " items added")

print("[" + time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()) + "*] " + "item end, totally " + str(total_num) + ' items added')

#----------main function----------
