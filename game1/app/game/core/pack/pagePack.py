#coding:utf8
"""
Created on 2011-7-13

@author: lan (www.9miao.com)
"""
class PagePack:
    """分页包裹"""
    def __init__(self,pageType,size=30):
        """
        @param items: [{'position':int,'wholeItem':{'porition':int,'itemComponent':Item Object}}]分页物品列表
        @param _pageTyep: int 分页的类型
        """
        self.items = []
        self._pageType = pageType
        self._tag = 0
        self._size = size
        
    def getSize(self):
        """获取包裹大小"""
        return self._size
        
    def getItemList(self):
        return [{'position':item['position'],'itemComponent':item['wholeItem']['itemComponent']} for item in self.items]
        
    def getPageType(self):
        """获取分页包裹的类型"""
        return self._pageType
    
    def setPageType(self,pageType):
        """设置分页包裹类型"""
        self._pageType = pageType
        
    def putItemByPosition(self, wholeItem):
        """根据位置放置物品
        @param position: int 物品的位置
        @param itemComponent: Item Object 物品
        """
        itemInfo={}
        itemInfo['position'] = self._tag
        itemInfo['wholeItem'] = wholeItem
        self.items.append(itemInfo)
        self._tag +=1
        
    def clearPagePack(self):
        """清空分页包裹中的数据"""
        self._tag = 0
        self.items = []
        
    def getPackageItemInfo(self):
        """获取包裹所有物品信息"""
        ItemsInfo = []
        for _item in self.items:
            itemInfo = {}
            itemInfo['position'] = _item['position']
            itemInfo['itemInfo'] = _item['wholeItem']['itemComponent'].formatItemInfo()
            ItemsInfo.append(itemInfo)
        return ItemsInfo
    
    def getRealPosition(self,position):
        """获取物品在包裹中得真实位置"""
        for item in self.items:
            if item['position'] == position:
                return item['wholeItem']['position']
        return -1
        
        
