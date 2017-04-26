#!/usr/bin/env python
#Filtrate data from Ju detail pages.

#----------model import----------

import os
import lxml
from lxml import etree

#----------model import----------


#----------global variables----------

fileLocation = '/root/tbdm/file/'
juDetailXpath = dict()

#----------global variables----------


#----------xpath definition----------

juDetailXpath['title'] = dict()
juDetailXpath['title']['kind'] = 1
juDetailXpath['title']['option'] = False
juDetailXpath['title']['xpath'] = ['//h2[@class="title"]/text()']
juDetailXpath['title']['only'] = [True]

juDetailXpath['type'] = dict()
juDetailXpath['type']['kind'] = 2
juDetailXpath['type']['option'] = False
juDetailXpath['type']['xpath'] = ['//div[@class="header clearfix"]/ul/li/a/text()', '//div[@class="header clearfix"]/a/img/@src']
juDetailXpath['type']['only'] = [False, True]

juDetailXpath['head_picture'] = dict()
juDetailXpath['head_picture']['kind'] = 2
juDetailXpath['head_picture']['option'] = False
juDetailXpath['head_picture']['xpath'] = ['//div[@class="item-pic-wrap"]/img/@src', '//div[@class="J_zoom pic "]/@style']
juDetailXpath['head_picture']['only'] = [True, True]

juDetailXpath['all_picture'] = dict()
juDetailXpath['all_picture']['kind'] = 1
juDetailXpath['all_picture']['option'] = True
juDetailXpath['all_picture']['xpath'] = ['//ul[@class="thumbnails"]/li/img/@data-big']
juDetailXpath['all_picture']['only'] = [False]

juDetailXpath['privilege'] = dict()
juDetailXpath['privilege']['kind'] = 1
juDetailXpath['privilege']['option'] = False
juDetailXpath['privilege']['xpath'] = ['//div[@class="biztag "]/label/text()']
juDetailXpath['privilege']['only'] = [False]

juDetailXpath['description'] = dict()
juDetailXpath['description']['kind'] = 1
juDetailXpath['description']['option'] = False
juDetailXpath['description']['xpath'] = ['//div[@class="description"]/ul/li/text()']
juDetailXpath['description']['only'] = [False]

juDetailXpath['start_time'] = dict()
juDetailXpath['start_time']['kind'] = 1
juDetailXpath['start_time']['option'] = True
juDetailXpath['start_time']['xpath'] = ['//div[@class="ju-clock J_juItemTimer"]/@data-targettime']
juDetailXpath['start_time']['only'] = [True]

juDetailXpath['ju_price'] = dict()
juDetailXpath['ju_price']['kind'] = 1
juDetailXpath['ju_price']['option'] = False
juDetailXpath['ju_price']['xpath'] = ['//span[@class="extra currentPrice"]/span[@class="J_actPrice"]/text()']
juDetailXpath['ju_price']['only'] = [True]

juDetailXpath['origin_price'] = dict()
juDetailXpath['origin_price']['kind'] = 1
juDetailXpath['origin_price']['option'] = True
juDetailXpath['origin_price']['xpath'] = ['//del[@class="originPrice"]/text()']
juDetailXpath['origin_price']['only'] = [True]

juDetailXpath['sale'] = dict()
juDetailXpath['sale']['kind'] = 1
juDetailXpath['sale']['option'] = True
juDetailXpath['sale']['xpath'] = ['//span[@class="soldnum"]/em/text()']
juDetailXpath['sale']['only'] = [True]

juDetailXpath['seller_name'] = dict()
juDetailXpath['seller_name']['kind'] = 1
juDetailXpath['seller_name']['option'] = False
juDetailXpath['seller_name']['xpath'] = ['//div[@class="tit  J_sellerInfoTit"]/a/text()']
juDetailXpath['seller_name']['only'] = [True]

juDetailXpath['seller_url'] = dict()
juDetailXpath['seller_url']['kind'] = 1
juDetailXpath['seller_url']['option'] = False
juDetailXpath['seller_url']['xpath'] = ['//div[@class="tit  J_sellerInfoTit"]/a/@href']
juDetailXpath['seller_url']['only'] = [True]

juDetailXpath['seller_rate'] = dict()
juDetailXpath['seller_rate']['kind'] = 1
juDetailXpath['seller_rate']['option'] = False
juDetailXpath['seller_rate']['xpath'] = ['//div[@class="con"]/table/tbody/tr[2]/td/text()']
juDetailXpath['seller_rate']['only'] = [False]

juDetailXpath['seller_promise'] = dict()
juDetailXpath['seller_promise']['kind'] = 1
juDetailXpath['seller_promise']['option'] = False
juDetailXpath['seller_promise']['xpath'] = ['//div[@class="con"]/ul[@class="clearfix J_PromiseCon"]/li/a/span/text()']
juDetailXpath['seller_promise']['only'] = [False]

#----------xpath definition----------


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
						print(date)
						print(juPage)
						print('\033[1;31mMatch Error\033[0m')
				juDetailResult['ju_id'] = juPage.split('-')[1]
				juDetailResult['item_id'] = juPage.split('-')[2]
				if(juDetailResult['head_picture'][0:16] == 'background-image'):
					juDetailResult['head_picture'] = juDetailResult['head_picture'][22:-2]
				print(juDetailResult)
			else:
				continue














