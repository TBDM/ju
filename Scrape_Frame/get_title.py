# -*- coding: utf-8 -*-
import sys
import subprocess
import pymongo
import re
import time
try:
	skip_num = int(sys.argv[1])
	limit_num = int(sys.argv[2])
except IndexError:
	skip_num = 0
	limit_num = 50
client = pymongo.MongoClient('119.29.96.77', 27017)
db = client.ju
item_list = db.ju.find({'title' : None}).skip(skip_num).limit(limit_num)
num = 0
try:
	subprocess.call(['mkdir', time.strftime("%Y%m%d", time.localtime())])
	subprocess.call(['mkdir', 'ju_trash'])
	print('create folder successful')
except Exception:
	print('create folder successful')


try:
	for item in item_list:
		print(str(item['item_id']))
		retcode = subprocess.call(['phantomjs', 'spider.js', 'https://item.taobao.com/item.htm?id=' + item['item_id']])
		if(retcode == 0):
			try:
				content = open(item['item_id'] + '.html').read()
				try:
					title = re.search('<h3 class="tb-main-title" data-title="([\S ]*)"', content).group(1)
					url = 1
					print(title)
					print('item.taobao.com')
					db.ju.update(
						{"item_id" : item['item_id']}, 
						{"$set" : {'title' : title, 'url' : url}}
					)
					subprocess.call(['mv', item['item_id'] + '.html', time.strftime("%Y%m%d", time.localtime()) + '/' + item['item_id'] + '.html'])
					num = num + 1
					print('sleep 10s')
					time.sleep(10)
				except AttributeError:
					try:
						title = re.search('<input type="hidden" name="title" value="([\S ]*)"', content).group(1)
						url = 2
						print(title)
						print('detail.tmall.com')
						db.ju.update(
							{"item_id" : item['item_id']}, 
							{"$set" : {'title' : title, 'url' : url}}
						)
						subprocess.call(['mv', item['item_id'] + '.html', time.strftime("%Y%m%d", time.localtime()) + '/' + item['item_id'] + '.html'])
						num = num + 1
						print('sleep 10s')
						time.sleep(10)
					except AttributeError:
						print('file error, try again later')
						subprocess.call(['mv', item['item_id'] + '.html', 'ju_trash/' + item['item_id'] + '.html'])
			except FileNotFoundError:
				print('file not found')
		else:
			retcode = subprocess.call(['phantomjs', 'spider.js', 'https://detail.tmall.hk/hk/item.htm?id=' + item['item_id']])
			if(retcode == 0):
				try:
					content = open(item['item_id'] + '.html').read()
					try:
						title = re.search('<input type="hidden" name="title" value="([\S ]*)"', content).group(1)
						url = 3
						print(title)
						print('detail.tmall.hk')
						db.ju.update(
							{"item_id" : item['item_id']}, 
							{"$set" : {'title' : title, 'url' : url}}
						)
						subprocess.call(['mv', item['item_id'] + '.html', time.strftime("%Y%m%d", time.localtime()) + '/' + item['item_id'] + '.html'])
						num = num + 1
						print('sleep 10s')
						time.sleep(10)
					except AttributeError:
						print('file error, try again later')
						subprocess.call(['mv', item['item_id'] + '.html', 'ju_trash/' + item['item_id'] + '.html'])
				except FileNotFoundError:
					print('file not found')
			else:
				retcode = subprocess.call(['phantomjs', 'spider.js', 'https://chaoshi.detail.tmall.com/item.htm?id=' + item['item_id']])
				if(retcode == 0):
					try:
						content = open(item['item_id'] + '.html').read()
						try:
							title = re.search('<input type="hidden" name="title" value="([\S ]*)"', content).group(1)
							url = 4
							print(title)
							print('chaoshi.detail.tmall.com')
							db.ju.update(
								{"item_id" : item['item_id']}, 
								{"$set" : {'title' : title, 'url' : url}}
							)
							subprocess.call(['mv', item['item_id'] + '.html', time.strftime("%Y%m%d", time.localtime()) + '/' + item['item_id'] + '.html'])
							num = num + 1
							print('sleep 10s')
							time.sleep(10)
						except AttributeError:
							print('file error, try again later')
							subprocess.call(['mv', item['item_id'] + '.html', 'ju_trash/' + item['item_id'] + '.html'])
					except FileNotFoundError:
						print('file not found')
				else:
					retcode = subprocess.call(['phantomjs', 'spider.js', 'https://detail.yao.95095.com/item.htm?id=' + item['item_id']])
					if(retcode == 0):
						try:
							content = open(item['item_id'] + '.html').read()
							try:
								title = re.search('<input type="hidden" name="title" value="([\S ]*)"', content).group(1)
								url = 5
								print(title)
								print('detail.yao.95095.com')
								db.ju.update(
									{"item_id" : item['item_id']}, 
									{"$set" : {'title' : title, 'url' : url}}
								)
								subprocess.call(['mv', item['item_id'] + '.html', time.strftime("%Y%m%d", time.localtime()) + '/' + item['item_id'] + '.html'])
								num = num + 1
								print('sleep 10s')
								time.sleep(10)
							except AttributeError:
								print('file error, try again later')
								subprocess.call(['mv', item['item_id'] + '.html', 'ju_trash/' + item['item_id'] + '.html'])
						except FileNotFoundError:
							print('file not found')
					else:
						print('oops! taobao has upgraded their spider ban')
except KeyboardInterrupt:
	print('')
	print('totally ' + str(num) + ' successed')
print('')
print('totally ' + str(num) + ' successed')