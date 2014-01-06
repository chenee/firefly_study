#coding:utf8
"""
Created on 2013-8-7

@author: lan (www.9miao.com)
"""
from twisted.web import resource, vhost

from twisted.internet import reactor
from globalobject import GlobalObject


reactor = reactor


def ErrorBack(reason):
    pass


class stop(resource.Resource):
    """stop service"""

    def render(self, request):
        """
        """
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('serverStop')
            d.addCallback(ErrorBack)
        reactor.callLater(0.5,reactor.stop)
        return "stop"

class reloadmodule(resource.Resource):
    """reload module"""

    def render(self, request):
        """
        """
        for child in GlobalObject().root.childsmanager._childs.values():
            d = child.callbackChild('sreload')
            d.addCallback(ErrorBack)
        return "reload"


class chenee(resource.Resource):
    def render(self, request):
        return "chenee is pig"


def initWeb():
        webroot = vhost.NameVirtualHost()
        webroot.addHost('0.0.0.0', './')

        webroot.putChild(stop.__name__, stop())
        webroot.putChild(reloadmodule.__name__, reloadmodule())
        webroot.putChild(chenee.__name__, chenee())

        return  webroot
