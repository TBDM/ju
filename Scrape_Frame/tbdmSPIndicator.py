#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file describes some special rules for items on
# Taobao events, which omits the start/end time during Ju-act.

#----------model import----------

import re
import time
import datetime

#----------model import----------


#----------global variables----------

#----------global variables----------


#----------class definition----------

def jiazhuang_festa_indicate(content, task):
    tag_search = re.search('<div class="logoPic logoPic_0" title="*([0-9])月([0-9])日', content)
    if(re.search('此商品参加活动，请提前收藏', content) or tag_search):
        begin_search = re.search('title="此商品([0-9])月([0-9])日', content)
        if(begin_search):
            try:
                datestr = '2017-' + begin_search.group(1) + '-' + begin_search.group(2)
                begin_time = int(time.mktime(datetime.datetime.strptime(datestr, "%Y-%m-%d").timetuple()))
                if(task['status'] == 0):
                    task['score'] = begin_time
                    task['status'] = 1
                    task['fail'] = 0
                    return True
            except Exception as _Eall:
                print("Failed to match Jiazhuang festival item " + task['itemID'])
                return False
    return False

def nvwang_festa_indicate(content, task):
    tag_search = re.search('<div class="logoPic logoPic_0" title="*([0-9])月([0-9])日([0-9])点', content)
    if(re.search('此商品参加活动，请提前收藏', content) or tag_search):
        begin_search = re.search('title="*([0-9])月([0-9])日([0-9])点', content)
        if(begin_search):
            try:
                datestr = '2017-' + begin_search.group(1) + '-' + begin_search.group(2) + '-' + begin_search.group(3)
                begin_time = int(time.mktime(datetime.datetime.strptime(datestr, "%Y-%m-%d-%H").timetuple()))
                if(task['status'] == 0):
                    task['score'] = begin_time
                    task['status'] = 1
                    task['fail'] = 0
                    return True
            except Exception as _Eall:
                print("Failed to match Nvwang festival item " + task['itemID'])
                return False
    return False
#----------class definition----------


#----------function definition----------

#----------function definition----------


#----------main function----------

#----------main function----------
