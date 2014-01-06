#coding:utf8
"""
Created on 2013-3-18

@author: lan (www.9miao.com)
"""
from app.game.core.PlayersManager import PlayersManager

def roleInfo(dynamicId,characterId):
    """获取角色的状态栏信息
    @param userId: int 用户id
    @param characterId: 角色的id 
    """
    player = PlayersManager().getPlayerBydynamicId(dynamicId)
    if dynamicId != player.getDynamicId():
        return {'result':False,'message':""}
    playerinfo = player.formatInfo()
    responsedata = {'result':True,'message':'',
                    'data':{'characterId':playerinfo['id'],
                            'rolename':playerinfo['nickname'],
                            'level':playerinfo['level'],
                            'exp':playerinfo['exp'],
                            'maxexp':playerinfo['maxExp'],
                            'coin':playerinfo['coin'],
                            'gold':playerinfo['gold'],
                            'tili':playerinfo['maxHp'],
                            'tilimax':playerinfo['maxHp'],
                            'huoli':playerinfo['energy'],
                            'maxhuoli':playerinfo['energy'],
                            'profession':playerinfo['profession']}}
    return responsedata

