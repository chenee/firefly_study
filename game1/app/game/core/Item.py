#coding:utf8
"""
Created on 2011-3-28

@author: sean_lan
"""

from app.game.component.baseInfo.ItemBaseInfoComponent import ItemBaseInfoComponent
from app.game.component.attribute.ItemAttributeComponent import ItemAttributeComponent
from app.game.component.pack.ItemPackComponent import ItemPackComponet
from app.share.dbopear import dbItems
from app.game.memmode import tbitemadmin
import datetime

class Item(object):
    """物品类"""
    
    def __init__(self,itemTemplateId = 0,id = 0,name =''):
        """初始化物品类
        @param id: int 物品在数据库中的id
        @param itemTemplateId: int 物品的模板id
        @param selfExtraAttributeId: []int list 物品自身附加属性
        @param dropExtraAttributeId: []int list 物品掉落时的附加属性 
        """
        self.baseInfo = ItemBaseInfoComponent(self,id,name,itemTemplateId)
        self.attribute = ItemAttributeComponent(self)
        self.pack = ItemPackComponet(self)
        self.exp = 0
        
    def initItemInstance(self,itemInstance):
        """初始化实际物品信息
        """
        self.exp = itemInstance['exp']
        self.baseInfo.setItemTemplateId(itemInstance['itemTemplateId'])
        self.attribute.setDurability(itemInstance['durability'])
        self.pack.setStack(itemInstance['stack'])
                
    def getWQtype(self):
        """获取装备类型 #0=衣服#1=裤子 #2=头盔#3=手套#4=靴子#5=护肩#6=项链#7=戒指#8=主武器#9=副武器#10=双手"""
        iteminfo=self.baseInfo.getItemTemplateInfo() #物品模板id信息
        typeid=iteminfo.get('bodyType',0)
        return typeid
    
    def formatItemInfo_new(self,suitecnt = 0):
        """格式化物品信息"""
        data = self.baseInfo.getItemTemplateInfo() #字典类型
        if self.baseInfo.getItemFinalyPrice()>0:
            data['buyingRateCoin'] = self.baseInfo.getItemFinalyPrice()
        data['stack'] = self.pack.getStack()
        data['templateId'] = self.baseInfo.getItemTemplateId()
        if self.baseInfo.getId()!=0:
            data['id']= self.baseInfo.getId()
        else:
            data['id'] = self.baseInfo.getItemTemplateId()
        data['isBound'] = 0
        data['nowQuality'] = data['baseQuality']
        return data
    
    def formatItemInfo(self):
        """格式化物品信息"""
        data = self.baseInfo.getItemTemplateInfo()
        data['id']= self.baseInfo.getId()
        data['templateId'] = self.baseInfo.getItemTemplateId()
        data['stack'] = self.pack.getStack()
        return data
    
    def getItemAttributes(self):
        """获取装备的附加属性
        """
        info = {}
        data = self.baseInfo.getItemTemplateInfo()
        info['Str'] = data.get('baseStr')
        info['Dex'] = data.get('baseDex')
        info['Vit'] = data.get('baseVit')
        info['Wis'] = data.get('baseWis')
        info['MaxHp'] = data.get('baseHpAdditional')
        info['PhyAtt'] = data.get('basePhysicalAttack')
        info['PhyDef'] = data.get('basePhysicalDefense')
        info['MigAtt'] = data.get('baseMagicAttack')
        info['MigAtt'] += self.attribute.extMagicAttack
        info['MigDef'] = data.get('baseMagicDefense')
        info['MigDef'] += self.attribute.extMagicDefense
        info['HitRate'] = data.get('baseHitAdditional')
        info['Dodge'] = data.get('baseDodgeAdditional')
        info['CriRate'] = data.get('baseCritAdditional')
        info['Speed'] = data.get('baseSpeedAdditional')
        info['Speed'] += self.attribute.extSpeedAdditional
        info['Block'] = data.get('baseBlockAdditional')
        info['Skill'] = [] if data.get('skill',0)==0 else [data.get('skill',0)]
        return info
        
    def InsertItemIntoDB(self,characterId = 0):
        """将物品信息写入数据库"""
        if self.baseInfo.id:#已经存在物品的实例
            return
        itemTemplateId = self.baseInfo.itemTemplateId
        isBound = 0
        durability = 0
        stack = self.pack.getStack()
        data = {'characterId':characterId,
                'itemTemplateId':itemTemplateId,
                'isBound':isBound,
                'accesstime':datetime.datetime.now(),
                'durability':durability,
                'stack':stack,'strengthen':0,
                'workout':0,'slot_1':0,'slot_2':0,
                'slot_3':0,'slot_4':0,'exp':self.exp}
        newitemmode = tbitemadmin.new(data)
        itemId = int(newitemmode._name.split(':')[1])
        self.baseInfo.setId(itemId)
        return itemId
    
    def destroyItemInDB(self):
        """删除数据库中的自身的信息"""
        if self.baseInfo.id!=0:
            return tbitemadmin.deleteMode(self.baseInfo.id)
        return False
    
    def formatItemInfoForWeiXin(self):
        """格式化物品信息
        """
        data = self.getItemAttributes()
        info = {}
        info['itemid'] = self.baseInfo.id
        info['icon'] = self.baseInfo.getItemTemplateInfo()['icon']
        info['itemname'] = self.baseInfo.getItemTemplateInfo()['name']
        info['itemdesc'] = self.baseInfo.getItemTemplateInfo()['description']
        info['tempid'] = self.baseInfo.getItemTemplateId()
        info['qlevel'] = self.attribute.strengthen
        info['attack'] = data['PhyAtt']
        info['fangyu'] = data['PhyDef']
        info['tili'] = data['MaxHp']
        info['minjie'] = data['Speed']
        info['price'] = self.baseInfo.getItemTemplateInfo()['buyingRateCoin']
        info['stack'] = 1
        info['qh'] = 1 if self.baseInfo.getItemTemplateInfo()['bodyType']>0 else 0
        return info        


