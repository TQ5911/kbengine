# -*- coding: utf-8 -*-

import KBEngine

from KBEDebug import *
import json
import gameconst
import dataUtils
import Item
import gearEnhance_gearconst as GEGCD

class SpiritBoardItem(Item.Item):
    def __init__(self, itemId, itemNum=1, bindType=dataUtils.getItemDefaultBindType(),  **kwargs):
        super(SpiritBoardItem, self).__init__(itemId, itemNum, bindType, **kwargs)
        self.anima = 0
        self.freeAnima = GEGCD.datas['gearFuLing_ExtraGain']['value']
        DEBUG_MSG("SpiritBoardItem: __init__ ", self)
        return

    def isSpiritBoardItem(self):
        return True

    def canMerge(self, withIt, **kwargs):
        return False

    def onSpecificItemChanged(self, savedJson):
        itemData = dataUtils.getCommItemData(self.itemId)
        self.quality = itemData['quality']
        savedDict = json.loads(savedJson)
        if savedDict:
            DEBUG_MSG("SpiritBoardItem: onSpecificItemChanged ", savedDict)
            self.anima = savedDict.get("anima", 0)
            self.freeAnima = savedDict.get("freeAnima", 0)
        return
    
    def addAnima(self, owner, gridID, addNum):
        if addNum <= 0:
            ERROR_MSG("SpiritBoardItem: addAnima, wrong args ", gridID, addNum)
            return False
        affixWashNumLimit = GEGCD.datas['affixWashNumLimit']['value']
        if self.anima + addNum > affixWashNumLimit:
            # 达到上限就给最大值
            self.anima = affixWashNumLimit
            owner.onMessagePre(GEGCD.datas['msgId_affixWashNumLimit']['value'], [])
        else:
            self.anima += addNum
            owner.onMessagePre(GEGCD.datas['msgId_addAffixWashNum']['value'], [str(addNum)])
        DEBUG_MSG("SpiritBoardItem: addAnima ", self)
        owner.client.onUpdateGridItemsJson(gameconst.BagType.BAG_TYPE_NORMAL, gridID, self.uniqueId, self.attr2Json())
        return True
    
    def deductAnima(self, owner, gridID, subNum):
        if subNum <= 0:
            ERROR_MSG("SpiritBoardItem: deductAnima, wrong args ", gridID, subNum)
            return False
        # 判断每日免费灵气和阴灵盘里的总灵气
        if subNum > (self.anima + self.freeAnima):
            ERROR_MSG("SpiritBoardItem: deductAnima, anima is not enough ", self)
            return False
        # 免费灵气足够，先使用免费的灵气
        if self.freeAnima >= subNum:
            self.freeAnima -= subNum
        else:
            # 免费灵气不足，一次性用完，再用阴灵盘灵气
            if self.freeAnima > 0:
                subNum -= self.freeAnima
                self.freeAnima = 0
            self.anima -= subNum
        DEBUG_MSG("SpiritBoardItem: deductAnima ", self)
        owner.client.onUpdateGridItemsJson(gameconst.BagType.BAG_TYPE_NORMAL, gridID, self.uniqueId, self.attr2Json())
        return True
    
    def getAnima(self):
        DEBUG_MSG("SpiritBoardItem: getAnima ", self)
        return self.anima + self.freeAnima

    def setAuctionTime(self, t, now=None):
        super().setAuctionTime(t, now=now)

    def attr2Json(self):
        _dict = super().attr2Dict()
        _dict["anima"] = self.anima
        _dict["freeAnima"] = self.freeAnima
        return json.dumps(_dict)

    def attr2Dict(self):
        _dict = super().attr2Dict()
        _dict["anima"] = self.anima
        _dict["freeAnima"] = self.freeAnima
        return _dict
    
    def onItemDailyUpdate(self):
        DEBUG_MSG('onItemDailyUpdate~spiritBoardItem')
        freeAnima = GEGCD.datas['gearFuLing_ExtraGain']['value']
        ret = freeAnima != self.freeAnima
        # 需要重置才需要下客户端
        if ret:
            self.freeAnima = freeAnima
            DEBUG_MSG('onItemDailyUpdate~spiritBoardItem update done~ ', self)
        return ret 