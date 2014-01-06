#coding:utf8
"""
Created on 2011-3-24

@author: sean_lan
"""

from app.game.component.Component import Component

class CharacterFinanceComponent(Component):
    """
    finance component for character
    """
    MAXCOIN = 999999

    def __init__(self,owner,coin=0,gold=0):
        """
        Constructor
        """
        Component.__init__(self,owner)
        self._coin = coin #角色的金币
        self._gold = gold #角色的

    #--------------------------coin------------------
    def getCoin(self):
        return self._coin

    def setCoin(self,coin):
        self._coin = coin


    def updateCoin(self,coin,state=1):
        if coin ==self._coin:
            return
        if coin>= self.MAXCOIN:
            self._coin = self.MAXCOIN
        else:
            self._coin = coin

    def addCoin(self,coin,state = 1):
        coin = self._coin + coin
        self.updateCoin(coin,state = state)

    #--------------------------gold------------
    def getGold(self):
        return self._gold

    def setGold(self,gold):
        self._gold = gold

    def updateGold(self,gold,state=1):
        delta = self._gold - gold
        if not delta:
            return
        self._gold = gold

    def consGold(self,consGold,consType,consDesc='',itemId=0):
        """金币消耗
        @param consGold: int 消耗的金币的数量
        @param consType: int 消耗的行为类型
        @param consDesc: str 消耗的描述
        @param itemId: int 相关物品的ID
        1.祈祷
        2.在商城中购买
        3.竞技场消费
        4.宠物商店刷新
        5.铁矿洞中立即完成
        6.国升级军徽
        7.购买活力值
        8.宠物培养
        9.军营中立即完成
        10.军营中加急训练
        11.铁矿洞点石成金
        12.其他
        """
        self.addGold(-consGold)

    def addGold(self,gold):
        nowgold = self._gold +gold
        if nowgold<0:
            return False
        self.updateGold(nowgold)
        return True



