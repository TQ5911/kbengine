# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import functools
import json

import utils
import gameengine
import gameconst
import gameglobal
import gameconfig
import redisUtils
import gamedecorator
import itemFactory
import dataUtils
import mailAssistor
import LogTrackingMgr
import dropAward
import gameclass

import message_Message_def as MMD
import auction_auctionConst as AUC_CONST
import gearBase_gearBase as GBGBD


RETURN_SERVER_TAG = 'returnServer'
RETURN_OWNER_TAG = 'returnOwner'
RETURN_TIME_TAG = 'returnTime'
RETURN_REASON_TAG = 'returnReason'
RETURN_DAY_TAG = 'leaseTime'

class ILease(object):
    """Avatar 租赁系统 Mixin"""

    def __init__(self):
        if not hasattr(self, 'leaseIncomeBindGold'):
            self.leaseIncomeBindGold = 0
        if not hasattr(self, 'leaseIncomeGold'):
            self.leaseIncomeGold = 0
        if not hasattr(self, 'leaseCoolDownList'):
            self.leaseCoolDownList = {}
        if not hasattr(self, '_leasePending'):
            self._leasePending = {}

    @property
    def leaseStub(self):
        return gameglobal.localLeaseStub

    # -------------------------------------------------------------
    # 通用工具
    # -------------------------------------------------------------

    def _getLeaseConst(self, key):
        data = AUC_CONST.datas.get(key)
        if data:
            return data.get('value', 0)
        return 0

    def _getLeasePriceLimit(self, itemId):
        gearData = GBGBD.datas.get(itemId)
        if gearData:
            return gearData.get('maxLeasePrice', 0)
        return 0

    def _isLeaseCoolDown(self, uniqueId):
        now = utils.curTS()
        endTime = self.leaseCoolDownList.get(uniqueId)
        if endTime and endTime > now:
            return True
        return False

    def _addLeaseCoolDown(self, uniqueId, endTime):
        self.leaseCoolDownList[uniqueId] = endTime

    def _removeLeaseCoolDown(self, uniqueId):
        self.leaseCoolDownList.pop(uniqueId, None)

    def _cleanExpiredLeaseCoolDown(self):
        now = utils.curTS()
        expiredIds = [uid for uid, endTime in self.leaseCoolDownList.items() if endTime <= now]
        for uid in expiredIds:
            self.leaseCoolDownList.pop(uid, None)

    def _findEquipInBag(self, uniqueId):
        bag = self.bagData
        if bag:
            grid, item = bag.getItemByUniqueId(uniqueId)
            if item and item.isEquipmentItem():
                return grid, item
        return None, None

    def _getEquipItemDataStr(self, item):
        return json.dumps(item.toItemSavedDict())

    def _canEquipItemLease(self, item):
        # 爆装
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NOT_RETURN:
            return True
        # 非绑
        if item.bindType == gameconst.ItemBindType.NORMAL:
            return True
        return False

    # -------------------------------------------------------------
    # 添加 / 取消租赁凭证（本服执行）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqAddLeaseTag(self, exposed, uniqueId):
        LOG_DBG("reqAddLeaseTag", self.gbID, uniqueId)

        _, item = self._findEquipInBag(uniqueId)
        if not item:
            LOG_INFO("reqAddLeaseTag item not found", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return
        
        if not self._canEquipItemLease(item):
            LOG_INFO("reqAddLeaseTag item cannot be leased", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('54481019', 0), [])
            return

        item.equipAttr.leaseTag = 1
        self.client.onAddLeaseTagSucc(uniqueId)

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqCancelLeaseTag(self, exposed, uniqueId):
        LOG_DBG("reqCancelLeaseTag", self.gbID, uniqueId)

        if uniqueId in self._leasePending:
            LOG_INFO("reqCancelLeaseTag pending", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return

        _, item = self._findEquipInBag(uniqueId)
        if not item:
            LOG_INFO("reqCancelLeaseTag item not found", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return

        if item.equipAttr.leaseTag != 1:
            LOG_INFO("reqCancelLeaseTag item leaseTag invalid", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return

        item.equipAttr.leaseTag = 0
        self.client.onCancelLeaseTagSucc(uniqueId)

    # -------------------------------------------------------------
    # 上架流程（跨服，二阶段提交）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqSaleItemInLease(self, exposed, uniqueId, pricePerDay, days):
        LOG_INFO("reqSaleItemInLease", self.gbID, uniqueId, pricePerDay, days)

        if not self.leaseStub:
            LOG_INFO("reqSaleItemInLease leaseStub not found", self.gbID)
            self.onMessagePre(MMD.datas.get('leaseServerUnavailable', 0), [])
            return

        # 并发校验
        if uniqueId in self._leasePending:
            LOG_INFO("reqSaleItemInLease pending", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return

        # 冷却校验
        if self._isLeaseCoolDown(uniqueId):
            LOG_INFO("reqSaleItemInLease cooldown", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('54481016', 0), [])
            return

        grid, item = self._findEquipInBag(uniqueId)
        if not item:
            LOG_INFO("reqSaleItemInLease item not found", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('itemNotFound', 0), [])
            return

        # 租赁标记
        if not item.equipAttr.leaseTag:
            LOG_INFO("reqSaleItemInLease item no tag", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('54481019', 0), [])
            return

        # 价格校验
        minPrice, maxPrice = self._getLeasePriceLimit(item.itemId)
        if pricePerDay < minPrice or pricePerDay > maxPrice:
            LOG_INFO("reqSaleItemInLease price invalid", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('leasePriceInvalid', 0), [])
            return

        # 时间校验
        minDays = self._getLeaseConst('leaseTimeMin')
        maxDays = self._getLeaseConst('leaseTimeMax')
        if days < minDays or days > maxDays:
            LOG_INFO("reqSaleItemInLease days invalid", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('leaseDaysInvalid', 0), [])
            return
        
        self._leasePending[uniqueId] = {
            'grid': grid,
            'item': item,
            'ts': utils.curTS(),
        }

        leaseInfo = {}
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NOT_RETURN:
            leaseInfo[RETURN_SERVER_TAG] = item.equipAttr.ownerServerId
            leaseInfo[RETURN_OWNER_TAG] = item.equipAttr.ownerGbId
            leaseInfo[RETURN_TIME_TAG] = item.equipAttr.returnTime
            leaseInfo[RETURN_REASON_TAG] = item.equipAttr.returnReason
        else:
            leaseInfo[RETURN_DAY_TAG] = days

        opUUID = KBEngine.genUUID64()
        self.leaseStub.addItemPrepare(
            self.gbID,
            item.uniqueId,
            item.itemId,
            json.dumps(item.toItemSavedDict()),
            pricePerDay,
            leaseInfo.get(RETURN_DAY_TAG, 0),
            leaseInfo.get(RETURN_SERVER_TAG, 0),
            leaseInfo.get(RETURN_OWNER_TAG, 0),
            leaseInfo.get(RETURN_TIME_TAG, 0),
            leaseInfo.get(RETURN_REASON_TAG, 0),
            opUUID,
        )

    def onReplyAddItemPrepare(self, uniqueId, result, opUUID):
        LOG_INFO("onReplyAddItemPrepare", self.gbID, uniqueId, result, opUUID)

        if result != 0:
            LOG_INFO("onReplyAddItemPrepare failed", self.gbID, uniqueId, result)
            self._leasePending.pop(uniqueId, None)
            self.onMessagePre(MMD.datas.get('leasePrepareFail', 0), [])
            return

        extra = self._leasePending.pop(uniqueId, None)
        if not extra:
            LOG_ERR("onReplyAddItemPrepare no pending data", self.gbID, uniqueId, result)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.get('leasePrepareFail', 0), [])
            return

        # 再检查一下 Tag
        grid, item = extra['grid'], extra['item']
        if item.equipAttr.leaseTag != 1:
            LOG_ERR("onReplyAddItemPrepare item no tag", self.gbID, uniqueId)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.get('54481019', 0), [])
            return

        # 扣除手续费
        feeType, feeAmount = self._getLeaseConst('leaseServiceFee')
        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(feeType, feeAmount)
        if not self.canDeductWealth(deductVal):
            LOG_INFO("onReplyAddItemPrepare not enough wealth", self.gbID, uniqueId)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.get('notEnoughMoney', 0), [])
            return

        srcType = 4
        detail = gameclass.AwardDetail(costId=feeType, costNum=feeAmount)
        self.deductWealth(srcType, deductVal, opUUID, detail)

        # 从背包扣除物品（与 prepare 使用同一个 opUUID）
        bagType = gameconst.BagType.BAG_TYPE_NORMAL
        srcType = 0
        detail = gameclass.AwardDetail(bagType=bagType, gridId=grid, itemId=item.itemId, uniqueId=uniqueId)
        self.getBagByType(bagType).cleanGridByGridId(self, grid, item.itemId, opUUID, srcType, detail)

        self.leaseStub.addItemCommit(uniqueId, self.gbID, opUUID)


    def onReplyAddItemCommit(self, uniqueId, result, opUUID):
        LOG_INFO("onReplyAddItemCommit result: ", opUUID, self.gbID, uniqueId, result)
        if result == 0:
            self.client.onSaleItemInLeaseSucc(uniqueId)
        else:
            self.onMessagePre(MMD.datas.get('leaseCommitFail', 0), [])

    # -------------------------------------------------------------
    # 租借流程（跨服，二阶段提交）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseItem(self, exposed, uniqueId):
        LOG_INFO("reqLeaseItem", self.gbID, uniqueId)

        if not self.leaseStub:
            LOG_ERR("reqLeaseItem leaseStub not found", self.gbID)
            self.onMessagePre(MMD.datas.get('leaseServerUnavailable', 0), [])
            return

        opUUID = KBEngine.genUUID64()
        self.leaseStub.leaseItemPrepare(uniqueId, gameconfig.serverId(), self.gbID, opUUID)

    def onReplyLeaseItemPrepare(self, uniqueId, totalPrice, result, opUUID):
        LOG_INFO("onReplyLeaseItemPrepare", self.gbID, uniqueId, totalPrice, result, opUUID)

        # 二次校验：背包空间、货币
        if self.getBagLeftGridCount(gameconst.BagType.BAG_TYPE_NORMAL) <= 0:
            LOG_INFO("onReplyLeaseItemPrepare bag full", self.gbID, uniqueId)
            self.leaseStub.leaseItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.get('bagFull', 0), [])
            return

        feeType, feeAmount = (1,2)
        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(feeType, feeAmount)
        if not self.canDeductWealth(deductVal):
            LOG_INFO("onReplyLeaseItemPrepare not enough gold", self.gbID, uniqueId)
            self.leaseStub.leaseItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.get('notEnoughGold', 0), [])
            return
        
        srcType = 4
        detail = gameclass.AwardDetail(costId=feeType, costNum=feeAmount)
        self.deductWealth(srcType, deductVal, opUUID, detail)

        self._leaseBuyCache[opUUID] = totalPrice
        self.leaseStub.leaseItemCommit(uniqueId, opUUID)

    def onReplyLeaseItemCommit(self, opUUID, uniqueId, result, startLeaseTime, ownerGBID, gold, bindGold, cost, itemId):
        LOG_INFO("onReplyLeaseItemCommit", self.gbID, uniqueId, result, opUUID)
        if result != 0:
            self._leaseBuyCache.pop(opUUID, None)
            self.onMessagePre(MMD.datas.get('leaseCommitFail', 0), [])
            return

        # 添加交易记录
        redisUtils.PlayerLeaseRecord.recordMessage(
            timestamp=startLeaseTime,
            leeorGBID=ownerGBID,
            leessGBID=self.gbID,
            itemId=itemId,
            uniqueId=uniqueId,
            bindGold=bindGold,
            gold=gold,
            cost=cost,
        )

    def onGiveLeaseItem(self, opUUID, uniqueId, itemData, returnOwnerServerId, returnOwnerGbId, returnEndTime):
        LOG_INFO("onGiveLeaseItem", self.gbID, opUUID, uniqueId, returnOwnerServerId, returnOwnerGbId, returnEndTime)

        itemDict = json.loads(itemData)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onGiveLeaseItem createItem failed", self.gbID, uniqueId)
            return
        attr = item.equipAttr
        if not attr:
            LOG_ERR("onGiveLeaseItem no equipAttr", self.gbID, uniqueId)
            return
        # 设置相关属性
        # 爆装已有归还属性，无需再设置；只需要处理首次需要归还的物品
        if attr.returnReason == gameconst.ItemReturnReason.NOT_RETURN:
            attr.ownerServerId = returnOwnerServerId
            attr.ownerGbId = returnOwnerGbId
            attr.returnTime = returnEndTime
            attr.returnReason = gameconst.ItemReturnReason.LEASE_RETURN

        bag = self.bagData
        srcType = 4
        detail = gameclass.AwardDetail(bagType=gameconst.BagType.BAG_TYPE_NORMAL, itemId=item.itemId, uniqueId=uniqueId)
        opStat, _ = bag.addItemsToNewGrid(self, item, opUUID, srcType, detail)
        if opStat != gameconst.BagOPStat.OPERATE_BAG_STAT_OK:
            # 背包满时发邮件
            # 这里一般是不会触发的
            LOG_ERR("onGiveLeaseItem add bag failed", self.gbID, uniqueId, opStat)
        else:
            self.client.onLeaseItemSucc(uniqueId, item.equipAttr.leasePricePerDay)

        # 写入承租方冷却列表
        self._addLeaseCoolDown(uniqueId, returnEndTime)

    def onAddLeaseIncome(self, uniqueId, itemId, bindGold, gold, opUUID, returnEndTime):
        LOG_INFO("onAddLeaseIncome", self.gbID, bindGold, gold, itemId, opUUID, returnEndTime, uniqueId)
        self.leaseIncomeBindGold += bindGold
        self.leaseIncomeGold += gold
        self.client.onUpdateLeaseIncome(self.leaseIncomeBindGold, self.leaseIncomeGold)

        # 写入承租方冷却列表
        self._addLeaseCoolDown(uniqueId, returnEndTime)


    # -------------------------------------------------------------
    # 下架流程（跨服）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqCancelSaleItemInLease(self, exposed, uniqueId):
        LOG_INFO("reqCancelSaleItemInLease", self.gbID, uniqueId)

        # 先检查下背包格子
        if self.getBagLeftGridCount(gameconst.BagType.BAG_TYPE_NORMAL) <= 0:
            LOG_INFO("reqCancelSaleItemInLease bag full", self.gbID, uniqueId)
            self.onMessagePre(MMD.datas.get('bagFull', 0), [])
            return

        if not self.leaseStub:
            LOG_INFO("reqCancelSaleItemInLease leaseStub not found", self.gbID)
            self.onMessagePre(MMD.datas.get('leaseServerUnavailable', 0), [])
            return

        self.leaseStub.cancelItem(self.gbID, uniqueId)

    def onReplyCancelItemInLease(self, uniqueId, result, itemDataStr):
        LOG_INFO("onReplyCancelItemInLease", self.gbID, uniqueId, result)
        if result != 0:
            self.onMessagePre(MMD.datas.get('leaseCancelFail', 0), [])
            return

        if self.getBagLeftGridCount(gameconst.BagType.BAG_TYPE_NORMAL) <= 0:
            LOG_ERR("onReplyCancelItemInLease bag full", self.gbID, uniqueId)
            # 这里并发格子满了，需要兜底
            self.onMessagePre(MMD.datas.get('54481015', 0), [])
            return

        itemDict = json.loads(itemDataStr)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onReplyCancelItemInLease createItem failed", self.gbID, uniqueId)
            return

        srcType = 4
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetail(bagType=gameconst.BagType.BAG_TYPE_NORMAL, itemId=item.itemId)
        self.bagData.addItemsToNewGrid(self, item, opUUID, srcType, detail)
        self.client.onCancelSaleItemInLeaseSucc(uniqueId)

    # -------------------------------------------------------------
    # 到期移除 / 归还
    # -------------------------------------------------------------

    def doRemoveLeasedItem(self, uniqueId):
        LOG_INFO("doRemoveLeasedItem", self.gbID, uniqueId)
        _, item = self._findEquipInBag(uniqueId)
        if not item:
            LOG_WARN("doRemoveLeasedItem item not found", self.gbID, uniqueId)
            return

        if hasattr(self, 'bodyEquipData') and self.bodyEquipData:
            slotId, bodyItem = self.bodyEquipData.getBodyEquipByUniqueId(uniqueId)
            if bodyItem:
                self.bodyEquipData.doBodyUndressEquip(self, bodyItem.equipAttr.equipType)

        bag = self.bagData
        if not bag:
            LOG_ERR("doRemoveLeasedItem bag not found", self.gbID, uniqueId)
            return

        gridId, _ = bag.getItemByUniqueId(uniqueId)
        if gridId < 0:
            LOG_ERR("doRemoveLeasedItem item grid not found", self.gbID, uniqueId)
            return

        srcType = 4
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetail(bagType=gameconst.BagType.BAG_TYPE_NORMAL, gridId=gridId, itemId=item.itemId, uniqueId=uniqueId)
        bag.cleanGridByGridId(self, gridId, item.itemId, opUUID, srcType, detail)

        self.client.onRemoveLeasedItem(uniqueId)

    def onReturnLeaseItemToOwner(self, uniqueId, itemData):
        LOG_INFO("onReturnLeaseItemToOwner", self.gbID, uniqueId)
        itemDict = json.loads(itemData)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onReturnLeaseItemToOwner createItem failed", self.gbID, uniqueId)
            return
        
        _, myItem = self._findEquipInBag(uniqueId)
        if myItem:
            LOG_ERR("onReturnLeaseItemToOwner item still in bag", self.gbID, uniqueId)
            return

        if hasattr(self, 'bodyEquipData') and self.bodyEquipData:
            slotId, bodyItem = self.bodyEquipData.getBodyEquipByUniqueId(uniqueId)
            if bodyItem:
                LOG_ERR("onReturnLeaseItemToOwner item still equipped", self.gbID, uniqueId)
                return

        # 重置归还状态
        item.equipAttr.returnReason = gameconst.ItemReturnReason.NOT_RETURN
        item.equipAttr.ownerServerId = 0
        item.equipAttr.ownerGbId = 0
        item.equipAttr.returnTime = 0

        # TODO: 配置邮件模板 ID（策划在 mail_mail 表中配置「租赁到期归还」）
        leaseReturnMailId = AUC_CONST.datas.get('leaseReturnMailId', {}).get('value', 0)
        mailVal = dropAward.MailWealthVal(itemObjs=[item])
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            leaseReturnMailId,
            extraAttach=mailVal,
            opUUID=KBEngine.genUUID64(),
            srcType=4,
        )

    # -------------------------------------------------------------
    # 提取收入（本服执行）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqTakeLeaseIncome(self, exposed):
        LOG_INFO("reqTakeLeaseIncome", self.gbID)

        bindGold = self.leaseIncomeBindGold
        gold = self.leaseIncomeGold
        if bindGold <= 0 and gold <= 0:
            LOG_INFO("reqTakeLeaseIncome no income", self.gbID)
            return

        addWealthVal = dropAward.AwardVal()
        if bindGold > 0:
            addWealthVal.addWealthByItemId(gameconst.ItemId.BIND_MONEY, bindGold)
        if gold > 0:
            addWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, gold)

        srcType = 4
        opUUID = KBEngine.genUUID64()

        if not self.canAddWealthVal(srcType, addWealthVal):
            LOG_ERR("reqTakeLeaseIncome cannot add wealth", self.gbID, bindGold, gold)
            return

        self.leaseIncomeBindGold = 0
        self.leaseIncomeGold = 0

        detail = gameclass.AwardDetail(moneyAmount=gold, bindMoneyAmount=bindGold)
        self.addWealth(srcType, addWealthVal, opUUID, detail)

        self.client.onTakeLeaseIncomeSucc(bindGold, gold)

    # -------------------------------------------------------------
    # 交易记录（本服 Redis）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseRecords(self, exposed, recordType, number):
        LOG_INFO("reqLeaseRecords", self.gbID, recordType, number)

        redisUtils.PlayerLeaseRecord.getMessageRecord(self, self.gbID, number)

    # -------------------------------------------------------------
    # 商店查询
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseShopSummary(self, exposed, equipType, equipSubType):
        LOG_INFO("reqLeaseShopSummary", self.gbID, equipType, equipSubType)

        if not self.leaseStub:
            LOG_ERR("reqLeaseShopSummary leaseStub not found", self.gbID)
            return

        self.leaseStub.getShopSummary(gameconfig.serverId(), equipType, equipSubType, self.gbID)

    def onLeaseShopSummaryResp(self, items):
        LOG_INFO("onLeaseShopSummaryResp", self.gbID, len(items))
        self.client.onLeaseShopSummary(items)

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseShopItems(self, exposed, itemId, page, pageSize):
        LOG_INFO("reqLeaseShopItems", self.gbID, itemId)

        if not self.leaseStub:
            LOG_ERR("reqLeaseShopSummary leaseStub not found", self.gbID)
            return

        self.leaseStub.getShopItems(gameconfig.serverId(), itemId, page, pageSize, self.gbID)

    def onLeaseShopItemsResp(self, itemId, items):
        LOG_INFO("onLeaseShopItemsResp", self.gbID, itemId, len(items))
        self.client.onLeaseShopItems(items)

    # -------------------------------------------------------------
    # 我的出租列表
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqMyLeaseSaleInfo(self, exposed):
        LOG_INFO("reqMyLeaseSaleInfo", self.gbID)

        if not self.leaseStub or not self.leaseStub.isLeaseCenterActive():
            return

        self.leaseStub.getMySaleList(gameconfig.serverId(), self.gbID)

    def onMyLeaseSaleInfo(self, items):
        LOG_INFO("onMyLeaseSaleInfo", self.gbID, len(items))
        self.client.onMyLeaseSaleInfo(items)

    # -------------------------------------------------------------
    # 状态与清理
    # -------------------------------------------------------------

    def onLeaseLoginInit(self):
        self._cleanExpiredLeaseCoolDown()

    def onLeaseDailyRefresh(self):
        self._cleanExpiredLeaseCoolDown()
