#coding:utf8
"""
Created on 2013年9月4日

@author: MSI
"""
from app.game.gatenodeservice import remoteserviceHandle
from app.game.core.PlayersManager import PlayersManager
from app.game.core.character.PlayerCharacter import PlayerCharacter

@remoteserviceHandle
def operaplayer_99(pid,oprea_str):
    """执行后台管理脚本
    """
    player = PlayersManager().getPlayerByID(pid)
    isOnline = 1
    if not player:
        player = PlayerCharacter(pid)
        isOnline = 0
    exec(oprea_str)#player.finance.addCoin(1000)脚本例子，通过角色类进行角色的各种操作，player.XXX.XXX
    if isOnline == 0:
        player.updatePlayerDBInfo()
    
    
