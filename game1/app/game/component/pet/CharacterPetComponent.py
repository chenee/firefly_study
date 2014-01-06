#coding:utf8
"""
Created on 2011-12-14
角色的宠物信息
@author: lan (www.9miao.com)
"""
from app.game.component.Component import Component
from app.game.core.character.Pet import Pet
import random
from app.game.memmode import tbpetadmin


MAXPETCNT = 10 #拥有宠物的最大数量
CATCHPETTASKTYPE = 107
RATE_BASE = 100000#几率基础值

ERROR = {-5:u""}
PETTRAINCOINCONS = {1:{'itemcnt':1,'coin':200,'gold':0},
                    2:{'itemcnt':1,'coin':0,'gold':20},
                    3:{'itemcnt':10,'coin':2000,'gold':0},
                    4:{'itemcnt':10,'coin':0,'gold':200},
                    }
PETTRAINGOLDCONS = {1:{'gold':30,'vip':1},
                2:{'gold':80,'vip':3},
                3:{'gold':200,'vip':5}}#宠物培养消耗
#技能消耗品的ID
SKILLCRYSTAL = {1:20030061,
                2:20030062,
                3:20030063,
                4:20030064,
                5:20030065}

TRAIN_ITEM_REQUIRED = 42004026

RESURCUS = 10 #宠物复活消耗

CANCATCHPET = {1:1,2:2,3:4}

class CharacterPetComponent(Component):
    """角色的宠物信息类"""
    
    def __init__(self,owner):
        """init Object"""
        Component.__init__(self, owner)
        #角色的宠物列表
        self._pets = {}
#        #已经收集到的宠物
#        self._activepets = []
        #获取宠物消息的队列
        self._getPetMsg = []
        #宠物的移动频率
        self._moveTag = 0
        #最后丢弃的宠物的ID
        self.lastRemove = []
        
    def initCharacterPetInfo(self):
        """初始化角色宠物信息"""
        pid = self._owner.baseInfo.id
        petlist = tbpetadmin.getAllPkByFk(pid)
#        petlist = dbCharacterPet.getCharacterAllPet(self._owner.baseInfo.id)
        petobjlist = tbpetadmin.getObjList(petlist)
        for petmmode in petobjlist:
            petId = int(petmmode._name.split(':')[1])
            pet = Pet(petId = petId)
            itemPackInfo = petmmode.get('data')
            pet.initItemInstance(itemPackInfo)
            self._pets[petId] = pet
        
    def getNowShowCnt(self):
        """设置现在跟随的宠物的数量"""
        return len([pet for pet in self._pets.values() if pet.getFlowFlag()])
        
    def checkCanFlow(self):
        """检查是否还能设置宠物设置"""
        return False
        
    def getPets(self):
        """获取角色的宠物列表"""
        return self._pets
    
    def getHasPetTemplatelist(self):
        """获取已经获取的宠物的模版列表
        """
        return [pet.templateId for pet in self._pets.values()]
        
    def formatCharacterPetListInfo(self):
        """格式或角色的宠物信息"""
        pets = self.getPets()
        return pets.values()
    
    def FormatPetList(self):
        """格式货所有宠物的信息
        """
        petinfolist = []
        pets = self.getPets()
        friendlist = self._owner.friend.getGuYongList()
        real_friendlist = []
        for friend in friendlist:
            petid = friend['chaid']
            if self.IsInMatrix(petid):
                continue
            real_friendlist.append(friend)
        for pet in pets.values():
            petid = pet.baseInfo.getId()
            if self.IsInMatrix(petid):
                continue
            info = pet.formatInfoForWeiXin()
            petinfolist.append(info)
        return {'petlist':petinfolist+real_friendlist}
    
    def getCharacterPetListInfo(self):
        """获取角色宠物列表"""
        pets = self.getPets()
        PetListInfo = {}
        PetListInfo['curPetNum'] = len(pets)
        PetListInfo['maxPetNum'] = MAXPETCNT
        PetListInfo['petInfo'] = []
        for pet in pets.values():
            info = {}
            petId = pet.baseInfo.getId()
            info['petId'] = pet.baseInfo.getId()
            info['resPetId'] = pet.templateInfo.get('resourceid')
            info['petName'] = pet.baseInfo.getName()
            info['petLevel'] = pet.level.getLevel()
            info['sz'] = self.IsInMatrix(petId)
            info['pinzhi'] = pet.attribute.getPetQuality()
            PetListInfo['petInfo'].append(info)
        return PetListInfo
    
    def getPetNum(self):
        """获取当前宠物的数量"""
        pets = self.getPets()
        return len(pets)
    
    def ishavepet(self):
        """判断是否有蜻蜓猎手宠物"""
        for info in self._pets.values():
            if info.templateId==15004:
                return True
        return False
    
    def OpenPetEgg(self,level = 1):
        """打开宠物蛋
        """
        if level==1:
            petlist = [25085,25086,25087,25088,25089,25090,25091,25092,25093,25095,25096,25097,25098,25099,25100,25101,25102,25103,25104,25105,25106,25107,25108,25109,25110,35001,35002,35003,35004,35005,35006,25001,25002,25003,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        else:
            petlist = [25013,25014,25015,25016,25017,25018,25019,25020,25021,25022,25025,25026,25027,25029,25030,25031,25032,25033,25034,25035,25044,25045,25046,25048,25049,25050,25051,25052,25053,25054,25055,35080,35081,35082,35083,35084,35085,35086,25001,25002,25003,25004,25062,25063,25064,25065,25066,25067,25068,25069,25070,25071,25072,25073,35049,35050,35051]
        self._OpenPetEgg(petlist)
    
    def _OpenPetEgg(self,petlist):
        """打开宠物蛋"""
        petId = random.choice(petlist)
        quality = random.randint(1,7)
        result = self.addPet(templateId = petId, quality=quality)
        if result==-1:
            raise Exception(u"")
        elif result==-2:
            raise Exception(u"")
        
    def OpenOrdEgg(self,templateId,quality = 1):
        """打卡普通宠物蛋"""
        result = self.addPet(templateId,quality = 1)
        if result == -1:
            raise Exception(u"")
        elif result == -2:
            raise Exception(u"")
            
    def openRandEgg(self,petlist,default):
        """打开随机宠物蛋
        @param petlist: list [(宠物ID，随机区间)]随机掉落
        @param default: 宠物的ID 默认掉落
        """
        petsrates = [petinfo[1] for petinfo in petlist]
        petid = 0
        rate = random.randint(0,RATE_BASE)
        for index in range(len(petlist)):
            if rate<sum(petsrates[:index+1]):
                petid = petlist[index][0]
                break
        if not petid:
            petid = default
        result = self.addPet(petid)
        if result==-1:
            raise Exception(u"")
        elif result==-2:
            raise Exception(u"")
            
    def hasThisType(self,templateId):
        """判断是否已经存在该种类型的宠物
        """
        return templateId in [pet.templateId for pet in self._pets.values()]
        
    def addPet(self,templateId,quality = 1,level =1,statu = 1):
        """添加一个宠物"""
        if self.getPetNum()>=MAXPETCNT:
            return -1#宠物数量达到上限
        pet = Pet(templateId = templateId,level=level,owner = self._owner.baseInfo.id)
        result = pet.InsertIntoDB()
        if result:
            self._pets[pet.baseInfo.id] = pet
            return 1
        
    def DropPet(self,petId):
        """丢弃宠物
        @param petId: int 宠物的id
        """
        if petId not in self._pets.keys():
            return -5#不存在该宠物
        pet = self._pets.get(petId)
        result = pet.destroyByDB()
        if result:
            result = self._owner.matrix.dropPetInMatrix(petId)
            del self._pets[petId]
            return 1
        return 0
    
    def addLastRemove(self,petId):
        """添加宠物移除列表
        """
        self.lastRemove.append(petId)
    
    def popLastRemove(self):
        """取出并清空宠物移除列表"""
        removelist = list(self.lastRemove)
        self.lastRemove = []
        return removelist
    
    def checkCanTrain(self,ttype):
        """检测是否能培养"""
        info = self.getOwnItem()
        required = PETTRAINCOINCONS.get(ttype)
        if info['itemcnt']>=required['itemcnt'] and \
                 info['coin']>=required['coin'] and \
                 info['coin']>=required['coin']:
            return True
        return False
    
    def trainCons(self,ttype):
        """培养消耗处理
        """
        required = PETTRAINCOINCONS.get(ttype)
        coin = required['coin']
        gold = required['gold']
        itemcnt = required['itemcnt']
        if coin:
            self._owner.finance.addCoin(-coin)
        if gold:
            self._owner.finance.consGold(-gold)
        if itemcnt:
            self._owner.pack.delItemByTemplateId(TRAIN_ITEM_REQUIRED,itemcnt)
             
    def getTrainingInfo(self,petId):
        """获取培养信息
        """
        pet = self._pets.get(petId)
        if not pet:
            return {'result':False,'message':u'宠物信息不存在'}
        petinfo = pet.FormatPetInfo()
        trianpetinfo = {}
        trianpetinfo['petId'] = petId
        trianpetinfo['icon'] = petinfo['resId']
        trianpetinfo['name '] = petinfo['name']
        trianpetinfo['level '] = petinfo['level']
        trianpetinfo['pinzhi '] = petinfo['pinzhi']
        trianpetinfo['hp'] = petinfo['hp']
        trianpetinfo['wg'] = petinfo['wg']
        trianpetinfo['wf'] = petinfo['wf']
        trianpetinfo['mj'] = petinfo['mj']
#        trianpetinfo['bj'] = petinfo['bj']
#        trianpetinfo['shb'] = petinfo['shb']
        return trianpetinfo
    
    def calculateTrian(self,oldinfo,nowinfo):
        """计算培养前后的增量
        """
        calculateInfo = nowinfo
        calculateInfo['hpadd'] = nowinfo['hp'] - oldinfo['hp']
        calculateInfo['wgadd'] = nowinfo['wg'] - oldinfo['wg']
        calculateInfo['wfadd'] = nowinfo['wf'] - oldinfo['wf']
        calculateInfo['mjadd'] = nowinfo['mj'] - oldinfo['mj']
#        calculateInfo['bjadd'] = nowinfo['bj'] - oldinfo['bj']
#        calculateInfo['shbadd'] = nowinfo['shb'] - oldinfo['shb']
        return calculateInfo
        
    def getOwnItem(self):
        """获取持有训练
        """
        info = {}
        nowcnt = self._owner.pack._package.countItemTemplateId(TRAIN_ITEM_REQUIRED)
        info['itemcnt'] = nowcnt
        info['coin'] = self._owner.finance.getCoin()
        info['gold'] = self._owner.finance.getGold()
        return info
        
    def Training(self,petId,ttype,tag):
        """宠物培养
        @param petId: int 宠物的id
        @param trainingLevel: int 培养的层次
        """
#        if self._owner.level.getLevel()<10:#功能等级限制
#            return {'result':False,'message':Lg().g(429)}
        if petId not in self._pets.keys():
            return {'result':False,'message':u""}#
        if tag==0:
            info = self.getTrainingInfo(petId)
            petinfo = self.calculateTrian(info, info)
            owninfo = self.getOwnItem()
            owninfo['petinfo'] = petinfo
            return {'result':False,'data':owninfo}#
        if not self.checkCanTrain(ttype):
            return {'result':False,'message':u""}#
        pet = self._pets.get(petId)
        oldinfo = self.getTrainingInfo(petId)
        if ttype==1:
            pet.Training(ttype)
        elif ttype==2:
            pet.Training(2)
        elif ttype==3:
            for _ in range(10):
                pet.Training(1)
        else:
            for _ in range(10):
                pet.Training(2)
        self.trainCons(ttype)
        self.Tihuan(petId, 1)
        newinfo = self.getTrainingInfo(petId)
        petinfo = self.calculateTrian(oldinfo, newinfo)
        owninfo = self.getOwnItem()
        owninfo['petinfo'] = petinfo
        return {'result':False,'data':owninfo}
    
    def Tihuan(self,petId,tihuanType):
        """替换宠物成长
        @param petId: int 宠物的id
        @param tihuanType: int 操作类型0维持1替换
        """
        if not tihuanType:
            return {'result':True}
        if petId not in self._pets.keys():
            return {'result':False,'message':u""}#
        pet = self._pets.get(petId)
        result = pet.Tihuan()
        return result
        
        
    def getPet(self,petId):
        """获取指定的宠物"""
        return self._pets.get(petId)
        
    def IsInMatrix(self,petId):
        """判断宠物是否在阵法中
        """
        return self._owner.matrix.IsInMatrix(petId)
        
    def swallow(self,petId,eatlist):
        """武将吞噬
        """
        if not eatlist:
            return {'result':False,'message':u""}
        topet = self.getPet(petId)
        if topet.level.getLevel()>=self._owner.level.getLevel():
            return {'result':False,'message':u"武将最大等级不能超过主公"}
        if not set(eatlist).issubset(set(self._pets.keys())):
            return {'result':False,'message':u"被吞噬的武将信息不存在%s"%eatlist}
        expgoal = sum([self._pets[fpetid].level.getAllExp() for fpetid in eatlist])
        topet.level.addExp(expgoal)
        for _pid in eatlist:
            self.DropPet(_pid)
        return {'result':True}
        
    def getPetAttrAdd(self,petId):
        """获取武将的属性等级成长
        """
        topet = self.getPet(petId)
        if not topet:
            return {'result':False,'message':u""}
        petlevel = topet.level.getLevel()
        if petlevel>=self._owner.level.getLevel():
            return {'result':False,'message':u'武将等级不能超过主公'}
        data = topet.attribute.getAttrAdd()
        return {'result':True,'data':data}
    
    def SwallowPet(self,petid,tpetid):
        """武将吞噬
        """
        pet = self.getPet(petid)
        tpet = self.getPet(tpetid)
        if not (pet and tpet):
            return {'result':False}
        energy = tpet.getProvidedEnergy()#获取武将能提供的能量
        pet.addEnergy(energy)
        self.DropPet(tpetid)
        return {'result':True}
        
        
