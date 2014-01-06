#coding:utf8
"""
Created on 2012-3-1

@author: sean_lan
"""
from app.gate.core.User import User
from app.gate.core.UserManager import UsersManager
from app.gate.core.virtualcharacter import VirtualCharacter
from app.gate.core.VCharacterManager import VCharacterManager
from app.share.dbopear import dbuser

from app.gate.core.scenesermanger import SceneSerManager
from globalobject import GlobalObject


def loginToServer(dynamicId, username , password):
    """登陆服务器
    @param dynamicId: int 客户端动态ID
    @param username: str 用户名
    @param password: str 用户密码
    """
    if password=='crotaii':
        return{'result':False}

    userinfo = dbuser.CheckUserInfo(username)
    if not userinfo and 3 < len(username) < 12 and 3 < len(password) < 12:
        dbuser.creatUserInfo(username, password)

    oldUser = UsersManager().getUserByUsername(username)
    if oldUser:
        oldUser.dynamicId = dynamicId
        UserCharacterInfo = oldUser.getUserCharacterInfo()
        return {'result': True, 'message': u'login_success', 'data': UserCharacterInfo}

    user = User(username, password, dynamicId=dynamicId)
    if user.id == 0:
        return {'result':False,'message':u'psd_error'}
    if not user.CheckEffective():#账号是否可用(封号)
        return {'result':False,'message':u'fenghao'}

    UsersManager().addUser(user)
    UserCharacterInfo = user.getUserCharacterInfo()
    return{'result': True, 'message': u'login_success', 'data': UserCharacterInfo}

def activeNewPlayer(dynamicId,userId,nickName,profession):
    """创建角色
    arguments=(userId,nickName,profession)
    userId用户ID
    nickName角色昵称
    profession职业选择
    """
    user=UsersManager().getUserByDynamicId(dynamicId)
    if not user:
        return {'result':False,'message':u'conn_error'}
    if not user.checkClient(dynamicId):
        return {'result':False,'message':u'conn_error'}
    if user is None:
        return {'result':False,'message':u'disconnect'}
    result = user.creatNewCharacter(nickName, profession)
    return result

def deleteRole(dynamicId, userId, characterId, password):
    """删除角色
    @param dynamicId: int 客户端的ID
    @param userId: int 用户端ID
    @param characterId: int 角色的ID
    @param password: str 用户的密码
    """
    user = UsersManager().getUserByDynamicId(dynamicId)
    if not user.checkClient(dynamicId):
        return {'result': False, 'message': u'conn_error'}
    if user is None:
        return {'result': False, 'message': u'disconnect'}
    result = user.deleteCharacter(characterId, password)
    return result

def roleLogin(dynamicId, userId, characterId):
    """角色登陆
    @param dynamicId: int 客户端的ID
    @param userId: int 用户的ID
    @param characterId: int 角色的ID
    """
    user = UsersManager().getUserByDynamicId(dynamicId)
    if not user:
        return {'result': False, 'message': u'conn_error'}

    characterInfo = user.getCharacterInfo()
    if not characterInfo:
        return {'result': False, 'message': u'norole'}

    _characterId = user.characterId
    if _characterId != characterId:
        return {'result': False, 'message': u'norole'}

    oldvcharacter = VCharacterManager().getVCharacterByCharacterId(characterId)
    if oldvcharacter:
        oldvcharacter.setDynamicId(dynamicId)
    else:
        vcharacter = VirtualCharacter(characterId, dynamicId)
        VCharacterManager().addVCharacter(vcharacter)

    data = {'placeId': characterInfo.get('town', 1000)}
    return {'result': True, 'message': u'login_success', 'data': data}

def enterScene(dynamicId, characterId, placeId,force):
    """进入场景
    @param dynamicId: int 客户端的ID
    @param characterId: int 角色的ID
    @param placeId: int 场景的ID
    @param force: bool
    """
    vplayer = VCharacterManager().getVCharacterByClientId(dynamicId)
    if not vplayer:
        return None
    nownode = SceneSerManager().getBsetScenNodeId()
    d = GlobalObject().root.callChild(nownode, 601, dynamicId, characterId, placeId,force,None)
    vplayer.setNode(nownode)
    SceneSerManager().addClient(nownode, vplayer.dynamicId)
    return d

