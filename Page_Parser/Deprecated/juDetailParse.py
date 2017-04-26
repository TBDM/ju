# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  

import json
import re

from bs4 import BeautifulSoup
def reportJuParseResult(startTime,biztag,description,image,sellerName,sellerURL,sellerRate,pageTitle,item,itemId,juId,itemPrice,originalPrice):
    repo = {
    'pageTitle' : pageTitle,
    'juId' : juId,
    'startTime' : startTime,
    'seller' : {'name' : sellerName,
    'url' : sellerURL,
    'rate' : sellerRate},
    'item' : {'name' : item,
    'id' : itemId,
    'imageURL' : image,
    'originalPrice' : originalPrice,
    'price' : itemPrice,
    'biztag' : biztag,
    'description' : description
    }
    }
    print json.dumps(repo, ensure_ascii=False)

def juDetailParse(content):
    body = BeautifulSoup(content,'html.parser',from_encoding='GB2312').body
    imgBox = body.find('img',attrs={"data-primary":True})
    infoItem = body.find('a',attrs={'data-itempic':True})
    catalogue = body.find('div',attrs={'class':"header clearfix"}).find_all('li')[-1].get_text()
    sellerInfo = body.find('div',attrs={'class':'widget-box seller-info'})
    startTime = body.find('div',attrs={'class':"ju-clock J_juItemTimer"})['data-targettime']
    biztag = []
    description = []
    image = []
    sellerRate = []
    for label in body.find('div',attrs={"class":"biztag "}).find_all('label'):
        biztag.append(label.get_text())
    for li in body.find('div',attrs={"class":"description"}).find_all('li'):
        description.append(li.get_text())
    image.append(imgBox['data-normal'])
    image.append(imgBox['data-big'])
    image.append(imgBox['src'])
    image.append(infoItem['data-itempic'])
    pageTitle = body.find('h2',attrs={'class':'title'}).get_text().replace('\n','').strip()
    item = infoItem['data-itemname']
    originalPrice = infoItem['data-originalprice']
    itemPrice = infoItem['data-itemprice']
    itemId = infoItem['data-itemid']
    juId = infoItem['data-juid']
    sellerName = sellerInfo.find('span')['data-nick']
    sellerURL = sellerInfo.find('a')['href']
    for rt in sellerInfo.find('table').find_all('td'):
        sellerRate.append(rt.get_text())
    reportJuParseResult(startTime,biztag,description,image,sellerName,sellerURL,sellerRate,pageTitle,item,itemId,juId,itemPrice,originalPrice)

if __name__ == '__main__':
    juDetailParse(open(raw_input('Filepath: '),'r').read())
