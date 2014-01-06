#coding:utf8
"""
Created on 2011-3-27

@author: sean_lan
"""
from app.game.component.Component import Component
from app.game.core.pack import Package,EquipmentSlot
from app.game.core.Item import Item
import copy,random
from app.share.dbopear import dbItems
from app.game.memmode import tbitemadmin,tb_equipment
from app.game import util



LOST_ONE = 1000#掉落一个几率
LOST_TOW = 10#掉落两个几率
LOST_THREE = 2#掉落三个几率
RATE_BASE = 100000#几率基础值
PET_EGG = 20700005
QHSIDLIST = [20030048,20030049,20030050]
MAX_STACK = 99

def getlostnum():
    """获取掉落装备的个数"""
    if (LOST_ONE+LOST_TOW+LOST_THREE)>RATE_BASE:
        raise Exception("keng die ne ?")
    rate = random.randint(0,RATE_BASE)
    if rate>(LOST_ONE+LOST_TOW+LOST_THREE):
        return 0
    elif rate>(LOST_ONE+LOST_TOW):
        return 3
    elif rate>(LOST_ONE):
        return 2
    else:
        return 1

def checkRate(rate):
    """检测几率是否成功
    """
    nowrate = random.randint(1,100)
    if nowrate<rate:
        return True
    return False


class CharacterPackageComponent(Component):
    """角色的包裹组件
    """

    def __init__(self, owner):
        """初始化玩家包裹组件
        @param _package: Package object 包裹栏
        @param _equipmentSlot: EquipmentSlot object 装备栏
        """
        Component.__init__(self, owner)
        self._package = None
        self._tempPackage = None
        self._equipmentSlot = None

    def initPack(self,packageSize = 50):
        """初始化包裹"""
        self.setPackage(size= packageSize)
        self.setEquipmentSlot()

    def getPackage(self):
        """返回角色包裹信息"""
        return self._package

    def setPackage(self ,size = 12):
        """读取数据库设置角色包裹
        @param size: int 包裹的大小
        """
        self._package = Package.Package(size)
        itemlist = tbitemadmin.getAllPkByFk(self._owner.baseInfo.id)
        itemobjlist = tbitemadmin.getObjList(itemlist)
#        itemsPackInfo = db_package.getAllItemsByCharacterId(self._owner.baseInfo.id)
        for itemmode in itemobjlist:
            itemId = int(itemmode._name.split(':')[1])
            item = Item(id =itemId)
            itemPackInfo = itemmode.get('data')
            item.initItemInstance(itemPackInfo)
            self._package.putItemInPackage(item)

    def setEquipmentSlot(self,size = 10):
        """设置角色装备栏
        @param size: int 装备栏默认为10个部位
        """
        playerId = self._owner.baseInfo.id
        self._equipmentSlot = EquipmentSlot.EquipmentSlot()
        equipmentsInfo = tb_equipment.getObjData(playerId)
        if not equipmentsInfo:
            ee = tb_equipment.new({'characterId':playerId})
            equipmentsInfo = {}
        for equipmentInfo in equipmentsInfo.items():
            if equipmentInfo[1]==-1:
                continue
            part,itemId = equipmentInfo
            self._equipmentSlot.putEquipmentInEquipmentSlot(part,itemId)

    def getEquipmentSlot(self):
        """获取角色装备栏"""
        return self._equipmentSlot

    def getEquipmentSlotItemList(self):
        """获取装备栏信息
        """
        itemlist = [(pos,self._package.getItemById(itemid)) \
                     for pos,itemid in self._equipmentSlot._items.items()]
        return itemlist

    def getEquipmentSetAttr(self):
        """获取装备的套装属性
        """
        itemlist = [self._package.getItemById(itemid) \
                     for itemid in self._equipmentSlot._items.values()]
        itemsetlist = [item.baseInfo.itemtemplateInfo['suiteId'] for item in itemlist \
                        if item and item.baseInfo.itemtemplateInfo['suiteId']]
        nowsets = set(itemsetlist)
        info = {}
        for setid in nowsets:
            setinfo = dbItems.ALL_SETINFO[setid]
            setcount = itemsetlist.count(setid)
            allsetattr = eval(setinfo['effect'])
            for key,value in allsetattr.items():
                if key <= setcount:
                    effect = eval(value.get('effect'))
                    info = util.addDict(info, effect)
        return info

    def getAllEquipttributes(self):
        """得到玩家装备附加属性列表"""
        EXTATTRIBUTE = {}
        for item in [self._package.getItemById(itemid) \
                     for itemid in self._equipmentSlot._items.values()]:
            if not item:
                continue
            info = item.getItemAttributes()
            EXTATTRIBUTE = util.addDict(EXTATTRIBUTE, info)
        equipsetattr = self.getEquipmentSetAttr()
        EXTATTRIBUTE = util.addDict(EXTATTRIBUTE, equipsetattr)
        return EXTATTRIBUTE

    def putNewItemInPackage(self,item):
        """放置一个新的物品到包裹栏中
        @param item: Item object 物品实例
        @param position: int 物品的位置
        @param packageType: int 包裹的类型
        @param turned: int 是否是反牌子获取的
        """
        package = self._package
        maxstack = item.baseInfo.getItemTemplateInfo().get('maxstack',1)
        if maxstack>1:
            nowstack = item.pack.getStack()
            templateId = item.baseInfo.getItemTemplateId()
            state = 0
            for _item in package.getItems().values():
                if _item.baseInfo.getItemTemplateId()==templateId:
                    _item.pack.updateStack(_item.pack.getStack()+nowstack)
                    state = 1
                    break
            if not state:
                if item.baseInfo.getId()==0:
                    item.InsertItemIntoDB(characterId = self._owner.baseInfo.id)
                package.putItemInPackage(item)
        else:
            if item.baseInfo.getId()==0:
                item.InsertItemIntoDB(characterId = self._owner.baseInfo.id)
            package.putItemInPackage(item)
        return 2

    def unloadedEquipment(self,fromPosition):
        """卸下装备
        @param fromPosition: int 物品在包裹中的位置
        @param toPosition: int 装备的位置
        """
        equipPackage = self.getEquipmentSlot()
        result2 = equipPackage.updateEquipment(fromPosition, -1)
        if result2:
            return {'result':True,'message':u''}
        else:
            return {'result':False,'message':u''}

    def putNewItemsInPackage(self,itemTemplateId,count):
        """添加物品到包裹栏"""
        item = Item(itemTemplateId =itemTemplateId)
        maxstack = item.baseInfo.getItemTemplateInfo().get('maxstack',1)
        itemcndlist = []
        if maxstack>1:
            while count>MAX_STACK:
                count -=MAX_STACK
                itemcndlist = [MAX_STACK]
            if count>0:
                itemcndlist.append(count)
        else:
            itemcndlist = [1]*count
        for count in itemcndlist:
            _item = copy.deepcopy(item)
            _item.pack.setStack( count)
            self.putNewItemInPackage(_item)
        return True

    def countItemTemplateId(self,TemplateId):
        """判断是否存在物品"""
        package = self._package
        count = package.countItemTemplateId(TemplateId)
        return count

    def delItemByTemplateId(self,templateId,count):
        """根据物品的模板id删除物品
        @param templateId: int 模板的id
        @param count: int 物品的数量
        """
        package = self._package
        equipidlist = self._equipmentSlot._items.values()
        if self.countItemTemplateId(templateId)<count:
            return -1#数量不足
        for itemid,item in package.getItems().items():
            if itemid in equipidlist or item.baseInfo.itemTemplateId!=templateId:
                continue
            if count==0:
                break
            nowstack = item.pack.getStack()
            if nowstack>=count:
                package.deleteitemById(itemid,count=count)
                break
            else:
                package.deleteitemById(itemid,count = -1)
                count -= nowstack
        return 1#成功

    def delItemByItemId(self,itemId,count=1):
        """根据物品的id删除物品
        @param itemId: int 物品的id
        @param count: int 物品的数量
        """
        package = self._package.getPropsPagePack()
        result = package.deleteitemById(itemId,count = count)
        return result#成功

    def useItem(self,itemid):
        """使用物品
        @param packageType: int 包裹分页类型 1 全部 2
        @param position: int 物品所在包裹位置
        """
        item = self._package.getItemById(itemid)
        if not item:
            return {'result':False}
        script = item.baseInfo.getUseScript()#物品使用的脚本
        if not script:
            return {'result':False,'message':""}
        professionRequired = item.baseInfo.getItemProfession()
        if professionRequired!=self._owner.profession.getProfession() and professionRequired!=0:
            return {'result':False,'message':""}
        if item.baseInfo.getLevelRequired()> self._owner.level.getLevel():
            return {'result':False,'message':""}
        try:
            exec(script)#执行任务脚本
        except Exception,e:
            return {'result':False,'message':e.message}
        self.delItemByItemId(itemid, 1)
        return {'result':True,'message':""}

    def openChest(self,itemsInfolist,default,requiredItem,requiredCount):
        """开启宝箱
        @param itemsInfo: list [(物品ID，物品数量，随机区间)]随机掉落
        @param default: (物品ID，物品数量)默认掉落
        @param requiredItem: int 需要消耗的物品的模板ID
        @param requiredCount: int 需要消耗的物品的数量
        """
        if requiredItem!=0:
            count = self._owner.pack.countItemTemplateId(requiredItem)
            itemInfo = dbItems.all_ItemTemplate.get(requiredItem)
            if count<requiredCount:
                raise Exception(u'%s数量不足'%itemInfo.get('name'))
        itemsrates = [item[2] for item in itemsInfolist]
        iteminfo = None
        rate = random.randint(0,RATE_BASE)
        for index in range(len(itemsInfolist)):
            if rate<sum(itemsrates[:index+1]):
                iteminfo = itemsInfolist[index]
                break
        if not iteminfo:
            iteminfo = default
        result = self.putNewItemsInPackage(iteminfo[0], iteminfo[1])
        if not result:
            raise Exception("")
        self.delItemByTemplateId(requiredItem, requiredCount)

    def getMosaicItemPackage(self):
        """获取镶嵌装备包裹信息
        """
        canMosaicItemList = []#可强化的物品的列表
        equipidlist = self._equipmentSlot._items.values()
        for _item in self._package.getItems().values():
            if _item :
                if _item.baseInfo.getItemBodyType()>0:
                    iteminfo = {}
                    iteminfo['item'] = _item
                    if _item.baseInfo.id in equipidlist:
                        iteminfo['itemtag'] = 2
                    else:
                        iteminfo['itemtag'] = 1
                    canMosaicItemList.append(iteminfo)
        itemlist = [{'itemid':item['item'].baseInfo.id,\
                     'icon':item['item'].baseInfo.itemtemplateInfo['icon'],
                     'stack':item['item'].pack.getStack(),
                     'tempid':item['item'].baseInfo.getItemTemplateId(),
                     'itemtag':item['itemtag']}
                     for item in canMosaicItemList]
        data =  {'itemlist':itemlist}
        return {'result':True,'data':data}

    def HuoQuSuiPianBaoguo(self):
        """获取包裹中的碎片信息
        """
        suipianList = []#碎片石列表
        for i_item in self._package.getItems().values():
            itemTempinfo = i_item.baseInfo.getItemTemplateInfo()
            if itemTempinfo.get('compound',0):
                info = {}
                info['itemid'] = i_item.baseInfo.id
                info['icon'] = itemTempinfo.get('icon',0)
                info['tempid'] = itemTempinfo.get('id',0)
                info['stack'] = i_item.pack.getStack()
                suipianList.append(info)
        return {'result':True,'data':{'itemlist':suipianList}}

    def getOneItemInfo(self,itemid):
        """获取当个物品的信息
        """
        i_item = self._equipmentSlot.getItemInfoByItemid(itemid)
        if not i_item:
            i_item = self._package.getItemById(itemid)
        if not i_item:
            return {'result':False,'message':u'物品信息不存在'}
        info = i_item.formatItemInfoForWeiXin()
        return {'result':True,'data':info}

    def CompoundItem(self,itemId):
        """合成物品
        """
        suipianinfo = dbItems.all_ItemTemplate.get(itemId)
        if not suipianinfo:
            return {'result':False,'message':u"碎片信息不存在"}
        coinrequired = suipianinfo.get('comprice',0)
        if coinrequired > self._owner.finance.getCoin():
            return {'result':False,'message':u"金币不足"}

        newtempid = suipianinfo.get('compound',0)
        newiteminfo = dbItems.all_ItemTemplate.get(newtempid)
        if not newiteminfo:
            return {'result':False,'message':u"该物品不能合成"}
        itemrequired = self._package.countItemTemplateId(itemId)
        if itemrequired<4:
            return {'result':False,'message':u"缺少材料"}
        self._owner.finance.addCoin(-coinrequired)
        self.delItemByTemplateId(itemId, 4)
        newiteminfo = dbItems.all_ItemTemplate.get(newtempid)
        script = newiteminfo.get('script',0)
        if script:
            exec(script)
        else:
            self.putNewItemsInPackage(newtempid, 1)
        return {'result':True,'message':u"合成成功"}


    def equipEquipmentByItemId(self,itemId):
        """穿上装备
        @param fromPosition: int 物品在包裹中的位置
        @param toPosition: int 装备的位置
        """
        item = self._package.getItemById(itemId)
        if not item:
            return {'result':False,'message':""}
        itemPageType = item.baseInfo.getItemPageType()
        if itemPageType!=1:
            return self.useItem( itemId)
        toPosition = item.baseInfo.getItemTemplateInfo().get('bodyType',0)
        if toPosition<1 or toPosition>6:
            return {'result':False,'message':""}
        if item.baseInfo.getItemBodyType()==-1:
            return {'result':False,'message':""}
        if item.baseInfo.getItemBodyType()!=toPosition:
            return {'result':False,'message':""}
        if item.baseInfo.getLevelRequired()> self._owner.level.getLevel():
            return {'result':False,'message':""}
        equipPackage = self.getEquipmentSlot()
        toItemid = equipPackage.getItemByPosition(toPosition)
        if not toItemid or toItemid<0:
            result2 = equipPackage.updateEquipment(toPosition, itemId)
            if result2:
                return {'result':True,'message':""}
            else:
                return {'result':False,'message':""}
        else:
            result1 = equipPackage.updateEquipment(toPosition, itemId)
            if result1:
                return {'result':True,'message':""}
            else:
                return {'result':False,'message':""}

    def getPackageItemList(self):
        """获取包裹的物品信息
        """
        data = {}
        itemList = self._package._items.values()
        equipidlist = self._equipmentSlot._items.values()
        data['itemlist'] = [{'itemid':itemInfo.baseInfo.id,
                             'icon':itemInfo.baseInfo.getItemTemplateInfo()['icon'],
                             'tempid':itemInfo.baseInfo.getItemTemplateId(),
                             'stack':itemInfo.pack.getStack(),
                             'exp':itemInfo.exp}\
                             for itemInfo in itemList \
                             if itemInfo.baseInfo.id not in equipidlist]
        return {'result':True,'data':data}

    def unloaded(self,itemId):
        """卸下装备
        """
        equipPackage = self.getEquipmentSlot()
        fromPosition = equipPackage.getItemPositionById(itemId)
        if fromPosition<0:
            return {'result':False,'message':u''}
        result2 = equipPackage.updateEquipment(fromPosition, -1)
        if result2:
            return {'result':True,'message':u''}
        else:
            return {'result':True,'message':u''}





