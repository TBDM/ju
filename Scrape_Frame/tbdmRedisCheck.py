#!/usr/bin/env python
# -*- coding: utf-8 -*-


#----------model import----------

import time
import random
import redis.exceptions
from datetime import datetime

import tbdmConfig
from tbdmSetting import tbdmDatabase
from tbdmLogging import tbdmLogger

#----------model import----------


#----------global variables----------

"""
@param:
    tbdmDb         tbdmDatabase instance.
    logger        tbdmLogger instance.
    mongoCli    MongoDB connections. This can be maintained by the manager in future, 
                        'cause pymongo(3.3.0) instances are thread-safe (but not fork-safe). 
    redis0Cli    Redis connections to db0. This can be maintained by the manager in future, 
                        'cause py-redis(2.10.5) instances are thread-safe. 
"""
#Workers maintain their own connections
tbdmDb = tbdmDatabase()

#----------global variables----------


#----------class definition----------
class redisCheck():
    """
    Scrape pipeline for TBDM Project.
    !! This class must be instantiated before use.
    @pythonVersion: 3.5.2
    @methods:
    tasker         Acquires tasks for this worker and sets up a 
                file lock for recovering.
    postman        Checks for last fail records and sends them back 
                to redis after task acquiring.
    worker         Does the work and record what have been done. 
    @author: X.Huang, P.Liu
    @maintenance: X.Huang, P.Liu
    @creation: 2016-11-8
    @modified: 2016-11-8
    @version: 0.01-alpha
    """
    redisCli = tbdmDb.tbdmRedis(addrOwner = 'xhuang', auth = True)

    def reporter(self):
        result = {0 : 0, 1 : 0, 2 : 0, "today" : 0, "nearnd" : {}, "total" : 0}
        nowstamp = time.time()
        todayLeft = (datetime.strptime("23:59:59", "%H:%M:%S") - 
                    datetime.strptime(datetime.fromtimestamp(nowstamp).strftime("%H:%M:%S"), "%H:%M:%S")).seconds
        with self.redisCli.pipeline() as poppipe:
            while True:
                try:
                    #Starting transaction
                    poppipe.watch('juList')
                    tasklist = poppipe.zrange('juList', 0, -1)
                    poppipe.execute()
                    if tasklist:
                        for item in tasklist:
                                score = int(item.decode().split('/')[2])
                                if (score == 0):
                                    result[0] += 1
                                elif (score <= nowstamp + 3600):
                                    result[1] += 1
                                elif (score <= nowstamp + 7200):
                                    result[2] += 1
                                if (score <= nowstamp + todayLeft):
                                    result["today"] += 1
                                else:
                                    if (score in result["nearnd"].keys()):
                                            result["nearnd"][score] += 1
                                    else:
                                        if (len(result["nearnd"]) < 12):
                                            result["nearnd"][score] = 1
                                        elif (score < max(result["nearnd"].keys())):
                                            result["nearnd"].pop()
                                            result["nearnd"][score] = 1
                                result["total"] += 1
                    else:
                        print("Redis returned empty list, exiting.")
                        #Redis returned no task
                    break
                except redis.exceptions.WatchError as _Ewatch:
                    print("Redis watch error, retry fetching.")
                    time.sleep(random.uniform(3, 5))
                    continue
                except Exception as _Eall:
                    print(_Eall)

        print("=====REPORT=====\nTasks: " + str(result["total"]))
        print("Tasks not fetched yet: " + str(result[0]))
        print("Tasks within 1 hour:   " + str(result[1]))
        print("Tasks within 2 hour:   " + str(result[2]))
        print("Tasks within today:    " + str(result["today"]))
        print("\nEarliest task after today: ") 
        for k, v in result["nearnd"].items():
            print(datetime.fromtimestamp(k).strftime("%Y-%m-%d %H:%M:%S") + " : " + str(v))
        print("=====ENDREP=====")
        return

#----------class definition----------


#----------function definition----------

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
    if (tbdmConfig.WHO_IAM == ''):
        # Check for Config
        print("Tell me who you are in tbdmConfig before starting RedisCheck.")
    else:
        rcheck = redisCheck()
        rcheck.reporter()

#----------main function----------
