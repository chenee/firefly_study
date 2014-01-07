#coding:utf8
"""
Created on 2013-3-19
好友信息
@author: lan
"""
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import firend
import json

@remoteserviceHandle
def GetFriendList_302(dynamicId,request_proto):
    """获取好友的排行列表
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    tag = argument.get('tag')
    index = argument.get('index')
    response = firend.GetFriendList(dynamicId, characterId, tag, index)
    return json.dumps(response)
    

@remoteserviceHandle
def GetPlayerInfo_221(dynamicId,request_proto):
    """获取角色的信息 1角色自身 2好友 3宠物
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    chtype = argument.get('type')
    tid = argument.get('tid')
    data = firend.GetSingleCharacterInfo(dynamicId, characterId, chtype, tid)
    return json.dumps(data)
    
@remoteserviceHandle
def GuYongHaoYou_2301(dynamicId,request_proto):
    """雇佣好友
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    tid = argument.get('friendid')
    data = firend.GuYongHaoYou(dynamicId,characterId,tid)
    return json.dumps(data)
    
@remoteserviceHandle
def GuYongRecord_2309(dynamicId,request_proto):
    """获取雇用的记录
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    data = firend.getGuyongRecord(dynamicId,characterId)
    return json.dumps(data)
    
    
