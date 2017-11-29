# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python version: 3.6.0 -*-
import json
import sys
import traceback
import time

sys.path.append('../')

from Conf.tbdmSetting import tbdmDatabase


def storeResult(db, file, type):
    item_num = 0
    if(type == 'ju'):
        collection = 'ju_detail'
    elif(type == 'item'):
        collection = 'item_detail'
    with open(file, 'r', encoding='UTF-8') as f:
        try:
            bulk = db[collection].initialize_unordered_bulk_op()
            for line in f:
                item = json.loads(line)
                if(type == 'ju' and len(item['error']) == 0):
                    print('Storing ju page '+item['ju_id'])
                    bulk.find({'ju_id': item['ju_id'], 'item_id': item['item_id'], 'timestamp': item['timestamp']}).upsert().update_one({'$setOnInsert':item})
                elif(type == 'item' and len(item['error']) == 0):
                    print('Storing item page ' + item['item_id'])
                    bulk.find({'item_id': item['item_id'], 'timestamp': item['timestamp']}).upsert().update({'$setOnInsert':item})
                item_num += 1
        except Exception as _Eall:
            traceback.print_exc()
        try:
            if(item_num > 0):
                bulk.execute()
        except:
            traceback.print_exc()
    return item_num

if __name__ == '__main__':
    # fileLocation = './test-ju.json'
    # type = 'ju'
    if(not len(sys.argv[2:])):
        print('Usage: '+sys.argv[0]+' [origin file] [page type]')
        sys.exit(0)
    fileLocation = sys.argv[1]
    type = sys.argv[2]
    tbdmDb = tbdmDatabase()
    mongod = tbdmDb.tbdmMongo(addrOwner = 'xmu_local', authDb = 'tbdm')
    res = storeResult(mongod, fileLocation, type)
    print("Finish " + str(res) + 'At: '+time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time())))