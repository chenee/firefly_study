#coding:utf8
"""
Created on 2011-9-5
战斗状态机
@author: lan (www.9miao.com)
"""
from app.game.core.fight.stateBuffer import StateBuffer
from app.share.dbopear import dbSkill
import copy


class BattleStateMachine:
    """战斗状态机"""
    MAXBUFNUM = 6#每个角色最多的buf个数
    
    def __init__(self,owner = None):
        """战斗状态机
        @param fight: Fight object 战斗实例
        """
        self.StatePool = {}
        self.owner = owner#状态池，保存战斗角色的buff状态
        
    def putBuff(self,targetId,buffId,executor):
        """给指定的目标添加一个buff
        @param targetId: int 目标的id
        @param buffId: int buff的ID
        @param executor: int 
        """
        if not self.StatePool.has_key(targetId):
            self.StatePool[targetId] = []
        bufflist = [buff.getID() for buff in self.StatePool[targetId]]
        goaldamage = self.buffListOffset(buffId, bufflist, executor, targetId)
        return goaldamage
        
    def buffListOffset(self,newbuff,buffList,actorId,enemyId):
        """buff之间的效果触发
        """
        goaldamage = 0
        nstack = 1
        while True:#buff连环触发的处理
            if not newbuff:
                break
            offbuffId = self.checkOffset(newbuff, buffList)
            if not offbuffId:
                break
            damage = 0
            offsetinfo = dbSkill.BUFF_BUFF.get(offbuffId,{})
            offsetEffect = offsetinfo.get(newbuff)
            newbuff = offsetEffect['nbuffId']
            nstack = offsetEffect['nstack']
            oldstack = self.getBuffStackOnTarget(enemyId, offbuffId)
            buffList.remove(offbuffId)
            self.clearBuffById(enemyId, offbuffId)
            actor = self.getTargetAttrWithBuf(actorId)
            enemy = self.getTargetAttrWithBuf(enemyId)
            if offsetEffect['effect']:
                exec(offsetEffect['effect'])
            goaldamage += damage
        self.addNewBuff(enemyId, newbuff, actorId, nstack)

        return goaldamage
    
    def addNewBuff(self,targetId,buffId,executor,stack):
        """添加新的buff
        """
        newbuff = StateBuffer(buffId, holder = targetId, executor = executor)
        newbuff.setStack(stack)
        buffIdlist = [buff.getID() for buff in self.StatePool[targetId]]
        if buffId in buffIdlist:#存在同样的buff时
            for buff in self.StatePool[targetId]:
                tbuffId = buff.getID()
                if buffId == tbuffId:
                    buff.addStack()
        else:
            ntype = newbuff.getBuffType()
            state = 0
            for buff in self.StatePool[targetId]:
                tbuffId = buff.getID()
                tbufftype = buff.getBuffType()
                tstack = buff.getStack()
                if ntype == tbufftype:
                    state = 1
                    if tstack>stack:
                        buff.addStack()
                    else:
                        self.StatePool[targetId].remove(buff)
                        self.StatePool[targetId].append(newbuff)
            if not state:
                self.StatePool[targetId].append(newbuff)
        
    def checkOffset(self,newbuff,buffList):
        """检测是否能继续替换
        """
        for buffId in buffList:
            offsetinfo = dbSkill.BUFF_BUFF.get(buffId,{})
            offsetEffect = offsetinfo.get(newbuff)
            if offsetEffect:
                return buffId
        return 0
                
    def clearBuffById(self,target,buffID):
        """根据buff的ID清除buff
        """
        if not self.StatePool.has_key(target):
            return
        for buff in self.StatePool[target]:
            if buff.getID()==buffID:
                self.StatePool[target].remove(buff)
    
    def getTargetAttrWithBuf(self,target):
        """获取角色的伴随buff后的属性
        @param target: int 目标在战场中的id
        """
        enemy = copy.deepcopy(self.owner.fighters[target])
        battleId = enemy['chaBattleId']
        side = battleId/10
        if side==1:
            lord = self.owner.alord
        else:
            lord = self.owner.plord
        lordattr = self.owner.fighters[lord]
        if lordattr['died'] or target==lord:
            EquipAttr = {}
        else:
            EquipAttr = lordattr['equip']
        enemy['chaTotalHp'] = (enemy['chaTotalHp']+EquipAttr.get('MaxHp',0))*\
                                (1+EquipAttr.get('MaxHpPercen',0))
        enemy['physicalAttack'] = (enemy['physicalAttack']+EquipAttr.get('PhyAtt',0))*\
                                (1+EquipAttr.get('PhyAttPercen',0))
        enemy['physicalDefense'] = (enemy['physicalDefense']+EquipAttr.get('PhyDef',0))*\
                                (1+EquipAttr.get('PhyDefPercen',0))
        enemy['hitRate'] = enemy['hitRate']+EquipAttr.get('HitRate',0)
        enemy['critRate'] = enemy['critRate']+EquipAttr.get('CriRate',0)
        enemy['dodgeRate'] = enemy['dodgeRate']+EquipAttr.get('Dodge',0)
        enemy['speed'] = enemy['speed']+EquipAttr.get('speed',0)
        if not self.StatePool.has_key(target):
            self.StatePool[target] = []
        for buff in self.StatePool[target]:
            executor = buff.getExecutor()
            actor = self.owner.fighters[executor]
            enemy = buff.getBuffEffect(actor,enemy)
        return enemy
    
    def getSkillAddition(self,targetId,skill):
        """获取技能效果加成
        @param targetId: int 目标的ID
        @param skill: int 技能的ID
        """
        #伤害加成
        damageAddition = 1
        if not self.StatePool.has_key(targetId):
            self.StatePool[targetId] = []
        for buff in self.StatePool[targetId]:
            buffId = buff.getID()
            stack = buff.getStack()
            addinfo = dbSkill.BUFF_SKILL.get(buffId,{})
            addition = addinfo.get(skill)
            if addition:
                damageAddition *= (1+addition*stack)
        return damageAddition
        
    def getTargetBuffList(self,target):
        """获取目标的bufflist
        @param target: int 目标的id
        """
        buffList = []
        if self.StatePool.has_key(target):
            buffList = [buff.getID() for buff in self.StatePool[target]]
        return buffList
    
    def getTargetBuffInfoList(self,target):
        """获取目标的的buff信息列表"""
        buffList = []
        if self.StatePool.has_key(target):
            buffList = [buff.formatBuffInfo() for buff in self.StatePool[target]]
        return buffList
    
    def getBuffStackOnTarget(self,target,buffId):
        """获取角色身上的buff的层叠数
        """
        stack = 0
        for buff in self.StatePool[target]:
            tbuffId = buff.getID()
            if tbuffId== buffId:
                stack = buff.getStack()
                break
        return stack
    
    def executeBuffEffects(self,target):
        """处理角色身上所有的buff效果"""
        if not self.StatePool.has_key(target):
            return False
        damage = None
        for buff in self.StatePool[target]:
            executor = buff.getExecutor()
            actor = self.getTargetAttrWithBuf(executor)
            enemy = self.getTargetAttrWithBuf(target)
            _damage1 = buff.getdotHotEffect(actor,enemy)
            _damage2 = buff.getdotTriggeredHotEffect(actor,enemy)
            if _damage1 or _damage2:
                if damage is None:
                    damage = 0
                damage = _damage1 + _damage2
        if damage is not None:
            self.executeBuffEffect(target,damage)
        return self.buffCDProcess(target)
                
    def executeBuffEffect(self,target,damage):
        """进行buff效果(计算buff伤害)
        @param target: int 目标的id
        @param buffId: int buff的ID
        """
        enemy = self.getTargetAttrWithBuf(target)
        data = {}
        data['chaId'] = -1#角色的Id
        data['chaName'] = ''#攻击方得名称
        data['chaLevel'] = 1
        data['chaBattleId']= -1#角色战斗ID
        data['skill'] = 0
        data['chaProfessionType'] = -1
        data['actionId'] = -1#动作ID
        data['counterHitActionId'] = -1
        data['isDeathOfCounterHit'] = -1
        data['txtEffectId'] = -1#文字特效（暴击等闪避）
        
#        data['skillId'] = -1#技能的ID
        data['chaEffectId'] = -1#角色释放技能特效
        data['chaEnemyEffectId'] = -1#角色技能承受特效
        data['chaThrowEffectId'] = -1
        data['chaAoeEffectId'] = -1#角色技能投射特效
        
        data['chaBuffArr'] = []#角色身上的buff
        data['chaBuffShowList'] = []#角色身上buff显示信息
        
        data['chaPowerUp'] = 0#+20 power增加
        data['chaPowerDown'] = 0#-20 power减少
        data['chaCurrentPower'] = 0#当前能量
        data['chaTotalHp'] = 0
        data['chaTotalPower'] = 0#受击方的总能量
        data['powerEffectId'] = 0#攻击方的能量特效
        data['chaChangeHp'] = 0#±20 正负HP，可能有加血技能
        data['chaCurrentHp'] = 0#角色的当前血量
        data['chaExpendHp'] = 0#角色技能消耗的血量
        data['chaStartPos'] = (0,0)#角色的起始坐标
        data['chaTargetPos'] = (0,0)#角色的目标坐标
        
        data['chaAttackType'] = 2
        data['isCriticalBlow'] = False
        data['enemyChaArr'] = []#所有受攻击者的信息
        
        info = {}
        info['enemyChaId'] = enemy['chaId']#受攻击者的角色的id
        info['enemyChaName'] = enemy['chaName']#攻击方得名称
        info['enemychaLevel'] = enemy['chaLevel']
        info['enemyProfessionType'] = enemy['chaProfessionType']
        info['enemyBattleId'] = target#受攻击者的战场id
        info['enemyActionId'] = 97#enemy['chaProfessionType']*1000+570#受攻击者的动作id
        info['enemyTxtEffectId'] = 0#受攻击者的文字特效
        
        info['chaEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['releaseEffect']
        info['chaEnemyEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['bearEffect']
        info['chaThrowEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['throwEffectId']
        info['chaEnemyAoeEffectId'] = dbSkill.ALL_SKILL_INFO[enemy['ordSkill']]['aoeEffectId']
        
        info['enemyBuffArr'] = []#受攻击者的buff列表
        info['enemyBuffShowList'] = []
        
        info['enemyPowerUp'] = 0#受攻击者的能量增量
        info['enemyCurrentPower'] = enemy['chaCurrentPower']#受攻击者的当前能量
        info['enemyTotalHp'] = enemy['chaTotalHp']#受击方的总血量
        info['enemyTotalPower'] = enemy['chaTotalPower']#受击方的总能量
        info['enemyPowerEffectId'] = 0#攻击方的能量特效
        info['enemyChangeHp'] = 0#受攻击者丢失的血量
        info['enemyCurrentHp'] = enemy['chaCurrentHp']#受攻击者的当前血量
        info['enemyCounterHit'] = 0#受攻击者是否反击 0没有 1反击
        info['enemyCounterHitActionId'] = 0#标识反击的动作
        info['enemyStartPos'] = enemy['chaPos']#受攻击者的起始坐标
        info['enemyTargetPos'] = enemy['chaPos']#受攻击者的目标坐标
        info['enemyDirection'] = enemy['chaDirection']#玩家朝向右，朝向右。2--玩家朝向左
        
        info['enemyChangeHp'] = -damage
        self.owner.fighters[target]['chaCurrentHp'] += info['enemyChangeHp']

        #判断死亡
        if self.owner.fighters[target]['chaCurrentHp']<=0:

            self.owner.fighters[target]['died']=1#角色死亡
            info['enemyActionId'] = 96#enemy['chaProfessionType']*1000+580
            if enemy['chaDirection']==1:
                self.owner.activeList.remove(target)
            else:
                self.owner.passiveList.remove(target)
        #判断血量溢出
        elif self.owner.fighters[target]['chaCurrentHp']>\
                        self.owner.fighters[target]['chaTotalHp']:
            self.owner.fighters[target]['chaCurrentHp'] = \
                        self.owner.fighters[target]['chaTotalHp']
        info['enemyBuffArr'] = self.getTargetBuffList(target)
        info['enemyBuffShowList'] = self.getTargetBuffInfoList(target)
        data['enemyChaArr'].append(info)
        
        #资源列表收集使用到的资源
#        self.owner.resourceCollect(data)
        self.owner.FightData.append(data)
        
    def OneBuffCDProcess(self,target,buffID):
        """buff的CD处理
        @param target: int 目标的id
        @param buffID: buff 的id
        """
        for buff in self.StatePool[target]:
            if buff.getID() == buffID:
                result = buff.cutTraceCD()
                if result<=0:
                    self.clearBuffById(target, buff.getID())
        
    def buffCDProcess(self,target):
        """buff的CD处理
        @param target: int 目标的id
        """
        tag = False
        for buff in self.StatePool[target]:
            result = buff.cutTraceCD()
            if result<=0:
                tag = True
                self.clearBuffById(target, buff.getID())
        return tag

            
        
