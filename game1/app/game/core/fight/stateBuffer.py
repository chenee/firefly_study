#coding:utf8
"""
Created on 2011-10-7

@author: lan (www.9miao.com)
"""
from app.share.dbopear import dbSkill

class StateBuffer(object):
    """Buff 状态
    """


    def __init__(self,buffID,holder = 0,executor = 0):
        """
        Constructor
        @param buffID: int buff的ID
        """
        self.id = buffID#buff的ID
        self.stack = 1#buff的层叠数
        self.traceCD = 1#剩余的回合数
        self.executor = executor#buff施加者的战场id
        self.holder = 0#持有者的战场id
        self.format = {}#buff的详细信息
        self.effectFormula = {'actor':{},'enemy':{}}#buff效果计算
        self.initBuffInfo()#初始化buff的信息
        
    def initBuffInfo(self):
        """初始化buff信息"""
        self.format = dbSkill.ALL_BUFF_INFO[self.id]
        self.traceCD = self.format['traceCD']+1
        
    def getID(self):
        """获取Buff的id"""
        return self.id
    
    def getName(self):
        """获取buff名称"""
        return self.format['buffName']
    
    def getExecutor(self):
        """获取施加者的战场id"""
        return self.executor
        
    def getStack(self):
        """获取buff的当前堆叠数"""
        return self.stack
    
    def addStack(self):
        """添加一层堆叠"""
        self.traceCD = self.format['traceCD']
        if self.stack>=self.getMaxStack():
            return False
        self.stack +=1
        return True
    
    def setStack(self,stack):
        """设置buff的最大堆叠数"""
        if stack>self.getMaxStack():
            return False
        return True
    
    def getTraceCD(self):
        """获取剩下回合数"""
        return self.traceCD
    
    def cutTraceCD(self):
        """剪掉一次回合数"""
        self.traceCD -=1
        return self.traceCD
    
    def getBuffType(self):
        """获取buff的类型
        """
        return self.format['buffType']
    
    def getMaxStack(self):
        """获取buff的最大堆叠数"""
        return self.format['maxStack']
    
    def getCanReplaceBuffList(self):
        """获取可以清除的Buff 列表"""
        return eval('['+self.format['replaceBuff']+']')
    
    def getBuffEffect(self,actor,enemy):
        """获取buff或者debuff效果"""
        effectFormula = self.format['buffEffects'].get('effectFormula','')
        exec(effectFormula)
        if self.hasTriggered(enemy):
            enemy = self.getTriggeredBuffEffect(actor, enemy)
        return enemy
    
    def getdotHotEffect(self,actor,enemy):
        """获取dot或者hot效果"""
        damage = 0
        dotHotFormula = self.format['buffEffects'].get('dotHotFormula','')
        exec(dotHotFormula)
        return damage
    
    def hasTriggered(self,enemy):
        """判断被动效果是否被触发"""
        effectTriggerCondition = self.format['buffEffects'].get('effectTriggerCondition','')
        if effectTriggerCondition and eval(effectTriggerCondition):
            return True
        return False
    
    def getTriggeredBuffEffect(self,actor,enemy):
        """获取被触发后的buff或debuff效果"""
        dotHotFormula = self.format['buffEffects'].get('dotHotFormula','')
        exec(dotHotFormula)
        return enemy
    
    def getdotTriggeredHotEffect(self,actor,enemy):
        """获取dot或者hot效果"""
        damage = 0
        if self.hasTriggered(enemy):
            dotHotFormula = self.format['buffEffects'].get('triggerDotHotFormula','')
            exec(dotHotFormula)
        return damage
    
    
    
    
    
    
