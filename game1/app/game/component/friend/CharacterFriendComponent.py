#coding:utf8
"""
Created on 2011-3-31

@author: sean_lan
"""

from app.game.component.Component import Component
from app.share.dbopear import dbFriend,dbZhanyi
from app.game.core.language.Language import Lg
from app.share.mcharacter.McharacterManager import McharacterManager

class CharacterFriendComponent(Component):
    """
    friend component for character
    """

    def __init__(self,owner):
        """
        Constructor
        """
        Component.__init__(self,owner)
        self._friendCount = 200#玩家拥有好友数量上限
        self._friends = set([]) #好友 set[好友角色id,好友角色id,好友角色id]
        self._guyong = set([]) #角色的雇用列表
        self.initFrined()

    def initFrined(self):
        self._friends = set(dbFriend.getFirendListByFlg(self._owner.baseInfo.id, 1))
        self._guyong = set(dbFriend.getGuYongList(self._owner.baseInfo.id))

    def getFriends(self):
        """获取好友角色列表"""
        return list(self._friends)

    def setFriends(self,friends):
        """设置好友角色列表"""
        self._friends = set(friends)

    def getFriendTop(self,tag,index):
        """获取好友的排行信息
        """
        characterId = self._owner.baseInfo.id
        if tag==1:
            data = dbFriend.getFriendTopGuanqia(characterId, index)
        elif tag==2:
            data = dbFriend.getFriendTopLevel(characterId, index)
        else:
            data = dbFriend.getAllCharacterTop(index)
        datalen = len(data)
        end = index + datalen
        friendlist = []
        ranktag = index
        for friend in data:
            ranktag += 1
            info = {}
            info['chaid'] = friend['id']
            info['rolename'] = friend['nickname']
            info['level'] = friend['level']
            info['skill'] = u'无'
            info['price'] = friend['level']*1000
            info['rank'] = ranktag
            info['guyong'] = True if friend['id'] in self._guyong else False
            friendlist.append(info)
        response = {'result':True,'message':u'','data':{'end':end,
                                                        'sp': True if datalen==20 else False,
                                                        'friendlist':friendlist}}
        return response

    def addFriend(self,characterId,playerId):
        """添加一个好友或者黑名单
        @param characterId: int 角色的id
        @param playerId: int 好友或者黑名单角色id
        """
        if len(self.getFriends())>= self._friendCount:
            return {'result':False,'message':Lg().g(317)}
        if playerId ==self._owner.baseInfo.id:
            return {'result':False,'message':Lg().g(318)}
        elif playerId in self.getFriends():#如果角色在好友中
            return {'result':False,'message':Lg().g(320)}
        else:
            dbFriend.addFriend(self._owner.baseInfo.id, playerId, 1, 0)
            self._friends.add(playerId)
            return {'result':True,'message':Lg().g(321)}

    def deleteFriend(self,characterId,friendId):
        """删除好友
        @param playerId: 角色的id
        """
        if friendId in self.getFriends():#如果在好友列表中
            self._friends.remove(friendId)
        result = dbFriend.deletePlayerFriend(characterId,friendId)
        if not result:
            return {'result':False,'message':Lg().g(325)}
        return {'result':True,'message':Lg().g(326)}

    def getFriendGuYong(self):
        """获取受雇用的好友的信息
        """

    def settleGuYong(self,friendid,result,zyid):
        """雇用结算
        """
        characterId = self._owner.baseInfo.id
        self._guyong.remove(friendid)
        dbFriend.UpdateGuYongState(characterId, friendid, 0)
        mcha = McharacterManager().getMCharacterById(friendid)
        rolename = mcha.get('nickname')
        zyinfo = dbZhanyi.ALL_ZHANGJIE_INFO.get(zyid)
        zyname = zyinfo.get('name','')
        dbFriend.addGuyongRecord(characterId, rolename, zyname,
                                  zyid, result, 100, 1)

    def GuYongHaoYou(self,tid):
        """雇用好友
        """
        characterId = self._owner.baseInfo.id
        if tid ==characterId:
            return {'result':False,'messge':u'不能雇用自己'}
        mcha = McharacterManager().getMCharacterById(tid)
        if not mcha:
            return {'result':False,'messge':u'好友信息不存在'}
        characterId = self._owner.baseInfo.id
        self.addFriend(characterId, tid)
        if tid in self._guyong:
            return {'result':False,'messge':u'已经被雇用'}
        from app.game.core.PlayersManager import PlayersManager
        from app.game.core.character.PlayerCharacter import PlayerCharacter
        toplayer = PlayersManager().getPlayerByID(tid)
        if not toplayer:
            toplayer = PlayerCharacter(tid)
        price = toplayer.level.getLevel()*1000
        if self._owner.finance.getCoin()<price:
            return {'result':False,'messge':u'资金不足无法雇用'}
        self._guyong.add(tid)#添加到雇用列表
        characterId = self._owner.baseInfo.id
        self._owner.finance.addCoin(-price)
        dbFriend.UpdateGuYongState(characterId,tid,1)
        return {'result':True,'messge':u'雇用成功'}

    def GetGuyongRecord(self):
        """获取雇用记录
        """
        characterId = self._owner.baseInfo.id
        datalist = dbFriend.getGuyongRecord(characterId)
        recordlist = []
        for record in datalist:
            info = {}
            info['datestr'] = str(record['reocrddate'])
            info['rolename'] = record['chaname']
            info['zyname'] = record['zyname']
            info['bresult'] = {1:u'胜利',2:u'失败'}.get('bresult',1)
            info['coin'] = record['coinbound']
            info['huoli'] = record['huoli']
            info['datestr'] = str(record['reocrddate'])
            recordlist.append(info)
        return {"result":True,'message':u'',"data":{'recordlist':recordlist}}

    def getGuYongList(self):
        """获取雇用列表
        """
        guyonglist = []
        for friend in self._guyong:
            info = {}
            mcha = McharacterManager().getMCharacterById(friend)
            if not mcha:
                continue
            info['chaid'] = friend
            info['chatype'] = 2
            info['tempid'] = mcha.get('profession')
            info['rolename'] = mcha.get('nickname')
            info['icon'] = mcha.get('profession')
            info['level'] = u'无'
            info['guanqia'] = u'无'
            info['skill'] = u'无'
            info['attack'] = 0
            info['fangyu'] = 0
            info['tili'] = 0
            info['minjie'] = 0
            info['price'] = mcha.get('level')*1000
            info['exp'] = 0
            guyonglist.append(info)
        return guyonglist


