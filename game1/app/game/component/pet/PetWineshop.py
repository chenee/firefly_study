#coding:utf8
"""
Created on 2012-5-30

@author: jt
"""
from component.Component import Component
from utils.dbopera import dbCharacterPet,dbPetShop
import random,time

def getpetshopsuiji():
    """宠物商店随机"""
    while True:
        rate=random.randint(1,100000)
        if rate>99900:
            yield 4
        elif rate>85000:
            yield 3 #  3低级宠物
        elif rate>50000:
            yield 2 #  2中级宠物
        else:
            yield 1 #  1高级宠物
    
TIME_DELTA = 1800
PQ_Generater = getpetshopsuiji()

class PetWineshop(Component):
    """宠物酒店
    """


    def __init__(self,owner):
        """初始化宠物酒店
        """
        Component.__init__(self,owner)
        self.owner=owner
        self.ctime=0#记录时间
        self.shop=[]#宠物商店 (存储3个宠物模板)#[宠物模板id,宠物模板id]
        self.cs=1#每天剩余免费次数
        self.indb = 0#是否已经写入数据库
        self.initPetWineshop()
        
    def initPetWineshop(self):
        """初始化酒馆信息
        """
        pid = self._owner.baseInfo.id
        info=dbPetShop.getByid(pid)#剩余时间记录
        if info:
            self.ctime=info.get('ctime')
            self.shop = eval(info.get('shop'))
            self.xy=info.get('xy')
            self.cs=info.get('cs')
            self.indb = 1
        else:
            self.refleshShop()
        
    def getSurplusTime(self):
        """获取剩余时间
        """
        nowtime = time.time()
        surplustime =  int(max(TIME_DELTA-(nowtime-self.ctime),0))
        if not surplustime:
            self.cs = 1
        return surplustime
        
    def refleshShop(self,purview=0):
        """获取商店中的商品"""
        self.FillShop()
        if purview==1:
            self.ctime = time.time()
    
    def findOnePet(self):
        """寻找一个武将
        """
        quality = PQ_Generater.next()
        shop=dbCharacterPet.shopAll.get(quality) #宠物模板信息列表
        count=len(shop)
        index=random.randint(0,count-1)
        return shop[index]
        
    def FillShop(self):
        """填充商店
        """
        petlist = []
        for i in range(3):
            petlist.append(self.findOnePet())
        self.shop = petlist
    
    def SellPet(self,petId):
        """出售某个武将
        """
        index = self.shop.index(petId)
        self.shop[index] = 0
    
    def dbupdate(self):
        """下线处理中，将信息记录到数据库中"""
        pid = self._owner.baseInfo.id
        shop = str(self.shop)
        ctime = int(self.ctime)
        cs = self.cs
        if self.indb:#如果有记录了
            dbPetShop.updateInfo(pid, shop, ctime, cs)
        else:
            dbPetShop.addInfo(pid, shop, ctime, cs)
        
        
