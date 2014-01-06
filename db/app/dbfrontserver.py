#coding:utf8
"""
Created on 2013-8-13

@author: lan (www.9miao.com)
"""
from globalobject import GlobalObject
from dbfront import initconfig

GlobalObject().stophandler = initconfig.doWhenStop

initconfig.loadModule()
