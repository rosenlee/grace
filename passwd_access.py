'''

带用户名、密码HTTP访问接口
示例
'''

import json

import time

import sys

import random

import datetime

import traceback
import base64
#import basicData

reload(sys)

sys.setdefaultencoding('utf-8')

import urllib
import urllib2

def getJsonText(url):


    request = Request(url)

    try:

        text = urlopen(request, timeout=100).read()
        #result = unicode(text,'GBK').encode('UTF-8')
        #result = text.encode('gbk', 'ignore')

        return text

    except :

        print ("url Exception")
        traceback.print_exc()

        return None

username="1234"
password="23422"

us_agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

st =  time.localtime()
displayTime = time.strftime("%Y-%m-%d %X", st)

def getAuthorization():
    authStr = "Basic " + base64.b64encode( username+ ":" + password);
    print("auth string= " + authStr)
    return authStr;

def getAttchament():
    try:
        requrl = "http://192.168.0.148:3000/"
        print(requrl)
        test_data={"pageNum":1,"pageSize":10,"version":1,"seq":1,"timestamp":"20181206113929","operator":"TS00000120181210152806PS_010x133"}
        td_encode = urllib.urlencode(test_data)
       # req = urllib2.Request(url=requrl, data=td_encode)
        ua_header = {"User-Agent":us_agent}

        req = urllib2.Request(url=requrl, headers=ua_header)
        req.add_header("Connection", "keep-alive")
        req.add_header("Content-Type", "application/json;charset=UTF-8")
        req.add_header("Authorization", getAuthorization());

        print ("req = ", req)
        response = urllib2.urlopen(req)  #接受反馈的信息
        #jsonText = json.loads(response.read())
        #print ("json= ", jsonText)
        print ("msg= " + response.read())
    except:
        print ("url Exception")
        traceback.print_exc()

        return None



def getExamine():
    requrl = "http://192.168.0.140:8080/examine/qryExamineItem"
    print(requrl)
    test_data={"pageNum":1,"pageSize":10,"version":1,"seq":1,"timestamp":"20181206113929","operator":"TS00000120181210152806PS_010x133"}
    td_encode = urllib.urlencode(test_data)
    req = urllib2.Request(url=requrl, data=td_encode)
    response = urllib2.urlopen(req)  #接受反馈的信息
    jsonText = json.loads(response.read())
    print ("req = ", req)
    print ("json= ", jsonText)
    print ("msg= " + jsonText['msg'])

## todo:
def getUrl():
    return "";

def getData():
    return "";

if __name__ == '__main__':
#
    if len(sys.argv) > 2 and sys.argv[1] == "-r":
       print ("read mode")

       # table = OpenFile(sys.argv[2]);

       exit()

    getAttchament()
    getExamine()
    print ("done!", displayTime)
