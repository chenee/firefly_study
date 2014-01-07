#coding:utf8
"""
Created on 2012-7-1
竞技场操作
@author: Administrator
"""
from app.game.core.PlayersManager import PlayersManager

def GetJingJiInfo3700(dynamicId,characterId):
    """获取竞技场信息
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    data = player.arena.getArenaAllInfo()
    return {'result':True,'data':data}



def ArenaBattle_3704(dynamicId,characterId,tocharacterId):
    """竞技场战斗
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':""}
    result = player.arena.doFight(tocharacterId)
    return result
    
