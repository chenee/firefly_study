#coding:utf8
"""
Created on 2011-3-27
@author: sean_lan
"""

class Package(object):
    """包裹栏
    @param _equipPagePack: BasePackage object  包裹一般物品分页
    @param _taskPagePack: BasePackage object  任务物品分页
    """
    LIMIT = 30
    MAXPAGE = 5
    def __init__(self,size=150):
        """
        @param size: int 包裹的大小
        """
        self._items = {}
        self._size = size
        
    def setSize(self,size):
        """设置包裹大小"""
        self._size = size
        
    def getPackageByType(self,packType):
        """根据包裹类型获取包裹实例"""
        return self
        
    def getPropsPagePack(self):
        """获取全部物品包裹"""
        return self
    
    def getTaskPagePackItem(self):
        """获取任务物品分页包裹物品列表信息"""
        return self._items
    
    def putItemInPackage(self,item):
        """初始化包裹栏
        @param position: int 放置的位置
        @param item: Item Object 物品实例
        """
        self._items[item.baseInfo.id] = item
        
    def getItemById(self,itemId):
        """根据物品的ID获取物品实例
        """
        return self._items.get(itemId)
        
    def getItems(self):
        """获取物品的list
        """
        return self._items
        
    def countItemTemplateId(self,templateId):
        """获取指定模板id的物品数量
        @param templateId: int 物品的模板id
        """
        count = 0
        for item in self._items.values():
            if item.baseInfo.getItemTemplateId()==templateId:
                count+=item.pack.getStack()
        return count
        
    def deleteitemById(self,itemid,count = -1):
        """删除包裹中的物品
        """
        item = self._items.get(itemid)
        if item:
            nowstack = item.pack.getStack()
            if count==-1 or nowstack<=count:
                item.destroyItemInDB()
                self._items.pop(itemid)
            else:
                item.pack.updateStack(nowstack-count)
            return True
        return False
    
    def removeItemById(self):
        pass
        
        
    
