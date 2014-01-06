#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dataloader import load_config_data,registe_madmin
from globalobject import GlobalObject
from app.game.core.PlayersManager import PlayersManager
from twisted.python import log

def doWhenStop():
    """服务器关闭前的处理
    """
    for player in PlayersManager()._players.values():
        try:
            player.updatePlayerDBInfo()
            PlayersManager().dropPlayer(player)
        except Exception as ex:
            log.err(ex)

GlobalObject().stophandler = doWhenStop

def loadModule():
    """
    """
    load_config_data()
    registe_madmin()
    from gatenodeapp import *

