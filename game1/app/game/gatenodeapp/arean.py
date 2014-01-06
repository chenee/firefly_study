#coding:utf8
"""
Created on 2013-7-17

@author: lan (www.9miao.com)
"""
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import arena
import json

@remoteserviceHandle
def GetJingJiInfo_3700(dynamicId, request_proto):
    """获取竞技场信息
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    data = arena.GetJingJiInfo3700(dynamicId, characterId)
    return json.dumps(data)

@remoteserviceHandle
def ArenaBattle_3704(dynamicId, request_proto):
    """竞技场战斗
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    tocharacterId = argument.get('tid')
    data = arena.ArenaBattle_3704(dynamicId, characterId, tocharacterId)
    response = {}
    response['result'] = data.get('result',False)
    response['message'] = data.get('message','')
    _responsedata = data.get('data')
    if _responsedata:
        battle = _responsedata.get('fight')
        setData = _responsedata.get('setData')
        fightdata = battle.formatFightData()
        response['data'] = fightdata
        fightdata['battleResult'] = battle.battleResult
        fightdata['setData'] = setData
    return json.dumps(response)

