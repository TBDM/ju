# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python version: 3.6.0 -*-
import traceback

import json
import pymongo


from tbdmSetting import tbdmDatabase


tbdmDb = tbdmDatabase()
mongoCli = tbdmDb.tbdmMongo(addrOwner = 'xzliu', authDb = 'tbdm')
mongod = mongoCli.tbdm

def getCollection(db, item_type):
	if(item_type == 'tmall'):
		co = db.tmall
	elif(item_type == 'tmall_hk'):
		co = db.tmall_hk
	return co

def storeResult(db, file):
	total = {}
	item_num = 0
	with open(file, 'r') as f:
		try:
			res = json.loads(f.read())
			for item_type in res:
				co = getCollection(db, item_type)
				bulk = co.initialize_unordered_bulk_op()
				for item in res[item_type]:
					if(not co.find_one({'item_id' : item['item_id']})):
						print('hit: ' + item_type + '-Q.Q-' + item['item_id'])
						item_num += 1
						bulk.find({'item_id' : item['item_id']}).upsert().update_one({'$setOnInsert' : item})
				try:
					total[item_type] = item_num
					if(item_num > 0):
						bulk.execute()
						item_num = 0
				except Exception as _Eall:
					traceback.print_exc()
			return total
		except:
			traceback.print_exc()


if __name__ == '__main__':
	res = storeResult(mongod, 'result.json')
	for key in res:
		print('Item type of ***' + key + '*** hit ' + str(res[key]))