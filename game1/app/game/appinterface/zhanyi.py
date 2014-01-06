#coding:utf8
"""
Created on 2013-1-8

@author: lan (www.9miao.com)
"""

from app.game.core.PlayersManager import PlayersManager

def getZhanYiInfo(dynamicId,characterId ,index):
    """获取角色的战役信息
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':""}
    zhanyiinfo = player.zhanyi.getZhanYiInfo(index)
    return zhanyiinfo

def zhangjieFight(dynamicId,characterId,zhangjieid):
    """章节战斗
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':""}
    fightresult = player.zhanyi.doZhangJie(zhangjieid)
    return fightresult




