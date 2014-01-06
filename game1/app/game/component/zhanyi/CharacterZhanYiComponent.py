#coding:utf8
"""
Created on 2013-1-8
角色的战役信息
@author: lan (www.9miao.com)
"""
from app.game.component.Component import Component
from app.game.core.character.Monster import Monster
from app.game.core.fight.battleSide import BattleSide
from app.game.core.Item import Item
from app.share.dbopear import dbZhanyi,dbDropout
from app.game.memmode import tb_zhanyi_record_admin

HUOLI_REQUIRED = 1#活力需求
#首次通关奖励
FIRST_BOUND = {1000:53000001,
               1001:53000001,
               1002:53000001,
               1003:53000001,
               1004:53000001,
               1005:42004026}

class CharacterZhanYiComponent(Component):
    """角色的战役信息
    """

    def __init__(self,owner):
        """初始化爬塔信息
        """
        Component.__init__(self, owner)
        self.record = {}#角色战役记录
        self.initData()

    def initData(self):
        """读取角色的初始化角色的战役信息
        """
        characterId = self._owner.baseInfo.id
        recordpklist = tb_zhanyi_record_admin.getAllPkByFk(characterId)
        recordlist = tb_zhanyi_record_admin.getObjList(recordpklist)
        self.record = dict([(recordObj.get('data').get('zhangjie'),recordObj.get('data')) for recordObj in recordlist])

    def getCurrentZJ(self):
        """获取角色当前战役的信息"""
        if self.record:
            _currentZJ = sorted(self.record.keys())[-1]
            zjlist = sorted(dbZhanyi.ALL_ZHANGJIE_INFO.keys())
            index = zjlist.index(_currentZJ)
            nextindex = index+1
            if nextindex<len(zjlist):
                _currentZJ = zjlist[nextindex]
        else:
            _currentZJ = 1000
        return _currentZJ

    def getCurrentZY(self):
        """获取当前战役的ID"""
        zhanjieInfo = dbZhanyi.ALL_ZHANGJIE_INFO.get(self.currentZJ)
        currentZY = zhanjieInfo.get('yid')
        return    currentZY

    @property
    def currentZJ(self):
        """获取当前章节的ID"""
        return self.getCurrentZJ()

    @property
    def currentZY(self):
        """获取当前战役的ID"""
        return self.getCurrentZY()


    def getZhanYiInfo(self,index):
        """获取张角信息
        """
        if index ==0:
            zid = self.currentZJ
        else:
            zid = index
        response = {}
        response['cityid'] = zid
        response['citylist'] = [record['star'] for record in self.record.values()]
        return {'result':True,'message':u'','data':response}

    def _getZhanYiInfo(self,index):
        """获取角色的当前战役信息
        """
        if index ==0:
            zid = self.currentZY
        else:
            zid = index
        gropInfo = dbZhanyi.ALL_ZHANGJIE_GROP.get(zid)
        if not gropInfo:
            return {}
#            return {'result':False,'message':u'地图信息不存在'}
        gropInfo = sorted(gropInfo)
        zyinfo = []
        for cityid in gropInfo:
            info = {}
            city = dbZhanyi.ALL_ZHANGJIE_INFO.get(cityid)
            cityId = city['id']
            info['mid'] = cityId
            record = self.record.get(cityId)
            if record:
                info['pj'] = record['star']
                info['zt'] = 2
            elif cityid==self.currentZJ:
                info['pj'] = 0
                info['zt'] = 1
            else:
                info['pj'] = 0
                info['zt'] = 0
            zyinfo.append(info)
        info = {}
        info['mapimg'] = 1
        info['mapid'] = zid
        info['citylist'] = zyinfo
        return info
#        info = {'index':zid,'zyinfo':zyinfo}
#        return {'result':False,'message':u'','data':info}

    def doZhangJie(self,zhangjieid):
        """章节战斗
        @param zhangjieid: int 章节的
        """
        if zhangjieid>self.currentZJ:
            return {'result':False,'message':u'当前章节未被激活'}
        zhanjieInfo = dbZhanyi.ALL_ZHANGJIE_INFO.get(zhangjieid)
        if not zhanjieInfo:
            return {'result':False,'message':u'战役信息不存在'}
        levelrequired = zhanjieInfo.get('levelrequired')
        if self._owner.level.getLevel()<levelrequired:
            return {'result':False,'message':u'当前等级不足'}
#        if self._owner.attribute.getEnergy() < HUOLI_REQUIRED:
#            return {'result':False,'message':u'当前活力不足'}
        self._owner.attribute.addEnergy(-HUOLI_REQUIRED)
        from app.game.core.fight.fight import Fight
        ruleInfo = eval(zhanjieInfo.get('mconfig'))
        temlist,rule = ruleInfo[0],ruleInfo[1]
        i = 100
        challengers = BattleSide([self._owner])
        deffen = []
        for tem in temlist:
            i+=1
            monser = Monster(id = i,templateId = tem)
            deffen.append(monser)
        defenders = BattleSide(deffen,state = 0)
        defenders.setMatrixPositionBatch(rule)
        data = Fight( challengers, defenders, 600)
        data.DoFight()
        battlestar = data.battlestar
        coinbound = 0
        huoliChange = -HUOLI_REQUIRED
        expBound = 0
        itemBound = []
        if data.battleResult == 1:#如果战斗胜利
            _reord = {'zhanyi':zhanjieInfo['yid'],'zhangjie':zhangjieid,'star':battlestar}
            characterId = self._owner.baseInfo.id
            if zhangjieid  not in self.record.keys():
                self.record[zhangjieid]=_reord
                self._owner.guanqia = zhangjieid
                _reord['characterId'] = characterId
                tb_zhanyi_record_admin.new(_reord)

            elif self.record[zhangjieid]['star']<battlestar:
                pk = self.record[zhangjieid]['id']
                zjrecord = tb_zhanyi_record_admin.getObj(pk)
                zjrecord.update('star', battlestar)

                self.record[zhangjieid]=_reord
            zhanjieInfo = dbZhanyi.ALL_ZHANGJIE_INFO.get(zhangjieid)
            coinbound = zhanjieInfo.get('coin')
            expBound = zhanjieInfo.get('exp')
            dropid = zhanjieInfo.get('dropid')
            dropoutIitem = dbDropout.getDropByid(dropid)
            if dropoutIitem:
                itemid = dropoutIitem.baseInfo.itemTemplateId
                itemBound.append(itemid)
                self._owner.pack.putNewItemInPackage(dropoutIitem)#添加物品奖励
            self._owner.finance.addCoin(coinbound)#添加金币奖励
            self._owner.level.addExp(expBound)#添加经验奖励
        self._owner.matrix.cleanMatrixSetting(result = data.battleResult,zyid=zhangjieid)
        setData = {'coin':coinbound,'exp':expBound,'star':battlestar,
                   'item':itemBound,'huoli':huoliChange}
        return {'result':True,'data':{'fight':data,'setData':setData}}

    def getCityInfo(self,mid):
        """获取单个城镇的信息
        """
        zhanjieInfo = dbZhanyi.ALL_ZHANGJIE_INFO.get(mid)
        info = {}
        info['mid'] = mid
        info['mnane'] = zhanjieInfo['name']
        info['mdesc'] = zhanjieInfo['mdesc']
        info['xiaoguai'] = zhanjieInfo['monsterdesc']
        info['boss'] = zhanjieInfo['boss']
        info['weiwang'] = zhanjieInfo['exp']
        info['coin'] = zhanjieInfo['coin']
        itemid = zhanjieInfo['itembound']
        iteminfo = {}
        if itemid:
            itemin = Item(itemTemplateId = itemid)
            iteminfo['wname'] = itemin.baseInfo.getName()
            iteminfo['pinzhi'] = itemin.baseInfo.getBaseQuality()
        info['wupin'] = iteminfo
        return {'result':True,'message':u'','data':info}


    def checkClean(self,zhangjieid):
        """检测章节是否通关
        """
        if self.currentZJ>zhangjieid:
            return True
        return False


