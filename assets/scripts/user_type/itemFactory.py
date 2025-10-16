# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import itemData_itemData as ITEMDATA
import gameconst
import dataUtils

import copy

import BaseItem
import Item
import gameengine
import lingShouEgg
import EquipmentItem

class ItemFactory(object):
    NormalItemClassMap = {
        gameconst.ItemSubType.Equipment: EquipmentItem.EquipmentItem,
    }

    LingShouItemClassMap = {
        gameconst.ItemSubType.LingShouEgg:      lingShouEgg.LingShouEggItem,
    }

    @staticmethod
    def getItemTypes(itemId):
        itemData = dataUtils.getCommItemData(itemId)
        if not itemData:
            gameengine.reportCritical('itemFactor::getItemTypes, no itemId:', itemId)
            return None, None
        return itemData['type'], itemData['subType']

    @classmethod
    def getItemClass(cls, itemId):
        itemType, subType = cls.getItemTypes(itemId)
        if itemType == gameconst.ItemType.Normal:
            return cls.NormalItemClassMap.get(subType, Item.Item)
        elif itemType == gameconst.ItemType.LingShou:
            return cls.LingShouItemClassMap.get(subType, Item.Item)
        else:
            ERROR_MSG("getItemClass, no itemType:", itemType, itemId)

    @classmethod
    def _createItem(cls, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        itemClass = cls.getItemClass(itemId)
        if not itemClass:
            gameengine.reportCritical('_createItem, no itemClass:', itemId, itemClass)
            return
        return itemClass(itemId, itemNum=itemNum, bindType=bindType, **kwargs)

    @classmethod
    def createItem(cls, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        if itemNum > maxStackSize:
            raise Exception('createItem itemNum error!! itemNum:%s maxStackSize:%s please use createItemList' %
                            (itemNum, maxStackSize))
            return

        it = cls._createItem(itemId, itemNum, bindType, **kwargs)
        if not it:
            return
        it.initNewItemAttr(**kwargs)
        return it

    @classmethod
    def createItemList(cls, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        itemObjList = []
        maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        for oneNum in range(0, itemNum, maxStackSize):
            addNum = min(maxStackSize, itemNum - oneNum)
            it = cls.createItem(itemId, addNum, bindType, **kwargs)
            if not it:
                return itemObjList
            itemObjList.append(it)
        return itemObjList

    @classmethod
    def createItemWithSavedDict(cls, dataDict):
        itemId = dataDict.get('itemId', 0)
        if not dataUtils.isValidItemId(itemId):
            return
        return BaseItem.PureItem(dataDict)

    @classmethod
    def forkItemObject(cls, itemObj, **overwriteParams):
        # XXX()(ITEM): deepcopy存在性能问题, 后面可能需要针对itemObj进行精细化copy处理
        m_newItemObj = copy.deepcopy(itemObj)
        for k, v in overwriteParams.items():
            if k == "itemNum":
                m_newItemObj.setItemNum(v)
            else:
                setattr(m_newItemObj, k, v)
        return m_newItemObj
