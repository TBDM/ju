# !/usr/bin/env python
# -*- coding: utf-8 -*-


#----------model import----------

import os
import time
import redis
import pymongo
from tbdmPrivacy import tbdmDatabase

#----------model import----------


#----------global variables----------

"""
@param:
	tbdmDb 		tbdmDatabase instance.
	mongoCli	MongoDB connections. This can be maintained by the manager in future, 
						'cause pymongo(3.3.0) instances are thread-safe (but not fork-safe). 
	redis0Cli	Redis connections to db0. This can be maintained by the manager in future, 
						'cause py-redis(2.10.5) instances are thread-safe. 
"""
#Workers maintain their own connections
tbdmDb = tbdmDatabase()
mongoCli = tbdmDb.tbdmMongo(addrOwner = 'jbtan')
redis0Cli = tbdmDb.tbdmRedis(addrOwner = 'jbtan', connDb = 0, auth = True)

#----------global variables----------

#----------class definition----------

#----------class definition----------


#----------function definition----------
Class workPipeline(tasknum, wid):
	"""
	Scrape pipeline for TBDM Project.
	!! This class must be instantiated before use.
	@pythonVersion: 3.5.2
	@methods:	tasker 		Acquires tasks for this worker and sets up a 
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
	tasknum = 10;
	wid = 0;

	def tasker(tasknum, wid):
		"""
		Tasker acquires tasks for this worker and sets up a file lock for recovering.
		@param:
				tasknum		Tasks to be executed at one run, no more than 100.
				wid 		Process id set by manager.
		"""
		#TODO: detect if there is a lock file. if so, do recovery instead of get task
		with redis0Cli.pipeline() as poppipe:
			try:
				#Starting transaction
				poppipe.muitl()
				taskqueue = poppipe.zrange('juList', 0, tasknum - 1)
				if taskqueue:
					for item in taskqueue:
						poppipe.zrem(item)
				else:
					#Redis returned no task, return error code 127
					return 127
				poppipe.execute()
			except Exception as _Eall:
				#TODO: deal with exceptions

		#Create new file lock for recovery
		try:
			os.mkdir('tbdmLock')
		except FileExistsError as _Efest:
			pass
		except Exception as _Eall:
			print('mkdir error' + _Eall)
			pass
		lockname = str(time.time()) + '_' + str(wid) + '.lock'
		with open('tbdmLock/' + lockname, 'w') as lockfile:
			for item in taskqueue:
				lockfile.write(item + '\n')

		return [taskqueue, lockname]

	def postman(wid = 0):
		"""
		Postman checks for last fail records and sends them back to redis after task acquiring.
		@param:
				wid 		Process id set by manager.
		"""
		try:
			with open('tbdmLock/fail_' + str(wid) + '.csv', 'r') as faillist:
				#TODO: send fail list back to redis
		except FileNotFoundError as _Efnfd:
			pass
		except Exception as _Eall:
			print('postman failed')


	def worker(taskqueue, lockname, wid = 0):
		"""
		Worker does the work and record what he/she has done. 
		@param:
				taskqueue	Work to be done.
				wid 		Process id set by manager.
				lockname	Name of lockfile for this session.
		"""
		#TODO4pan:	deal with tasks then set up schedule_time 
		#			and status for redis records
		#Scrape
		#Record results to tbdmStore
		#Record succ.csv to tbdmLog
		#Record fail_wid.csv to tbdmLock

		# notice the manager and remove lock
		# NOTA:	Removing the lockfile means all processes went as expected,
		#		otherwise return before removing lockfile to do recovery 
		#		at next run.
		os.remove('tbdmLock' + lockname)
		return success_num

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
	wp = workPipeline()
	[taskqueue, lockname] = wp.tasker();
	wp.postman();
	success_num = wp.worker(taskqueue, lockname);

#----------main function----------
