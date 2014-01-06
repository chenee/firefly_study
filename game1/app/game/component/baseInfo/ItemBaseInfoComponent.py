#coding:utf8
"""
Created on 2011-3-27

@author: sean_lan
"""
from app.game.component.baseInfo.BaseInfoComponent import BaseInfoComponent
import copy

from app.share.dbopear import dbItems

QUALITY_COLOR = {0:'000000',
                 1:'6fca26',
                 2:'2b50de',
                 3:'c526ca',
                 4:'f5b300',
                 5:'ef7700',
                 6:'e02a0f',
                 7:'ee115c'}#品质对应的色值

class ItemBaseInfoComponent(BaseInfoComponent):
    """物品基础信息组件类
    @param id: int 物品的id
    @param basename: str 物品的名称
    @param itemTemplateId:  int 物品的模板id
    """

    def __init__(self,owner, id, basename,itemTemplateId):
        """初始化物品基础信息"""
        BaseInfoComponent.__init__(self, owner, id, basename)
        self.itemTemplateId = itemTemplateId
        self.finalyPrice = -1#self.getItemTemplateInfo().get("buyingRateCoin",0)
        #self.templateInfo = self.getItemTemplateInfo()
    @property
    def itemtemplateInfo(self):
        return dbItems.all_ItemTemplate[self.itemTemplateId]

    def getitemPage(self):
        """获取物品在包裹中的分页类型"""
        return self.getItemTemplateInfo().get("itemPage",0)

    def getBaseQuality(self):
        """获取物品品质"""
        return self.getItemTemplateInfo().get("baseQuality",0)

    def getItemTemplateId(self):
        """获取物品模板Id
        """
        return self.itemTemplateId

    def setItemTemplateId(self,itemTemplateId):
        """设置物品的模板Id
        @param itemTemplateId: int 物品的模板Id
        """
        self.itemTemplateId = itemTemplateId

    def getItemTemplateInfo(self):
        """获取物品的模板信息"""
        data = {}
        if self.itemTemplateId!= -1 and self.itemTemplateId!=0:
            self._baseName = dbItems.all_ItemTemplate[self.itemTemplateId]['name']
            data = copy.deepcopy(dbItems.all_ItemTemplate[self.itemTemplateId])
        return data

    def getItemSellType(self):
        """获取物品出售类型"""
        return self.getItemTemplateInfo().get("sellType",1)

    def getItemDropType(self):
        """获取物品丢弃类型"""
        return self.getItemTemplateInfo().get("dropType",1)

    def setItemPrice(self,price):
        """设置物品的价格"""
        self.finalyPrice = price

    def getItemFinalyPrice(self):
        """获取物品的最终价格"""
        return self.finalyPrice

    def getItemPrice(self):
        """获取物品的商店价格"""
        return self.getItemTemplateInfo().get("buyingRateCoin",0)

    def getItemProfession(self):
        """获取物品职业限制"""
        return self.getItemTemplateInfo().get("professionRequire",0)

    def getItemBodyType(self):
        """获取物品的装备部位"""
        return self.getItemTemplateInfo().get("bodyType",-1)

    def getName(self):
        """获取物品名称"""
        return self.getItemTemplateInfo().get("name","")

    def getRichName(self):
        """获取带颜色的物品名称"""
        htmstr = "<font  color='#%s'>%s</font>"
        quality = self.getItemTemplateInfo().get("baseQuality",u'')
        colorstr = QUALITY_COLOR.get(quality,'000000')
        name = self.getName()
        return htmstr%(colorstr,name)

    def getUseScript(self):
        """获取物品使用效果脚本"""
        return self.getItemTemplateInfo().get("script",u'')

    def getItemUseType(self):
        """物品是否可以使用
        """
        usetype = self.getItemTemplateInfo().get("useType",u'')
        if usetype==1:
            return True
        return False

    def getItemPageType(self):
        """获取物品的类型"""
        return self.getItemTemplateInfo().get("itemPage",1)

    def getLevelRequired(self):
        """获取等级需求"""
        return self.getItemTemplateInfo().get("levelRequire",1)

    def getWeaponType(self):
        return self.getItemTemplateInfo().get("weaponType",-1)



