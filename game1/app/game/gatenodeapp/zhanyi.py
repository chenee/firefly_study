#coding:utf8
"""
Created on 2013-1-8
剧情信息
@author: lan (www.9miao.com)
"""
from app.game.gatenodeservice import remoteserviceHandle
import json

from app.game.appinterface import zhanyi

@remoteserviceHandle
def GetNowZhanYiInfo_4500(dynamicId,request_proto):
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    index = argument.get('index')
    data = zhanyi.getZhanYiInfo(dynamicId, characterId, index)
    return json.dumps(data)

@remoteserviceHandle
def ZhangJieFight_4501(dynamicId,request_proto):
    """江湖战斗
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    zhangjieid = argument.get('zjid')
    data = zhanyi.zhangjieFight(dynamicId, characterId, zhangjieid)
    response = {}
    response['result'] = data.get('result',False)
    response['message'] = data.get('message','')
    _responsedata = data.get('data')
    if _responsedata:
        battle = _responsedata.get('fight')
        setData = _responsedata.get('setData')
        fightdata = battle.formatFightData()
        response['star'] = battle.battlestar
        response['data'] = fightdata
        fightdata['battleResult'] = battle.battleResult
        fightdata['setData'] = setData
    return json.dumps(response)
