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

juDetailXpath['head_picture'] = dict()
juDetailXpath['head_picture']['kind'] = 2
juDetailXpath['head_picture']['option'] = False
juDetailXpath['head_picture']['xpath'] = ['//div[@class="item-pic-wrap"]/img/@src', '//div[@class="J_zoom pic "]/@style']
juDetailXpath['head_picture']['only'] = [True, True]

juDetailXpath['picture'] = dict()
juDetailXpath['picture']['kind'] = 1
juDetailXpath['picture']['option'] = True
juDetailXpath['picture']['xpath'] = ['//ul[@class="thumbnails"]/li/img/@data-big']
juDetailXpath['picture']['only'] = [False]

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
								if(len(resultList) == 1):
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
				if(juDetailResult['head_picture'][0:16] == 'background-image'):
					juDetailResult['head_picture'] = juDetailResult['head_picture'][22:-2]
				print(juDetailResult)
			else:
				continue














