# -*- coding:utf-8 -*- 


"""
跌幅较大的股票筛选器 
Created on 2015/08/05
@author: Rosen Lee
@group : 
@contact: rosenlove@qq.com
"""
import pandas as pd
from pandas.compat import StringIO
import numpy as np
import time
import re
import lxml.html
from lxml import etree
import json
#from tushare_src.stock import billboard as bd
import time
import sys
import basicData

try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

curdate=time.strftime('%Y-%m-%d',time.localtime(time.time()))

if len(sys.argv) > 1:
	print sys.argv[1]
	curdate=sys.argv[1]
else:
	print "请输入参数！"
	#当前时间
	
	



url = "http://stock.jrj.com.cn/action/lhb/getYybSbList.jspa?vname=jryyblhb1&sbDay=1d&date="+curdate+"&page=1&psize=200&order=desc&sort=ttimes&_dc=1441160193229"

print url
request = Request(url)
text = urlopen(request, timeout=10).read()
#print text.decode('utf-8').encode('gbk')

#text = text.decode('GBK', 'ignore')
#获得JSON数据
#{"summary":{"datetime":"2015-09-03 23:08:12","total":376},"column":{"branch_code":0,"branch_name":1,"enddate":2,"bvalue":3,"svalue":4,"tvalue":5,"ttimes":6,"activetimes":7}, 
#"data":[["200077791","华泰证券股份有限公司广州天河东路证券营业部","","11320.9221","400.3927","11721.3148","5",""],["200388021","中国中投证券有限责任公司无锡清扬路证券营业部","","6725.8300","1940.1100","8665.9400","5",""],["200665359","国金证券股份有限公司上海奉贤区金碧路证券营业部","","2666.0599","2595.9524","5262.0123","5",""]]};
js = json.loads(text[14:-1].decode('utf-8'))
#获得到列表数据，类型为list
jdata = js['data']
#上榜营业部总数量
jtotal = js['summary']['total']
print  js['summary']['datetime'], jtotal
#列名
jcolumn = js['column']
filename=curdate[:10]+".csv"
print filename
#print jcolumn
csvfile=open(filename, "w")
corecsvfile=open("core"+filename, "w")

terminate = False
#输出列表
for elem in jdata:
	if basicData.isInCoreYYBU(elem[1]):
		terminate = True
		#print elem
		#for  e in elem:	
			#print e.encode('utf-8', 'ignore'),",",
			#print "\n"
	for  e in elem:		
		print >> csvfile,  e.encode('utf-8', 'ignore'),",",
		if terminate:
			print >>corecsvfile, e.encode('utf-8', 'ignore'),",",
	print >> csvfile, "\n"

	if terminate:
		print >> corecsvfile, "\n"
	terminate = False

#print >> csvfile, jdata
csvfile.close()
corecsvfile.close()
#print jdata[1][1]

















