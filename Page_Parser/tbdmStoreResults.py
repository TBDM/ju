# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python version: 3.6.0 -*-
import traceback

import json
import pymongo


from tbdmSetting import tbdmDatabase


tbdmDb = tbdmDatabase()
mongoCli = tbdmDb.tbdmMongo(addrOwner = 'xzliu', authDb = 'test')
mongod = mongoCli.test


def storeResult(db, file):
	total = {}
	item_num = 0
	with open(file, 'r') as f:
		try:
			bulk = db['ItemDetail'].initialize_unordered_bulk_op()
			for line in f:
				item = json.loads(line)
				print(item)
				if(not db['ItemDetail'].find_one({'item_id' : item['item_id'], 'timestamp': item['timestamp']})):
					print('hit: ' + item['item_id'])
					item_num += 1
					bulk.insert(item)
		except Exception as _Eall:
			traceback.print_exc()
		try:
			if(item_num > 0):
				bulk.execute()
		except:
			traceback.print_exc()
	return item_num


if __name__ == '__main__':
	res = storeResult(mongod, 'result.json')
	print("ok" + str(res))