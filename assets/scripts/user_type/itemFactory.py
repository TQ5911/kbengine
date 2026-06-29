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
        gameconst.ItemSubEnum.Equipment: EquipmentItem.EquipmentItem,
    }

    LingShouItemClassMap = {
        gameconst.ItemSubEnum.LingShouEgg: lingShouEgg.LingShouEggItem,
    }

    @staticmethod
    def getItemTypes(itemId):
        _itemData = dataUtils.getCommItemData(itemId)
        if not _itemData:
            gameengine.panicStack('itemFactor::getItemTypes, no itemId:', itemId)
            return None, None
        return _itemData['type'], _itemData['subType']

    @classmethod
    def getItemClass(cls, itemId):
        _itemType, subType = cls.getItemTypes(itemId)
        if _itemType == gameconst.ItemEnum.Normal:
            return cls.NormalItemClassMap.get(subType, Item.Item)
        elif _itemType == gameconst.ItemEnum.LingShou:
            return cls.LingShouItemClassMap.get(subType, Item.Item)
        else:
            LOG_ERR("getItemClass, no _itemType:", _itemType, itemId)

    @classmethod
    def _createItem(cls, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(), **keywordargs):
        _itemClass = cls.getItemClass(itemId)
        if not _itemClass:
            gameengine.panicStack('_createItem, no itemClass:', itemId, _itemClass)
            return
        return _itemClass(itemId, itemNum=itemNum, bindType=bindType, **keywordargs)

    @classmethod
    def createItem(cls, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        _maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        if itemNum > _maxStackSize:
            raise Exception('createItem itemNum error!! itemNum:%s maxStackSize:%s please use createItemList' %
                            (itemNum, _maxStackSize))
        
        _it = cls._createItem(itemId, itemNum, bindType, **kwargs)
        if not _it:
            return
        _it.initNewItemAttr(**kwargs)
        return _it

    @classmethod
    def createItemList(cls, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        _itemObjList = []
        maxStackSize = BaseItem.BaseItem.maxStackSize(itemId)
        for _oneNum in range(0, itemNum, maxStackSize):
            addNum = min(maxStackSize, itemNum - _oneNum)
            _it = cls.createItem(itemId, addNum, bindType, **kwargs)
            if not _it:
                return _itemObjList
            _itemObjList.append(_it)
        return _itemObjList

    @classmethod
    def createItemWithSavedDict(cls, dataDict):
        _itemId = dataDict.get('itemId', 0)
        if not dataUtils.isValidItemId(_itemId):
            return

        return BaseItem.PureItem(dataDict)

    @classmethod
    def forkItemObject(cls, itemObj, **overwriteParams):
        # XXX()(ITEM): deepcopy存在性能问题, 后面可能需要针对itemObj进行精细化copy处理
        mNewItemObj = copy.deepcopy(itemObj)
        for k, v in overwriteParams.items():
            if k == "itemNum":
                mNewItemObj.setItemNum(v)
            else:
                setattr(mNewItemObj, k, v)
        return mNewItemObj
