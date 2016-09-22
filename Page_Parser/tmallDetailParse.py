# !/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')  

import json
import re
import time
from bs4 import BeautifulSoup

def reportTmallParseResult(shopRate,shopName,shopURL,shopAge,shopArea,itemName,itemDesc,attrList,orginPrice,promoPrice,imageURL,indInfo,inJu,colleNum):
    repo = {
    'parseTime':time.time(),
    'shopInfo':{
    'shopName':shopName,
    'shopURL':shopURL,
    'shopArea':shopArea,
    'shopAge':shopAge,
    'shopRate':shopRate
    },
    'itemInfo':{
    'itemName':itemName,
    'itemDesc':itemDesc,
    'itemAttr':attrList,
    'originalPrice':orginPrice,
    'promoPrice':promoPrice,
    'indInfo':indInfo,
    'images':imageURL,
    'colleNum':colleNum
    },
    'juInfo':inJu
    }
    print json.dumps(repo, ensure_ascii=False)

def tmallDetailParse(content):
    body = BeautifulSoup(content,'html.parser',from_encoding='GB2312').body
    shopInfo = body.find('div',attrs={'id':'shopExtra'})
    shopRate = []
    rateArea = BeautifulSoup(shopInfo.find('textarea').get_text(),'html.parser',from_encoding='GB2312')
    for rates in rateArea.find_all('em',attrs={'class':'count'}):
        shopRate.append(rates['title'])
    for ratesComp in rateArea.find_all('span',attrs={'class':'rateinfo'}):
        try:
            indicator = str(ratesComp.em['class'])
            if 'lower' in indicator:
                indicator = '-'
        except KeyError,e:
            indicator = ''
        shopRate.append(indicator + ratesComp.em.get_text())
    shopName = shopInfo.find('a',attrs={'class':'slogo-shopname'}).get_text()
    shopURL = shopInfo.find('a',attrs={'class':'slogo-shopname'})['href']
    shopAge = rateArea.find('span',attrs={'class':'tm-shop-age-num'}).get_text()
    shopArea = rateArea.find('li',attrs={'class':'locus'}).div.get_text().strip()
    itemBox = body.find('div',attrs={'id':'content'})
    itemInfo = itemBox.find('div',attrs={'class':'tb-detail-hd'})
    itemName = itemInfo.h1.get_text().strip()
    itemDesc = itemInfo.p.get_text().strip()
    orginPrice = itemBox.find('dl',attrs={'class':'tm-price-panel'}).span.get_text()
    promoPrice = itemBox.find('div',attrs={'class':'tm-promo-price'}).span.get_text()
    indInfo = itemBox.find('ul',attrs={'class':'tm-ind-panel'}).get_text().strip().split('\n')
    colleNum = re.findall(r'\d+',itemBox.find('span',attrs={'id':'J_CollectCount'}).get_text())
    attrList = []
    imageURL = []
    for li in itemBox.find('ul',attrs={'id':'J_AttrUL'}).find_all('li'):
        attrList.append(li.get_text())
    for img in body.find('div',attrs={'class':'tb-gallery'}).find_all('img'):
        imageURL.append(img['src'])
    try:
        inJu = itemBox.find('a',attrs={'class':'linkJu'}).parent.strong.get_text()
    except:
        inJu = 'Parse juTime Error'
    reportTmallParseResult(shopRate,shopName,shopURL,shopAge,shopArea,itemName,itemDesc,attrList,orginPrice,promoPrice,imageURL,indInfo,inJu,colleNum)

if __name__ == '__main__':
    tmallDetailParse(open(raw_input('Filepath: '),'r').read())
