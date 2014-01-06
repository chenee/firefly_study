#coding:utf8
"""
Created on 2011-3-23

@author: sean_lan
"""
from app.share.dbopear import dbuser
from memclient import mclient
from app.share.mcharacter.mcharacter import Mcharacter

INITTOWN = 1000

class User:
    """用户类"""

    def __init__(self, name, password, dynamicId=-1):
        """
        @param id: int 用户的id
        @param name: str用户的名称
        @param password: str 用户的密码
        @param pid: int 邀请者的id
        @param dynamicId: str 登录时客户端的动态ID
        @param characterId: dict 用户的角色
        @param isEffective: bool 是否是有效的
        """
        self.id = 0
        self.name = name
        self.password = password
        self.pid = 0
        self.dynamicId = dynamicId
        self.isEffective = True
        self.characterId = 0
        self.characterInfo = {}

        self.initUser()

    def initUser(self):
        """初始化用户类"""
        data = dbuser.getUserInfoByUsername(self.name,self.password)
        if not data:
            self.isEffective = False
            return

        if not data['enable']:
            self.isEffective = False

        self.id = data.get('id',0)
        self.pid = data.get('pid',0)
        self.characterId = data.get('characterId',0)

    def getNickName(self):
        """获取账号名
        """
        return self.name

    def CheckEffective(self):
        """检测账号是否有效"""
        return self.isEffective

    def checkClient(self,dynamicId):
        """检测客户端ID是否匹配"""
        return self.dynamicId == dynamicId

    def getUserCharacterInfo(self):
        """获取角色信息"""
        info = {}
        info['userId'] = self.id
        info['defaultId'] = self.characterId
        if not self.characterId:
            info['hasRole'] = False
        else:
            info['hasRole'] = True
        return info

    def getCharacterInfo(self):
        """获取角色的信息"""
        if not self.characterInfo:
            self.characterInfo = dbuser.getUserCharacterInfo(self.characterId)
        return self.characterInfo

    def setDynamicId(self,dynamicId):
        """设置动态ID
        @param dynamicId: int 客户端动态ID
        """
        self.dynamicId = dynamicId

    def getDynamicId(self):
        """获取用户动态ID"""
        return self.dynamicId

    def creatNewCharacter(self ,nickname ,profession):
        """创建新角色
        @profession （int） 角色职业 （0 新手 1战士 2 法师 3 游侠 ）
        """
        if profession not in range(1,7):
            return {'result':False,'message':u'profession_error'}
        if len(nickname)<2 or len(nickname)>20:
            return {'result':False,'message':u'yhm_buhege'}
        if self.characterId:
            return {'result':False,'message':u'yijingchuangjian'}
        if not dbuser.checkCharacterName(nickname):
            return {'result':False,'message':u'yhm_yicunzai'}
        characterId = dbuser.creatNewCharacter(nickname, profession, self.id)
        if characterId:
            self.characterId = characterId
            data = {}
            data['userId'] = self.id
            data['newCharacterId'] = characterId
            cinfo = {'id': characterId,
                     'level': 1,
                     'profession': profession,
                     'nickname': nickname
                    }
            mcha = Mcharacter(characterId, 'character%d' % characterId, mclient)
            mcha.initData(cinfo)
            mcha.insert()
            return {'result': True, 'message': u'创建角色成功', 'data': data}
        else:
            return {'result': False, 'message': u'创建角色失败'}

    def disconnectClient(self):
        """断开"""
        from app.gate.rootservice.rservices import SavePlayerInfoInDB, pushObject
        # dynamicId = self.dynamicId
        SavePlayerInfoInDB(self.dynamicId)
        msg = u"您账户其他地方登录"
        self.isEffective = False
        pushObject(905,msg, [self.dynamicId])


