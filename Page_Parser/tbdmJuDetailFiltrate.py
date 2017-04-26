#!/usr/bin/env python

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

fileLocation = '/root/tbdm/file/'
juDetailXpath = {
    'title': {
        'option': False, 
        'xpath': ['//h2[@class="title"]/text()'], 
        'only': [True]
    }, 
    'type': {
        'option': False, 
        'xpath': ['//div[@class="header clearfix"]/ul/li/a/text()', '//div[@class="header clearfix"]/a/img/@src'], 
        'only': [False, True]
    }, 
    'head_picture': {
        'option': False, 
        'xpath': ['//div[@class="item-pic-wrap"]/img/@src', '//div[@class="J_zoom pic "]/@style', '//div[@class="J_zoom pic"]/@style'], 
        'only': [True, True, True]
    }, 
    'all_picture': {
        'option': True, 
        'xpath': ['//ul[@class="thumbnails"]/li/img/@data-big'], 
        'only': [False]
    }, 
    'privilege': {
        'option': False, 
        'xpath': ['//div[@class="biztag"]/label/text()', '//div[@class="biztag "]/label/text()'], 
        'only': [False, False]
    }, 
    'description': {
        'option': False, 
        'xpath': ['//div[@class="description"]/ul/li/text()'], 
        'only': [False]
    }, 
    'start_time': {
        'option': True, 
        'xpath': ['//div[@class="ju-clock J_juItemTimer"]/@data-targettime'], 
        'only': [True]
    }, 
    'ju_price': {
        'option': False, 
        'xpath': ['//span[@class="extra currentPrice"]/span[@class="J_actPrice"]/text()'], 
        'only': [True]
    }, 
    'origin_price': {
        'option': True, 
        'xpath': ['//del[@class="originPrice"]/text()'], 
        'only': [True]
    }, 
    'sale': {
        'option': True, 
        'xpath': ['//span[@class="soldnum"]/em/text()'], 
        'only': [True]
    }, 
    'seller_name': {
        'option': False, 
        'xpath': ['//div[@class="tit  J_sellerInfoTit"]/a/text()'], 
        'only': [True]
    }, 
    'seller_url': {
        'option': False, 
        'xpath': ['//div[@class="tit  J_sellerInfoTit"]/a/@href'], 
        'only': [True]
    }, 
    'seller_rate': {
        'option': False, 
        'xpath': ['//div[@class="con"]/table/tbody/tr[2]/td/text()'], 
        'only': [False]
    }, 
    'seller_promise': {
        'option': False, 
        'xpath': ['//div[@class="con"]/ul[@class="clearfix J_PromiseCon"]/li/a/span/text()'], 
        'only': [False]
    }
}

#----------global variables----------


#----------function definition----------

def parseJuDetailPage(htmlStr, htmlName):
    treeObj = etree.HTML(htmlStr)
    # Here we get a HTML tree so that we can use xpath to find the element we need.

    for info in juDetailXpath:
        # Find the information we need via the dict we declared.
        isMatched = False
        # Once we find the information, set the isMatched as True and then break out of the loop.
        for i in range(len(juDetailXpath[info]['xpath'])):
            # Find a useful xpath to get the information we need.
            resultList = treeObj.xpath(juDetailXpath[info]['xpath'][i])
            # The if statements below are used to make sure we match the right element as we predicted.
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
            # The information we need but can not be found in juDetailResult
            # So there must be some errors.
            if(info == 'ju_price'):
                # when the price is not an integer xpath can not match the right price
                # so we need to use regular expression to get the price.
                
                ########################################
                #               WARNING                #
                ########################################
                # watch out for the error IndexError.

                juPriceRawStr = re.search('<span class="J_actPrice">([\S]+)</span>', htmlStr).group(0)
                juPriceStr = juPriceRawStr.replace('<i>', '').replace('</i>', '').replace('<span class="J_actPrice">', '').replace('</span>', '')
                juDetailResult['ju_price'] = juPriceStr
                continue

                ########################################
                #               WARNING                #
                ########################################
            
            # print the information for debuging.
            print(htmlName)
            print(info)
            print('\033[1;31mMatch Error\033[0m')
            return -1
    # Do not forget to set ju_id and item_id that are stored in the filename.
    juDetailResult['ju_id'] = htmlName.split('-')[1]
    juDetailResult['item_id'] = htmlName.split('-')[2]
    
    # Here we have parsed all the useful data
    # What we need to do next is to clean the data
    
    # From:     \n title \n
    # To:       title
    juDetailResult['title'] = juDetailResult['title'].strip()

    # From:     background-image: url(head_picture_url);
    # To:       head_picture_url
    if(juDetailResult['head_picture'][0:16] == 'background-image'):
        juDetailResult['head_picture'] = juDetailResult['head_picture'][22:-2]

    # From:     ms
    # To:       s
    if('start_time' in juDetailResult):
        juDetailResult['start_time'] = juDetailResult['start_time'][0:10]

    # From:     \n ju_price \n
    # To:       ju_price
    juDetailResult['ju_price'] = juDetailResult['ju_price'].strip()
    
    # From:     ¥origin_price
    # To:       origin_price
    if('origin_price' in juDetailResult):
        juDetailResult['origin_price'] = juDetailResult['origin_price'][1:]

    # From:     ['rate ↑', 'rate -', 'rate ↓']
    # To:       [['rate', '1'], ['rate', '0'], ['rate','-1']
    for i in range(3):
        if(juDetailResult['seller_rate'][i][-1:] == '↑'):
            juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '1']
        if(juDetailResult['seller_rate'][i][-1:] == '-'):
            juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '0']
        if(juDetailResult['seller_rate'][i][-1:] == '↓'):
            juDetailResult['seller_rate'][i] = [juDetailResult['seller_rate'][i][0:-2], '-1']
        

    return juDetailResult

#----------function definition----------


#----------main function----------

if __name__ == "__main__":
    for date in os.listdir(fileLocation):
        # Filtrate the page day by day.
        n = 0
        if(os.path.isdir(fileLocation + date) and len(date) == 8 and re.match('^([0-9]{8})$', date)):
            # Only if the path is a direction and the folder name is like YYYYMMDD can it be parsed.
            for juPage in os.listdir(fileLocation + date + '/success/'):
                n = n + 1
                juDetailResult = dict()
                # the dict juDetailResult is used to store the content we parsed temporarily.
                if(juPage[0:8] == 'juDetail'):
                    # Ju detail page will be named like juDetail-JuID-ItemID-Timestrap.html
                    pageObj = open(fileLocation + date + '/success/' + juPage, 'r', encoding='UTF-8')
                    pageStr = pageObj.read()
                    print(parseJuDetailPage(pageStr, juPage))
                else:
                    continue
                if(n == 10):
                    break
