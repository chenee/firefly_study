#coding:utf8
"""
Created on 2013-3-18

@author: lan (www.9miao.com)
"""
from app.game.gatenodeservice import remoteserviceHandle
from app.game.appinterface import roleinfo
import json
    
@remoteserviceHandle
def RoleInfo_105(dynamicId,request_proto):
    """获取角色的状态栏信息
    """
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    data = roleinfo.roleInfo(dynamicId,characterId)
    return json.dumps(data)



