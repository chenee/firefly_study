#coding:utf8
"""
Created on 2013-3-20
阵法信息
@author: lan (www.9miao.com)
"""

from app.game.gatenodeservice import remoteserviceHandle
import json
from app.game.appinterface import pet


@remoteserviceHandle
def GetCharacterMatrixInfo_2306(dynamicId,request_proto):
    """获取角色阵法的信息
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    response = pet.GetCharacterMatrixInfo(dynamicId, characterId)
    return json.dumps(response)
    
    
@remoteserviceHandle
def GetAllPetList_2300(dynamicId,request_proto):
    """获取角色的所有宠物信息
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    response = pet.GetAllPetListFormatForWeixin(dynamicId, characterId)
    return json.dumps(response)
    
    
@remoteserviceHandle
def SetCharacterMatrix_2307(dynamicId,request_proto):
    """设置角色的阵法
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    petId = argument.get('petId')
    chatype = argument.get('chatype')
    operationType = argument.get('operType')
    fromPos = argument.get('fromPos')
    toPos = argument.get('toPos')
    response = pet.SettingMatrix(dynamicId, characterId,
                                  petId,chatype,operationType, fromPos, toPos)
    return json.dumps(response)
    
@remoteserviceHandle
def SwallowPet_3505(dynamicId,request_proto):
    """武将吞噬
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    petId = argument.get('petid')
    tpetid = argument.get('tpetid')
    response = pet.SwallowPet(dynamicId, characterId,petId,tpetid)
    return json.dumps(response)
