# -*- Python Ver: 3.6.0 *-
# -*- coding: utf-8 -*-
# 
from tbdmLogging import	tbdmLogger

import re
import os

filterlog = tbdmLogger('filterlog', loglevel = 30).log
patterns = [
		r"(\s{3,})", #blank
		r"(?i)(<SCRIPT)[\s\S]*?((</SCRIPT>)|(/>))", #script
		r"(?i)(<STYLE)[\s\S]*?((</STYLE>)|(/>))" #style
	]

def filter_html(filename):
	"""
	@author: Xuezhang.Liu
	"""
	if (filename == None):
		filterlog.error('Open File Error: filename is none.')
		return None
	else:
		#filter patterns
		try:
			rx = re.compile('|'.join(patterns))
			with open(filename, 'r', encoding = "utf-8") as f:
				content = f.read()
			content = rx.sub('', content)
			nfilename = filename[:-5] + '-filtered.html'
			with open(nfilename, 'w', encoding = "utf-8") as f2:
				f2.write(content)
			os.remove(filename)
		except Exception as _Eall:
			filterlog.error("Filter Error:" + str(_Eall))
			return None
		else:
			return nfilename

if __name__ == '__main__':
	print('import me plz...')
	# filter_html('20170324/success/43043016730-1490351218-filtered.html')