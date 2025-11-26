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
import gzip
import gamelog
import _pickle as cPickle
import time

class Item(BaseItem.BaseItem):
    # 配置数据在 itemData_itemData的物品

    def __init__(self, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        super(Item, self).__init__(itemId, itemNum, bindType, **kwargs)
        return

    def initNewItemAttr(self, **kwargs):
        # 创建一个新物品时候的初始化
        self.uniqueId = KBEngine.genUUID64()
        itemData = dataUtils.getCommItemData(self.itemId)
        self.itemType = itemData['type']
        self.itemSubType = itemData['subType']
        self.quality = itemData['quality']
        expireTime = itemData['expirationDate']
        expireTimeStr = itemData.get('itemTimeOut')
        if expireTime > 0:
            self.expireTime = utils.getNow() + expireTime
        elif expireTimeStr:
            if expireTimeStr.startswith('cityBattle'):
                self.expireTime = utils.getSiegeWarItemExpireTime()
            else:
                self.expireTime = int(utils.parseTimeStr(expireTimeStr))

        if itemData.get('usableTime'):
            self.enableTime = utils.parseTimeStr(itemData['usableTime'])
        self.lockStatus = gameconst.ItemLockStatus.UNLOCKED
        return True

    def onSpecificItemChanged(self, attrJson):
        itemData = dataUtils.getCommItemData(self.itemId)
        self.itemType = itemData['type']
        self.itemSubType = itemData['subType']
        self.quality = itemData['quality']
        if not attrJson:
            return
        dic = json.loads(attrJson)
        self.__dict__.update(dic)
        return

    def attr2Json(self):
        m_dict = self.attr2Dict()
        return json.dumps(m_dict) if m_dict else ""

    def attr2Dict(self):
        m_dict = {}
        m_dict["lockStatus"] = self.lockStatus
        return m_dict

    def canMerge(self, withIt, skipItemId=False, skipBindType=False, skipMaxStack=False,
                 skipExpired=False, now=utils.getNow(), **kwargs):
        if not skipItemId and self.itemId != withIt.itemId:
            return False
        if not skipBindType and self.bindType != withIt.bindType:
            return False
        if not skipMaxStack and self.maxStackSize(self.itemId) <= 1:
            return False
        if self.expireTime != withIt.expireTime:
            return False
        if self.enableTime != withIt.enableTime:
            return False
        if self.lockStatus != withIt.lockStatus:
            return False
        return True

    def getItemName(self):
        m_data = dataUtils.getCommItemData(self.itemId)
        if m_data is None:
            return ''
        return m_data['name']


class ReUseItem(Item):
    # 可以重复使用的物品
    def __init__(self, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        super(ReUseItem, self).__init__(itemId, itemNum, bindType, **kwargs)
        self.useTimes = 0

    def initNewItemAttr(self, **kwargs):
        # 创建一个新物品时候的初始化
        super(ReUseItem, self).initNewItemAttr(**kwargs)
        itemData = dataUtils.getCommItemData(self.itemId)
        self.useTimes = itemData['useNum']
        return True

    def attr2Dict(self):
        dic = super(ReUseItem, self).attr2Dict()
        dic['useTimes'] = self.useTimes
        return dic

    def canMerge(self, withIt, **kwargs):
        return False

    def isReUseItem(self):
        return True

