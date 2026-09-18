# -*- coding: utf-8 -*-

from KBEDebug import *
import KBEngine

import functools
import gzip
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
import gametimer

import message_Message_def as MMD
import auction_auctionConst as AUC_CONST
import gearBase_gearBase as GBGBD
import antiAddictCategory_antiAddictCategory_def as ACACD
import agent_agentFunction as A_AFD
import agent_agentConfig as A_ACD
import itemData_itemType as IDITD
import itemData_itemData_set as IDID_SET
import gearBase_typeExplanation as GBTED
import gearBase_typeTab as GBTTD
import gearBase_gearConst as GBGC


RETURN_SERVER_TAG = 'returnServer'
RETURN_OWNER_TAG = 'returnOwner'
RETURN_TIME_TAG = 'returnTime'
RETURN_REASON_TAG = 'returnReason'
RETURN_DAY_TAG = 'leaseTime'

LEASE_RETURN_KEY_ITEM = 'itemData'
LEASE_RETURN_KEY_END_TIME = 'returnEndTime'
LEASE_RETURN_KEY_UUID = 'opUUID'

LEASE_INCOME_KEY_GOLD = 'gold'
LEASE_INCOME_KEY_BIND_GOLD = 'bindGold'
LEASE_INCOME_KEY_TIMETS = 'timets'

# 查询过滤等级位掩码的位数（uint32，bit N 对应等级 N）
LEASE_FILTER_MAX_LEVEL = 32


def _levelListToMask(levelList):
    """等级列表转 uint32 位掩码；存在越界等级时返回 None"""
    if not levelList:
        return 0xFFFFFFFF # 不过滤

    mask = 0
    for lv in levelList:
        if not isinstance(lv, int) or isinstance(lv, bool) or lv < 0 or lv >= LEASE_FILTER_MAX_LEVEL:
            LOG_ERR("_levelListToMask level out of range", lv)
            return None
        mask |= 1 << lv
    return mask

# 租赁服务错误码（与 leaseServer 保持一致）
LEASE_OK = 0
LEASE_NOT_FOUND = 1
LEASE_ITEM_LOCKED = 2
LEASE_PARAM_ERROR = 3
LEASE_STATUS_ERROR = 4
LEASE_ALREADY_EXISTS = 5
LEASE_NOT_OWNER = 6
LEASE_TIMEOUT = 7
LEASE_IN_COOLDOWN = 8
LEASE_DB_ERROR = 9
LEASE_RATE_LIMIT = 10
LEASE_SELF_LEASE = 11
LEASE_SHELF_FULL = 12

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
        if not hasattr(self, 'leasePendingReturnItems'):
            self.leasePendingReturnItems = {}
        if not hasattr(self, 'leasePendingRemoveItems'):
            self.leasePendingRemoveItems = {}
        if not hasattr(self, 'leasePendingIncome'):
            self.leasePendingIncome = {}

    @property
    def leaseStub(self):
        return gameglobal.localLeaseStub

    # -------------------------------------------------------------
    # 通用工具
    # -------------------------------------------------------------
    def _getLeaseCost(self, itemId):
        return gameconst.ItemIdEnum.COIN, AUC_CONST.datas['rentalCost']['value']

    def _getLeaseDayLimit(self, itemId):
        day = AUC_CONST.datas['rentalTime']['value']
        return day[0], day[1]

    def _getLeasePriceLimit(self, itemId):
        gearData = GBGBD.datas.get(itemId)
        if gearData:
            return 1, gearData['rentalPric']
        return 1, 0

    def _isLeaseCoolDown(self, uniqueId):
        now = utils.curTS()
        endTime = self.leaseCoolDownList.get(uniqueId)
        if endTime:
            if endTime > now:
                return True
            self.leaseCoolDownList.pop(uniqueId, None)
        return False

    def _addLeaseCoolDown(self, uniqueId, endTime):
        self.leaseCoolDownList[uniqueId] = endTime

    def _findLeaseEquipInBag(self, uniqueId):
        bag = self.bagData
        if bag:
            grid, item = bag.getItemByUniqueId(uniqueId)
            if item and item.isEquipmentItem():
                return grid, item
        return None, None

    def _canEquipItemLease(self, item):
        # 爆装
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NORMAL:
            return True
        # 非绑
        if item.bindType == gameconst.ItemBindType.NORMAL:
            return True
        return False

    # -------------------------------------------------------------
    # 上架流程（跨服，二阶段提交）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(2)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqSaleItemInLease(self, exposed, uniqueId, pricePerDay, days):
        LOG_INFO("reqSaleItemInLease", uniqueId, pricePerDay, days)
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.Rental, 
                A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        if self.checkPopupSecondaryPassword([(gameconst.SecondaryPasswordCheckType.RENTAL_ITEM,)]):
            LOG_WARN("reqSaleItemInLease failed, need popup sp")
            return
        
        if not self.leaseStub:
            LOG_INFO("reqSaleItemInLease leaseStub not found")
            self.onMessagePre(MMD.datas.rent01, [])
            return

        grid, item = self._findLeaseEquipInBag(uniqueId)
        if not item:
            LOG_INFO("reqSaleItemInLease item not found", uniqueId)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        # 价格校验
        minPrice, maxPrice = self._getLeasePriceLimit(item.itemId)
        if (minPrice > 0 and pricePerDay < minPrice) or (maxPrice > 0 and pricePerDay > maxPrice):
            LOG_INFO("reqSaleItemInLease price invalid", uniqueId, minPrice, maxPrice)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        # 时间校验
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NORMAL:
            # 爆装检查剩余时间
            leftTime = item.equipAttr.returnTime - utils.curTS()
            if leftTime < AUC_CONST.datas['rentalTimelimit']['value'] * gameconst.ONE_DAY_COST_SECONDS:
                LOG_INFO("reqSaleItemInLease return time invalid", uniqueId, leftTime)
                self.onMessagePre(MMD.datas.rent06, [])
                return
        else:
            # 自己装备检查出租天数
            minDays, maxDays = self._getLeaseDayLimit(item.itemId)
            if days < minDays or days > maxDays:
                LOG_INFO("reqSaleItemInLease days invalid", uniqueId)
                self.onMessagePre(MMD.datas.rent01, [])
                return
            
        # 并发校验
        if uniqueId in self._leasePending:
            LOG_INFO("reqSaleItemInLease pending", uniqueId)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        # 冷却校验
        if self._isLeaseCoolDown(uniqueId):
            LOG_INFO("reqSaleItemInLease cooldown", uniqueId)
            self.onMessagePre(MMD.datas.rent09, [])
            return

        if not self._canEquipItemLease(item):
            LOG_INFO("reqSaleItemInLease item cannot be leased", uniqueId)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        self._leasePending[uniqueId] = {
            'grid': grid,
            'item': item,
            'ts': utils.curTS(),
        }

        leaseInfo = {}
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NORMAL:
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
            item.equipAttr.enhanceLv,
            item.equipAttr.grade,
            opUUID,
        )

        LogTrackingMgr.LogTrackingMgr.rent_item_sale(
            self.gbID,
            self.accountEntity.clientDistinctId,
            item.itemId,
            item.uniqueId,
            pricePerDay,
        )

    def onReplyAddItemPrepare(self, uniqueId, result, opUUID):
        LOG_DBG("onReplyAddItemPrepare", uniqueId, result, opUUID)
        if result != 0:
            LOG_INFO("onReplyAddItemPrepare failed", uniqueId, result)
            self._leasePending.pop(uniqueId, None)
            # TODO: 若需要区分提示，可配置 rentalShelfFullMsg
            self.onMessagePre(MMD.datas.rent01, [])
            return

        extra = self._leasePending.pop(uniqueId, None)
        if not extra:
            LOG_ERR("onReplyAddItemPrepare no pending data", uniqueId, result)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        # 再检查一下
        grid, item = extra['grid'], extra['item']
        nowItem = self.bagData.getItemObjByGridId(grid)
        if not nowItem or nowItem.uniqueId != item.uniqueId:
            LOG_WARN('onReplyAddItemPrepare item change:', item.uniqueId, nowItem and nowItem.uniqueId)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent01, [])
            return
        if not self._canEquipItemLease(item):
            LOG_INFO("onReplyAddItemPrepare item cannot be leased", uniqueId)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        if self.bagData.isLocked():
            LOG_WARN("onReplyAddItemPrepare lock bag fail:", uniqueId)
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            return

        # 扣除手续费
        feeType, feeAmount = self._getLeaseCost(item.itemId)
        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(feeType, feeAmount)
        res = self.canDeductWealth(deductVal)
        if not res:
            LOG_INFO("onReplyAddItemPrepare not enough wealth", uniqueId, res())
            self.leaseStub.addItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent01, [])
            return

        srcType = ACACD.datas.BONUS_SRC_LEASE_ADD_ITEM
        detail = gameclass.AwardDetailCls(costId=feeType, costNum=feeAmount)
        self.deductWealth(srcType, deductVal, opUUID, detail)

        # 从背包扣除物品（与 prepare 使用同一个 opUUID）
        bagType = gameconst.BagTypeEnum.BAG_TYPE_NORMAL
        detail = gameclass.AwardDetailCls(bagType=bagType, gridId=grid, itemId=item.itemId, uniqueId=uniqueId)
        self.getBagByType(bagType).cleanGridByGridId(self, grid, item.itemId, opUUID, srcType, detail)

        # 暂存返还信息，commit 失败时通过邮件返还装备与手续费
        self._leasePending[uniqueId] = {
            'item': item,
            'feeType': feeType,
            'feeAmount': feeAmount,
        }

        self.leaseStub.addItemCommit(uniqueId, self.gbID, opUUID)


    def onReplyAddItemCommit(self, uniqueId, result, opUUID):
        LOG_DBG("onReplyAddItemCommit result: ", opUUID, uniqueId, result)
        refund = self._leasePending.pop(uniqueId, None)
        if result:
            LOG_WARN('ILease::onReplyAddItemCommit failed:', uniqueId, result)
            # 装备与手续费已扣除，通过邮件返还
            if refund:
                item = refund['item']
                mailVal = dropAward.MailAttachVal(itemObjs=[item])
                mailVal.addWealthByItemId(refund['feeType'], refund['feeAmount'])
                mailAssistor.sendMailToPlayers(
                    [self.gbID],
                    GBGC.datas['equipReturnItem1']['value'],
                    extraAttach=mailVal,
                    opUUID=opUUID,
                    srcType=ACACD.datas.BONUS_SRC_LEASE_ADD_ITEM,
                )
                self.onMessagePre(MMD.datas.rent01, [])
            else:
                LOG_ERR("_refundLeaseAddItem no refund data", uniqueId, opUUID)
                self.onMessagePre(MMD.datas.rent01, [])
            return

        self.client.onSaleItemInLeaseSucc(uniqueId)

    # -------------------------------------------------------------
    # 租借流程（跨服，二阶段提交）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(2)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseItem(self, exposed, uniqueId):
        LOG_INFO("reqLeaseItem", uniqueId)
        if not self.checkAuthDisassembleAndMsg(
                A_AFD.Rental, 
                A_ACD.datas['restrictedPromptMsg1']['value']):
            return

        if not self.leaseStub:
            LOG_ERR("reqLeaseItem leaseStub not found")
            return

        opUUID = KBEngine.genUUID64()
        # 费率配置在调用时读取并透传给租赁中心服，保证热更后立即生效
        prop01 = AUC_CONST.datas['rentalProp01']['value']
        prop02 = AUC_CONST.datas['rentalProp02']['value']
        self.leaseStub.leaseItemPrepare(uniqueId, gameconfig.serverId(), self.gbID, opUUID, prop01, prop02)

    def onReplyLeaseItemPrepare(self, uniqueId, totalPrice, result, opUUID):
        LOG_DBG("onReplyLeaseItemPrepare", uniqueId, totalPrice, result, opUUID)
        if result:
            LOG_INFO('ILease::onReplyLeaseItemPrepare failed:', opUUID, uniqueId, result)
            if result == LEASE_SELF_LEASE:
                self.onMessagePre(MMD.datas.rent07, [])
                return
            if result == LEASE_TIMEOUT:
                self.onMessagePre(MMD.datas.redeem08, [])
                return
            if result in (LEASE_STATUS_ERROR, LEASE_NOT_FOUND):
                self.onMessagePre(MMD.datas.rent12, [])
                self.client.onLeaseItemSucc(uniqueId)
                return

            self.onMessagePre(MMD.datas.rent02, [])
            return

        # 二次校验：背包空间、货币
        if self.getBagLeftGridCount(gameconst.BagTypeEnum.BAG_TYPE_NORMAL) <= 0:
            LOG_INFO("onReplyLeaseItemPrepare bag full", uniqueId)
            self.leaseStub.leaseItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent02, [])
            return

        feeType, feeAmount = gameconst.ItemIdEnum.MONEY, totalPrice
        deductVal = dropAward.DeductWealthVal()
        deductVal.addWealthByItemId(feeType, feeAmount)
        res = self.canDeductWealth(deductVal)
        if not res:
            LOG_INFO("onReplyLeaseItemPrepare not enough gold", uniqueId, res())
            self.leaseStub.leaseItemRollback(uniqueId, opUUID)
            self.onMessagePre(MMD.datas.rent02, [])
            return
        
        srcType = ACACD.datas.BONUS_SRC_LEASE
        detail = gameclass.AwardDetailCls(costId=feeType, costNum=feeAmount)
        self.deductWealth(srcType, deductVal, opUUID, detail)

        # 暂存费用信息，commit 失败时通过邮件返还
        self._leasePending[uniqueId] = {
            'feeType': feeType,
            'feeAmount': feeAmount,
        }

        self.leaseStub.leaseItemCommit(uniqueId, self.gbID, opUUID)

    def onReplyLeaseItemCommit(self, opUUID, uniqueId, result, startLeaseTime, endLeaseTime, lessorGBID, ownerGBID, gold, bindGold, cost, itemData):
        LOG_DBG("onReplyLeaseItemCommit", uniqueId, result, opUUID)
        refund = self._leasePending.pop(uniqueId, None)
        if result != 0:
            LOG_WARN("onReplyLeaseItemCommit failed", uniqueId, result)
            # 租金已扣除，通过邮件返还
            if refund:
                mailVal = dropAward.MailAttachVal()
                mailVal.addWealthByItemId(refund['feeType'], refund['feeAmount'])
                mailAssistor.sendMailToPlayers(
                    [self.gbID],
                    GBGC.datas['equipReturnItem2']['value'],
                    extraAttach=mailVal,
                    opUUID=opUUID,
                    srcType=ACACD.datas.BONUS_SRC_LEASE,
                )
                self.onMessagePre(MMD.datas.rent02, [])
            else:
                LOG_ERR("onReplyLeaseItemCommit no refund data", uniqueId, opUUID)
                self.onMessagePre(MMD.datas.rent02, [])
            return

        self.client.onLeaseItemSucc(uniqueId)

        # 添加交易记录
        redisUtils.PlayerLeaseRecord.recordMessage(
            timestamp=startLeaseTime,
            returnTime=endLeaseTime,
            lessorGBID=lessorGBID,
            lesseeGBID=self.gbID,
            ownerGBID=ownerGBID,
            itemData=itemData,
            uniqueId=uniqueId,
            bindGold=bindGold,
            gold=gold,
            cost=cost,
            opUUID=opUUID,
        )

        # 
        itemDict = json.loads(itemData)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onReplyLeaseItemCommit log failed", uniqueId)
            return
        LogTrackingMgr.LogTrackingMgr.rent_item_deal(
            self.gbID,
            self.accountEntity.clientDistinctId,
            item.itemId,
            uniqueId,
            cost,
            gold,
            bindGold,
            ownerGBID,
            0,
            lessorGBID,
            0,
        )
        self.onMessagePre(MMD.datas.rent11, [str(gameconst.ItemIdEnum.MONEY), str(cost), str(item.itemId), str(1)])

    @gamedecorator.offlineCallback
    def onGiveLeaseItem(self, opUUID, uniqueId, itemData, returnOwnerServerId, returnOwnerGbId, returnEndTime):
        LOG_INFO("onGiveLeaseItem", opUUID, uniqueId, returnOwnerServerId, returnOwnerGbId, returnEndTime)

        itemDict = json.loads(itemData)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onGiveLeaseItem createItem failed", uniqueId, opUUID)
            return

        # 设置归还属性
        item.updateOwnerInfoByLease(returnOwnerGbId, returnOwnerServerId, returnEndTime)

        bag = self.bagData
        srcType = ACACD.datas.BONUS_SRC_LEASE
        if self.getBagLeftGridCount(gameconst.BagTypeEnum.BAG_TYPE_NORMAL) <= 0:
            # 背包满（极少触发，前置流程中会检查格子），通过邮件发送装备，避免玩家损失
            # 邮件有效期设为租期截止时刻，过期后附件不可领取，防止超期领取造成装备复制
            LOG_WARN("onGiveLeaseItem bag full, send by mail", uniqueId)
            mailVal = dropAward.MailAttachVal(itemObjs=[item])
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                GBGC.datas['equipReturnItem2']['value'],
                extraAttach=mailVal,
                expiredTime=returnEndTime,
                opUUID=opUUID,
                srcType=srcType,
            )
            self.onMessagePre(MMD.datas.rent02, [])
        else:
            detail = gameclass.AwardDetailCls(bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL, itemId=item.itemId, uniqueId=uniqueId)
            bag.addItemsToNewGrid(self, item, opUUID, srcType, detail)

        # 写入承租方冷却列表
        self._addLeaseCoolDown(uniqueId, returnEndTime)

        # 保存待移除装备数据，用于到期处理
        self.leasePendingRemoveItems[uniqueId] = {
            LEASE_RETURN_KEY_ITEM: itemData,
            LEASE_RETURN_KEY_END_TIME: returnEndTime,
            LEASE_RETURN_KEY_UUID: opUUID,
        }

        # 设置承租方到期移除定时器
        self._setupLeaseExpireTimer(uniqueId, returnEndTime)

    @gamedecorator.offlineCallback
    def onAddLeaseIncome(self, uniqueId, itemId, bindGold, gold, opUUID, returnEndTime, itemData):
        LOG_INFO("onAddLeaseIncome", bindGold, gold, itemId, opUUID, returnEndTime, uniqueId)

        # 防重：已存在的延迟收益不再重复记录
        if opUUID in self.leasePendingIncome:
            LOG_ERR("onAddLeaseIncome duplicate opUUID", opUUID)
            return

        # 写入出租方冷却列表
        self._addLeaseCoolDown(uniqueId, returnEndTime)

        # 保存待归还装备数据，并设置出租方到期归还定时器
        if itemData:
            self.leasePendingReturnItems[uniqueId] = {
                LEASE_RETURN_KEY_ITEM: itemData,
                LEASE_RETURN_KEY_END_TIME: returnEndTime,
                LEASE_RETURN_KEY_UUID: opUUID,
            }
            self._setupLeaseReturnTimer(uniqueId, returnEndTime)
        else:
            LOG_ERR(f"ILease::onAddLeaseIncome no sale item data, uniqueId: {uniqueId}")

        # 记录延迟收益，启动到账定时器
        arriveTime = utils.curTS() + AUC_CONST.datas['auctionPaymentDelayTime']['value'] * gameconst.ONE_MINUTE_COST_SECONDS
        self.leasePendingIncome[opUUID] = {
            LEASE_INCOME_KEY_GOLD: gold,
            LEASE_INCOME_KEY_BIND_GOLD: bindGold,
            LEASE_INCOME_KEY_TIMETS: arriveTime,
        }
        self._setupLeaseIncomeTimer(opUUID, arriveTime)

        #
        self.onMessagePre(MMD.datas.rent10, [str(itemId), str(1)])

    # -------------------------------------------------------------
    # 下架流程（跨服）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(1)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqCancelSaleItemInLease(self, exposed, uniqueId):
        LOG_INFO("reqCancelSaleItemInLease", uniqueId)
        if not self.leaseStub:
            LOG_INFO("reqCancelSaleItemInLease leaseStub not found")
            self.onMessagePre(MMD.datas.rent03, [])
            return

        # 先检查下背包格子
        if self.getBagLeftGridCount(gameconst.BagTypeEnum.BAG_TYPE_NORMAL) <= 0:
            LOG_INFO("reqCancelSaleItemInLease bag full", uniqueId)
            self.onMessagePre(MMD.datas.rent05, [])
            return

        # 锁定背包，防止并发操作导致格子被占用
        if not self.bagData.tryLockBag(3, 'lease_cancel_sale'):
            LOG_INFO("_doCancelSaleItemInLease lock bag failed", uniqueId)
            self.onMessagePre(MMD.datas.rent03, [])
            return

        self.leaseStub.cancelItem(self.gbID, uniqueId)

        LogTrackingMgr.LogTrackingMgr.rent_item_cancel(
            self.gbID,
            self.accountEntity.clientDistinctId,
            0,
            uniqueId,
            0,
            'cancel'
        )

    def onReplyCancelItemInLease(self, uniqueId, result, itemDataStr):
        LOG_DBG("onReplyCancelItemInLease", uniqueId, result)
        # 解锁背包（与 _doCancelSaleItemInLease 中的 tryLockBag 配对）
        self.bagData.unLockBag()

        if result:
            LOG_INFO('ILease::onReplyCancelItemInLease failed:', uniqueId, result)
            self.onMessagePre(MMD.datas.rent03, [])

            # 可能已经租出去了
            if result == LEASE_STATUS_ERROR or result == LEASE_NOT_FOUND:
                self.client.onCancelSaleItemInLeaseSucc(uniqueId)
            return

        itemDict = json.loads(itemDataStr)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("onReplyCancelItemInLease createItem failed", uniqueId)
            return

        returnTime = item.getReturnTime()
        if returnTime and returnTime < utils.curTS():
            LOG_INFO("onReplyCancelItemInLease item already expired", uniqueId, returnTime)
            self.onMessagePre(MMD.datas.redeem07, [])
            self.client.onCancelSaleItemInLeaseSucc(uniqueId)
            return

        if self.getBagLeftGridCount(gameconst.BagTypeEnum.BAG_TYPE_NORMAL) <= 0:
            # 背包被并发操作占满，通过邮件返还装备
            # 爆装邮件有效期设为归还截止时刻，过期后附件不可领取，防止超期领取
            LOG_ERR("onReplyCancelItemInLease bag full, send by mail", uniqueId, itemDataStr)
            mailVal = dropAward.MailAttachVal(itemObjs=[item])
            mailAssistor.sendMailToPlayers(
                [self.gbID],
                GBGC.datas['equipReturnItem3']['value'],
                extraAttach=mailVal,
                expiredTime=returnTime,
                opUUID=KBEngine.genUUID64(),
                srcType=ACACD.datas.BONUS_SRC_LEASE_CANCEL,
            )
            self.onMessagePre(MMD.datas.rent05, [])
            return

        srcType = ACACD.datas.BONUS_SRC_LEASE_CANCEL
        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls(bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL, itemId=item.itemId)
        self.bagData.addItemsToNewGrid(self, item, opUUID, srcType, detail)
        self.client.onCancelSaleItemInLeaseSucc(uniqueId)

    # -------------------------------------------------------------
    # 提取收入（本服执行）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqTakeLeaseIncome(self, exposed):
        LOG_INFO("reqTakeLeaseIncome")

        bindGold = self.leaseIncomeBindGold
        gold = self.leaseIncomeGold
        if bindGold <= 0 and gold <= 0:
            LOG_INFO("reqTakeLeaseIncome no income")
            return

        addWealthVal = dropAward.AwardVal()
        if bindGold > 0:
            addWealthVal.addWealthByItemId(gameconst.ItemIdEnum.BIND_MONEY, bindGold)
        if gold > 0:
            addWealthVal.addWealthByItemId(gameconst.ItemIdEnum.MONEY, gold)

        srcType = ACACD.datas.BONUS_SRC_LEASE_INCOME
        opUUID = KBEngine.genUUID64()

        if not self.canAddWealthVal(srcType, addWealthVal):
            LOG_ERR("reqTakeLeaseIncome cannot add wealth", bindGold, gold)
            return

        self.leaseIncomeBindGold = 0
        self.leaseIncomeGold = 0

        detail = gameclass.AwardDetailCls(moneyAmount=gold, bindMoneyAmount=bindGold)
        self.addWealth(srcType, addWealthVal, opUUID, detail)

        self.client.onTakeLeaseIncomeSucc(bindGold, gold)

    # -------------------------------------------------------------
    # 交易记录（本服 Redis）
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseRecords(self, exposed, recordType, number):
        LOG_DBG("reqLeaseRecords", recordType, number)

        redisUtils.PlayerLeaseRecord.getMessageRecord(self, self.gbID, number, recordType)

    # -------------------------------------------------------------
    # 商店查询
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseShopSummary(self, exposed, categoryId, school, quality):
        LOG_DBG("reqLeaseShopSummary", categoryId, school, quality)

        if not self.leaseStub:
            LOG_ERR("reqLeaseShopSummary leaseStub not found")
            return

        typeInfo = []
        itemIdList = []

        mainType = GBTTD.AuctionCategoryDic.get(categoryId)
        if school == 0:
            for curSchool in gameconst.ALL_SCHOOL_TYPE:
                categoryInfo = GBTED.auctionDic.get((mainType, curSchool))
                categoryInfo and typeInfo.extend(categoryInfo)
        else:
            typeInfo = GBTED.auctionDic.get((mainType, school))

        if not typeInfo:
            LOG_ERR("reqLeaseShopSummary:: not found typeInfo", categoryId, school, quality)
            return

        for mainType, subType in typeInfo:
            if quality == gameconst.ItemQuality.ALL_QUALITY:
                for curQuality in gameconst.ItemQuality.COLL_QUALITY:
                    itemIdList.extend(GBGBD.auctionDic.get((mainType, subType, curQuality), []))
            else:
                itemIdList.extend(GBGBD.auctionDic.get((mainType, subType, quality), []))

        itemIdList = list(set(itemIdList))
        self.leaseStub.getShopSummary(categoryId, itemIdList, self.gbID)

    def onLeaseShopSummaryResp(self, categoryId, items):
        LOG_DBG("onLeaseShopSummaryResp", categoryId, items)
        self.client.onLeaseShopSummary(categoryId, items)

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqLeaseShopItems(self, exposed, itemId, page, pageSize, gradeList, enhanceLvList):
        LOG_DBG("reqLeaseShopItems", itemId, enhanceLvList, gradeList)

        if not self.leaseStub:
            LOG_ERR("reqLeaseShopItems leaseStub not found")
            return

        if page < 0 or pageSize > 32:
            LOG_ERR("reqLeaseShopItems pagesize limit:", page, pageSize)
            return

        enhanceLvMask = _levelListToMask(enhanceLvList)
        gradeMask = _levelListToMask(gradeList)
        if enhanceLvMask is None or gradeMask is None:
            LOG_ERR("reqLeaseShopItems filter level out of range", enhanceLvList, gradeList)
            return

        self.leaseStub.getShopItems(itemId, page, pageSize, self.gbID, enhanceLvMask, gradeMask)

    def onLeaseShopItemsResp(self, itemId, page, pageSize, items):
        LOG_DBG("onLeaseShopItemsResp", itemId, page, pageSize, len(items))
        if not items:
            data = {'itemId': itemId, 'page': page, 'pageSize': pageSize, 'items': items}
            zStr = gzip.compress(json.dumps(data).encode('ascii'))
            self.streamStringProxy(zStr, '', gameconst.StreamStringID.LEASE_SHOP_ITEMS)
            return

        gbIds = []
        for item in items:
            gbIds.append(item['lessorGbId'])
        redisUtils.RedisUtils.getUsersInfo(gbIds, functools.partial(self._onGetLessorInfoForShopItems, itemId, page, pageSize, items))

    def _onGetLessorInfoForShopItems(self, itemId, page, pageSize, items, userInfos):
        LOG_DBG("_onGetLessorInfoForShopItems", itemId, len(items), len(userInfos))
        userInfoCache = {}
        for userInfo in userInfos:
            if userInfo:
                userInfoCache[userInfo.gbId] = userInfo.name

        for item in items:
            lessorGbId = item.get('lessorGbId', 0)
            lessorServerId = item.get('lessorServerId', 0)
            item['lessorName'] = userInfoCache.get(lessorGbId, '')
            if lessorServerId:
                serverData = gameglobal.mapleServerInfo.get(int(lessorServerId), None)
                if serverData:
                    item['lessorServerName'] = serverData.get('server_name', '')
                else:
                    item['lessorServerName'] = ''
                    LOG_WARN("_onGetLessorInfoForShopItems:: no server data", lessorGbId, lessorServerId)
            else:
                item['lessorServerName'] = ''

        data = {'itemId': itemId, 'page': page, 'pageSize': pageSize, 'items': items}
        zStr = gzip.compress(json.dumps(data).encode('ascii'))
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.LEASE_SHOP_ITEMS)

    # -------------------------------------------------------------
    # 我的出租列表
    # -------------------------------------------------------------

    @gamedecorator.limitcall(0.5)
    @gamedecorator.checkGameconfigEnable('lease')
    def reqMyLeaseSaleInfo(self, exposed):
        LOG_DBG("reqMyLeaseSaleInfo")

        if not self.leaseStub:
            LOG_ERR("reqMyLeaseSaleInfo leaseStub not found")
            return

        self.leaseStub.getMySaleList(self.gbID)

    def _calcLeasePendingIncome(self):
        """计算当前延迟到账的收益总额"""
        delayGold = 0
        delayBindGold = 0
        for pending in self.leasePendingIncome.values():
            delayGold += pending.get(LEASE_INCOME_KEY_GOLD, 0)
            delayBindGold += pending.get(LEASE_INCOME_KEY_BIND_GOLD, 0)
        return delayGold, delayBindGold

    def onMyLeaseSaleInfo(self, items):
        LOG_DBG("onMyLeaseSaleInfo", len(items))
        delayGold, delayBindGold = self._calcLeasePendingIncome()
        data = {
            'gold': self.leaseIncomeGold,
            'bindGold': self.leaseIncomeBindGold,
            'delayGold': delayGold,
            'delayBindGold': delayBindGold,
            'items': items,
        }
        zStr = gzip.compress(json.dumps(data).encode('ascii'))
        self.streamStringProxy(zStr, '', gameconst.StreamStringID.MY_LEASE_SALE_INFO)

    # -------------------------------------------------------------
    # 租赁到期定时器管理
    # -------------------------------------------------------------

    def _setupLeaseExpireTimer(self, uniqueId, returnEndTime):
        """承租方：设置到期移除定时器"""
        LOG_INFO(f"ILease::_setupLeaseExpireTimer uniqueId: {uniqueId}, returnTime: {returnEndTime}")
        self._datetimeCallback(returnEndTime, 'doLeaseExpire', (uniqueId,), gametimer.TIMER_TAG_LEASE_EXPIRE)

    def doLeaseExpire(self, uniqueId):
        """承租方到期：本地移除装备"""
        LOG_INFO(f"ILease::doLeaseExpire uniqueId: {uniqueId}")
        if uniqueId not in self.leasePendingRemoveItems:
            LOG_ERR("doLeaseExpire no pending data", uniqueId)
            return

        # 先尝试从背包中查找
        gridId, item = self._findLeaseEquipInBag(uniqueId)
        if item:
            if self.bagData.isLocked():
                LOG_WARN("doLeaseExpire lock bag fail, will retry", uniqueId)
                self._setupLeaseExpireTimer(uniqueId, utils.curTS() + 3)
                return
            self._doLeaseExpireRemoveFromBag(uniqueId, gridId, item.itemId)
            return

        # 尝试脱身上装备
        self.cell.cellLeaseExpireRemoveEquip(uniqueId)

    def _doLeaseExpireRemoveFromBag(self, uniqueId, gridId, itemId):
        """从背包中移除租赁到期装备，处理成功后 pop pending"""
        LOG_INFO(f"ILease::_doLeaseExpireRemoveFromBag uniqueId: {uniqueId}")
        pending = self.leasePendingRemoveItems.get(uniqueId)
        if not pending:
            LOG_ERR("lease expire no pending data when remove from bag", uniqueId)
            return

        # 这里再判断一下
        # 如果 returntime 大于当前时间，存在异常不能移除
        _, item = self._findLeaseEquipInBag(uniqueId)
        if item and (not item.equipAttr.returnTime or item.equipAttr.returnTime > utils.curTS()):
            LOG_WARN(f"ILease::_doLeaseExpireRemoveFromBag returntime err, uniqueId: {uniqueId}")
            self.leasePendingRemoveItems.pop(uniqueId, None)
            return

        srcType = ACACD.datas.BONUS_SRC_LEASE_RETURN
        opUUID = pending[LEASE_RETURN_KEY_UUID]
        detail = gameclass.AwardDetailCls(bagType=gameconst.BagTypeEnum.BAG_TYPE_NORMAL, gridId=gridId, itemId=itemId, uniqueId=uniqueId)
        self.bagData.cleanGridByGridId(self, gridId, itemId, opUUID, srcType, detail)

        self.leasePendingRemoveItems.pop(uniqueId, None)
        self.client.onRemoveLeasedItem(uniqueId)

    def cellLeaseExpireRemoveEquipCB(self, uniqueId, success):
        """cell 租赁到期卸下装备回调
        success=True 表示装备本来不在身上，或者已成功卸下
        success=False 表示身上装备被锁，需要重试
        """
        LOG_INFO("cellLeaseExpireRemoveEquipCB", uniqueId, success)
        if not success:
            self._setupLeaseExpireTimer(uniqueId, utils.curTS() + 3)
            return

        # cell 已处理完毕，继续尝试从背包扣除
        gridId, item = self._findLeaseEquipInBag(uniqueId)
        if item:
            if self.bagData.isLocked():
                LOG_WARN("doLeaseExpire lock bag fail, will retry", uniqueId)
                self._setupLeaseExpireTimer(uniqueId, utils.curTS() + 3)
                return
            self._doLeaseExpireRemoveFromBag(uniqueId, gridId, item.itemId)
            return

        # 背包中也没有，整个移除流程完成
        self.leasePendingRemoveItems.pop(uniqueId, None)
        self.client.onRemoveLeasedItem(uniqueId)

    def _setupLeaseReturnTimer(self, uniqueId, returnEndTime):
        """出租方：设置到期归还定时器"""
        LOG_INFO(f"ILease::_setupLeaseReturnTimer uniqueId: {uniqueId}, returnTime: {returnEndTime}")
        self._datetimeCallback(returnEndTime, 'doLeaseReturnToOwner', (uniqueId,), gametimer.TIMER_TAG_LEASE_RETURN)

    def doLeaseReturnToOwner(self, uniqueId):
        """出租方到期：本地给自己发邮件归还装备"""
        LOG_INFO("doLeaseReturnToOwner", uniqueId)
        pending = self.leasePendingReturnItems.pop(uniqueId, None)
        if not pending:
            LOG_ERR("doLeaseReturnToOwner no pending data", uniqueId)
            return

        itemData = pending[LEASE_RETURN_KEY_ITEM]
        itemDict = json.loads(itemData)
        item = itemFactory.ItemFactory.createItemWithSavedDict(itemDict)
        if not item:
            LOG_ERR("doLeaseReturnToOwner createItem failed", uniqueId)
            return

        # 说明自己不是原主人
        if item.equipAttr.returnReason != gameconst.ItemReturnReason.NORMAL:
            LOG_WARN("ILease::doLeaseReturnToOwner no need return")
            return

        # 发邮件给自己
        leaseReturnMailId = GBGC.datas['equipReturnMailID']['value']
        mailVal = dropAward.MailAttachVal(itemObjs=[item])
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            leaseReturnMailId,
            extraAttach=mailVal,
            despArgs=(GBGBD.datas[item.itemId]['name'],),
            opUUID=pending[LEASE_RETURN_KEY_UUID],
            srcType=ACACD.datas.BONUS_SRC_LEASE_RETURN,
        )

    def _setupLeaseIncomeTimer(self, opUUID, arriveTime):
        """出租方：设置收益延迟到账定时器"""
        LOG_INFO(f"ILease::_setupLeaseIncomeTimer opUUID: {opUUID}, arriveTime: {arriveTime}")
        self._datetimeCallback(arriveTime, 'doLeaseIncomeArrival', (opUUID,), gametimer.TIMER_TAG_LEASE_INCOME)

    def doLeaseIncomeArrival(self, opUUID):
        """延迟收益到账"""
        LOG_INFO("doLeaseIncomeArrival", opUUID)
        pending = self.leasePendingIncome.pop(opUUID, None)
        if not pending:
            LOG_ERR("doLeaseIncomeArrival no pending data", opUUID)
            return

        gold = pending.get(LEASE_INCOME_KEY_GOLD, 0)
        bindGold = pending.get(LEASE_INCOME_KEY_BIND_GOLD, 0)
        if gold <= 0 and bindGold <= 0:
            return

        self.leaseIncomeGold += gold
        self.leaseIncomeBindGold += bindGold
        if self.client:
            delayGold, delayBindGold = self._calcLeasePendingIncome()
            self.client.onUpdateLeaseIncome(self.leaseIncomeBindGold, self.leaseIncomeGold, delayBindGold, delayGold)

    def onLeaseLoginInit(self):
        # 时间小于等于当前时间时 _datetimeCallback 会立即触发，
        # 此时 avatar init 还没完成，回调依赖的 accountEntity 尚未准备好，故延迟 0.5s 再触发
        nowTS = utils.curTS()

        # 承租方：遍历待移除列表，重建租赁到期定时器
        for uniqueId, pending in list(self.leasePendingRemoveItems.items()):
            returnEndTime = max(pending.get(LEASE_RETURN_KEY_END_TIME, 0), nowTS + 1)
            self._setupLeaseExpireTimer(uniqueId, returnEndTime)

        # 出租方：遍历待归还列表，重建归还定时器
        for uniqueId, pending in list(self.leasePendingReturnItems.items()):
            returnEndTime = max(pending.get(LEASE_RETURN_KEY_END_TIME, 0), nowTS + 1)
            self._setupLeaseReturnTimer(uniqueId, returnEndTime)

        # 出租方：遍历延迟收益列表，重建到账定时器
        for opUUID, pending in list(self.leasePendingIncome.items()):
            arriveTime = max(pending.get(LEASE_INCOME_KEY_TIMETS, 0), nowTS + 1)
            self._setupLeaseIncomeTimer(opUUID, arriveTime)

    # -------------------------------------------------------------
    # 流程测试接口（客户端尚未接入时，供服务端直接调用自测）
    # -------------------------------------------------------------

    def testGetFirstEquipmentItem(self):
        for _, item in self.bagData.gridIdToGridObj.items():
            if item.isEquipmentItem(): return item
        return None

    def testSaleFirstEquip(self, pricePerDay=1, days=1):
        """上架背包中第一个可租赁的装备"""
        bag = self.bagData
        if not bag:
            LOG_INFO("testSaleFirstEquip: bag is None")
            return
        for gridId, item in bag.gridIdToGridObj.items():
            if item and item.isEquipmentItem() and self._canEquipItemLease(item):
                LOG_INFO("testSaleFirstEquip: selling", item.uniqueId, pricePerDay, days)
                self.reqSaleItemInLease(None, item.uniqueId, pricePerDay, days)
                return
        LOG_INFO("testSaleFirstEquip: no leasable equip found")

    def testSaleEquipByUniqueId(self, uniqueId, pricePerDay=1, days=1):
        """上架指定 uniqueId 的装备"""
        LOG_INFO("testSaleEquipByUniqueId", uniqueId, pricePerDay, days)
        self.reqSaleItemInLease(None, uniqueId, pricePerDay, days)

    def testLeaseItem(self, uniqueId):
        """租借指定 uniqueId 的装备"""
        LOG_INFO("testLeaseItem", uniqueId)
        self.reqLeaseItem(None, uniqueId)

    def testCancelSaleItem(self, uniqueId):
        """下架指定 uniqueId 的装备"""
        LOG_INFO("testCancelSaleItem", uniqueId)
        self.reqCancelSaleItemInLease(None, uniqueId)

    def testTakeLeaseIncome(self):
        """提取租赁收入"""
        LOG_INFO("testTakeLeaseIncome")
        self.reqTakeLeaseIncome(None)

    def testQueryLeaseShopSummary(self, equipType=0, equipSubType=0):
        """查询租赁商店摘要"""
        LOG_INFO("testQueryLeaseShopSummary", equipType, equipSubType)
        self.reqLeaseShopSummary(None, equipType, equipSubType)

    def testQueryLeaseShopItems(self, itemId, page=1, pageSize=10, enhanceLvList=(), gradeList=()):
        """查询租赁商店某物品的列表"""
        LOG_INFO("testQueryLeaseShopItems", itemId, page, pageSize, enhanceLvList, gradeList)
        self.reqLeaseShopItems(None, itemId, page, pageSize, enhanceLvList, gradeList)

    def testQueryMyLeaseSaleInfo(self):
        """查询我的出租列表"""
        LOG_INFO("testQueryMyLeaseSaleInfo")
        self.reqMyLeaseSaleInfo(None)

    def testQueryLeaseRecords(self, recordType=0, number=10):
        """查询租赁交易记录"""
        LOG_INFO("testQueryLeaseRecords", recordType, number)
        self.reqLeaseRecords(None, recordType, number)
