#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from rootservice import rservices
from localservice import lservices

def loadModule():
    rservices.init()
    lservices.init()


