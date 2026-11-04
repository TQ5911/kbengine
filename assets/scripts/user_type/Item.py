# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine
import json
import abc
import gameengine
import gameconst
import dataUtils
import utils
import userType
import itemData_itemData as ITEMDATA
import itemFactory
import BaseItem
import SoulInfo
import gzip
import gamelog
import _pickle as cPickle
import time

class Item(BaseItem.BaseItem):
    # 配置数据在 itemData_itemData的物品

    def __init__(self, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        super(Item, self).__init__(itemId, itemNum, bindType, **kwargs)

    def initNewItemAttr(self, **kwargs):
        # 创建一个新物品时候的初始化
        self.uniqueId = KBEngine.genUUID64()
        _itemData = dataUtils.getCommItemData(self.itemId)
        self.itemType = _itemData['type']
        self.itemSubType = _itemData['subType']
        self.quality = _itemData['quality']
        expireTime = _itemData['expirationDate']
        expireTimeStr = _itemData.get('itemTimeOut')
        if expireTime > 0:
            self.expireTime = utils.curTS() + expireTime
        elif expireTimeStr:
            if expireTimeStr.startswith('cityBattle'):
                self.expireTime = utils.getSiegeWarItemExpireTime()
            else:
                self.expireTime = int(utils.parseTimeStr(expireTimeStr))

        if _itemData.get('usableTime'):
            self.enableTime = utils.parseTimeStr(_itemData['usableTime'])
        self.lockStatus = gameconst.ItemLockStatus.UNLOCKED
        if kwargs.get('rollProps'):
            self.rollProps = kwargs['rollProps']
        else:
            self.rollProps = {}
            if 'extra' in kwargs:
                if 'school' in kwargs['extra']:
                    allowLucky = self.bindType != gameconst.ItemBindType.BIND
                    self.rollProps = utils.rollItemProps(self.itemId, self.itemSubType, kwargs['extra']['school'], allowLucky)

        self._initSoulData(kwargs)
        return True

    def _initSoulData(self, kwargs):
        if self.isSoul():
            SoulInfo.initItem(self, kwargs)

    def onSpecificItemChanged(self, attrJson):
        _itemData = dataUtils.getCommItemData(self.itemId)
        self.itemType = _itemData['type']
        self.itemSubType = _itemData['subType']
        self.quality = _itemData['quality']
        if attrJson:
            _dic = json.loads(attrJson)
            self.__dict__.update(_dic)
        self._ensureSoulData()
        return

    def _ensureSoulData(self):
        if self.isSoul():
            SoulInfo.ensureItem(self)

    def exportSoulPayload(self):
        self._ensureSoulData()
        return SoulInfo.readItem(self)

    def hasSoulAffix(self):
        if not self.isSoul():
            return False
        return SoulInfo.hasAnyProp(self.exportSoulPayload())

    def getSoulQualityScore(self):
        if not self.isSoul():
            return 0
        return SoulInfo.calcBaseQualityScore(self.exportSoulPayload()['baseProps'])

    def attr2Dict(self):
        mDict = {}
        mDict["lockStatus"] = self.lockStatus
        rollProps = self.__dict__.get('rollProps')
        if rollProps is None:
            rawAttrJson = self.__dict__.get('attrJson')
            loaded = json.loads(rawAttrJson) if isinstance(rawAttrJson, str) and rawAttrJson else {}
            rollProps = loaded['rollProps'] if isinstance(loaded, dict) and 'rollProps' in loaded else {}
        mDict["rollProps"] = rollProps
        if self.isSoul():
            self._ensureSoulData()
            mDict.update(SoulInfo.itemPersistDict(self))
        return mDict

    def attr2Json(self):
        mDict = self.attr2Dict()
        return json.dumps(mDict) if mDict else ""

    def simpleAttr2Json(self):
        return self.attr2Json()
    
    def canMerge(self, withItem, skipItemId=False, skipBindType=False, skipMaxStack=False,
                 skipExpired=False, now=utils.curTS(), **kwargs):
        if not skipItemId and self.itemId != withItem.itemId:
            return False
        if not skipBindType and self.bindType != withItem.bindType:
            return False
        if not skipMaxStack and self.maxStackSize(self.itemId) <= 1:
            return False
        if self.expireTime != withItem.expireTime:
            return False
        if self.enableTime != withItem.enableTime:
            return False
        if self.lockStatus != withItem.lockStatus:
            return False
        if self.isSoul() or withItem.isSoul():
            return False
        if self.rollProps or withItem.rollProps:
            return False
        return True

    def getItemName(self):
        mData = dataUtils.getCommItemData(self.itemId)
        if mData is None:
            return ''
        return mData['name']


class ReUseItem(Item):
    # 可以重复使用的物品
    def __init__(self, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **keywordargs):
        super(ReUseItem, self).__init__(itemId, itemNum, bindType, **keywordargs)
        self.useTimes = 0

    def attr2Dict(self):
        _dic = super(ReUseItem, self).attr2Dict()
        _dic['useTimes'] = self.useTimes
        return _dic

    def initNewItemAttr(self, **kwargs):
        # 创建一个新物品时候的初始化
        super(ReUseItem, self).initNewItemAttr(**kwargs)
        _itemData = dataUtils.getCommItemData(self.itemId)
        self.useTimes = _itemData['useNum']
        return True

    def isReUseItem(self):
        return True

    def canMerge(self, withIt, **kwargs):
        return False

