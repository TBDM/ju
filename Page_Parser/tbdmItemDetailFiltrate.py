#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Filtrate data from Item detail pages.

########################################
#               WARNING                #
########################################
# Your HTML files directory must be list like this:
#           dir/
#           ...
#               20170526/
#                   success/
#                   error/
#                   success.log
#               20170525/
#               20170524/
#               20170523/
#               ...
########################################
#               WARNING                #
########################################

#----------model import----------

import json
import os
import re
import sys
import time
import traceback

from lxml import etree

sys.path.append('../')

from Scaffold.tbdmLogging import tbdmLogger

# ----------model import----------

#----------global variables----------


parseLog = tbdmLogger('parse_item_error_log', loglevel = 20).log

#----------function definition----------

def getItemType(htmlStr):
    if(re.search('title="淘宝网"', htmlStr) or re.search('淘宝网</title>', htmlStr)):
        return '1'
        #魅力惠
    if(re.search('href="//meilihui.tmall.com/"', htmlStr)):
        return '9'
    if(re.search('title="天猫Tmall.com"', htmlStr)):
        return '2'
    if(re.search('title="天猫超市-chaoshi.tmall.com"', htmlStr) or re.search('<title>【天猫超市】', htmlStr)):
        return '3'
        #天猫国际官方直营
    if(re.search('<a class="sslogo" href="//jinkou.tmall.com"', htmlStr) or re.search('https://gw.alicdn.com/tps/TB1u4pXPXXXXXX4XpXXXXXXXXXX-908-116.png', htmlStr)):
        return '4'
    if(re.search('title="喵鲜生-全球健康好味道"', htmlStr)):
        return '5'
    if(re.search('title="天猫国际"', htmlStr) or re.search('//img.alicdn.com/tps/i4/TB1..d2JXXXXXajapXXqXA0IVXX-232-80.png', htmlStr)):
        return '6'
    if(re.search('title="天猫美妆-mei.tmall.com"', htmlStr) or re.search('//img.alicdn.com/tps/i1/TB1nEsdLXXXXXcYXFXXNyvXJXXX-83-32.png', htmlStr)):
        return '7'
    if(re.search('title="95095医药馆"', htmlStr) or re.search('//img.alicdn.com/tps/i3/T1Jaa0FQ4bXXcMw42c-148-34.png', htmlStr)):
        return '8'
    return '10'

def parseItemDetailPage(htmlStr, htmlName, htmlType, juDetailXpath):
    treeObj = etree.HTML(htmlStr)
    # Here we get a HTML tree so that we can use xpath to find the element we need.
    juDetailResult['error'] = list()
    for info in juDetailXpath[htmlType]:
        # Find the information we need via the dict we declared.
        isMatched = False
        # Once we find the information, set the isMatched as True and then break out of the loop.
        for i in range(len(juDetailXpath[htmlType][info]['xpath'])):
            # Find a useful xpath to get the information we need.
            try:
                resultList = treeObj.xpath(juDetailXpath[htmlType][info]['xpath'][i])
                # The if statements below are used to make sure we match the right element as we predicted.
                if(len(resultList) != 0):
                    if(juDetailXpath[htmlType][info]['only'][i]):
                        if(len(resultList) == 1 and resultList[0] != ''):
                            juDetailResult[info] = resultList[0]
                            isMatched = True
                    else:
                        juDetailResult[info] = resultList
                        isMatched = True
                if(isMatched):
                    break
            except Exception as _Eall:
                parseLog.error('parsing error' + str(_Eall)+'htmlType:' + htmlType + 'htmlName:' + htmlName + 'info:'+info)
        if(not(info in juDetailResult) and not(juDetailXpath[htmlType][info]['option'])):
            # The information we need but can not be found in juDetailResult
            # So there must be some errors.

               
            
            # add the information for debuging.
            juDetailResult['error'].append(info)
            
    # Do not forget to set ju_id and item_id that are stored in the filename.
    juDetailResult['item_id'] = htmlName.split('-')[0]
    # print(juDetailResult['item_id'])
    juDetailResult['timestamp'] = htmlName.split('-')[1]
    juDetailResult['item_type'] = htmlType
    # print(itemType(htmlStr))

    # Here we have parsed all the useful data
    # What we need to do next is to clean the data

    if(htmlType == '2' or htmlType == '6' or htmlType == '1'):
        try:
        # From:     \n title \n
        # To:       title
            if('title' in juDetailResult):
                juDetailResult['title'] = juDetailResult['title'].strip()
            
            if(len(treeObj.xpath('//strong[@class="sold-out-tit"]/text()')) == 1):
                if(treeObj.xpath('//strong[@class="sold-out-tit"]/text()')[0] == '此商品已下架'):
                    juDetailResult['error'].append('此商品已下架')
            
            if('seller_rate_str' in juDetailResult):
                if(htmlType != '1'):
                    tempTree = etree.HTML(juDetailResult['seller_rate_str'].replace('em', 'em '))
                    temp = [['','',''],['','',''],['','','']]
                    for i in range(3):
                        tmp = tempTree.xpath('//div[@class="shop-rate"]/ul/li[' + str(i + 1) + ']/a/em/@title')
                        if len(tmp) > 0:
                            temp[i][0] = tmp[0][:-1]
                            rate_class = tempTree.xpath('//div[@class="shop-rate"]/ul/li[' + str(i + 1) + ']/a/span/b/@class')
                            if(len(rate_class) == 0):
                                temp[i][1] = '1'
                            else:
                                if(rate_class[0] == 'fair'):
                                    temp[i][1] = '0'
                                if(rate_class[0] == 'lower'):
                                    temp[i][1] = '-1'
                            rate_percent = tempTree.xpath('//div[@class="shop-rate"]/ul/li[' + str(i + 1) + ']/a/span/em/text()')[0]
                            if(rate_percent[0:1] == '-'):
                                temp[i][2] = '0.00'
                            else:
                                temp[i][2] = rate_percent[:-1]
                            juDetailResult['seller_rate'] = temp
                        else:
                            pass
                    del(i)
                    del(temp)
                    del(juDetailResult['seller_rate_str'])
                    juDetailResult['seller_name'] = tempTree.xpath('//div[@class="extend"]/ul/li[1]/div/a/text()')
                    juDetailResult['seller_age'] = tempTree.xpath('//div[@class="extend"]/ul/li[3]/div/span[@class="tm-shop-age-num"]/text()')
                    juDetailResult['seller_location'] = tempTree.xpath('//div[@class="extend"]/ul/li[4]/div/text()')
                    juDetailResult['seller_url'] = tempTree.xpath('//div[@class="other"]/a[@class="enter-shop"]/@href')
                    del(tempTree)
                else:
                    tbShopRate=[]
                    tempTree = juDetailResult['seller_rate_str']
                    # print(tempTree)
                    if(tempTree.xpath('./a/img/@src')):
                        tbShopHeader = tempTree.xpath('./a/img/@src')
                    # print(tempTree.xpath('//div[@class="tb-shop-age-content"]'))
                    if(tempTree.xpath('//div[@class="tb-shop-age-content"]')):
                        tbShopAge = tempTree.xpath('//div[@class="tb-shop-age-content"]')[0]
                        tbShopAge = "".join(tbShopAge.xpath('string(.)').split())
                    else:
                        tbShopAge = ""
                    tbShopName = "".join(tempTree.xpath('//div[@class="tb-shop-name"]')[0].xpath('string(.)').split())
                    # tbShopRank = tempTree.xpath('//div[@class="tb-shop-rank tb-rank-cap"]/dl/dt/text()')[0].strip()
                    # tbShopRank = tbShopRank + str(len(tempTree.xpath('//div[@class="tb-shop-rank tb-rank-cap"]/dl/dd/a/i')))
                    tbShopSeller = "".join(tempTree.xpath('//div[@class="tb-shop-seller"]')[0].xpath('string(.)').split())
                    tbShopIcon = "".join(tempTree.xpath('//div[@class="tb-shop-icon"]')[0].xpath('string(.)').split())
                    tbShopRateEle = tempTree.xpath('//div[@class="tb-shop-rate"]/dl')
                    for i in range(len(tbShopRateEle)):
                        # print(tbShopRateEle[i].xpath('string(.)').split())
                        tbShopRate.append(tbShopRateEle[i].xpath('string(.)'))
                    juDetailResult['tb_shop_header'] = tbShopHeader 
                    if(tbShopAge != ''):
                        juDetailResult['tb_shop_age'] = tbShopAge
                    juDetailResult['tb_shop_name'] = tbShopName
                    # juDetailResult['tb_shop_rank'] = tbShopRank
                    juDetailResult['tb_shop_seller'] = tbShopSeller
                    juDetailResult['tb_shop_icon'] = tbShopIcon
                    juDetailResult['tb_shop_rate'] = tbShopRate
                    del(juDetailResult['seller_rate_str'])
                    del(tempTree)
        except Exception as _Eall:
            parseLog.error(str(_Eall))
        try:
            if('class_str' in juDetailResult):
                if(htmlType != '1' ):
                    classList = juDetailResult['class_str'].xpath('dl/dt/text()')
                    classDict = dict()
                    for i in range(len(classList)):
                        if(classList[i] == '数量'):
                            if(len(juDetailResult['class_str'].xpath('//em[@id="J_EmStock"]/text()')) == 1):
                                classDict['数量'] = juDetailResult['class_str'].xpath('//em[@id="J_EmStock"]/text()')[0]
                                continue
                        if(classList[i] == '服务'):
                            continue
                        if(classList[i] == '花呗分期'):
                            continue
                        class_style = list()
                        if(len(juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/@style')) != 0):
                            class_style_raw = juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/@style')
                            class_style = list()
                            for class_style_str in class_style_raw:
                                class_style.append(class_style_str.replace('background:url(', '').replace(') center no-repeat;', ''))
                            del(class_style_raw)
                        classDict[classList[i]] = [juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/span/text()'), class_style]
                        del(class_style)
                else:
                    classList = juDetailResult['class_str'].xpath('dl/dt/text()')
                    classDict = {}
                    for i in range(len(classList)):
                        if(classList[i] == '颜色分类'):
                            class_style = list()
                            if(len(juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/@style')) != 0):
                                class_style_raw = juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/@style')
                                class_style = list()
                                for class_style_str in class_style_raw:
                                    class_style.append(class_style_str.replace('background:url(', '').replace(') center no-repeat;', ''))
                                del(class_style_raw)
                            classDict[classList[i]] = [juDetailResult['class_str'].xpath('dl[' + str(i + 1) + ']/dd/ul/li/a/span/text()'), class_style]
                            del(class_style)
                        elif(classList[i] == '数量'):
                            classDict['数量'] = juDetailResult['class_str'].xpath('./dl[@class="tb-amount tb-clear"]//em')[0].xpath('string(.)')[1:-1]
                            # print(classDict['数量'])
                        else:
                            continue
                juDetailResult['class'] = classDict
                del(i)
                del(classDict)
                del(juDetailResult['class_str'])
        except Exception as _Eall:
            parseLog.error(str(_Eall))
        # From:     （collect_number人气）
        # To:       collect_number
        try:
            if('collect_number' in juDetailResult):
                if(htmlType != '1'):
                    juDetailResult['collect_number'] = juDetailResult['collect_number'][1:-3]
                else:
                    # From:     (collect_number)
                    # To:       collect_number
                    juDetailResult['collect_number'] = juDetailResult['collect_number'][2:-3]
                    # print(juDetailResult['collect_number'])

            if('attribute' in juDetailResult):
                if(htmlType != '1'):
                    juDetailResult['attribute'] = '-QAQ-'.join(juDetailResult['attribute']).replace('\xa0', ' ').split('-QAQ-')
                else:
                    # CCC Certificate strip
                    attrCCC = juDetailResult['attribute'][0].xpath('./li[1]')[0]
                    attrCCCStr = str(attrCCC.xpath('string(.)')).replace('\xa0',' ')
                    # print(attrCCCStr)
                    attrList = juDetailResult['attribute'][0].xpath('./li/text()')
                    attrList = '-QAQ-'.join(attrList).replace('\xa0', ' ').split('-QAQ-')[1:]
                    attrList.insert(0,attrCCCStr)
                    # print(attrList)
                    juDetailResult['attribute'] = attrList
                    del(attrList)
            if(not('origin_price' in juDetailResult) and not('tmall_price' in juDetailResult)):
                juDetailResult['error'].append('no price')
        except Exception as _Eall:
            parseLog.error(str(_Eall))
    return juDetailResult

def handleItem(resultList, failedDict, pageStr, juPage, itemType, juDetailXpath):
    item = parseItemDetailPage(pageStr, juPage, itemType, juDetailXpath)
    if (item != None):
        resultList.append(item)
        print('Item ' + item['item_id'] + ' parsed.')
        return 1
    else:
        failedDict[itemType].append(juPage)
        parseLog.error('Parsing error: ' + juPage + 'htmlType: ' + str(itemType))
        return 0

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
    # fileName = 'test.json'
    # fileLocation = 'D:\\test\\'
    if(not len(sys.argv[2:])):
        print('Usage: '+sys.argv[0]+' [origin file] [outfile]')
        sys.exit(0)
    fileLocation = sys.argv[1]
    fileName = sys.argv[2]
    with open('item_xpath.json','r',encoding='utf-8') as f:
        juDetailXpath = json.load(f)
    item_num = 0
    total = 0
    result = []
    failed = {str(i):[] for i in range(0,10)}
    with open(fileName, 'w+', encoding='utf-8') as f:
        for date in os.listdir(fileLocation):
            print(date)
            # Filtrate the page day by day.
            if(os.path.isdir(fileLocation + date) and len(date) == 8 and re.match('^([0-9]{8})$', date)):
                # Only if the path is a direction and the folder name is like YYYYMMDD can it be parsed.
                for juPage in os.listdir(fileLocation + date + '/success/'):
                    juDetailResult = dict()
                    if(len(juPage.split('-'))== 3 and juPage.split('-')[2] == 'filtered.html'):
                        # Item detail page will be named like ItemID-Timestrap-filtered.html
                        pageObj = open(fileLocation + date + '/success/' + juPage, 'r', encoding='UTF-8')
                        pageStr = pageObj.read()
                        itemType = getItemType(pageStr)
                        if(itemType in('2','6','1')):
                            item_num = item_num + handleItem(result,failed,pageStr, juPage,itemType,juDetailXpath)
                        else:
                            pass
                        if(len(result) > 1000):
                            try:
                                for item in result:
                                    f.write(json.dumps(item,ensure_ascii=False)+'\n')
                            except Exception as _Eall:
                                traceback.print_exc()
                            del(result)
                            result = []
                        total = total + 1
                    else:
                        continue
        try:
            for item in result:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
        except Exception as _Eall:
            traceback.print_exc()
    print('###############################')
    print('All work done in ' + fileLocation + '.' + time.strftime('%Y-%m-%d-%H:%M', time.localtime(time.time())))
    print('There are ' + str(total - item_num) + '/' + str(total) + ' items failed:(')
    parseLog.info('###############################')
    parseLog.info('All work done in '+ fileLocation +'.')
    parseLog.info('There are '+str(total-item_num)+'/'+str(total)+' items failed:(')
    parseLog.info('###############################')
    for (k,y) in failed.items():
        if(len(y) != 0):
            print('HTML Type: ' + str(k))
            parseLog.error('HTML Type: ' + str(k))
            for item in y:
                print('info: ' + item)
                parseLog.error('info: '+ item)
    parseLog.info('###############################')
    print('###############################')
