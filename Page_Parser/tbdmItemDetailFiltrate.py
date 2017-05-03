#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Filtrate data from Ju detail pages.

########################################
#               WARNING                #
########################################
# Your HTML files must be list like this:
#   root/         
#   ...
#       tbdm/
#       ...
#           file/
#           ...
#               20170526/
#                   success/
#                   error/
#                   success.log
#               20170525/
#               20170524/
#               20170523/
#               ...
# 
# 
# Set the global variable fileLocation 
# as '/root/tbdm/file/'
########################################
#               WARNING                #
########################################

#----------model import----------

import os
from lxml import etree
import re

#----------model import----------


#----------global variables----------

fileLocation = '/data/TBDMdocs/'
juDetailXpath = {
    '0': {
        'title': {
            'option': False, 
            'xpath': ['//h3[@class="tb-main-title"]/text()'], 
            'only': [True]
        }
    },
    '1': {
        'title': {
            'option': False, 
            'xpath': ['//h3[@class="tb-main-title"]/text()'], 
            'only': [True]
        }, 
        'head_picture': {
            'option': False, 
            'xpath': ['//img[@id="J_ImgBooth"]/@src'], 
            'only': [True]
        }, 
        'all_picture': {
            'option': False, 
            'xpath': ['//ul[@id="J_UlThumb"]/li/div/a/img/@src'], 
            'only': [False]
        }, 
        
    },
    '2': {
        'seller_rate_str': {
            'option': False, 
            'xpath': ['//textarea[@class="ks-datalazyload"]/text()'], 
            'only': [True]
        }, 
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
        'head_picture': {
            'option': False, 
            'xpath': ['//img[@id="J_ImgBooth"]/@src'], 
            'only': [True]
        }, 
        'all_picture': {
            'option': False, 
            'xpath': ['//ul[@id="J_UlThumb"]/li/a/img/@src'], 
            'only': [False]
        }, 
        'collect_number': {
            'option': False, 
            'xpath': ['//span[@id="J_CollectCount"]/text()'], 
            'only': [True]
        }, 
        'privilege': {
            'option': True,
            'xpath': ['//div[@class="tb-detail-hd"]/p/text()'], 
            'only': [True]
        },
        'sell_point': {
            'option': True,
            'xpath': ['//div[@class="tb-detail-hd"]/h4[@class="tb-detail-sellpoint"]/text()'], 
            'only': [True]
        },
        'origin_price': {
            'option': True, 
            'xpath': ['//dl[@id="J_StrPriceModBox"]/dd/span[@class="tm-price"]/text()', '//dl[@class="tm-tagPrice-panel"]/dd/span[@class="tm-price"]/text()'],
            'only': [True, True]
        }, 
        'tmall_price' : {
            'option': True, 
            'xpath': ['//dl[@id="J_PromoPrice"]/dd/div/span[@class="tm-price"]/text()'],
            'only': [True]
        },
        'tmall_price_deposit' : {
            'option': True, 
            'xpath': ['//dl[@class="tm-dj-panel"]/dd/span[@class="tb-wrTuan-deposit"]/text()'],
            'only': [True]
        },
        'tmall_price_reason' : {
            'option': True, 
            'xpath': ['//dl[@id="J_PromoPrice"]/dd/div/em[2]/text()', '//dl[@id="J_PromoPrice"]/dd/div/img/@src'],
            'only': [True, True]
        },
        'tmall_price_promotion' : {
            'option': True, 
            'xpath': ['//dl[@class="tm-shopPromo-panel"]/div/dd/text()'],
            'only': [True]
        },
        'sale_number' : {
            'option': False, 
            'xpath': ['//ul[@class="tm-ind-panel"]/li[1]/div/span[@class="tm-count"]/text()', '//div[@id="J_WrtAmount"]/span/em/text()'],
            'only': [True, True]
        },
        'review_number' : {
            'option': False, 
            'xpath': ['//ul[@class="tm-ind-panel"]/li[2]/div/span[@class="tm-count"]/text()'],
            'only': [True]
        },
        'tmall_point' : {
            'option': False, 
            'xpath': ['//ul[@class="tm-ind-panel"]/li[3]/div/a/span[@class="tm-count"]/text()'],
            'only': [True]
        },
        'class_str' : {
            'option': False, 
            'xpath': ['//div[@class="tb-skin"]/div[@class="tb-sku"]'],
            'only': [True]
        },
        'promise' : {
            'option': False, 
            'xpath': ['//ul[@class="tb-serPromise"]/li/a/text()'],
            'only': [False]
        },
        'attribute' : {
            'option': True, 
            'xpath': ['//ul[@id="J_AttrUL"]/li/text()'],
            'only': [False]
        }

    },
    '3': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    }, 
    '4': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    },
    '5': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    },
    '6': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    },
    '7': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    },
    '8': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    },
    '9': {
        'title': {
            'option': False, 
            'xpath': ['//div[@class="tb-detail-hd"]/h1/a/text()', '//div[@class="tb-detail-hd"]/h1/text()'], 
            'only': [True, True]
        }, 
    }
}

#----------global variables----------


#----------function definition----------

def itemType(htmlStr):
    if(re.search('title="淘宝网"', htmlStr) or re.search('淘宝网</title>', htmlStr)):
        return '1'
    if(re.search('title="天猫Tmall.com"', htmlStr)):
        return '2'
    if(re.search('title="天猫超市-chaoshi.tmall.com"', htmlStr) or re.search('<title>【天猫超市】', htmlStr)):
        return '3'
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
    return '9'

def parseItemDetailPage(htmlStr, htmlName, htmlType):
    treeObj = etree.HTML(htmlStr)
    # Here we get a HTML tree so that we can use xpath to find the element we need.

    for info in juDetailXpath[htmlType]:
        # Find the information we need via the dict we declared.
        isMatched = False
        # Once we find the information, set the isMatched as True and then break out of the loop.
        for i in range(len(juDetailXpath[htmlType][info]['xpath'])):
            # Find a useful xpath to get the information we need.
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
        if(not(info in juDetailResult) and not(juDetailXpath[htmlType][info]['option'])):
            # The information we need but can not be found in juDetailResult
            # So there must be some errors.

            if(htmlType == '2'):
                if(len(treeObj.xpath('//strong[@class="sold-out-tit"]/text()')) == 1):
                    if(treeObj.xpath('//strong[@class="sold-out-tit"]/text()')[0] == '此商品已下架'):
                        print(htmlName)
                        print(info)
                        print(juDetailResult)
                        print(htmlType)
                        return -3

            # print the information for debuging.
            print(htmlName)
            print(info)
            print(resultList)
            print(juDetailResult)
            print(htmlType)
            print('\033[1;31mMatch Error\033[0m')
            return -1
    # Do not forget to set ju_id and item_id that are stored in the filename.
    juDetailResult['item_id'] = htmlName.split('-')[0]
    juDetailResult['item_type'] = itemType(htmlStr)

    # Here we have parsed all the useful data
    # What we need to do next is to clean the data
    
    # From:     \n title \n
    # To:       title
    juDetailResult['title'] = juDetailResult['title'].strip()

    if(htmlType == '2'):
        tempTree = etree.HTML(juDetailResult['seller_rate_str'].replace('em', 'em '))
        temp = [['','',''],['','',''],['','','']]
        for i in range(3):
            temp[i][0] = tempTree.xpath('//div[@class="shop-rate"]/ul/li[' + str(i + 1) + ']/a/em/@title')[0][:-1]
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
        del(i)
        del(temp)
        del(juDetailResult['seller_rate_str'])
        juDetailResult['seller_name'] = tempTree.xpath('//div[@class="extend"]/ul/li[1]/div/a/text()')
        juDetailResult['seller_age'] = tempTree.xpath('//div[@class="extend"]/ul/li[3]/div/span[@class="tm-shop-age-num"]/text()')
        juDetailResult['seller_location'] = tempTree.xpath('//div[@class="extend"]/ul/li[4]/div/text()')
        juDetailResult['seller_url'] = tempTree.xpath('//div[@class="other"]/a[@class="enter-shop"]/@href')
        del(tempTree)

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
        juDetailResult['class'] = classDict
        del(i)
        del(classDict)
        del(juDetailResult['class_str'])
        
        # From:     （collect_number人气）
        # To:       collect_number
        juDetailResult['collect_number'] = juDetailResult['collect_number'][1:-3]

        if('attribute' in juDetailResult):
            juDetailResult['attribute'] = '-QAQ-'.join(juDetailResult['attribute']).replace('\xa0', ' ').split('-QAQ-')



        if(not('origin_price' in juDetailResult) and not('tmall_price' in juDetailResult)):
            print(htmlName)
            print(juDetailResult)
            print(htmlType)
            print('\033[1;31mMatch Error\033[0m')
            return -2


    # # From:     background-image: url(head_picture_url);
    # # To:       head_picture_url
    # if(juDetailResult['head_picture'][0:16] == 'background-image'):
    #     juDetailResult['head_picture'] = juDetailResult['head_picture'][22:-2]

    # # From:     ms
    # # To:       s
    # if('start_time' in juDetailResult):
    #     juDetailResult['start_time'] = juDetailResult['start_time'][0:10]

    # # From:     \n ju_price \n
    # # To:       ju_price
    # juDetailResult['ju_price'] = juDetailResult['ju_price'].strip()
    
    # # From:     ¥origin_price
    # # To:       origin_price
    # if('origin_price' in juDetailResult):
    #     juDetailResult['origin_price'] = juDetailResult['origin_price'][1:]

    # # From:     ['rate ↑', 'rate -', 'rate ↓']
    # # To:       [['rate', '1'], ['rate', '0'], ['rate','-1']
    # for i in range(3):
    #     if(juDetailResult['seller_rate'][i][-1:] == '↑'):
    #         juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '1']
    #     if(juDetailResult['seller_rate'][i][-1:] == '-'):
    #         juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '0']
    #     if(juDetailResult['seller_rate'][i][-1:] == '↓'):
    #         juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '-1']

    return juDetailResult

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
    for date in os.listdir(fileLocation):
        # Filtrate the page day by day.
        if(os.path.isdir(fileLocation + date) and len(date) == 8 and re.match('^([0-9]{8})$', date)):
            # Only if the path is a direction and the folder name is like YYYYMMDD can it be parsed.
            for juPage in os.listdir(fileLocation + date + '/success/'):
                juDetailResult = dict()
                # the dict juDetailResult is used to store the content we parsed temporarily.
                if(len(juPage.split('-'))== 3 and juPage.split('-')[2] == 'filtered.html'):
                    # Item detail page will be named like ItemID-Timestrap-filtered.html
                    pageObj = open(fileLocation + date + '/success/' + juPage, 'r', encoding='UTF-8')
                    pageStr = pageObj.read()
                    if(itemType(pageStr) == '2'):
                        print(parseItemDetailPage(pageStr, juPage, itemType(pageStr)))
                else:
                    continue
