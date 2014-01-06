#coding:utf8
"""
Created on 2011-9-5

@author: lan (www.9miao.com)
"""
from app.game.core.character.Character import Character
from app.share.dbopear import dbMonster

class Monster(Character):
    """怪物类
    """
    TotalSeed = 100000.0
    BOSSTYPE = 10 #boss的怪物类型
    
    def __init__(self,id = -1,name='',templateId= 0,x = 300,y = 400,matrixId = 0,rule = []):
        """初始化怪物类
        """
        data=dbMonster.All_MonsterInfo.get(templateId)
        Character.__init__(self, id, name)
        self.setCharacterType(Character.MONSTERTYPE)#设置角色类型为怪物类型
        self.templateId = int(data['id'])
        self.formatInfo = {}
        self.matrixId = matrixId
        self.rule = rule
        self.mconfig = 0
        self.initialiseToo(data)
        
    def initialiseToo(self,data):
        """初始化怪物信息
            @param id: int 怪物主键id
        """
        self.formatInfo['templateId'] = data['id']
        self.formatInfo['name'] = data['nickname']
        self.formatInfo['type']=data['viptype']
        self.formatInfo['level'] = data['level']
        self.formatInfo['difficulty'] = data.get('difficulty',1)
        self.formatInfo['hp'] = data['hp']
        self.formatInfo['mp'] = data['mp']
        self.formatInfo['speed'] = data['Speed']
        self.formatInfo['maxHp'] = data['hp']
        self.formatInfo['maxMp'] = data['mp']
        self.formatInfo['hitRate'] = data['Hit']
        self.formatInfo['criRate']=data['Force']
        self.formatInfo['block'] = 0
        self.formatInfo['dodgeRate']=data['Dodge']
        self.formatInfo['PhysicalAttack'] = data['PhysicalAttack']
        self.formatInfo['MagicAttack'] = data['MagicAttack']
        self.formatInfo['PhysicalDefense'] = data['PhysicalDefense']
        self.formatInfo['MagicDefense'] = data['MagicDefense']
        self.formatInfo['speed'] = data['Speed']
        self.formatInfo['resourceid'] = data['resourceid']
        self.formatInfo['dropoutid'] = data['dropoutid']
        self.formatInfo['ordSkill'] = data['ordSkill']
        self.formatInfo['skill'] = eval('['+data['skill']+']')
        self.formatInfo['moveable'] = data['moveable']
        self.formatInfo['expbound'] = data.get('expbound',100)
        self.formatInfo['icon'] = data.get('icon',100)
        self.formatInfo['type'] = data.get('type',100)
        
    def getMonsterType(self):
        """获取怪物的类型"""
        return self.formatInfo.get('type',1)
    
    def getMatrixId(self):
        """获取怪物的阵法ID"""
        return self.matrixId
    
    def setMatrixId(self,matrixId):
        """设置阵法的ID"""
        self.matrixId = matrixId
    
    def getRule(self):
        """获取怪物的阵法摆放规则"""
        return self.rule
    
    def setRule(self,rule):
        """设置阵法规则"""
        self.rule = rule
        
    def getMconfig(self):
        """获取怪物的场景配置ID
        """
        return self.mconfig
    
    def setMconfig(self,mconfig):
        """获取怪物的场景配置ID
        """
        self.mconfig = mconfig
    
    def getFightData(self):
        """获取怪物战斗数据"""
        fightdata = {}
        fightdata['chaId'] = self.baseInfo.id               #角色的ID
        fightdata['chaName'] = self.formatInfo['name']  #角色的昵称
        fightdata['chaLevel'] = self.formatInfo['level']#角色的等级
        fightdata['characterType'] = self.getCharacterType()#角色的类型  1:玩家角色 2:怪物 3:宠物
        fightdata['difficulty'] = self.formatInfo['difficulty']#怪物难度
        fightdata['figureType'] = self.formatInfo['templateId']
        fightdata['chaBattleId'] = 0                        #角色在战场中的id
        fightdata['chaProfessionType'] = self.formatInfo['resourceid']#角色的角色形象ID
        fightdata['chaIcon'] = self.formatInfo['icon']
        fightdata['chatype'] = self.formatInfo['type']
        fightdata['chaDirection'] = 1#(角色在战斗中的归属阵营)1--(主动方)玩家朝向右，朝向右。2(被动方)--玩家朝向左
        fightdata['chaCurrentHp'] = self.formatInfo['hp']#角色当前血量
        fightdata['chaCurrentPower'] = 0#角色的当前能量
        fightdata['chaTotalHp'] = self.formatInfo['maxHp']#角色的最大血量s
        fightdata['chaTotalPower'] = Character.MAXPOWER#角色的最大能量
        fightdata['chaPos'] = (0,0)#角色的坐标
        fightdata['physicalAttack'] = self.formatInfo['PhysicalAttack']#角色的物理攻击
        fightdata['magicAttack'] = self.formatInfo['MagicAttack']#角色的魔法攻击
        fightdata['physicalDefense'] = self.formatInfo['PhysicalDefense']#角色的物理防御
        fightdata['magicDefense'] = self.formatInfo['MagicDefense']#角色的魔法防御
        fightdata['speed'] = self.formatInfo['speed']#角色的攻速
        fightdata['hitRate'] = 100#self.formatInfo['hitRate']#角色的命中
        fightdata['critRate'] = self.formatInfo['criRate']#角色的当前暴击率
        fightdata['block'] = self.formatInfo['block']#角色抗暴
        fightdata['dodgeRate'] = self.formatInfo['dodgeRate']#角色的闪避几率
        fightdata['ActiveSkillList'] = self.formatInfo['skill'] #角色的主动攻击技能
        fightdata['ordSkill'] = self.formatInfo['ordSkill']#角色的普通攻击技能
        fightdata['canDoMagicSkill'] = 1#可否释放魔法技能
        fightdata['canDoPhysicalSkill'] = 1#可否释放物理技能
        fightdata['canDoOrdSkill'] = 1#可否进行普通攻击
        fightdata['canBeTreat'] = 1#可否被治疗
        fightdata['canBeAttacked'] = 1#可否被攻击
        fightdata['canDied'] = 1#是否可死亡
        fightdata['skillIDByAttack'] = 0#被攻击的技能的ID 普通攻击为 0
        fightdata['expbound'] = self.formatInfo.get('expbound',100)#经验奖励
        fightdata['chaPz'] = self.formatInfo['difficulty']
        fightdata['equip'] = {}
        return fightdata
