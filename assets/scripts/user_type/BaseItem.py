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
import time
import sys


class PureItem(userType.UserSoleType):
    def __init__(self, dataDic):
        self.__dict__['itemId'] = dataDic['itemId']
        self.__dict__['itemNum'] = dataDic['itemNum']
        self.__dict__['uniqueId'] = dataDic['uniqueId']
        self.__dict__['bindType'] = dataDic['bindType']

        itemType, itemSubType = itemFactory.ItemFactory.getItemTypes(dataDic['itemId'])
        self.__dict__['itemType'] = itemType
        self.__dict__['itemSubType'] = itemSubType

        self.__dict__['createTime'] = dataDic['createTime']

        itemData = dataUtils.getCommItemData(dataDic['itemId'])
        enableTime = utils.parseTimeStr(itemData['usableTime']) if itemData.get('usableTime') else 0

        expirationDate = itemData.get('expirationDate')
        expireTimeStr = itemData.get('itemTimeOut')
        expireTime = 0
        if expirationDate:
            expireTime = dataDic.get('expireTime', 0)
        elif expireTimeStr:
            if expireTimeStr.startswith('cityBattle'):
                expireTime = utils.getSiegeWarItemExpireTime()
            else:
                expireTime = int(utils.parseTimeStr(expireTimeStr))

        self.__dict__['enableTime'] = dataDic.get('enableTime', enableTime)
        self.__dict__['expireTime'] = expireTime
        self.__dict__['attrJson'] = dataDic['attrJson']
        self.__dict__['lockStatus'] = dataDic.get('lockStatus', gameconst.ItemLockStatus.UNLOCKED)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__init__(state)
        return self

    def __getattr__(self, name):
        self.changeToSpecificItem()
        return getattr(self, name)

    def __setattr__(self, name, value):
        if name == '__class__':
            # 热更时候 resetCls会obj.__class__ = cls，这会触发 PureItem.__setattr__，
            # 如果不做这个特殊判断，会执行changeToSpecificItem转化为具体的item，最后
            # 又会执行 return setattr(self, name, value)，将 item的 __class__ 又重新设置为 PureItem
            return object.__setattr__(self, name, value)
        self.changeToSpecificItem()
        return setattr(self, name, value)

    def changeToSpecificItem(self):
        itemClass = itemFactory.ItemFactory.getItemClass(self.__dict__['itemId'])
        try:
            object.__setattr__(self, '__class__', itemClass)
            if hasattr(self, 'attrJson'):
                self.onSpecificItemChanged(self.attrJson)
                # 转换为item后，attrJson 是多余的属性，可以删除，否则checkUserType报错
                delattr(self, 'attrJson')
        except Exception as e:
            object.__setattr__(self, '__class__', PureItem)
            raise e

    def toBagItemDict(self, gridId):
        bagItemSavedDic = self.toItemSavedDict()
        bagItemSavedDic['gridId'] = gridId
        return bagItemSavedDic

    def toItemSavedDict(self, itemNum=None):
        return {
            'itemId': self.itemId,
            'itemNum': itemNum if itemNum else self.itemNum,
            'createTime': self.createTime,
            'expireTime': self.expireTime,
            'enableTime': self.enableTime,
            'uniqueId': self.uniqueId,
            'bindType': self.bindType,
            'attrJson': self.attrJson,
            'lockStatus': self.lockStatus,
        }

    def setItemBind(self, bindType=dataUtils.getItemDefaultBindType()):
        self.bindType = bindType

    def isEquipmentItem(self):
        return dataUtils.isEquipItemByItemId(self.itemId)

    def isReUseItem(self):
        return dataUtils.isReUseItem(self.itemId)
    
    def isLocked(self):
        return self.lockStatus == gameconst.ItemLockStatus.LOCKED


class BaseItem(userType.UserSoleType, metaclass=abc.ABCMeta):

    @staticmethod
    def maxStackSize(itemId):
        if dataUtils.isEquipItemByItemId(itemId):
            return 1
        itemData = dataUtils.getCommItemData(itemId)
        return itemData.get('maxStackSize')

    def __init__(self, itemId, itemNum, bindType=dataUtils.getItemDefaultBindType(), **kwargs):
        self.itemId = itemId
        self.setItemNum(itemNum)
        self.createTime = utils.getNow()
        self.expireTime = 0
        self.itemType = 0
        self.itemSubType = 0
        self.quality = 0
        self.uniqueId = 0
        self.enableTime = 0
        if bindType != gameconst.ItemBindType.BIND and bindType != gameconst.ItemBindType.NORMAL:
            bindType = dataUtils.getItemDefaultBindType()
        self.bindType = bindType
        self.lockStatus = gameconst.ItemLockStatus.UNLOCKED

    def __setstate__(self, state):
        self.__init__(state['itemId'], state['itemNum'], bindType=state['bindType'])
        self.__dict__.update(state)
    
    def setLockStatus(self, status):
        self.lockStatus = status
    
    def __setattr__(self, key, value):
        if key == "itemNum":
            raise AttributeError('itemNum can not be assigned, please use ItemAPI.setItemNum')
        object.__setattr__(self, key, value)
        return

    def setItemNum(self, itemNum):
        if itemNum > self.maxStackSize(self.itemId) or itemNum < 0:
            gameengine.reportCritical('itemNum error', self.itemId, itemNum, self.maxStackSize(self.itemId))
            return
        object.__setattr__(self, 'itemNum', itemNum)

    def isEquipmentItem(self):
        return False

    def isReUseItem(self):
        return False

    def getEnhanceLevel(self):
        return 0

    @abc.abstractmethod
    def canMerge(self, withIt, **kwargs):
        """判断物品是否可以被merge都一起"""
        raise NotImplementedError

    @abc.abstractmethod
    def getItemName(self):
        """获取该ItemObj物品名称"""
        raise NotImplementedError

    def setItemBind(self, bindType=dataUtils.getItemDefaultBindType()):
        self.bindType = bindType

    def setItemExpireTime(self, expireTime):
        self.expireTime = expireTime

    def isExpired(self):
        if self.expireTime and self.expireTime < utils.getNow():
            return True

        return False

    def isEnabled(self):
        if not self.enableTime or utils.getNow() > self.enableTime:
            return True
        return False

    def clearRoleBindData(self, **kwargs):
        # 清除和角色绑定的数据, 物品交易给新玩家时候调用
        return

    def onItemDailyUpdate(self):
        return

    @abc.abstractmethod
    def initNewItemAttr(self, **kwargs):
        """创建物品后初始化物品数据"""
        raise NotImplementedError

    @abc.abstractmethod
    def onSpecificItemChanged(self, attrJson):
        """从json结构初始化物品数据, 该方法需要和`BaseItem.attr2Json`一起初始化"""
        raise NotImplementedError

    @abc.abstractmethod
    def attr2Json(self):
        """將其他属性转化为json.dumps str, 该方法需要和`BaseItem.onSpecificItemChanged`一起初始化"""
        raise NotImplementedError

    @abc.abstractmethod
    def attr2Dict(self):
        """將其他属性转化为Dict"""
        raise NotImplementedError

    def getReplaceItemWhenExpire(self, owner):
        itemData = dataUtils.getCommItemData(self.itemId)
        replaceItemId, bind = itemData.get("recycleReplaceItem", (0, 0))
        return itemFactory.ItemFactory.createItem(replaceItemId, self.itemNum, bind)

    def toBagItemDict(self, gridId):
        bagItemSavedDic = self.toItemSavedDict()
        bagItemSavedDic['gridId'] = gridId
        return bagItemSavedDic

    def toItemSavedDict(self, itemNum=None):
        return {
            'itemId': self.itemId,
            'itemNum': itemNum if itemNum else self.itemNum,
            'createTime': self.createTime,
            'expireTime': self.expireTime,
            'enableTime': self.enableTime,
            'uniqueId': self.uniqueId,
            'bindType': self.bindType,
            'attrJson': self.attr2Json(),
            'lockStatus': self.lockStatus,
        }

    def getItemLevel(self):
        return 1

    def isExpiredReplaceItem(self):
        itemData = dataUtils.getCommItemData(self.itemId)
        return itemData.get("recycleForm", 0)
    
    def isLocked(self):
        return self.lockStatus == gameconst.ItemLockStatus.LOCKED