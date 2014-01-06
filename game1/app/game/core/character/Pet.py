#coding:utf8
"""
Created on 2012-5-29

@author: Administrator
"""
from .Character import Character
from app.game.component.level.PetLevelComponent import PetLevelComponent
from app.game.component.attribute.PetAttributeComponent import PetAttributeComponent
from app.share.dbopear import dbSkill
from twisted.python import log

from app.share.dbopear import dbCharacterPet
#import random
from app.game.memmode import tbpetadmin 


class Pet(Character):
    """宠物类"""
    
    def __init__(self,petId = 0,name = '',templateId = 0,owner = 0,level =1):
        """初始化宠物的信息"""
        #角色类型
        Character.__init__(self, petId, name)
        self.setCharacterType(self.PETTYPE)
        self.templateId = templateId
        self._owner = owner#宠物的拥有者的ID
        self.level = PetLevelComponent(self,level=level)
        self.attribute = PetAttributeComponent(self)
        self.chuancheng = False
        self._chuancheng = False
        self.fate = {}#宠物的命格
        self.position = (300,400)
        self.skill = []
        self.energy = 0
        #宠物是否跟随
        self.flowFlag = False
        if self.templateId:
            self.initData()
        
    def initData(self):
        """不存在实例时的初始化方式"""
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        if not templateinfo:
            log.err("Pet template %d not exits"%self.templateId)
        self.skill = [templateinfo.get('skill')] if templateinfo.get('skill') else []
        self.baseInfo.setName(templateinfo.get('nickname',''))
        StrGrowth = templateinfo.get('StrGrowth')
        WisGrowth = templateinfo.get('WisGrowth')
        VitGrowth = templateinfo.get('VitGrowth')
        DexGrowth = templateinfo.get('DexGrowth')
        self.attribute.initData(StrGrowth, WisGrowth, VitGrowth, DexGrowth, -1)
        
    def initItemInstance(self,petInstanceData):
        """存在数据库实例时的初始化方式"""
        self.templateId = petInstanceData.get('templateID')
        StrGrowth = petInstanceData.get('StrGrowth')
        WisGrowth = petInstanceData.get('WisGrowth')
        VitGrowth = petInstanceData.get('VitGrowth')
        DexGrowth = petInstanceData.get('DexGrowth')
        self._owner = petInstanceData.get('ownerID')
        hp = petInstanceData.get('hp')
        self.chuancheng = bool(petInstanceData.get('chuancheng'))
        self._chuancheng = bool(petInstanceData.get('_chuancheng'))
        self.flowFlag = bool(petInstanceData.get('showed'))
        self.attribute.initData(StrGrowth, WisGrowth, VitGrowth, DexGrowth, hp)
        self.level.setExp(petInstanceData.get('exp'))
        self.level.setLevel(petInstanceData.get('level'))
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        self.skill = [templateinfo.get('skill')] if templateinfo.get('skill') else []
        if petInstanceData.get('name'):
            self.baseInfo.setName(petInstanceData.get('name',''))
        else:
            self.baseInfo.setName(templateinfo.get('nickname',''))
            
    def getProvidedEnergy(self):
        """获取宠物能提供的能量
        """
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        goalEnergy = templateinfo.get('energy',0)+self.energy
        return goalEnergy
        
    @property
    def templateInfo(self):
        return dbCharacterPet.PET_TEMPLATE.get(self.templateId)
    
    def addEnergy(self,exp):
        """添加能量
        """
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        maxEnergy = templateinfo.get('maxenergy')
        self.energy+=exp
        if self.energy>=maxEnergy:
            self.energy-=maxEnergy
            self.templateId = templateinfo.get('growpet')
        prop = {'templateId':self.templateId,'energy':self.energy}
        petmode = tbpetadmin.getObj(self._owner.baseInfo.getId())
        petmode.update_multi(prop)
        
    def InsertIntoDB(self):
        """将不存在的实例写入数据库，生成数据库中的实例"""
        characterId = self._owner
        hp = self.attribute.getMaxHp()
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        StrGrowth = templateinfo.get('StrGrowth')
        WisGrowth = templateinfo.get('WisGrowth')
        VitGrowth = templateinfo.get('VitGrowth')
        DexGrowth = templateinfo.get('DexGrowth')
        level = self.level.getLevel()
        data = {'ownerID':characterId,
                'templateID':self.templateId,
                'name':u'',
                'level':level,
                'exp':0,
                'hp':hp,
                'StrGrowth':StrGrowth,
                'WisGrowth':WisGrowth,
                'VitGrowth':VitGrowth,
                'DexGrowth':DexGrowth,
                'showed':0,
                'chuancheng':0,
                '_chuancheng':0,}
        petmmode = tbpetadmin.new(data)
        petId = int(petmmode._name.split(':')[1])
#        petId = dbCharacterPet.InsertPetInfoInDB_new(characterId, self.templateId,
#                                            hp,StrGrowth,WisGrowth,
#                                            VitGrowth,DexGrowth,level)
        if petId:
            self.baseInfo.setId(petId)
            return True
        return False
    
    def destroyByDB(self):
        """删除宠物在数据库中的数据"""
        tbpetadmin.deleteMode(self.baseInfo.id)
#        result = dbCharacterPet.DelPetInfo(self.baseInfo.id)
        return True
    
    def updateFate(self,position,fateId):
        """设置宠物的命格"""
        self.fate[position] = fateId
    
    def Training(self,trainingLevel):
        """培养
        @param trainingLevel: int 培养的级别
        """
        data = self.attribute.PetTrain(trainingLevel)
        return data
    
    def Tihuan(self):
        """宠物属性替换
        """
        result = self.attribute.Tihuan()
        return result
        
#    def updatePosition(self,position,index,force = 0):
#        """更新宠物的坐标"""
#        positionRange = {1:(range(80,100),range(-100,-80)),
#                         2:(range(80,100),range(80,100)),
#                         3:(range(-100,-80),range(-100,-80)),
#                         4:(range(-100,-80),range(80,100)),
#                         5:(range(-20,20),range(80,100)),
#                         6:(range(-20,20),range(-100,-80)),
#                         7:(range(-100,-80),range(-20,20)),
#                         8:(range(80,100),range(-20,20)),
#                         }
#                         
#        _positionRange = {1:(range(-100,-80),range(-80,-40)),
#                         2:(range(-100,-80),range(40,80)),
#                         3:(range(-160,-120),range(-80,-40)),
#                         4:(range(-160,-120),range(40,80)),
#                         5:(range(-20,20),range(40,80)),
#                         6:(range(-20,20),range(-80,-40)),
#                         7:(range(80,100),range(-80,-40)),
#                         8:(range(-100,80),range(-80,-40))
#                         }
#        offsertX = random.choice(range(-100,100))
#        offsertY = random.choice(range(-100,100))#random.randint(-40,40)
#        self.position = (position[0]+offsertX,position[1]+offsertY)
        
    def getPosition(self):
        """获取宠物的位置"""
        return self.position
        
    
    def restorationHp(self,Surplus):
        """宠物回血"""
        cons = self.attribute.getMaxHp()-self.attribute.hp#消耗
        if cons< 0:
            return Surplus
        su = Surplus -cons
        if su>0:
            self.attribute.addHp(su)
            return su
        else:
            self.attribute.addHp(Surplus)
            return 0
        
    def formatPetInfo(self):
        """格式化宠物信息"""
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        attrinfo = self.attribute.getAtrribute()
        info = attrinfo
        if self.skill:
            skillInfo = dbSkill.ALL_SKILL_INFO.get(self.skill[0],{})
        else:
            skillInfo = {}
        info['id'] = self.baseInfo.getId()#宠物的实例ID
        info['name'] = self.baseInfo.getName()#宠物的名称
        info['desc'] = templateinfo.get('descript','')#描述
        info['flowFlag'] = self.flowFlag#释放更随
        info['inMatrixFlag'] = False#是否在阵法中
        info['texing'] = u""#特性
        info['icon'] = templateinfo.get('icon',0)#图标
        info['type'] = templateinfo.get('type',0)#图标路径
        info['resPetId'] = templateinfo.get('resourceid',0)#资源
        info['quality'] = self.attribute.getPetQuality()#品质
        info['skillname'] = skillInfo.get('skillName',u"")#技能
        info['jnicon'] = skillInfo.get('icon',0)#技能图标
        info['level'] = self.level.getLevel()#等级
        info['exp'] = self.level.getExp()#经验
        info['maxExp'] = self.level.getMaxExp()#升级经验
        info['shenjia'] = templateinfo.get('coin',0)
        info['manualHp'] = 0#最大血量加成
        info['manualPhyAttack'] = 0#物攻加成
        info['manualMagicAttack'] = 0#魔攻加成
        info['manualPhyDefense'] = 0#物防加成
        info['manualMagicDefense'] = 0#魔防加成
        info['manualHitRate'] = 0#命中
        info['manualDodgeRate'] = 0#闪避加成
        info['manualSpeed'] = 0#攻速加成
        info['manualCritRate'] = 0#暴击加成
        info['manualBlock'] = 0#格挡加成
        return info
    
    def SerializationPetInfo(self,bearer):
        """序列化宠物信息"""
        info = self.formatPetInfo()
        bearer.petId = info['id']
        bearer.resPetId = info['resPetId']
        bearer.petName = info['name']
        bearer.petLevel = info['level']
        bearer.inMatrixFlag = info['inMatrixFlag']
        bearer.petDes = info['desc']
        bearer.baseHp = info['hp']
        bearer.manualHp = info['manualHp']
        bearer.basePhyAttack = info['PhyAtt']
        bearer.manualPhyAttack = info['manualPhyAttack']
        bearer.baseMagicAttack = info['MigAtt']
        bearer.manualMagicAttack = info['manualMagicAttack']
        bearer.basePhyDefense = info['PhyDef']
        bearer.manualPhyDefense = info['manualPhyDefense']
        bearer.baseMagicDefense = info['MigDef']
        bearer.manualMagicDefense = info['manualMagicDefense']
        bearer.baseHitRate = info['HitRate']
        bearer.manualHitRate = info['manualHitRate']
        bearer.baseDodgeRate = info['Dodge']
        bearer.manualDodgeRate = info['manualDodgeRate']
        bearer.petName = info['name']
        bearer.baseSpeed = info['Speed']
        bearer.manualSpeed = info['manualSpeed']
        bearer.baseCritRate = info['CriRate']
        bearer.manualCritRate = info['manualCritRate']
        bearer.baseBlock = info['Block']
        bearer.manualBlock = info['manualBlock']
        bearer.icon = info['icon']
        bearer.type = info['type']
        bearer.petSkillInfo = info['skillname']
        bearer.flowFlag = info['flowFlag']
        bearer.liliang = info['Str']
        bearer.zhili = info['Wis']
        bearer.naili = info['Vit']
        bearer.minjie = info['Dex']
        bearer.maxHp = info['MaxHp']
        bearer.curExp = info['exp']
        bearer.maxExp = info['maxExp']
        bearer.curQuality = info['quality']
        bearer.texing = info['texing']
        return bearer
        
    def getFightData(self):
        """获取怪物战斗数据"""
        info = self.formatPetInfo()
        templateinfo = dbCharacterPet.PET_TEMPLATE.get(self.templateId)
        fightdata = {}
        fightdata['chaId'] = self.baseInfo.id           #角色的ID
        fightdata['chaName'] = self.baseInfo.getName()  #角色的昵称
        fightdata['chaLevel'] = self.level.getLevel()#角色的等级
        fightdata['characterType'] = self.getCharacterType()#角色的类型  1:玩家角色 2:怪物 3:宠物
        fightdata['figureType'] = info['resPetId']
        fightdata['chaBattleId'] = 0                        #角色在战场中的id
        fightdata['difficulty'] = self.attribute.getPetQuality()#怪物难度
        fightdata['chaProfessionType'] = info['resPetId']#角色的角色形象ID
        fightdata['chaIcon'] = info['icon']
        fightdata['chatype'] = info['type']
        fightdata['chaDirection'] = 1#(角色在战斗中的归属阵营)1--(主动方)玩家朝向右，朝向右。2(被动方)--玩家朝向左
        fightdata['chaCurrentHp'] = info['MaxHp']#角色当前血量
        fightdata['chaCurrentPower'] = info['power']#角色的当前能量
        fightdata['chaTotalHp'] = info['MaxHp']#角色的最大血量s
        fightdata['chaTotalPower'] = Character.MAXPOWER#角色的最大能量
        fightdata['chaPos'] = (0,0)#角色的坐标
        fightdata['physicalAttack'] = info['PhyAtt']+info['manualPhyAttack']#角色的物理攻击
        fightdata['magicAttack'] = info['MigAtt']+info['manualMagicAttack']#角色的魔法攻击
        fightdata['physicalDefense'] = info['PhyDef']+info['manualPhyDefense']#角色的物理防御
        fightdata['magicDefense'] = info['MigDef']+info['manualMagicDefense']#角色的魔法防御
        fightdata['speed'] = info['Speed']+info['manualSpeed']#角色的攻速
        fightdata['hitRate'] = info['HitRate']+info['manualHitRate']#角色的命中
        fightdata['critRate'] = info['CriRate']+info['manualCritRate']#角色的当前暴击率
        fightdata['block'] = info['Block']+info['manualBlock']
        fightdata['dodgeRate'] = info['Dodge']+info['manualDodgeRate']#角色的闪避几率
        fightdata['ActiveSkillList'] = self.skill#self.skill#角色的主动攻击技能
        fightdata['ordSkill'] = templateinfo.get('ordSkill')#角色的普通攻击技能
        fightdata['canDoMagicSkill'] = 1#可否释放魔法技能
        fightdata['canDoPhysicalSkill'] = 1#可否释放物理技能
        fightdata['canDoOrdSkill'] = 1#可否进行普通攻击
        fightdata['canBeTreat'] = 1#可否被治疗
        fightdata['canBeAttacked'] = 1#可否被攻击
        fightdata['canDied'] = 1#是否可死亡
        fightdata['skillIDByAttack'] = 0#被攻击的技能的ID 普通攻击为 0
        fightdata['expbound'] = 0#经验奖励
        fightdata['equip'] = {}
        fightdata['chaPz'] = self.attribute.getPetQuality()
        return fightdata
        
    def formatInfoForWeiXin(self):
        """格式化角色信息
        """
        attrinfo = self.getFightData()
        info = {}
        info['chaid'] = attrinfo['chaId']
        info['chatype'] = 3
        info['tempid'] = self.templateId
        info['rolename'] = attrinfo['chaName']
        info['icon'] = attrinfo['chaIcon']
        info['level'] = attrinfo['chaLevel']
        info['guanqia'] = u'无'
        skillinfo = dbSkill.ALL_SKILL_INFO.get(self.skill[0])
        info['skill'] = u'无' if not skillinfo else skillinfo['skillName']
        info['attack'] = attrinfo.get('physicalAttack',0)
        info['fangyu'] = attrinfo.get('physicalDefense',0)
        info['tili'] = attrinfo['chaTotalHp']
        info['minjie'] = self.attribute.getPetQuality()
        info['price'] = self.level.getLevel()*1000
        info['exp'] = self.energy
        return info    
    
    
        
