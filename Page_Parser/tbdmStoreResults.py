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


def storeResult(db, file):
	total = {}
	item_num = 0
	with open(file, 'r') as f:
		try:
			res = json.loads(f.read())
			for item_type in res:
				bulk = db[item_type].initialize_unordered_bulk_op()
				for item in res[item_type]:
					if(not db[item_type].find_one({'item_id' : item['item_id'], 'timestamp': item['timestamp']})):
						print('hit: ' + item_type + '-Q.Q-' + item['item_id'])
						item_num += 1
						bulk.insert(item)
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