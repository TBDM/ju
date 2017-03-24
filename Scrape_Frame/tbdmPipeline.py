#!/usr/bin/env python
# -*- coding: utf-8 -*-


#----------model import----------

import os
import time
import pickle
import random
import redis.exceptions

import tbdmscraper
import tbdmConfig
from tbdmSetting import tbdmDatabase
from tbdmLogging import tbdmLogger
from tbdmSlack import tbdmSlack

#----------model import----------


#----------global variables----------

"""
@param:
	tbdmDb 		tbdmDatabase instance.
	logger		tbdmLogger instance.
	mongoCli	MongoDB connections. This can be maintained by the manager in future, 
						'cause pymongo(3.3.0) instances are thread-safe (but not fork-safe). 
	redis0Cli	Redis connections to db0. This can be maintained by the manager in future, 
						'cause py-redis(2.10.5) instances are thread-safe. 
"""
#Workers maintain their own connections
tbdmDb = tbdmDatabase()
logger = tbdmLogger('tbdmWorkpipe').log
redisCli = tbdmDb.tbdmRedis(addrOwner = 'xhuang', auth = True)
mongoCli = tbdmDb.tbdmMongo(addrOwner = 'xhuang', authDb = 'tbdm')
slacker = tbdmSlack()

NO_TASK_HALT = 300

#----------global variables----------


#----------class definition----------
class workPipeline():
	"""
	Scrape pipeline for TBDM Project.
	!! This class must be instantiated before use.
	@pythonVersion: 3.5.2
	@methods:
	tasker 		Acquires tasks for this worker and sets up a 
				file lock for recovering.
	postman		Checks for last fail records and sends them back 
				to redis after task acquiring.
	worker 		Does the work and record what have been done. 
	@author: X.Huang, P.Liu
	@maintenance: X.Huang, P.Liu
	@creation: 2016-11-8
	@modified: 2016-11-8
	@version: 0.01-alpha
	"""
	tasknum = tbdmConfig.TASK_NUM;
	time_wait_flag = True

	def tasker(self):
		if os.path.exists("tbdmPipelock.lock"):
			logger.warning("Lock file detected, recovering from lock.")
			with open("tbdmPipelock.lock", "rb") as f:
				tasklist = pickle.load(f)
		else:
			with redisCli.pipeline() as poppipe:
				while True:
					try:
						#Starting transaction
						poppipe.watch('juList')
						tasklist = poppipe.zrange('juList', 0, self.tasknum - 1)
						if tasklist:
							poppipe.multi()
							for item in tasklist:
								poppipe.zrem('juList', item)
						else:
							logger.warning("Redis returned empty list, halting worker.")
							slacker.post_message("Redis returned empty list, halting worker for " + str(NO_TASK_HALT)
												 + " seconds.")
							time.sleep(NO_TASK_HALT)
							continue
							#Redis returned no task
						poppipe.execute()
						tbdmscraper.task_locker(tasklist)
						break
					except redis.exceptions.WatchError as _Ewatch:
						logger.warning("Redis watch error, retry fetching.")
						time.sleep(random.uniform(3, 5))
						continue
					except Exception as _Eall:
						logger.error(_Eall)
		return tasklist

	def manager(self):
		"""
		Tasker acquires tasks for this worker and sets up a file lock for recovering.
		@param:
				tasknum		Tasks to be executed at one run, no more than 100.
		"""
		taskstrs = self.tasker()
		taskdicts = tbdmscraper.task_strs2dicts(taskstrs)
		if(tbdmscraper.task_min_score(taskdicts) > time.time()):
			sleeptime = int((tbdmscraper.task_min_score(taskdicts) - time.time()) % 420) + 30
			if(self.time_wait_flag):
				logger.warning("Worker halts waiting for latest tasktime for " + str(sleeptime) + " seconds.")
				self.time_wait_flag = False
			tbdmscraper.task_back2redis(taskdicts)
			time.sleep(sleeptime)
		else:
			if(not self.time_wait_flag):
				logger.warning("Worker continued from task time waiting.")
				self.time_wait_flag = True
			(success_cnt, total_cnt) = tbdmscraper.request_page(taskdicts)
			logger.warning("Worker finished " + str(success_cnt) + " out of " + str(total_cnt))

#----------class definition----------


#----------function definition----------

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
	workpipe = workPipeline()
	try:
		tbdmscraper.display.start()
	except Exception as _Eall:
		logger.critical("Manager reported an error " + str(_Eall))
		time.sleep(3)

	while (not os.path.exists('stopPipe')):
		try:
			workpipe.manager()
		except Exception as _Eall:
			logger.critical("Manager reported an error " + str(_Eall))
			time.sleep(3)
			tbdmscraper.driver.quit()
			tbdmscraper.display.stop() 
		else:
			logger.info("Manager finished one round.")
	tbdmscraper.driver.quit()
	tbdmscraper.display.stop() 
	logger.warning("Manager stopped on detecting flag.")
	slacker.post_message("Manager stopped on detecting flag.")

#----------main function----------
