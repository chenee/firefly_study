#coding:utf8
"""
Created on 2012-5-21
物品合成
@author: Administrator
"""
from app.game.core.PlayersManager import PlayersManager
from app.share.dbopear import dbItems

def GetCompoundPackage_2109(dynamicId,characterId):
    """获取合成包裹的信息
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    response = player.pack.HuoQuSuiPianBaoguo()
    return response

    
def GetOneItemInfo(dynamicId, characterId,itemid):
    """获取单个物品的详细信息
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    response = player.pack.getOneItemInfo(itemid)
    return response

    
def GetCompoundItem(dynamicId, characterId,tempid):
    """获取当前碎片能合成的物品的信息
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    suipianinfo = dbItems.all_ItemTemplate.get(tempid)
    if not suipianinfo:
        return {'result':False,'message':u"碎片信息不存在"}
    newtempid = suipianinfo.get('compound',0)
    newiteminfo = dbItems.all_ItemTemplate.get(newtempid)
    if not newiteminfo:
        return {'result':False,'message':u"该物品不能合成"}
    response = {}
    info = {}
    info['itemid'] = 0
    info['icon'] = newiteminfo['icon']
    info['itemname'] = newiteminfo['name']
    info['itemdesc'] = newiteminfo['description']
    info['tempid'] = newiteminfo['id']
    info['qlevel'] = 0
    info['attack'] = newiteminfo['basePhysicalAttack']
    info['fangyu'] = newiteminfo['basePhysicalDefense']
    info['minjie'] = newiteminfo['baseSpeedAdditional']
    info['tili'] = newiteminfo['baseHpAdditional']
    info['price'] = newiteminfo['buyingRateCoin']
    info['stack'] = 1
    info['qh'] = 1 if newiteminfo['bodyType']>0 else 0
    response['hcprice'] = suipianinfo.get('comprice',0)
    response['iteminfo'] = info
    return {'result':True,'message':u"",'data':response}

    
def CompoundItem(dynamicId, characterId, tempid):
    """合成物品
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    response = player.pack.CompoundItem(tempid)
    return response


