#coding:utf8
"""
Created on 2013-9-4

@author: hg (www.9miao.com)
"""

from twisted.internet import reactor
from twisted.web.server import Site
from twisted.web import vhost
from handle import OperaPlayer,DayRecored,Statistics


def loadModule():
    root = vhost.NameVirtualHost()
    root.putChild('opera', OperaPlayer())#在浏览器地址栏输入http://localhost:2012/opera?username=xx&opera_str=xxx  username是要操作的账号  opera_str是要操作的脚本
    root.putChild('dayrecored', DayRecored())
    root.putChild('statistics', Statistics())#statistics单服总数据
    reactor.listenTCP(2012,Site(root))

