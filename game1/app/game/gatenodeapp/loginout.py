#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from app.game.gatenodeservice import remoteserviceHandle
from app.game.core.PlayersManager import PlayersManager


@remoteserviceHandle
def NetConnLost_2(dynamicId):
    """loginout
    """
    player = PlayersManager().getPlayerBydynamicId(dynamicId)
    if not player:
        return True
    player.updatePlayerDBInfo()
    PlayersManager().dropPlayer(player)
    return True
    
