def str_to_time(str1, str2):
	now_time = int(str(time.time())[0:10])
	if(str1.find('日') == '-1'):
		if(str2.find('开始') == '-1'):

		else:
		
	else:
		str1 = str1.replace('月', '-')
		str1 = str1.replace('日', '')
		str1 = time.strftime("%Y", time.localtime()) + '-' + str1 + ':00'
		return int(time.mktime(time.strptime(str1, '%Y-%m-%d %H:%M:%S')))
