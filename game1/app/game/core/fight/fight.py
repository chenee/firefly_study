#coding:utf8
"""
Created on 2011-9-2
战斗类
战场ID分配规则
2位数 第一位 表示战斗阵营 1主动 2被动方
后一位表示阵眼的位置
@author: lan (www.9miao.com)
"""
#from core.PlayersManager import PlayersManager
import random,math
from app.game.core.fight.BattleStateMachine import BattleStateMachine
from app.share.dbopear import dbSkill

import copy


POWEREFFECTID = 0
HITDISTANCE = 60#打击距离
#战斗发起方
ActiveSidePosition = {1:(413,417),2:(495,447),3:(585,484),
                      4:(353,444),5:(433,473),6:(525,510),
                      7:(272,478),8:(352,506),9:(442,543)}
#被攻击方
PassiveSidePosition = {1:(766,241),2:(849,272),3:(938,307),
                      4:(838,220),5:(920,248),6:(1008,284),
                      7:(899,193),8:(980,222),9:(1071,258)}

DODGEEFFECT = 9999#闪避的文字特效
IGNOREEFFECT = 9998#破防的文字特效
COUNTERATTACK = 9997#反击的文字特效
CRITEFFECT = 9996#暴击的文字特效
CATCHPETEFF = 9995 #抓宠成功的特效
IMMUNITYEFFECT = 0#免疫的文字特效
BOSSDIFFICULTY = 5#boss的困难标识
CATCHPETSKILLGROUP = 8108 #抓宠技能的技能组ID
POWATTUP = 0 #攻击方每次能量增长
POWDEFUP = 0 #被攻击方每次能量增长


#抓宠的方法
############################################
#CATCHRANGE = {1:range(65,217),2:range(9,217),3:range(1,217)}

#伤害计算公式
def DamageFormula(actor,enemy,attackType,skillFormulass,state = 1):
    """伤害计算公式"""
    defense = {1:enemy['physicalDefense'],
               2:enemy['magicDefense']}.get(attackType,0)
    attack = 0
    exec(skillFormulass)
    if attack<=0:
        return attack
    hurt =  int(round(attack-defense)+random.randint(1,5))
    if enemy['chaLevel']<20:
        hurt =  int(round(attack-defense)+random.randint(1,5))
    else:
        hurt =  int(max(round((attack - defense)+random.randint(1,10)),
                   10+random.randint(10,60)))
    if hurt < 0 and state == 2:
        hurt = 1
    return hurt


class Fight:
    """战斗类"""
    
    WIDTH = 1000    #战场的宽度
    HEIGHT = 570    #战场的高度
    MOVEABLE = 300  #活动区域的起始纵坐标
    DISTANCE_X = 100    #角色在X轴上得距离
    DISTANCE_Y = 50     #角色在Y轴上得距离
    DISTANCE_PHA = 120  #方阵到中心点的间距
    MAX_ROUND = 30  #战斗的最大回合数
    
    def __init__(self,activeSide,passiveSide,center):
        """初始化战斗类
        @param center: int 碰撞点的坐标
        @param activeSide: 攻击方
        @param passiveSide: 防守方
        """
        self.ActiveSidePosition = ActiveSidePosition    #主动方的方阵坐标
        self.PassiveSidePosition = PassiveSidePosition   #被动方的方阵坐标
        self.activeSide = activeSide    #主动方对象
        self.passiveSide = passiveSide  #被动方对象
        self.alord = 0                  #主攻方主将
        self.plord = 0                  #被攻击方主将
        self.fighters = {}              #所有战斗成员数据{chaBattleId:fightdata}
        self.center = center            #战斗碰撞点的坐标
        self.activeList = []            #主动方的成员的战场id列表
        self.passiveList = []           #被动方得成员的战场id列表
        self.order = []                 #战斗序列
        self.now_round = 0              #战斗的当前回合数
        self.FightData = []             #战斗产生的数据
        self.initData = []
        self.resources = set([0])             #战斗中用到的资源列表
        self.battleStateMachine = BattleStateMachine(self)#战斗的状态机
        self.fixBattleSidePosition()    #初始化战场
        self.battleResult = 1           #战斗结果
        self.hasboss = False            #战斗中是否有boss
        self.initOrder()                #安排出手顺序
        
        
    def initBattlefield(self):
        """初始化战场，确定战场中的每个位置"""
        if self.center<500:
            self.center=550
        x = 1
        y = 1
        for grid in range(1,10):
            apos = [self.center-self.DISTANCE_X*x-self.DISTANCE_PHA,\
                    self.MOVEABLE+y*self.DISTANCE_Y]
            #生成的主动方坐标
            ppos = [self.center+self.DISTANCE_X*x+self.DISTANCE_PHA,\
                    self.MOVEABLE+y*self.DISTANCE_Y]
            #生成的被动方坐标
            self.ActiveSidePosition[grid] = apos
            self.PassiveSidePosition[grid]= ppos
            y += 1
            if grid%3 ==0:
                x +=1
                y = 1
                
    def fixBattleSidePosition(self):
        """确定战斗成员的位置,初始化战场,初始化角色技能CD
        """
        alord = self.activeSide.getLord()
        plord = self.passiveSide.getLord()
        for activeMember in self.activeSide.getMembers():#初始化主动方
            eyeNo = self.activeSide.getCharacterEyeNo(activeMember['chaId'],
                                        characterType=activeMember['characterType'])
            activeMember['chaPos'] = eyeNo#初始角色的在战场中的位置
            activeMember['chaDirection'] = 1#设置角色的阵营
            battleId = 10 + eyeNo
            if activeMember['chaId']==alord:
                self.alord = battleId
            activeMember['chaBattleId'] = battleId#分配角色的战场Id
            activeMember['died'] = 0#角色是否死亡
            activeMember['nextReleaseSkill'] = 0#角色下次释放的技能序号
            activeMember['skillIDByAttack '] = 0#角色遭受的攻击的技能id
            activeMember['reactionAddition'] = 0#角色的反伤加成
            activeMember['skillCDRecord'] = [{'skillID':skillID,'traceCD':0} for\
                                              skillID in activeMember['ActiveSkillList']\
                                               if skillID>0]
            self.initData.append(copy.deepcopy(activeMember))
            self.fighters[10 + eyeNo] = activeMember
            self.activeList.append(10 + eyeNo)
            self.resources.add(activeMember['chaProfessionType']*1000+530)
            if activeMember['difficulty']==5:
                self.hasboss = True
            
        for passiveMember in self.passiveSide.getMembers():#初始化主动方
            eyeNo = self.passiveSide.getCharacterEyeNo(passiveMember['chaId'],
                                        characterType=passiveMember['characterType'])
            passiveMember['chaPos'] = eyeNo
            passiveMember['chaDirection'] = 2
            battleId = 20 + eyeNo
            if passiveMember['chaId']==plord:
                self.plord = battleId
            passiveMember['chaBattleId'] = 20 + eyeNo
            passiveMember['died'] = 0#角色是否死亡
            passiveMember['nextReleaseSkill'] = 0#角色下次释放的技能序号
            passiveMember['skillIDByAttack '] = 0#角色遭受的攻击的技能id
            passiveMember['reactionAddition'] = 0#角色的反伤加成
            passiveMember['skillCDRecord'] = [{'skillID':skillID,'traceCD':0}\
                         for skillID in passiveMember['ActiveSkillList']]
                            #角色是否技能的CD记录
            self.initData.append(copy.deepcopy(passiveMember))
            self.fighters[20 + eyeNo] = passiveMember
            self.passiveList.append(20 + eyeNo)
            self.resources.add(passiveMember['chaProfessionType']*1000+530)
            if passiveMember['difficulty']==5:
                self.hasboss = True
            
    def initOrder(self):
        """初始化战斗次序"""
        self.order = sorted(self.fighters.keys(),reverse=True,\
                            key = lambda d:self.fighters[d]['speed'])
        
    def findTarget(self,actorId,targetType=2,rule = 1):
        """寻找目标
        @param actorId: int 行动者的ID
        @param targetType: int 目标的类型  1己方 2敌方
        @param rule: int 查找规则 1单体 2全体
        """
        targetList = []#技能作用目标
        actorId_EyeNo = actorId%10      #根据行动者的id得到行动者所在阵法的位置
        actor = self.fighters[actorId]
        actorId_Camp = actor['chaDirection']       #根据行动者的id得到行动者所在战场的阵营
        if actorId_Camp ==1:
            enemyList = self.passiveList
            ownList = self.activeList
        else:
            enemyList = self.activeList
            ownList = self.passiveList
            
        lines = {1:[1,4,7],2:[2,5,8],3:[3,6,9]}#所有的行数
        rows = {1:[1,2,3],2:[4,5,6],3:[7,8,9]} #所有的列数
        ruleDict = {1:[1,2,3],2:[2,1,3],3:[3,2,1]}#不同行列的寻找对手规则
        for key,value in lines.items():
            if actorId_EyeNo in value:
                lineno = key   #目标列号
                break
        for key,value in rows.items():
            if actorId_EyeNo in value:
                rowno = key    #目标列号
                break
        
        if targetType == 1:#当目标位己方时
            target_Camp = actorId_Camp
            candidatelist = ownList #攻击的目标列表
            candidate = actorId     #攻击参照点
        else:#当目标位敌方时
            target_Camp = 3 - actorId_Camp
            candidatelist = enemyList
            dd = ruleDict.get(lineno)
            sequence = lines[dd[0]]+lines[dd[1]]+lines[dd[2]]
            candidatelist.sort(key= lambda d: sequence.index(d%10))
            candidate = candidatelist[0]
            candidate_EyeNo = candidate%10
            for key,value in lines.items():
                if candidate_EyeNo in value:
                    lineno = key   #目标列号
                    break
            for key,value in rows.items():
                if candidate_EyeNo in value:
                    rowno = key
                    break
            
        if rule ==1:#单体
            targetList = [candidate]
        elif rule ==2:#全体
            targetList = candidatelist
        elif rule ==3:#竖排
            targetList = [ ind+target_Camp*10 for ind in lines.get(lineno)]
            targetList = set(targetList).intersection(candidatelist)
        elif rule ==4:#横排
            targetList = [ ind+target_Camp*10 for ind in rows.get(rowno)]
            targetList = set(targetList).intersection(candidatelist)
        elif rule ==5:#后排
            targetList = [ ind+target_Camp*10 for ind in rows.get(3)]
            targetList = set(targetList).intersection(candidatelist)
            if not targetList:
                targetList = [candidate]
        elif rule ==6:#后排单体
            targetList = [ ind+target_Camp*10 for ind in rows.get(3)]
            dd = ruleDict.get(lineno)
            sequence = lines[dd[0]]+lines[dd[1]]+lines[dd[2]]
            targetList.sort(key= lambda d: sequence.index(d%10))
            targetList = set(targetList).intersection(candidatelist)
            if not targetList:
                targetList = [candidate]
            else:
                targetList = [list(targetList)[0]]
            
        elif rule ==7:#主将锁定
            if actorId_Camp==1:
                targetList = [self.plord]
            else:
                targetList = [self.alord]
            if not targetList:
                return [candidate]
        return targetList
    
    def skillCDProcess(self):
        """所有角色的技能CD处理"""
        for actor in self.order:
            self.actorSkillCDProcess(actor)
        
    def actorSkillCDProcess(self,actor):
        """行动者技能CD处理"""
        skills = self.fighters[actor]['skillCDRecord']
        for skill in skills:
            if skill['traceCD']>0:
                skill['traceCD']-=1
            
    def canDoSkill(self,actor,skillID):
        """判断是否能使用技能
        @param actor: int 行动者的ID
        @param releaseNo: 行动者释放技能的序号
        @param skillID: int 技能的ID
        """
        skillAttributeType = dbSkill.ALL_SKILL_INFO[skillID]['attributeType']
        #技能的属性类型 1物理 2魔法
        skillExpendPower = dbSkill.ALL_SKILL_INFO[skillID]['expendPower']#技能能量消耗
        skillGroup = dbSkill.ALL_SKILL_INFO[skillID]['skillGroup']
        if skillGroup == CATCHPETSKILLGROUP and self.hasboss:#有boss存在时不能抓捕
            return False
        nowPower = self.fighters[actor['chaBattleId']]['chaCurrentPower']
        if nowPower< skillExpendPower:#能量不够时
            return False
        if not actor['canDoPhysicalSkill'] and skillAttributeType==1:
            return False
        if not actor['canDoMagicSkill'] and skillAttributeType==2:
            return False
        return True
        
    def canDoOrdSkill(self,actor,OrdSkill):
        """判断是否能静心普通的攻击
        @param actor: int 行动者的ID
        @param OrdSkill: int 普通技能的ID
        """
        if actor['canDoOrdSkill']:
            return True
        return False
    
    @property
    def battlestar(self):
        """获取战斗评级
        """
        if self.battleResult!=1:
            return 0
        if self.now_round==1:
            return 3
        elif self.now_round==2:
            return 2
        else:
            return 1
    
    def CanBeAttacked(self,target):
        """判断目标是否是可被攻击的"""
        if self.fighters[target]['canBeAttacked']:
            return True
        return False
    
    def DoFight(self):
        """战斗计算
        """
        while True:#如果一方的所有成员死亡，或者总回合数超过15回合，战斗结束
            if (not self.activeList) or (not self.passiveList) or self.now_round>15:
                break
            self.now_round +=1
            self.RoundProcess()#每回合处理
        if self.activeList and self.passiveList:
            self.battleResult = 2#战平
        elif self.activeList:
            self.battleResult = 1#胜利
        else:
            self.battleResult = 2#失败
        
    def RoundProcess(self):
        """回合处理"""
        for actor in self.order:
            if (not self.activeList) or (not self.passiveList) or self.now_round>15:
                break
            if (actor not in self.activeList) and (actor not in self.passiveList):
                continue
            self.goFight(actor)
            self.actorSkillCDProcess(actor)
    
    def doBufferEffect(self,actor):
        """处理buff效果
        @param actor: int 行动者的ID
        """
        self.battleStateMachine.executeBuffEffects(actor)
            
    def goFight(self,actorId):
        """开始战斗计算
        @param actor: int 行动者的ID
        """
        if self.fighters[actorId]['died']:
            return
        actor = self.battleStateMachine.getTargetAttrWithBuf(actorId)
        self.battleStateMachine.executeBuffEffects(actorId)#处理buff
        if self.fighters[actorId]['died']:
            return
        releaseSkill = 0#将要释放的技能（包括战斗技能和普通攻击的技能）
        skillID = 0
        skillIDCD = 0
        OrdSkill = self.fighters[actorId]['ordSkill']#角色的普通攻击技能
        releaseNo = self.fighters[actorId]['nextReleaseSkill']#角色释放技能的序号
        if self.fighters[actorId]['ActiveSkillList']:
            skillID = self.fighters[actorId]['ActiveSkillList'][releaseNo]#角色要释放的战斗技能
            skillIDCD = self.fighters[actorId]['skillCDRecord'][releaseNo]['traceCD']#技能的CD
        
        if skillID>0 and skillIDCD<1 and self.canDoSkill(actor,skillID):#判断是否能释放技能
            releaseSkill = skillID
        elif self.canDoOrdSkill(actor, OrdSkill):#判断是否能进行
            releaseSkill = OrdSkill
        else:
#            if bufftag:
#                self.battleStateMachine.executeBuffEffect(actorId,0)#当轮到自身,但不能攻击时,只做buff的处理
            return
        self.doSkill(actor,releaseSkill)

    def doSkill(self,actor,skillId):
        """进行技能攻击"""
        skillType = {True:1,False:2}.get(skillId==actor['ordSkill'])
        data = {}
        data['chaId'] = actor['chaId']#角色的Id
        data['chaName'] = actor['chaName']#攻击方得名称
        data['chaLevel'] = actor['chaLevel']
        data['chaBattleId']= actor['chaBattleId']#角色战斗ID
        data['skill'] = skillId
        data['chaProfessionType'] = actor['chaProfessionType']#角色的
        data['actionId'] = {True:99,False:98}.get(skillType==1)#动作ID
        data['counterHitActionId'] = 97#受反击时的动作
        data['isDeathOfCounterHit'] = 0 #攻击方是否被反击致死 0:否，1：是
        data['txtEffectId'] = 0#文字特效（暴击等闪避）
        data['chaEffectId'] = dbSkill.ALL_SKILL_INFO[skillId]['releaseEffect']#角色释放技能特效
        data['chaEnemyEffectId'] = dbSkill.ALL_SKILL_INFO[skillId]['bearEffect']#角色技能承受特效
        data['chaThrowEffectId'] = dbSkill.ALL_SKILL_INFO[skillId]['throwEffectId']#角色技能投射特效
        data['chaAoeEffectId'] = dbSkill.ALL_SKILL_INFO[skillId]['aoeEffectId']#角色技能投射特效
        data['chaBuffArr'] = []#角色身上的buff
        data['chaBuffShowList'] = []#角色身上buff显示信息
        data['chaPowerUp'] = 0#+20 power增加
        data['chaPowerDown'] = 0#-20 power减少
        data['chaCurrentPower'] = actor['chaCurrentPower']#当前能量
        data['chaTotalHp'] = actor['chaTotalHp']
        data['chaTotalPower'] = actor['chaTotalPower']#受击方的总能量
        data['powerEffectId'] = 0#攻击方的能量特效
        data['chaChangeHp'] = 0#±20 正负HP，可能有加血技能
        data['chaCurrentHp'] = actor['chaCurrentHp']#角色的当前血量
        data['chaExpendHp'] = 0#角色技能消耗的血量
        data['chaStartPos'] = actor['chaPos']#角色的起始坐标
        data['chaTargetPos'] = actor['chaPos']#角色的目标坐标
        data['chaAttackType'] = 3-dbSkill.ALL_SKILL_INFO[skillId]['distanceType']
        data['isCriticalBlow'] = False
        data['chaDirection'] = actor['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
        data['enemyChaArr'] = []#所有受攻击者的信息
        
        skillRangeType = dbSkill.ALL_SKILL_INFO[skillId]['rangeType']#技能的范围类型 1单体 2全体 ..
        releaseCD = dbSkill.ALL_SKILL_INFO[skillId]['releaseCD']#技能的调息时间
        skillExpendPower = dbSkill.ALL_SKILL_INFO[skillId]['expendPower']#技能能量消耗
        skillExpendHp = dbSkill.ALL_SKILL_INFO[skillId]['expendHp']#技能血量消耗
        targetType = dbSkill.ALL_SKILL_INFO[skillId]['targetType']#技能的目标类型
        #查找攻击的角色
        targetList = list(self.findTarget(actor['chaBattleId'],targetType = targetType, rule = skillRangeType))
        for target in targetList:
            enemy = self.battleStateMachine.getTargetAttrWithBuf(target)
            if not enemy['canBeAttacked'] and targetType == 3:
                continue
            self.calculateDamage(data, actor, enemy, skillId)
        if data['enemyChaArr']:
            nowReleaseSkill = actor['nextReleaseSkill']
            if self.fighters[actor['chaBattleId']]['skillCDRecord'] and skillType ==2:
                self.fighters[actor['chaBattleId']]['skillCDRecord'][nowReleaseSkill]['traceCD'] = releaseCD+1
            self.fighters[actor['chaBattleId']]['nextReleaseSkill']+=1#下次释放技能的序号指向下一个技能
            if self.fighters[actor['chaBattleId']]['nextReleaseSkill']>=len(actor['ActiveSkillList']):
                self.fighters[actor['chaBattleId']]['nextReleaseSkill']=0
            self.fighters[actor['chaBattleId']]['chaCurrentPower'] -= skillExpendPower
            powerup = 0
            if skillExpendPower == 0:
                powerup = int(actor['speed']*2/actor['chaLevel'])
                self.fighters[actor['chaBattleId']]['chaCurrentPower'] += powerup
            #判断能量溢出
            if self.fighters[actor['chaBattleId']]['chaCurrentPower']>self.fighters[actor['chaBattleId']]['chaTotalPower']:
                data['powerEffectId'] = POWEREFFECTID
                self.fighters[actor['chaBattleId']]['chaCurrentPower'] =\
                            self.fighters[actor['chaBattleId']]['chaTotalPower']
            data['chaCurrentPower'] = self.fighters[actor['chaBattleId']]['chaCurrentPower']
            self.fighters[actor['chaBattleId']]['chaCurrentHp'] -= skillExpendHp
            data['chaPowerUp'] += powerup
            data['chaPowerDown'] -= skillExpendPower
            data['chaExpendHp'] -= skillExpendHp
            data['chaBuffArr'] = self.battleStateMachine.getTargetBuffList(actor['chaBattleId'])
            data['chaBuffShowList'] = self.battleStateMachine.getTargetBuffInfoList(actor['chaBattleId'])
            self.FightData.append(data)
#            self.resourceCollect(data)
            
        ################################################
        #添加反伤是否造成攻击者死亡的处理                                          
        direction = actor['chaDirection']
        #看是否进行反伤死亡的处理
        if ((direction==1 and self.passiveList) or (direction==2 and self.activeList))\
         and self.fighters[actor['chaBattleId']]['chaCurrentHp']<=0 and data['chaCurrentHp']>0:
            data['isDeathOfCounterHit'] = 1
            
    def calculateDamage(self,data,actor,enemy,skillId):
        """计算伤害值"""
        info = {}
        info['enemyChaId'] = enemy['chaId']#受攻击者的角色的id
        info['enemyChaName'] = enemy['chaName']#攻击方得名称
        info['enemychaLevel'] = enemy['chaLevel']
        info['enemyProfessionType'] = enemy['chaProfessionType']
        info['enemyBattleId'] = enemy['chaBattleId']#受攻击者的战场id
        info['enemyActionId'] = 97#enemy['chaProfessionType']*1000+570#受攻击者的动作id
        info['enemyCounterHitActionId'] = 0#enemy['chaProfessionType']*1000+550#反击时的动作ID
        info['enemyTxtEffectId'] = 0#受攻击者的文字特效
        info['chaEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['releaseEffect']
        info['chaEnemyEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['bearEffect']
        info['chaThrowEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['throwEffectId']
        info['chaEnemyAoeEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['aoeEffectId']
        info['enemyBuffArr'] = []#受攻击者的buff列表
        info['enemyBuffShowList'] = []#受攻击者的buff信息列表
        info['enemyPowerUp'] = 0#受攻击者的能量增量
        info['enemyPowerEffectId'] = 0##受攻击方的能量特效
        info['enemyCurrentPower'] = enemy['chaCurrentPower']#受攻击者的当前能量
        info['enemyTotalHp'] = enemy['chaTotalHp']#受击方的总血量
        info['enemyTotalPower'] = enemy['chaTotalPower']#受击方的总能量
        info['enemyChangeHp'] = 0#受攻击者丢失的血量
        info['enemyCurrentHp'] = enemy['chaCurrentHp']#受攻击者的当前血量
        info['enemyCounterHit'] = 0#受攻击者是否反击 0没有 1反击
        info['enemyStartPos'] = enemy['chaPos']#受攻击者的起始坐标
        info['enemyTargetPos'] = enemy['chaPos']#受攻击者的目标坐标
        info['enemyDirection'] = enemy['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
        self.fighters[enemy['chaBattleId']]['skillIDByAttack'] = skillId
#        skillDistanceType = dbSkill.ALL_SKILL_INFO[skillId]['distanceType']#技能的距离类型 1远程 2近身
        skillAttributeType = dbSkill.ALL_SKILL_INFO[skillId]['attributeType']#技能的属性类型 1物理 2魔法
        skillTargetType = dbSkill.ALL_SKILL_INFO[skillId]['targetType']#技能的目标类型 1自身 2己方 3敌方

        try:
            skillFormula = dbSkill.ALL_SKILL_INFO[skillId]['effect']['formula']#技能计算公式
            skillclearBuffId= dbSkill.ALL_SKILL_INFO[skillId]['effect']['clearBuffId']#清除buff的id
            skilladdBuffId = dbSkill.ALL_SKILL_INFO[skillId]['effect']['addBuffId']#添加buff的ID
        except Exception:
            raise Exception("%d skill ID not exits"%skillId)
        
        if not enemy['canBeAttacked']:#判断角色是否能被攻击
            return
#        if skillDistanceType==2:#根据技能距离判断攻击者的最终位置
#            if enemy['chaDirection']==1:
#                data['chaTargetPos'] = enemy['chaPos']
#            else:
#                data['chaTargetPos'] = enemy['chaPos']
            #添加移动的资源
            
        hitRate = actor['hitRate'] - enemy['dodgeRate']
        rate = random.randint(1,100)
        if rate <hitRate or skillTargetType == 1:#判断是否命中，命中时的操作
            
            #能量变更
            info['enemyPowerUp'] += POWDEFUP
            self.fighters[enemy['chaBattleId']]['chaCurrentPower'] += info['enemyPowerUp']
            #判断能量溢出
            if self.fighters[enemy['chaBattleId']]['chaCurrentPower']>=\
                            self.fighters[enemy['chaBattleId']]['chaTotalPower']:
                info['enemyPowerEffectId'] = POWEREFFECTID
                self.fighters[enemy['chaBattleId']]['chaCurrentPower'] =\
                            self.fighters[enemy['chaBattleId']]['chaTotalPower']
#            info['enemyCurrentPower'] = self.fighters[enemy['chaBattleId']]['chaCurrentPower']
            #判断是否免疫伤害
            if not enemy['canBeTreat']:
                info['enemyTxtEffectId'] = IMMUNITYEFFECT
                damage = 0
            else:
                #伤害计算
                damage = DamageFormula(actor,enemy,skillAttributeType,skillFormula,state=skillTargetType)
                    #获取伤害加成
                addition = self.battleStateMachine.getSkillAddition(enemy['chaBattleId'], skillId)
                    #计算技能产生的总的伤害
                damage = damage*addition
                
                #技能buff操作处理
                    #清除buff
                buffdamage = 0
                if skillclearBuffId:
                    clearrate = dbSkill.ALL_SKILL_INFO[skillId]['effect']['clearRate']
                    rate = random.randint(0,100)
                    if rate < clearrate:
                        self.battleStateMachine.clearBuffById(enemy['chaBattleId'], skillclearBuffId)
                    #添加buff
                if skilladdBuffId:
                    addrate = dbSkill.ALL_SKILL_INFO[skillId]['effect']['addRate']
                    rate = random.randint(0,100)
                    if rate < addrate:
                        buffdamage += self.battleStateMachine.putBuff(enemy['chaBattleId'],\
                                                 skilladdBuffId,actor['chaBattleId'])
                #总的伤害
                damage += buffdamage
            
                #判断暴击(非技能攻击时方可暴击)
                rate = random.randint(1,100)
                isOrdSkill =  (actor['ordSkill']==skillId)
                if rate <actor['critRate'] and isOrdSkill:
                    #发生暴击
                    info['enemyTxtEffectId'] = CRITEFFECT
#                    if actor['characterType'] ==1:
#                        data['isCriticalBlow'] = True
#                    #暴击特效资源获取
#                    if actor['characterType']==1:
#                        resource = actor['chaProfessionType']*10000+actor['chaProfessionType']*1000\
#                        +actor['chaProfessionType']*100+actor['chaProfessionType']*10+actor['chaProfessionType']
#                        if actor['chaProfessionType'] in [2,4]:
#                            resource2 = actor['chaProfessionType']*10000+actor['chaProfessionType']*1000\
#                                    +actor['chaProfessionType']*100+actor['chaProfessionType']*10
#                            self.resources.add(resource2)
#                        self.resources.add(actor['chaProfessionType'])
#                        self.resources.add(actor['chaProfessionType']*10+actor['chaProfessionType'])
#                        self.resources.add(resource)
                    #暴击最终伤害计算
                    damage *= {1:2,2:1.5}.get(skillAttributeType,1)#计算暴击后的伤害
                    
                #血量变更
                if abs(damage)<1:#当伤害的绝对值小于1强制掉1点血或加1点血
                    if damage<0:
                        damage = -1
                    elif damage>0:
                        damage = 1
                    else:
                        damage = 0
                        
            #反伤的处理            
            reactionaddition = enemy['reactionAddition']#角色的反伤比例
            reactiondamage = damage*reactionaddition
            self.fighters[actor['chaBattleId']]['chaCurrentHp'] -= reactiondamage
            data['chaExpendHp'] -= reactiondamage
            
            #伤害后的计算
            info['enemyChangeHp'] = -int(math.ceil(damage))
            self.fighters[enemy['chaBattleId']]['chaCurrentHp']+= info['enemyChangeHp']
            if self.fighters[enemy['chaBattleId']]['chaCurrentHp']<=0:
                #记录受伤害的动作
                info['enemyActionId'] = 96#enemy['chaProfessionType']*1000 + 580
                self.fighters[enemy['chaBattleId']]['died'] = 1
                enemy['died'] = 1
                if enemy['chaDirection']==1:
                    self.activeList.remove(enemy['chaBattleId'])
                else:
                    self.passiveList.remove(enemy['chaBattleId'])
                    
            #判断血量溢出
            elif self.fighters[enemy['chaBattleId']]['chaCurrentHp']>\
                                self.fighters[enemy['chaBattleId']]['chaTotalHp']:
                self.fighters[enemy['chaBattleId']]['chaCurrentHp'] =\
                                 self.fighters[enemy['chaBattleId']]['chaTotalHp']
#            rate = random.randint(1,100)#判断反击
        else:
            #闪避处理
            info['enemyTxtEffectId'] = DODGEEFFECT
                
        info['enemyBuffArr'] = self.battleStateMachine.getTargetBuffList(enemy['chaBattleId'])
        info['enemyBuffShowList'] = self.battleStateMachine.getTargetBuffInfoList(enemy['chaBattleId'])
        data['enemyChaArr'].append(info)
        
        
    def resourceCollect(self,data):
        """资源收集处理
        @param data: dict 战斗的数据
        """
        self.resources.add(data['actionId'])
        self.resources.add(data['counterHitActionId'])
        self.resources.add(data['chaEffectId'])
        self.resources.add(data['chaEnemyEffectId'])
        self.resources.add(data['chaThrowEffectId'])
        self.resources.add(data['powerEffectId'])
#        self.resources = self.resources | set(data['chaBuffArr'])
        for enemyData in data['enemyChaArr']:
            self.resources.add(enemyData['enemyActionId'])
            self.resources.add(enemyData['enemyTxtEffectId'])
            self.resources.add(enemyData['chaEffectId'])
            self.resources.add(enemyData['chaEnemyEffectId'])
            self.resources.add(enemyData['chaThrowEffectId'])
            self.resources.add(enemyData['enemyCounterHitActionId'])
            self.resources.add(enemyData['enemyPowerEffectId'])
            for buffShow in enemyData['enemyBuffShowList']:
                self.resources.add(buffShow['buffEffectId'])
                self.resources.add(buffShow['buffIconId'])


    def SerializationResource(self,bearer):
        """序列化资源列表数据
        """
        bearer.extend([resourceId for resourceId in self.resources if resourceId>0])

    def SerializationInitBattleData(self,bearer):
        """序列化战斗初始化数据"""
        formats = ['chaId','chaBattleId','chaName','chaLevel','chaProfessionType',\
                  'chaDirection','chaCurrentHp','chaCurrentPower','chaTotalHp',\
                  'chaTotalPower','chaPos','chaIcon','chatype']
        for _initdata in self.initData:
            initdata = bearer.add()
            for _iteam in formats:
                if not _initdata[_iteam]:
                    continue
                if _iteam =='chaPos':
                    initdata.chaPos.extend([int(_initdata['chaPos'][0]),
                                            int(_initdata['chaPos'][1])])
                    continue
                setattr(initdata,_iteam,_initdata[_iteam])
        
    def SerializationStepData(self,bearer):
        """序列化战斗中每回合的数据"""
        for _setpdata in self.FightData:
            setpdata = bearer.add()
            for _item in _setpdata.items():
                if _item[0] == 'chaBuffArr':
                    setpdata.chaBuffArr.extend(_item[1])
                    continue
                if _item[0] == 'chaBuffShowList':
                    for _tt in _item[1]:
                        buffShow = setpdata.chaBuffShowList.add()
                        buffShow.buffId = _tt['buffId']
                        buffShow.buffLayerCount = _tt['buffLayerCount']
                        buffShow.buffRemainRoundCount = _tt['buffRemainRoundCount']
                        buffShow.buffEffectId = _tt['buffEffectId']
                        buffShow.buffIconId = _tt['buffIconId']
                        buffShow.buffName = _tt['buffName']
                    continue
                if _item[0] == 'chaStartPos':
                    setpdata.chaStartPos.extend(_item[1])
                    continue
                if _item[0] == 'chaTargetPos':
                    setpdata.chaTargetPos.extend(_item[1])
                    continue
                
                if _item[0] == 'enemyChaArr':
                    for _t in _item[1]:
                        enemyCha = setpdata.enemyChaArr.add()
                        for _titem in _t.items():
                            if _titem[0] == 'enemyBuffArr':
                                enemyCha.enemyBuffArr.extend(_titem[1])
                                continue
                            if _titem[0] == 'enemyBuffShowList':
                                for _t1 in _titem[1]:
                                    buffShow = enemyCha.enemyBuffShowList.add()
                                    buffShow.buffId = _t1['buffId']
                                    buffShow.buffLayerCount = _t1['buffLayerCount']
                                    buffShow.buffRemainRoundCount = _t1['buffRemainRoundCount']
                                    buffShow.buffEffectId = _t1['buffEffectId']
                                    buffShow.buffIconId = _t1['buffIconId']
                                    buffShow.buffName = _t1['buffName']
                                    buffShow.bufDes = _t1['buffDes']
                                continue
                            if _titem[0] == 'enemyStartPos':
                                enemyCha.enemyStartPos.extend(_titem[1])
                                continue
                            if _titem[0] == 'enemyTargetPos':
                                enemyCha.enemyTargetPos.extend(_titem[1])
                                continue
                            if type(_titem[1])==type(u''):
                                setattr(enemyCha,_titem[0],_titem[1])
                            else:
                                setattr(enemyCha,_titem[0],int(_titem[1]))
                    continue
                try:
                    if type(_item[1])==type(u'') or type(_item[1])==type(''):
                        setattr(setpdata,_item[0],_item[1])
                    else:
                        setattr(setpdata,_item[0],int(_item[1]))
                except Exception,e:
                    raise str(e)+str(_item)
                
    def formatFightStartData(self):
        """格式化战斗初始化数据
        """
        formats = ['chaId','chaBattleId','chaName','chaLevel',\
                  'chaDirection','chaCurrentHp','chaTotalHp','chaPz',\
                  'chaPos','chaIcon']
        formatdata = []
        for _initdata in self.initData:
            initdata = {}
            for _iteam in formats:
                if not _initdata[_iteam]:
                    continue
                initdata.update({_iteam:_initdata[_iteam]})
            formatdata.append(initdata)
        return formatdata
    
    def formatFightStepData(self):
        """格式化战斗回合数据
        """
        formatdata = []
        actorformats = ['chaBattleId','chaExpendHp','chaId','actionId','enemyChaArr',
                        'chaCurrentHp','chaTotalHp','skill','chaBuffShowList','txtEffectId']
        enemyformats = ['enemyBattleId','enemyChaId','enemyActionId',
                        'enemyChangeHp','enemyCurrentHp','enemyTotalHp','enemyBuffShowList']
        for _setpdata in self.FightData:
            stepdata = {}
            for _iteam in actorformats: 
                if _iteam == 'enemyChaArr':
                    enemyChaArr = _setpdata['enemyChaArr']
                    enemylist = []
                    for enemy in enemyChaArr:
                        enemydata = {}
                        for _itemname in enemyformats:
                            if _itemname=='enemyBuffShowList':
                                enemydata['enemyBuff'] = 0 if not enemy['enemyBuffShowList'] \
                                   else enemy['enemyBuffShowList'][-1]
                                continue
                            enemydata[_itemname] = enemy[_itemname]
                        enemylist.append(enemydata)
                    stepdata['enemyChaArr']=enemylist
                    continue
                elif _iteam == 'chaBuffShowList':
                    stepdata['chaBuff'] = 0 if not _setpdata['chaBuffShowList'] \
                            else _setpdata['chaBuffShowList'][-1]
                    continue
                stepdata[_iteam] =_setpdata[_iteam]
            formatdata.append(stepdata)
        return formatdata
                
    def formatFightData(self):
        """格式化战斗的信息
        """
        formatdata = {}
        formatdata['battleResult'] = self.battleResult
        formatdata['startData'] = self.formatFightStartData()
        formatdata['stepData'] = self.formatFightStepData()
        return formatdata

from app.game.core.fight.battleSide import BattleSide            

def DoFight(actors,deffeners,now_X,preDict = {'extVitper':0,'extStrper':0,
                                 'extDexper':0,'extWisper':0,'extSpiper':0,
                                 'preVitper':1,'preStrper':1,
                                 'preDexper':1,'preWisper':1,'preSpiper':1}):
    """进行战斗"""
    challengers = BattleSide(actors)
    defenders = BattleSide(deffeners,preDict = preDict)
    fight = Fight( challengers, defenders, now_X)
    fight.DoFight()
    return fight

def DoGroupFight(actors,maxtir_a,deffeners,maxtir_b):
    """进行战斗
    @param actors: []角色实例列表
    @param maxtir_a: {}角色阵法信息 key:角色id,value:阵法位置
    @param deffeners: []怪物实例列表
    @param maxtir_b: {}怪物真发信息 key:怪物动态id,value:阵法位置
    """
    challengers = BattleSide(actors,matrixType = 1,matrixSetting = maxtir_a)
    defenders = BattleSide(deffeners,matrixType = 1,matrixSetting = maxtir_b)
    fight = Fight(challengers, defenders, 550)
    fight.DoFight()
    return fight



