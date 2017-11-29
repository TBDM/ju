# !/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python version: 3.6.0 -*-
import json
import sys
import traceback

sys.apth.append('../')

from Conf.tbdmSetting import tbdmDatabase


def storeResult(db, file):
    item_num = 0
    with open(file, 'r', encoding='UTF-8') as f:
        try:
            bulk = db['JuDetail'].initialize_unordered_bulk_op()
            for line in f:
                item = json.loads(line)
                if(not db['ItemDetail'].find_one({'item_id' : item['item_id'], 'ju_id': item['ju_id']})):
                    print('hit: ' + item['ju_id'])
                    item_num += 1
                    bulk.insert(item)
                else:
                    print(item['item_id']+'already in database.')
        except Exception as _Eall:
            traceback.print_exc()
        try:
            if(item_num > 0):
                bulk.execute()
        except:
            traceback.print_exc()
    return item_num

if __name__ == '__main__':
    if(not len(sys.argv[1:])):
        print('Usage: '+sys.argv[0]+' [origin file]')
        sys.exit(0)
    fileLocation = sys.argv[1]
    tbdmDb = tbdmDatabase()
    mongod = tbdmDb.tbdmMongo(addrOwner = 'xmu_local', authDb = 'tbdm')
    res = storeResult(mongod, fileLocation)
    print("Finish " + str(res))