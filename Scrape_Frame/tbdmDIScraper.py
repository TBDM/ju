# !/usr/bin/env python
# -*- Python Ver: 3.5.2 -*-
# -*- coding: utf-8 -*-
# Scraper for pipeline with displays.

#----------model import----------

# Import built-in models
import re
import os
import sys
import time
import pickle
import traceback
import subprocess

# Import third-part models
import requests
from selenium import webdriver
import selenium.common.exceptions

# Import custom models
import tbdmConfig
import tbdmFilter
from tbdmSetting import tbdmDatabase
from tbdmLogging import tbdmLogger
from tbdmSlack import tbdmSlack
import tbdmLogPoster

#----------model import----------


#----------global variables----------

tbdmDb = tbdmDatabase()
worklog = tbdmLogger("worker", loglevel = 30).log # logging.DEBUG - 10, increase 10 for every level
slacker = tbdmSlack()


ANTISPDR_TIME = 150 # Penalty time for being caught by Tmall Anti-spider
PENALIZE_TIME = 10801 # 3h penalty time and 1s for fail mark
task_keylist = ["juID", "itemID", "score", "status", "urlType", "fail"]
url_arch = ["https://detail.ju.taobao.com/home.htm?id=",
            "https://item.taobao.com/item.htm?id=",
            "https://detail.tmall.hk/hk/item.htm?id=",
            "https://chaoshi.detail.tmall.com/item.htm?id=",
            "https://detail.yao.95095.com/item.htm?id="]

#----------global variables----------


#----------class definition----------

#----------class definition----------


#----------function definition----------

class Worker():
    firefox_driver = webdriver.Firefox()
    redisCli = tbdmDb.tbdmRedis(addrOwner = 'xhuang', auth = True)

    def save_gecko_page(self, filename, filter_flag = True):
        try:
            with open(filename, 'w+', encoding = "utf-8") as f:
                f.write(self.firefox_driver.page_source)
            if (filter_flag):
                tbdmFilter.filter_html(filename)
        except Exception as _Eall:
            worklog.error("Failed to save page: " + filename + " , said: " + str(_Eall))

    def task_locker(self, tasks = None, filename = "tbdmPipelock.lock"):
        if (tasks == None):
            try:
                os.remove(filename)
            except Exception as _Eall:
                worklog.error("Locker Error:" + str(_Eall))
        else:
            with open(filename, "ab+") as f:
                pickle.dump(tasks, f, 0)

    def task_back2redis(self, taskdicts):
        for task in taskdicts:
            if (task['status'] > 0 and task['score'] == 0):
                task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
        tasks = self.task_dicts2strs(taskdicts)
        with self.redisCli.pipeline() as redisp:
            for task in tasks:
                redisp.zadd('juList', int(task.split('/')[2]), task)
            try:
                redisp.execute()
            except Exception as _Eall:
                worklog.error("Feedback to Redis failed." + str(_Eall))
                slacker.post_message("Feedback to Redis failed, task info dumped to fbRedis.lock .")
                self.task_locker(self.task_dicts2strs(taskdicts), "fbRedis.lock")
                return None
            else:
                self.task_locker(None)
                with open('toRedis.log','a+', encoding = "utf-8") as f:
                    f.write(str(taskdicts) + "\n")
                return 0

    def task_min_score(self, taskdicts):
        scores = []
        for task in taskdicts:
            scores.append(task['score'])
        return min(scores)

    def task_dicts2strs(self, taskdicts):
        """
        @author: X.Huang
        """
        taskstrs = []
        for task in taskdicts:
            try:
                taskstr = ''
                for i in range(0, len(task_keylist)):
                    taskstr += str(task[task_keylist[i]]) + '/'
            except Exception as _Eall:
                worklog.error('Invalid task dict: ' + str(task))
            else:
                taskstrs.append(taskstr)
        return taskstrs

    def task_strs2dicts(self, tasks):
        taskdicts = []
        for task in tasks:
            try:
                task = task.decode().split('/')
            except AttributeError as _Eattr:
                worklog.error("Task from Redis not properly encoded, trying without decode: " + str(task))
                task = task.split('/')
            except Exception as _Eall:
                worklog.error('Invalid task string: ' + str(task))
            try:
                taskdicts.append({'juID' : str(task[0]),
                                  'itemID' : str(task[1]),
                                  'score' : int(task[2]),
                                  'status' : int(task[3]),
                                  'urlType' : int(task[4]),
                                  'fail' : int(task[5])
                                })
            except Exception as _Eall:
                worklog.error('Invalid task: ' + str(task))
        return taskdicts
           
    def item_indicate(self, task, url, datestr):
        """
        @author: P.Liu X.Huang L.Xuezhang
        """
        try:
            content = self.firefox_driver.page_source
            if (("login" in self.firefox_driver.current_url) or 
                ("anti" in self.firefox_driver.current_url)):
                    # Failure situation
                    task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
                    task['fail'] += 1
                    worklog.error('Redirected to login page: ' + task['itemID'] + ','+task['juID'] + ',' + str(url) + ',' + 
                                    str(task['score']) + "\n")
                    slacker.post_message('Oops! Pan said that I must tell you I have requseted a login page!')
                    tbdmLogPoster.post_log('notification', tbdmConfig.WHO_IAM + 'Oops! Pan said that I must tell you I have requseted a login page!')
                    self.firefox_driver.delete_all_cookies()
                    time.sleep(tbdmConfig.SLEEP_TIME + ANTISPDR_TIME)
                    return 0
            elif (re.findall("很抱歉，您查看的宝贝不存在，可能已下架或者被转移", content) or re.findall("很抱歉，您查看的商品找不到了",content)):
                task['fail'] += 9
                return 0
            if ('tmall.hk' in self.firefox_driver.current_url):
                task['urlType'] = 2
            elif ('chaoshi.detail.tmall.com' in self.firefox_driver.current_url):
                task['urlType'] = 3
            elif ('yao.95095.com' in self.firefox_driver.current_url):
                task['urlType'] = 4
            else:
                task['urlType'] = 1 
            if (task['status'] > 2):
                task['status'] += 1
                if (task['score'] > 0):
                    task['score'] += 86400 # Scrape on next day
                else:
                    task['score'] = int(time.time() / 10) * 10 + 86400
            nfilename = datestr + '/success/' + task['itemID'] + '-' + str(int(time.time())) + '.html'
            self.save_gecko_page(nfilename)
            with open(datestr + '/success.log','a', encoding = "utf-8") as f:
                f.write(task['itemID'] + ',' + str(task['status']) + ',' + str(url) + ',' + str(task['score']) + "\n")
            return 1
        except Exception:
            task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
            task['fail'] += 1
            nfilename = datestr + '/error/' + task['itemID'] + '-' + task['juID'] + '-' + str(int(time.time()))  + '.html'
            self.save_gecko_page(nfilename)
            worklog.error('Fetch-parsing Error:' + task['itemID'] + ',' + str(url) + ',' + str(task['score']) + "\n")
            return 0

    def juDetail_indicate(self, task, datestr):
        try:
            content = self.firefox_driver.page_source
            # item_source = re.findall('<a target="_blank" href="//(.*)tracelog=jubuybigpic"', content)[0].replace("&amp;", "&")            
            # if ('tmall.hk' in item_source):
            #     task['urlType'] = 2
            # elif ('chaoshi.detail.tmall.com' in item_source):
            #     task['urlType'] = 3
            # elif ('yao.95095.com' in item_source):
            #     task['urlType'] = 4
            # else:
            #     task['urlType'] = 1
            if (re.findall('infotext J_Infotext', content) or re.findall('卖光', content)):
                if (task['status'] < 3):
                    task['status'] = 3
            else:
                mix_time = re.findall('data-targettime="([0-9]{13})"', content)
                if (re.findall('buyaction J_JuSMSRemind', content)):
                    task['status'] = 1
                    task['score'] = int(mix_time[0]) // 1000
                elif re.findall('buyaction J_BuySubmit', content):
                    task['status'] = 2
                    task['score'] = int(mix_time[0]) // 1000
                
                else:
                    worklog.error("juStatus-parsing error: " + str(_Eall) + " on task:" + str(task))
                    print(traceback.format_exc())
                    task['fail'] += 1
                    task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
                    nfilename = datestr + '/error/juDetail-' + task['itemID'] + '-' + task['juID'] + '-' + str(int(time.time()))  + '.html'
                    self.save_gecko_page(nfilename, False)
                    return False
            nfilename = datestr + '/success/juDetail-' + task['itemID'] + '-' + task['juID'] + '-' + str(int(time.time()))  + '.html'
            self.save_gecko_page(nfilename, False)
            return True
        except Exception as _Eall:
            print(traceback.format_exc())
            task['fail'] += 1
            task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
            worklog.error("Time-parsing error: " + str(_Eall) + " on task:" + str(task)) 
            nfilename = datestr + '/error/juDetail-' + task['itemID'] + '-' + task['juID'] + '-' + str(int(time.time()))  + '.html'
            self.save_gecko_page(nfilename, False)
            return False

    def juDetail_request(self, url, task, datestr):
        try:
            self.firefox_driver.get(url)
            if (("login" in self.firefox_driver.current_url) or 
                ("anti" in self.firefox_driver.current_url)):
                task['fail'] += 1
                task['score'] += int(time.time() / 10) * 10 + PENALIZE_TIME
                worklog.critical("Redirected to login page: " + str(_Eall) + " on task:" + str(task))
                return False
            elif(self.firefox_driver.current_url == "https://ju.taobao.com/"):
                task['fail'] += 9 #ju canceled
                return False
            else:
                return self.juDetail_indicate(task, datestr)

        except selenium.common.exceptions.TimeoutException:
            task['fail'] +=1
            task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
            worklog.critical("Request ju " + task['itemID'] + "timeout!")
            slacker.post_message('Master, I have trouble when requesting a page(Timeout).You may check out your network:)')
            #tbdmLogPoster.post_log('notification', tbdmConfig.WHO_IAM + 'Master, I have trouble when requesting a page(Timeout).You may check out your network:)')
            return False
        except KeyboardInterrupt:
            pass

    def request_page(self, taskdicts):
        success_cnt = 0
        total_cnt = len(taskdicts)
        datestr = time.strftime("%Y%m%d", time.localtime())
        self.firefox_driver.set_page_load_timeout(tbdmConfig.PAGE_LOAD_TIMEOUT)
        
        if not os.path.isdir(datestr):
            os.mkdir(datestr)
        if not os.path.isdir(datestr + '/error'):
            os.mkdir(datestr + '/error')
        if not os.path.isdir(datestr + '/success'):
            os.mkdir(datestr + '/success')

        try:
            for task in taskdicts:
                if (task['score'] > time.time()):
                    total_cnt -= 1
                    continue;
                if (task['fail'] > 8):
                    worklog.error("Too many failures, abandon task: " + str(task))
                    slacker.post_message("Task " + str(task) + " was abandoned for failures.", channel = "worker")
                    with open(datestr + "/abandoned_task.log", "a+", encoding = "utf-8") as f:
                        f.write(str(task))
                    taskdicts.remove(task)
                    continue;
                if (task['status'] > 15):
                    worklog.info("Track of " + str(task) + " finished. Hooray!")
                    slacker.post_message("Track of " + str(task) + " finished. Hooray!", channel = "worker")
                    with open(datestr +"/finished_task.log", "a+", encoding = "utf-8") as f:
                        f.write(str(task))
                    taskdicts.remove(task)
                    continue
                if (task['urlType'] > 0 and task['urlType'] < 5):
                    reqseq = task['urlType']
                else:
                    reqseq = 1
                if (task['status'] < 3):
                    if (not self.juDetail_request(url_arch[0] + task['juID'] + "&item_id=" + task['itemID'], task, datestr)):
                        time.sleep(tbdmConfig.SLEEP_TIME)
                        continue
                    time.sleep(tbdmConfig.SLEEP_TIME)
                try:
                    self.firefox_driver.get(url_arch[reqseq] + task['itemID'])
                    time.sleep(tbdmConfig.SLEEP_TIME)
                    success_cnt += self.item_indicate(task, reqseq + 1, datestr)
                except selenium.common.exceptions.TimeoutException:
                    task['fail'] +=1
                    task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
                    worklog.critical("Request" + task['itemID'] + "timeout!")
                    slacker.post_message('Master, I have trouble when requesting a page(Timeout).You may check out your network.')
                    tbdmLogPoster.post_log('notification', tbdmConfig.WHO_IAM + 'Master, I have trouble when requesting a page(Timeout).You may check out your network.')
                    continue
        except KeyboardInterrupt:
            pass
        except Exception as _Eall:
            time.sleep(tbdmConfig.SLEEP_TIME)
            worklog.critical('Oops! Something went wrong during page requesting.' + str(_Eall) +'\n')
            task['score'] = int(time.time() / 10) * 10 + PENALIZE_TIME
            task['fail'] += 1
        finally:
            self.task_back2redis(taskdicts)
            return (success_cnt, total_cnt)

#----------function definition----------


#----------main function----------

if __name__ == '__main__':
    print('Import me pls, meow.')

#----------main function----------
