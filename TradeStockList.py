# -*- coding:utf-8 -*- 


"""

Created on 2015/10/23
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
import time
import sys
import random
import basicData


try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request


def getJsonText(url):
	time.sleep(random.randint(1, 9))
	request = Request(url)
	text = urlopen(request, timeout=10).read()
	return text


if len(sys.argv) < 2 :
	print "useage: "+sys.argv[0]+" stockcode  [date]"
	exit()
	
stockcode=sys.argv[1]
inListHistUrl="http://stock.jrj.com.cn/action/lhb/getTimeBystcode.jspa?stockcode="+stockcode
#[{"date":"20151021"},{"date":"20151020"},{"date":"20150901"},{"date":"20150828"},{"date":"20150827"},{"date":"20150821"},{"date":"20150819"},{"date":"20150818"},{"date":"20150814"},{"date":"20150811"},{"date":"20150806"}] 
inListHistData=getJsonText(inListHistUrl)
inListHistArray=eval(inListHistData[1:-3])
inListHistUrlArray=[]
for node in inListHistArray:	
	#itsdate=inListHistArray[0].values() #['20151023']
	itsdate=node.values() #['20151023']
	itsdatestr="".join(itsdate)
	itsdatefmt=itsdatestr[0:4]+"-"+itsdatestr[4:6]+"-"+itsdatestr[6:8]
	url = "http://stock.jrj.com.cn/share,"+stockcode+",lhb"+itsdatefmt+".shtml"
	#print url
	inListHistUrlArray.append(url)
	
print inListHistUrlArray
#exit()

#获得'http://stock.jrj.com.cn/share,000564,lhb2015-10-23.shtml' 包含的href的标签内容
#其实就应该只抓到http://summary.jrj.com.cn/lhb/jymx.shtml?yybcode=200058697,000564
#这种类型的连接，因为其他的都不是有对比的。如：
#http://summary.jrj.com.cn/lhb/yyb2015.shtml?yybcode=200058697

def getHrefs(histUrl):
	text=getJsonText(histUrl)
	#request = Request(url)
	#text = getJsonText(url)
	#print text.decode('utf-8').encode('gbk')

	html = lxml.html.parse(StringIO(text))

	#res = html.xpath('//div[@class=\"table-s1 mt\"]/table')
	#res2 = html.xpath('//div[@class=\"table-s1 mt\"]/table/')
	#res3 = html.xpath('//div[@class=\"table-s1 mt\"]/table/tr')
	#res4 = html.xpath('//div[@class=\"table-s1 mt\"]/table/tr/td/text()')
	#res5 = html.xpath('//div[@class=\"table-s1 mt\"]/table/tr/td/text() | //div[@class=\"table-s1 mt\"]/table/tr/td /a')
	res6 = html.xpath('//div[@class=\"table-s1 mt\"]/table/tr/td/a[@href]')

	sarr6 =   [etree.tostring(node) for node in res6]
	
	#from HTMLParser import HTMLParser
	#h = HTMLParser()
	#print h.unescape(js["statuses"][0]['description'])
	
	return sarr6



#时间
seldate="2015-07-21"
urllst = []
def getTradeDetailUrls(seldate, sarr6):
	urllst = []
	#正则表达式提取连接
	re_str = 'yybcode=(.*)\">'
	re_pat = re.compile(re_str)
	for  node in sarr6:
		if "jymx" in node:
			search_ret = re_pat.search(node)
			#print node
			if search_ret:   
					#print search_ret.groups()[0]
					
					lst = search_ret.groups()[0].split(',')
					urltrade = "http://stock.jrj.com.cn/action/lhb/getStockTradeDetail.jspa?&vname=listStd"+lst[1]+"&date="+seldate+"&stockcode="+lst[1]+"&yybcode="+lst[0]+"&_dc=1445437228612"
					urllst.append((urltrade, lst[0]))
					
	#获得营业部代码和股票代码
	#>>> lst
	#['200585495', '000564']
	lst = search_ret.groups()[0].split(',')
	#print urllst
	return urllst

comment='''for node in urllst:
	json = getJsonText(node)
	json = 
	print json.decode('utf-8').encode('gbk')
'''
#json = getJsonText(urllst[5])

def handleJson(json,  yybcode, filecsv):
	#print urlcode
	#json=urlcode[0]
	txt=json.replace('\n','')
	txt=txt.replace('\'','')
	re_str='data:\[\[(.*)\]\]\};'
	re_pat = re.compile(re_str)
	search_ret = re_pat.search(txt)
	ele=search_ret.groups()[0]
	se =  ele.split('],[')
	#print se
	
	buytimes = 0
	selltimes = 0 
	buytotal = 0
	selltotal= 0
	for node  in se:
		print >> filecsv, node, yybcode
		print node.decode('utf-8').encode('gbk')
		#获得每天的交易具体信息，并分列
		line = node.split(',')
		if float(line[2]) > 0:
			buytimes += 1
			buytotal += float(line[2])
		if float(line[3]) > 0:
			selltimes += 1
			selltotal += float(line[3])
	#净利润
	netrate = selltotal - buytotal;
	#操作交易额
	optotal=selltotal + buytotal
	#操作成功利润率
	opsuccess=netrate/optotal;
	print yybcode, " 买入次数:", buytimes, " 买入总额:", buytotal, " 卖出次数:", selltimes,  " 卖出总额:", selltotal, " 净利润:", netrate, " 操作成功利润率:", opsuccess
	print  "--------------------------------"+basicData.getYYBDataByCode(yybcode)+"--------------------------------------"
	line =se[0].split(',')
	#print "line : ", line
	
	return se


filecsv=open("trade.csv", "w")
#se = handleJson(json)

hrefarr = getHrefs(inListHistUrlArray[0])
urllst = getTradeDetailUrls(seldate, hrefarr)

for link in urllst:
	#print  "link: ",link
	json = getJsonText(link[0])	
	se = handleJson(json, link[1], filecsv)
	time.sleep(1)

filecsv.close()












