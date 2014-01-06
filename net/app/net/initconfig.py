#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from globalobject import GlobalObject
from datapack import DataPackProtoc
import netapp


def callWhenConnLost(conn):
    dynamicId = conn.transport.sessionno
    GlobalObject().remote['gate'].callRemote("netconnlost",dynamicId)


GlobalObject().netfactory.doConnectionLost = callWhenConnLost
dataprotocl = DataPackProtoc(78,37,38,48,9,0)
GlobalObject().netfactory.setDataProtocl(dataprotocl)



def loadModule():
    netapp.initNetApp()
    import gatenodeapp
