#coding:utf8
"""
Created on 2013-8-2

@author: lan (www.9miao.com)
"""
from singleton import Singleton

class GlobalObject:

    __metaclass__ = Singleton

    def __init__(self):
        self.root = None#分布式root节点
        self.webroot = None


