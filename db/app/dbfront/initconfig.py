#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from twisted.internet import reactor

import memmode
from madminanager import MAdminManager
from McharacterManager import McharacterManager

def doWhenStop():
    """服务器关闭前的处理
    """
    print "##############################"
    print "##########checkAdmins#############"
    print "##############################"
    MAdminManager().checkAdmins()

def initData():
    """载入角色初始数据
    """
    McharacterManager().initData()

def register_madmin():
    """注册数据库与memcached对应
    """
    MAdminManager().register(memmode.tb_character_admin)
    MAdminManager().register(memmode.tb_zhanyi_record_admin)
    MAdminManager().register(memmode.tbitemadmin)
    MAdminManager().register(memmode.tb_matrix_amin)
    MAdminManager().register(memmode.tbpetadmin)

def CheckMemDB(delta):
    """同步内存数据到数据库
    """
    MAdminManager().checkAdmins()
    reactor.callLater(delta, CheckMemDB, delta)

def loadModule():
#     mclient.flush_all()
    register_madmin()
    initData()
    CheckMemDB(1800)



