#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from globalobject import GlobalObject, addToRootService
from app.gate.core.UserManager import UsersManager
from app.gate.core.VCharacterManager import VCharacterManager
from app.gate.core.scenesermanger import SceneSerManager

def forwarding(key,dynamicId,data):
    """
    """
    if key in GlobalObject().localservice._targets:
        return GlobalObject().localservice.callTarget(key,dynamicId,data)
    else:
        user = UsersManager().getUserByDynamicId(dynamicId)
        if not user:
            return
        oldvcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
        if not oldvcharacter:
            return
        if oldvcharacter.getLocked():#判断角色对象是否被锁定
            return
        node = VCharacterManager().getNodeByClientId(dynamicId)
        return GlobalObject().root.callChild(node, key, dynamicId, data)


def pushObject(topicID, msg, sendList):
    """
    """
    GlobalObject().root.callChild("net", "pushObject", topicID, msg, sendList)

def opera_player(pid,oprea_str):
    """
    #vcharacter是虚拟角色，VCharacterManager()虚拟角色管理器，{角色id:虚拟角色实例}
    """
    vcharacter = VCharacterManager().getVCharacterByCharacterId(pid)
    if not vcharacter:
        node = "game1"
    else:
        node = vcharacter.getNode()
    GlobalObject().root.callChild(node,99,pid,oprea_str)


def SavePlayerInfoInDB(dynamicId):
    """将玩家信息写入数据库
       node: 用于判定是 game1，game2，。。。。。这些节点
       magic number: 2 --> "maybe save to db"
    """
    vcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
    nodeid = vcharacter.getNode()
    d = GlobalObject().root.callChild(nodeid,2,dynamicId)
    return d

def SaveDBSuccedOrError(result,vcharacter):
    """写入角色数据成功后的处理
    @param result: 写入后返回的结果
    @param vcharacter: 角色的实例
    """
    vcharacter.release()#释放角色锁定
    return True

def dropClient(deferResult,dynamicId,vcharacter):
    """清理客户端的记录
    @param result: 写入后返回的结果
    """
    node = vcharacter.getNode()
    if node:  #角色在场景中的处理
        SceneSerManager().dropClient(node, dynamicId)

    VCharacterManager().dropVCharacterByClientId(dynamicId)
    UsersManager().dropUserByDynamicId(dynamicId)

def netconnlost(dynamicId):
    """客户端断开连接时的处理
    @param dynamicId: int 客户端的动态ID
    """
    vcharacter = VCharacterManager().getVCharacterByClientId(dynamicId)
    if vcharacter and vcharacter.getNode()>0:#判断是否已经登入角色
        vcharacter.lock()#锁定角色
        d = SavePlayerInfoInDB(dynamicId)#保存角色,写入角色数据
        d.addErrback(SaveDBSuccedOrError, vcharacter)#解锁角色
        d.addCallback(dropClient, dynamicId, vcharacter)#清理客户端的数据
    else:
        UsersManager().dropUserByDynamicId(dynamicId)



def init():
    addToRootService(forwarding)
    addToRootService(pushObject)
    addToRootService(opera_player)
    addToRootService(netconnlost)

