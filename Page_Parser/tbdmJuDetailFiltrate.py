#!/usr/bin/env python
#Filtrate data from Ju detail pages.

#----------model import----------

import os
from lxml import etree
import re

#----------model import----------


#----------global variables----------

fileLocation = '/root/tbdm/file/'
juDetailXpath = {
    'title': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//h2[@class="title"]/text()'], 
        'only': [True]
    }, 
    'type': {
        'kind': 2, 
        'option': False, 
        'xpath': ['//div[@class="header clearfix"]/ul/li/a/text()', '//div[@class="header clearfix"]/a/img/@src'], 
        'only': [False, True]
    }, 
    'head_picture': {
        'kind': 3, 
        'option': False, 
        'xpath': ['//div[@class="item-pic-wrap"]/img/@src', '//div[@class="J_zoom pic "]/@style', '//div[@class="J_zoom pic"]/@style'], 
        'only': [True, True, True]
    }, 
    'all_picture': {
        'kind': 1, 
        'option': True, 
        'xpath': ['//ul[@class="thumbnails"]/li/img/@data-big'], 
        'only': [False]
    }, 
    'privilege': {
        'kind': 2, 
        'option': False, 
        'xpath': ['//div[@class="biztag"]/label/text()', '//div[@class="biztag "]/label/text()'], 
        'only': [False, False]
    }, 
    'description': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//div[@class="description"]/ul/li/text()'], 
        'only': [False]
    }, 
    'start_time': {
        'kind': 1, 
        'option': True, 
        'xpath': ['//div[@class="ju-clock J_juItemTimer"]/@data-targettime'], 
        'only': [True]
    }, 
    'ju_price': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//span[@class="extra currentPrice"]/span[@class="J_actPrice"]/text()'], 
        'only': [True]
    }, 
    'origin_price': {
        'kind': 1, 
        'option': True, 
        'xpath': ['//del[@class="originPrice"]/text()'], 
        'only': [True]
    }, 
    'sale': {
        'kind': 1, 
        'option': True, 
        'xpath': ['//span[@class="soldnum"]/em/text()'], 
        'only': [True]
    }, 
    'seller_name': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//div[@class="tit  J_sellerInfoTit"]/a/text()'], 
        'only': [True]
    }, 
    'seller_url': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//div[@class="tit  J_sellerInfoTit"]/a/@href'], 
        'only': [True]
    }, 
    'seller_rate': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//div[@class="con"]/table/tbody/tr[2]/td/text()'], 
        'only': [False]
    }, 
    'seller_promise': {
        'kind': 1, 
        'option': False, 
        'xpath': ['//div[@class="con"]/ul[@class="clearfix J_PromiseCon"]/li/a/span/text()'], 
        'only': [False]
    }
}

#----------global variables----------


#----------function definition----------



#----------function definition----------


#----------main function----------

if __name__ == "__main__":
    for date in os.listdir(fileLocation):
        #Filtrate the page day by day.
        for juPage in os.listdir(fileLocation + date + '/success/'):
            juDetailResult = dict()
            if(juPage[0:8] == 'juDetail'):
                pageObj = open(fileLocation + date + '/success/' + juPage, 'r', encoding='UTF-8')
                pageStr = pageObj.read()
                treeObj = etree.HTML(pageStr)
                
                for info in juDetailXpath:
                    isMatched = False
                    for i in range(juDetailXpath[info]['kind']):
                        resultList = treeObj.xpath(juDetailXpath[info]['xpath'][i])
                        if(len(resultList) != 0):
                            if(juDetailXpath[info]['only'][i]):
                                if(len(resultList) == 1 and resultList[0] != ''):
                                    juDetailResult[info] = resultList[0]
                                    isMatched = True
                            else:
                                juDetailResult[info] = resultList
                                isMatched = True
                        if(isMatched):
                            break
                    if(not(info in juDetailResult) and not(juDetailXpath[info]['option'])):
                        if(info == 'ju_price'):
                            juPriceRawStr = re.search('<span class="J_actPrice">([\S]+)</span>', pageStr).group(0)
                            juPriceRawStr.replace('<i>', '').replace('</i>', '')
                            juDetailResult['ju_price'] = juPriceRawStr
                            continue
                        print(date)
                        print(juPage)
                        print(info)
                        print('\033[1;31mMatch Error\033[0m')
                juDetailResult['ju_id'] = juPage.split('-')[1]
                juDetailResult['item_id'] = juPage.split('-')[2]
                if(juDetailResult['head_picture'][0:16] == 'background-image'):
                    juDetailResult['head_picture'] = juDetailResult['head_picture'][22:-2]
                print(juDetailResult)
            else:
                continue
