#coding:utf8
"""
Created on 2012-5-14

@author: Administrator
"""
from app.game.component.Component import Component
from app.share.dbopear import dbProfession
import time

HPDRUG = [20000000,20000001,20000002]
ENERGY_TIME = 1800#隔30分钟涨一点活力

class CharacterAttributeComponent(Component):

    MAXENERGY = 30
    """角色属性组件类"""
    def __init__(self, owner,hp = 100, mp = 100, energy = 200):
        """
        Constructor
        """
        Component.__init__(self, owner)

        self._hp = hp #当前生命:
        self._mp = mp #目前的法力ֵ
        self._energy = energy #当前活力
        self._timestamp = time.time()


#===================获取当前等级一级基础属性================================
    def getExpEff(self):
        """获取经验获取百分比"""
        effectExpEff = 1#self._owner.effect.getEffectInfo().get('ExpEff',0)
        return effectExpEff


    def getLevelStr(self):
        """获取当前等级基础力量"""
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelStr = level*dbProfession.tb_Profession_Config[profession]['perLevelStr']
        return levelStr

    def getLevelDex(self):
        """获取当前等级基础敏捷"""
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelDex = level*dbProfession.tb_Profession_Config[profession]['perLevelDex']
        return levelDex

    def getLevelVit(self):
        """获取当前等级基础耐力"""
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelVit = level*dbProfession.tb_Profession_Config[profession]['perLevelVit']
        return levelVit

    def getLevelWis(self):
        """获取当前等级智力"""
        profession = self._owner.profession.getProfession()
        level = self._owner.level.getLevel()
        levelWis = level*dbProfession.tb_Profession_Config[profession]['perLevelWis']
        return levelWis

#========================================================

    def getHp(self):
        """获取角色当前血量"""
        if self._hp>self.getMaxHp():
            self.updateHp(self.getMaxHp())
        return self._hp

    def setHp(self,hp):
        """设置角色血量值
        """
        maxhp = self.getMaxHp()
        if hp>maxhp:
            self._hp = maxhp
        else:
            self._hp = hp

    def updateHp(self,hp,state = 1):
        """更新角色血量值
        """
        maxhp = self.getMaxHp()
        if hp>maxhp:
            hp = maxhp
        elif hp<=0:
            hp=1
        self._hp = hp

    def addHp(self,hp):
        """加血"""
        self.updateHp(self.getHp()+hp)

    def Restoration(self):
        """恢复角色满状态
        """
        self.setHp(self.getMaxHp())

    def getMp(self):
        """获取角色当前魔力值"""
        if self._hp>self.getMaxMp():
            self.updateMp(self.getMaxMp())
        return self._mp

    def setMp(self,mp):
        """设置角色魔力值
        """
        if self._owner.level.getLevel() == 1 and self._owner.level.getExp()== 0:
            self.updateMp(self.getMaxMp())
        else:
            self._mp = mp

    def updateMp(self,mp):
        """更新角色魔力值
        """
        maxmp = self.getMaxMp()
        if mp>maxmp:
            mp = maxmp
        elif mp<0:
            mp=0
        self._mp = mp

    def addMp(self,mp):
        """加蓝"""
        self.updateMp(self.getMp()+mp)

    def getEnergy(self):
        """获取角色当前活力值"""
        energyadd = self.calculateEnergy()
        self._energy = self._energy+energyadd
        return self._energy

    def calculateEnergy(self):
        """计算活力增长值
        """
        nowtime = time.time()
        delta = int(nowtime-self._timestamp)
        energy = delta/ENERGY_TIME
        self._timestamp += energy*ENERGY_TIME
        return energy

    def initEnergy(self,energy):
        """初始化活力
        """
        outtime = 0
        now = int(time.time())
        t1 = int(now)/ENERGY_TIME
        t2 = int(outtime)/ENERGY_TIME
        energyadd = int(t1 - t2)
        sptime = int(now)%ENERGY_TIME
        self._timestamp = now-sptime
        nowenergy = energy+energyadd
        self.setEnergy(nowenergy)

    def setEnergy(self,energy):
        """设置角色活力
        """
        if energy>self.MAXENERGY:
            self._energy = self.MAXENERGY
        else:
            self._energy = energy

    def updateEnergy(self,energy):
        """更新角色活力
        """
        maxEnergy = self.MAXENERGY
        if energy>maxEnergy:
            energy = maxEnergy
        elif energy<0:
            energy=0
        self._energy = energy

    def addEnergy(self,energy):
        """加活力"""
        nowenergy =  self._energy + energy
        self.setEnergy(nowenergy)


    def getMaxHp(self):
        """
                    计算当前最大HP
        """
        EquipAttr = self._owner.pack.getAllEquipttributes()#所有装备的属性效果（包括套装）
        profession = self._owner.profession.getProfession()
        attrper = dbProfession.tb_Profession_Config[profession]
        nowVit = self.getLevelVit()
        baseMaxHp = int(nowVit*attrper.get('perHPVit',1)+EquipAttr.get('MaxHp',0))
        MaxHp = int(baseMaxHp*(1+EquipAttr.get('MaxHpPercen',0)))
        return MaxHp

    def getCharacterAttr(self):
        """获取角色的所有属性
        """
        EquipAttr = self._owner.pack.getAllEquipttributes()#所有装备的属性效果（包括套装）
        profession = self._owner.profession.getProfession()
        attrper = dbProfession.tb_Profession_Config[profession]
        info = {}
        baseStr = self.getLevelStr()
        baseDex = self.getLevelDex()
        baseVit = self.getLevelVit()
        baseWis = self.getLevelWis()
        info['Str'] = int(baseStr)
        info['Dex'] = int(baseDex)
        info['Vit'] = int(baseVit)
        info['Wis'] = int(baseWis)
        #过渡参数
        baseMaxHp = int(info['Vit']*attrper.get('perHPVit',1)+\
                        EquipAttr.get('MaxHp',0))
        basePhyAtt = int(info['Str']*attrper.get('perPhyAttStr',1)+\
                         EquipAttr.get('PhyAtt',0))
        basePhyDef = int(info['Str']*attrper.get('perPhyDefStr',1)+\
                         info['Vit']*attrper.get('perPhyDefVit',1)+\
                         EquipAttr.get('PhyDef',0))
        baseMigAtt = int(info['Wis']*attrper.get('perMigAttWis',1)+\
                         EquipAttr.get('MigAtt',0))
        baseMigDef = int(info['Wis']*attrper.get('perMigDefWis',1)+\
                         info['Vit']*attrper.get('perMigDefVit',1)+\
                         EquipAttr.get('MigDef',0))
        #二级属性
        info['MaxHp'] = int(baseMaxHp*(1+EquipAttr.get('MaxHpPercen',0)))
        info['power'] = EquipAttr.get('power',0)
        info['PhyAtt'] = int(basePhyAtt*(1+EquipAttr.get('PhyAttPercen',0)))
        info['PhyDef'] = int(basePhyDef*(1+EquipAttr.get('PhyDefPercen',0)))
        info['MigAtt'] = int(baseMigAtt*(1+EquipAttr.get('MigAttPercen',0)))
        info['MigDef'] = int(baseMigDef*(1+EquipAttr.get('MigDefPercen',0)))
        info['HitRate'] = 100 + EquipAttr.get('HitRate',0)
        info['Dodge'] = EquipAttr.get('Dodge',0)
        info['CriRate'] = 5 + EquipAttr.get('CriRate',0)
        info['Speed'] = int(info['Dex']*attrper.get('perSpeedDex',1) +\
                            EquipAttr.get('Speed',0))+40
        info['Block'] = EquipAttr.get('Block',0)
        info['Skill'] = list(set(EquipAttr.get('Skill',[])))
        return info




