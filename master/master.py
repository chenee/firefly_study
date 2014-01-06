#coding:utf8
"""
Created on 2013-8-2

@author: lan (www.9miao.com)
"""
# import subprocess
import json
import sys
from twisted.internet import reactor
from twisted.python import log

from logobj import loogoo
from globalobject import GlobalObject

from root import PBRoot, BilateralFactory

from delayrequest import DelaySite
import webapp



reactor = reactor


class Master:
    def __init__(self, configpath):
        """
        """
        self.configpath = configpath

        config = json.load(open(self.configpath, 'r'))
        mastercnf = config.get('master')
        self.rootport = mastercnf.get('rootport')
        self.webport = mastercnf.get('webport')
        self.masterlog = mastercnf.get('log')

    def __startRoot(self):
        GlobalObject().root = PBRoot("rootservice")
        reactor.listenTCP(self.rootport, BilateralFactory(GlobalObject().root))


    def __startWeb(self):
        GlobalObject().webroot = webapp.initWeb()
        reactor.listenTCP(self.webport, DelaySite(GlobalObject().webroot))


    def startMaster(self):

        self.__startRoot()
        self.__startWeb()

        if self.masterlog:
            log.addObserver(loogoo(self.masterlog))#日志处理
        log.startLogging(sys.stdout)

        reactor.run()

    # def startChildren(self):
    #     """
    #     """
    #     print "start children ......"
    #     config = json.load(open(self.configpath, 'r'))
    #     sersconf = config.get('servers')
    #     for sername in sersconf.keys():
    #         cmds = 'python %s %s %s' % (self.mainpath, sername, self.configpath)
    #         subprocess.Popen(cmds, shell=True)
    #     reactor.run()
