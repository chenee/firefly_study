#coding:utf8
"""
Created on 2011-3-27

@author: sean_lan
"""
import math

class BasePackage(object):
    """
    base package object
    @param size: int 包裹的大小
    @param _items: object list 包裹中的物品列表
    """

    def __init__(self, size,packageType=0):
        """根据背包大小初始化背包
        """
        self._size = 100
        self._packageType = packageType
        self.limit = 30
        self._items = []

    def getSize(self):
        """获取背包大小
        """
        return self._size

    def setSize(self, size):
        """设置背包大小
        """
        self._size = size

    def getPackageType(self):
        """获取包裹类型"""
        return self._packageType

    def setPackageType(self,packageType):
        """设置包裹类型"""
        self._packageType = packageType

    def getItemList(self):
        """获取物品列表"""
        return self._items

    def getItems(self):
        """获取包裹中的物品"""
        return self._items

    def setItems(self, items):
        """设置包裹中的物品
        @param items: Items object list
        """
        self._items = items

    def getOneRecordByPosition(self, position):
        """获取指定位置的物品以及物品的位置信息
        @param position: int 表示包裹中的位置
        """
        for item in self._items:
            if item['position'] == position:
                return item
        return None

    def getItemByPosition(self, position):
        """根据坐标得到物品
        @param position: int 物品的位置
        """
        for item in self._items:
            if item['position'] == position:
                return item['itemComponent']
        return None

    def getPositionByItemId(self,itemId):
        """根据物品的ID查找物品在包裹中的位置
        @param itemId: int 物品的id
        """
        for item in self._items:
            if item['itemComponent'].baseInfo.id ==itemId:
                return item['position']
        return -1#没有找到时返回-1

    def getItemInfoByItemid(self,itemid):
        """根据物品id获得物品实例
        @param itemid: int 物品id
        """
        va=self.getPositionByItemId(itemid)
        if va!=-1:
            return self.getItemByPosition(va)
        else:
            return None

    def putItemByPosition(self, position, itemComponent):
        """根据位置放置物品
        @param position: int 物品的位置
        @param itemComponent: Item Object 物品
        """
        for item in self._items:
            if position == item['position']:
                item['itemComponent']=itemComponent
                return
        self._items.append({'position':position, 'itemComponent':itemComponent})

    def updateItemStack(self,position,stack):
        """更新物品层叠数"""
        for fromItem in self._items:
            if position == fromItem['position']:
                if stack==0:
                    self._items.remove(fromItem)
                    self.deleteItemInPackage(position)
                    return
                fromItem['itemComponent'].pack.updateStack(stack)

    def removeItemByPosition(self,position):
        """移除包裹中的物品"""
        for fromItem in self._items:
            if position == fromItem['position']:
                self._items.remove(fromItem)

    def findSparePositionForItem(self):
        """寻找包裹栏中可以放置物品的位置"""
        for position in range(0, self._size):
            result = self.getItemByPosition(position)
            if result is None:
                return position
        return -1

    def isFull(self):
        """ 判断临时包裹是否已满"""
        position = self.findSparePositionForItem
        if position == -1:
            return True
        return False

    def canPutItem(self, item,count):
        """该position上能否放置物品
        @param toPosition: 目标位置
        @param formerPosition: 原来的位置
        """
        maxstack = item.baseInfo.getItemTemplateInfo().get('maxstack',1)
        requiredcnt = math.ceil(count/(maxstack*1.0))
        nowcnt = self.findSparePositionNum()
        if nowcnt<requiredcnt:
            return False
        return True

    def canMergeItem(self, toPosition, formerPosition):
        """
                     能否合并物品
        @param toPosition: 目标位置
        @param formerPosition: 原来的位置
        """
        dragItem = self.getItemByPosition(formerPosition)
        destItem = self.getItemByPosition(toPosition)
        if not destItem :
            return True
        destItemTemplate = destItem.baseInfo.getItemTemplateInfo()
        dragItemTemplate = dragItem.baseInfo.getItemTemplateInfo()
        if dragItem is destItem:
            return True
        if destItemTemplate['stack'] == -1:
            return False
        if destItemTemplate['id'] <> dragItemTemplate['id']:
            return False
        return True

    def MergeItems(self,fromposition,toposition):
        """合并物品"""
        state = 0
        if fromposition== toposition:
            return 1 #位置一致，不能合并
        fromItem = self.getItemByPosition(fromposition)
        toItem = self.getItemByPosition(toposition)
        if not fromItem or not toItem:
            return 1 #有物品不存在不能合并
        maxstack = fromItem.baseInfo.getItemTemplateInfo().get('maxstack',1)
        fromstack = fromItem.pack.getStack()
        tostack = toItem.pack.getStack()
        if fromstack == maxstack:
            return 0   #起始位置物品堆叠数达到上限，不能进行合并
        if fromItem.baseInfo.getItemTemplateId()!=toItem.baseInfo.getItemTemplateId():
            return 1 #物品类型不同不能合并
        if tostack == maxstack:#置换
            self.transpositionItems(fromposition, toposition)
            return 0
        if tostack+fromstack<maxstack:
            startstack = tostack+fromstack
            endstack = 0
        else:
            startstack = maxstack
            endstack = tostack+fromstack-maxstack
        fromItem.pack.updateStack(startstack)
        if startstack != maxstack:
            state = 1
        if endstack<=0:
            self.deleteItemInPackage(toposition)
        else:
            toItem.pack.updateStack(tostack+fromstack-maxstack)
        return state

    def MergePackage(self):
        """合并包裹中能合并的物品"""
        positionList = [item['position'] for item in self._items]
        for i in range(len(positionList)):
            fromposition = positionList[i]
            if i ==len(positionList)-1:
                return
            for toposition in positionList[i+1:]:
                state = self.MergeItems(fromposition, toposition)
                if not state:
                    break

    def clearPackage(self):
        """清空包裹中的物品"""
        self.setItems([])

    def getPackageItemInfo(self):
        """获取包裹所有物品信息"""
        ItemsInfo = []
        for _item in self._items:
            itemInfo = {}
            itemInfo['position'] = _item['position']
            itemInfo['itemInfo'] = _item['itemComponent'].formatItemInfo()
            ItemsInfo.append(itemInfo)
        return ItemsInfo

    def dropItemByPosition(self,position):
        """删除物品"""
        for item in self._items:
            if item['position']== position:
                self._items.remove(item)

    def findSparePositionNum(self):
        """获取剩余空隙位置的数量"""
        return self._size-len(self._items)

    def countItemTemplateId(self,templateId):
        """获取指定模板id的物品数量
        @param templateId: int 物品的模板id
        """
        count = 0
        for item in self._items:
            if item['itemComponent'].baseInfo.getItemTemplateId()==templateId:
                count+=item['itemComponent'].pack.getStack()
        return count

    def getItemTemplateIdPositions(self,templateId):
        """指定模板id的物品数量及数量"""
        infos = []
        for item in self._items:
            if item['itemComponent'].baseInfo.getItemTemplateId()==templateId:
                info = {}
                info['position'] = item['position']
                info['stack'] = item['itemComponent'].pack.getStack()
                infos.append(info)
        return infos

    def getItemPositionById(self,itemId):
        """根据物品的id获取物品的位置"""
        for item in self._items:
            if item['itemComponent'].baseInfo.getId()==itemId:
                return item['position']
        return -1

    def getItemByVirtualPostion(self,position,page):
        """根据虚拟的坐标和包裹分页获取物品"""
        postion = self.getRealPostion(position, page)
        item = self.getItemByPosition(postion)
        return item

    def getRealPostion(self,position,page):
        """获取物品在包裹中的真实位置"""
        realPostion = position + (page-1)*30
        return realPostion

    def getVirtualPostion(self,postion):
        """获取虚拟的坐标与分页"""
        page = (postion/self.limit)+1
        vpostion = postion%self.limit
        return page,vpostion

