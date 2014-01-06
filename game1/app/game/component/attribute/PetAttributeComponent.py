#coding:utf8
"""
Created on 2012-5-29
宠物的属性
@author: Administrator
"""
from app.game.component.Component import Component
import random
from app.share.dbopear import dbCharacterPet
from app.game.memmode import tbpetadmin

GROW_ATTR = 20#成长与每级属性增长值比
PHYATT_STR = 7#物攻与力量比
MIGATT_WIS = 7#魔攻与智力比
PHYDEF_STR = 0#物防与力量比
PHYDEF_VIT = 3#物防与耐力比
MIGDEF_WIS = 0#魔防与智力比
MIGDEF_VIT = 3#魔防与耐力比
MAXHP_VIT = 18#血量与耐力比


def Train(quality,traintype):
    """宠物培养
    @param traintype: int 培养方式
    """
    down = dbCharacterPet.PET_TRAIN_CONFIG[quality].get('down_%d'%traintype)
    up = dbCharacterPet.PET_TRAIN_CONFIG[quality].get('up_%d'%traintype)
    info = {}
    info['StrGrowthAdd'] = random.randint(down,up)
    info['WisGrowthAdd'] = random.randint(down,up)
    info['VitGrowthAdd'] = random.randint(down,up)
    info['DexGrowthAdd'] = random.randint(down,up)
    return info


class PetAttributeComponent(Component):
    """宠物属性相关
    """

    def __init__(self,owner):
        """
        Constructor
        @param hp: int 宠物的当前血量
        @param StrGrowth: int 宠物的力量成长
        @param WisGrowth: int 宠物的智力成长
        @param VitGrowth: int 宠物的耐力（体力）成长
        @param DexGrowth: int 宠物的敏捷成长
        """
        Component.__init__(self, owner)
        self.hp = 0
        self.StrGrowth = 0
        self.WisGrowth = 0
        self.VitGrowth = 0
        self.DexGrowth = 0
        self.StrGrowthAdd = 0
        self.WisGrowthAdd = 0
        self.VitGrowthAdd = 0
        self.DexGrowthAdd = 0

    def initData(self,StrGrowth,WisGrowth,VitGrowth,DexGrowth,hp):
        """初始化角色属性
        """
        self.StrGrowth = StrGrowth
        self.WisGrowth = WisGrowth
        self.VitGrowth = VitGrowth
        self.DexGrowth = DexGrowth
        self.hp = hp
        if hp==-1:
            self.hp = self.getMaxHp()

    def getMaxHp(self):
        """获取宠物的最大血量"""
#        fateattrs = self.getAllFateAttr()
        level = self._owner.level.getLevel()
        vit = self.VitGrowth*level/GROW_ATTR
        maxhp = int(vit*MAXHP_VIT)
        return maxhp

    def getHp(self):
        """获取角色当前血量"""
        if self.hp>self.getMaxHp():
            self.updateHp(self.getMaxHp())
        return self.hp

    def setHp(self,hp):
        """设置角色血量值
        """
        maxhp = self.getMaxHp()
        if hp>maxhp:
            self.hp = maxhp
        else:
            self.hp = hp

    def updateHp(self,hp):
        """更新角色血量值
        """
        maxhp = self.getMaxHp()
        if hp>maxhp:
            hp = maxhp
        elif hp<0:
            hp=0
        self.hp = hp

    def addHp(self,hp):
        """加血"""
        self.updateHp(self.getHp()+hp)

    def getAtrribute(self):
        """获取宠物的属性
        """
#        fateattrs = self.getAllFateAttr()
        level = self._owner.level.getLevel()
        info = {}
        info['Str'] = int(self.StrGrowth*level/GROW_ATTR)#力量
        info['Dex'] = self.DexGrowth*level*1.0/GROW_ATTR#敏捷
        info['Vit'] = int(self.VitGrowth*level/GROW_ATTR)#耐力
        info['Wis'] = int(self.WisGrowth*level/GROW_ATTR)#智力
        info['hp'] = self.hp#当前血量
        info['MaxHp'] = self.getMaxHp()#最大血量
        info['PhyAtt'] = int(info['Str']*PHYATT_STR)#物攻
        info['MigAtt'] = int(info['Wis']*MIGATT_WIS)#魔攻
        info['PhyDef'] = int(info['Str']*PHYDEF_STR + info['Vit']*PHYDEF_VIT)#物防
        info['MigDef'] = int(info['Wis']*MIGDEF_WIS + info['Vit']*MIGDEF_VIT)#魔防
        info['Speed'] = info['Dex']*5
        info['HitRate'] = int(100)
        info['Dodge'] = 5
        info['CriRate'] = 5
        info['power'] = 40
        info['Block'] = 0
        return info

    def getPetCurGrowth(self):
        """获取宠物当前成长信息"""
        info = {}
        info['StrGrowth'] = self.StrGrowth
        info['StrGrowthMax'] = self.StrGrowth
        info['WisGrowth'] = self.WisGrowth
        info['WisGrowthMax'] = self.WisGrowth
        info['VitGrowth'] = self.VitGrowth
        info['VitGrowthMax'] = self.VitGrowth
        info['DexGrowth'] = self.DexGrowth
        info['DexGrowthMax'] = self.DexGrowth

    def getPetQuality(self):
        """获取宠物品质"""
        goalGrowth = self.StrGrowth+self.VitGrowth+self.DexGrowth+self.WisGrowth#总成长
        if goalGrowth<80:
            quality = 1
        elif 80<=goalGrowth<100:
            quality = 2
        elif 100<=goalGrowth<120:
            quality = 3
        else:
            quality = 4
        return quality

    def PetTrain(self,traintype):
        """宠物培养
        @param traintype: int 培养类型
        """
        tamplateInfo = dbCharacterPet.PET_TEMPLATE.get(self._owner.templateId)
        quality  = tamplateInfo['baseQuality']
        info = Train(quality,traintype)
        maxgrowth = self.getMaxGrowth()
        self.StrGrowthAdd += min(info.get('StrGrowthAdd'),maxgrowth.get('StrGrowth')-self.StrGrowth)
        self.WisGrowthAdd += min(info.get('WisGrowthAdd'),maxgrowth.get('WisGrowth')-self.WisGrowth)
        self.VitGrowthAdd += min(info.get('VitGrowthAdd'),maxgrowth.get('VitGrowth')-self.VitGrowth)
        self.DexGrowthAdd += min(info.get('DexGrowthAdd'),maxgrowth.get('DexGrowth')-self.DexGrowth)
#        attrchange = self.CalculatePetGrowth()
#        trainData = {}
#        trainData['baseLiLiang'] = attrchange['basePhyAtt']#self.StrGrowth+self.StrGrowthAdd
#        trainData['changeLiLiang'] = attrchange['PhyAttChange']#self.StrGrowthAdd
#        trainData['baseZhiLi'] = attrchange['baseMigAtt']#self.WisGrowth+self.WisGrowthAdd
#        trainData['changeZhiLi'] = attrchange['MigAttChange']#self.WisGrowthAdd
#        trainData['baseNaiLi'] = attrchange['basePhyDef']#self.VitGrowth+self.VitGrowthAdd
#        trainData['changeNaiLi'] = attrchange['PhyDefChange']#self.VitGrowthAdd
#        trainData['baseMinJie'] = attrchange['baseMaxHp']#self.DexGrowth+self.DexGrowthAdd
#        trainData['changeMinJie'] = attrchange['MaxHpChange']#self.DexGrowthAdd
#        return True

    def CalculatePetGrowth(self):
        """计算宠物的培养后的属性加成
        """
        nowattr = self.getAtrribute()
        StrGrowth,self.StrGrowth = self.StrGrowth,self.StrGrowth+self.StrGrowthAdd
        DexGrowth,self.DexGrowth = self.DexGrowth,self.DexGrowth+self.DexGrowthAdd
        VitGrowth,self.VitGrowth = self.VitGrowth,self.VitGrowth+self.VitGrowthAdd
        WisGrowth,self.WisGrowth = self.WisGrowth,self.WisGrowth+self.WisGrowthAdd
        lastattr = self.getAtrribute()
        self.StrGrowth,self.DexGrowth,self.VitGrowth,self.WisGrowth = \
        StrGrowth,DexGrowth,VitGrowth,WisGrowth
        info = {}
        info['basePhyAtt'] = lastattr['PhyAtt']
        info['PhyAttChange'] = lastattr['PhyAtt'] - nowattr['PhyAtt']
        info['baseMigAtt'] = lastattr['MigAtt']
        info['MigAttChange'] = lastattr['MigAtt'] - nowattr['MigAtt']
        info['basePhyDef'] = lastattr['PhyDef']
        info['PhyDefChange'] = lastattr['PhyDef'] - nowattr['PhyDef']
        info['baseMaxHp'] = lastattr['MaxHp']
        info['MaxHpChange'] = lastattr['MaxHp'] - nowattr['MaxHp']
        return info

    def Tihuan(self):
        """宠物属性替换"""
        self.StrGrowth += self.StrGrowthAdd
        self.WisGrowth += self.WisGrowthAdd
        self.DexGrowth += self.DexGrowthAdd
        self.VitGrowth += self.VitGrowthAdd
        props = {}
        if self.StrGrowthAdd:
            props['StrGrowth'] = self.StrGrowth
        if self.StrGrowthAdd:
            props['WisGrowth'] = self.WisGrowth
        if self.StrGrowthAdd:
            props['DexGrowth'] = self.DexGrowth
        if self.StrGrowthAdd:
            props['VitGrowth'] = self.VitGrowth
        if props:
            petmode = tbpetadmin.getObj(self._owner.baseInfo.getId())
            petmode.update_multi(props)
#            dbCharacterPet.updatePetInfo(self._owner.baseInfo.id, props)
        self.StrGrowthAdd = 0
        self.WisGrowthAdd = 0
        self.DexGrowthAdd = 0
        self.VitGrowthAdd = 0
        return {'result':True,'message':u""}

    def getMaxGrowth(self):
        """获取宠物的最高属性成长
        """
        tamplateInfo = dbCharacterPet.PET_TEMPLATE.get(self._owner.templateId)
        attrtype = tamplateInfo['attrType']
        quality  = tamplateInfo['baseQuality']
        typeinfo = dbCharacterPet.PET_GROWTH.get(attrtype,{})
        growth = typeinfo.get(quality,{})
        return growth

#    def getAllFateAttr(self):
#        """获取所有的命格属性
#        """
#        from core.PlayersManager import PlayersManager
#        attrs = {}
#        palyer = PlayersManager().getPlayerByID(self._owner._owner)
#        if not palyer:
#            return attrs
#        for fateId in self._owner.fate.values():
#            fate = palyer.fate.fates.get(fateId)
#            info = fate.getFateAttr()
#            attrs = addDict(attrs, info)
#        return attrs

    def getAttrAdd(self):
        """获取武将的等级属性成长
        """
        info = {}
        info['petid'] = self._owner.baseInfo.id
        info['hpgrowth'] = self.VitGrowth*MAXHP_VIT/GROW_ATTR
        info['attgrowth'] = self.StrGrowth*PHYATT_STR/GROW_ATTR
        info['spgrowth'] = self.DexGrowth*0.5/GROW_ATTR
        info['defgrowth'] = self.StrGrowth*PHYDEF_STR/GROW_ATTR +\
                            self.VitGrowth*PHYDEF_VIT/GROW_ATTR
        return info




