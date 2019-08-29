# -*- coding:utf-8 -*-

import sys

import traceback

from distutils.core import setup
import py2exe, os, pymssql
import suds
import decimal
import uuid
import string
import random
import time
import _mssql
import socket
print("sys.path =", sys.path)
import imp
imp.find_module('suds', sys.path)
from wtforms import *
from flask_wtf import *
from email.mime import *

# import jinja2

'''
	build.py
	rosen, 2019.08.13
	打包发布程序
	
	jinja 用2.8版本的
	click 用5.1版本的
	安装 flask_wtf, werkzeug

'''

setup(
	version = "0.1.0",
    description = " -后台",
    name = "finger control @",
	# 指定生成的目标文件，
	console=['app.py'], 
	zipfile = None,
	options = {'py2exe': { 
				"bundle_files": 1,
				"includes" : ["pymssql", "_mssql", "xml", 'werkzeug',"lxml._elementpath", "lxml.etree", 'flask', 'flask_wtf', 'jinja2', 'jinja2.ext', 
				'email.mime.audio',
				'email.mime.multipart','email.mime', 'email.mime.text', 'email.mime.image', 'email.mime.message'],
				"dll_excludes": ['jinja2' ] 
				# "dll_excludes": ['jinja2', 'jinja2.asyncsupport','jinja2.asyncfilters' ] 
				} 
			}
	# data_files=[("static",["static/*"])]
                  # ("etc",["etc/finger.conf", "etc/soap.conf","etc/XMLSchema.xsd", "etc/xml.xsd" ]),
                  # ("sql",["sql/accessControl.sql" ]),
                  # ("scripts",["scripts/run.bat", "scripts/stop.bat" ]),
				   # os.path.join(os.path.split(pymssql.__file__)[0], '_mssql.pyd')
				# ]

)
