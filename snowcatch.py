# -*- coding: utf-8 -*-
import urllib,urllib2
import os,time,sys
import cookielib
import json
import base64
import re
#发送邮件所需库
import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib

import lxml.html
from lxml import etree

from pandas.compat import StringIO

import snowparse as sp 
import snowcatch_config as config #目前是定义登录用户私密数据


'''
<Introduction>
——————————————————————————————————————————
雪球网组合调仓提醒
a. 支持实时短信提醒（太贵了，尼玛买不起短信平台的服务）
b. 支持实时邮件提醒

'''
#常量
pre_url = r'http://www.xueqiu.com/cubes/rebalancing/history.json?cube_symbol='
login_url = r'http://xueqiu.com/user/login'
name_url = r'http://xueqiu.com/P/'
pre_id = 1000000	#设置一个较低的值，保证第一次对比的now_id比其大

#邮件相关常量
authInfo = {'server' : 'smtp.qq.com' , 'user' : 'xueqiutips@qq.com' , 'password' : 'XXX'}
fromAdd = 'xueqiutips@qq.com'


#获取cookie
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)
#安装opener后，此后调用urlopen()都会使用安装过的opener(意思就是发的请求就是带cookie的了)

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36"}   #伪装成浏览器
'''data = {
	"areacode" : "86",
	"password" : "5124694000a",
	"remember_me" : "on",
	"telephone" : "13566699624"
	}
'''
	
post_data = urllib.urlencode(config.data)
request = urllib2.Request(login_url,post_data,headers)
try:
	r = opener.open(request)
except urllib2.HTTPError, e:
	print u"该去输入验证码了啦"
	print e.code			#一般是400	

print "login on success!"

url = 'http://xueqiu.com/7610708650'

def GetUser(url):
	# base64string = base64.encodestring('%s:%s' % ("api", "1674a71d8e1bf40d2777c007717bffc3"))[:-1]
	# authheader = "Basic %s"%base64string
	# values = {"mobile" : phonenumber ,
		# "message" : message }
	# data = urllib.urlencode(values)
	request = urllib2.Request(url, headers = headers)
	# request.add_header("Authorization", authheader)

	try:
		result = urllib2.urlopen(request)
	except IOError,e:
		print "wrong api and key!"
		print e.code
	text = result.read()
	return text

def PaserData(data):
     html = lxml.html.parse(StringIO(data))
     res = html.xpath('//div[@class=\"status_box \"]/script')
     arr =   [etree.tostring(node) for node in res]
     #get SNB.data
     sptxt = arr[0].split('SNB.data')
     startpos = sptxt[2].index('{')
     lastpos = sptxt[2].rindex(';')

     jsdata = json.loads(sptxt[2][startpos:lastpos])
     
     #过滤HTML 标签 正则表达式 
     dr = re.compile(r'<[^>]+>',re.S)
     #dd = dr.sub('',Html)
     if jsdata:
     	from HTMLParser import HTMLParser
	h = HTMLParser()
        i = 0
	for item in jsdata["statuses"]: 
           desc = dr.sub('', h.unescape(item['description']))
           print "content:", i, desc
	   i = i + 1

     return  ;

def PaserSNData(sndata):
    pass



	
if __name__ == '__main__' :
	GetUser(url)
	
	
