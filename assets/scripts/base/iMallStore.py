# -*- coding: utf-8 -*-
from KBEDebug import *
import utils
import KBEngine
import gameconst
import gameclass
import dropAward
import awardContext
import LogTrackingMgr
import gamedecorator

import mall_giftStore as MGS
import mall_mountsStore as MMS
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import mall_mallConst as MMC


class IMallStore(object):

    def __init__(self):
        LOG_INFO('IMallStore::__init__')

    @gamedecorator.checkGameconfigEnable('pay')
    @gamedecorator.limitcall(1)
    def reqGiftStoreLimit(self, exposed):
        LOG_INFO('IMallStore::reqGiftStoreLimit:', exposed)
        self.sendMallGiftStoreLimit()

    @gamedecorator.checkGameconfigEnable('pay')
    @gamedecorator.limitcall(1)
    def reqMountStoreLimit(self, exposed):
        LOG_INFO('IMallStore::reqMountStoreLimit:', exposed)
        self.sendMallMountStoreLimit()

    @gamedecorator.checkGameconfigEnable('pay')
    @gamedecorator.limitcall(1)
    def reqBuyGiftStore(self, exposed, storeId):
        LOG_INFO('IMallStore::reqBuyGiftStore:', exposed, storeId)
        cfg = MGS.datas.get(storeId)
        if not cfg:
            result = gameconst.MallStoreResult.WRONG_ARGS
            LOG_ERR('reqBuyGiftStore:: storeId not found', storeId)
        else:
            result = self._processMallPurchase(gameconst.MallStoreType.GIFT, storeId, cfg, self.giftStorePurchaseNumDic)
        self.client.onBuyMallGiftStoreResult(storeId, result)

    @gamedecorator.checkGameconfigEnable('pay')
    @gamedecorator.limitcall(1)
    def reqBuyMountStore(self, exposed, storeId):
        LOG_INFO('IMallStore::reqBuyMountStore:', exposed, storeId)
        cfg = MMS.datas.get(storeId)
        if not cfg:
            result = gameconst.MallStoreResult.WRONG_ARGS
            LOG_ERR('reqBuyMountStore:: storeId not found', storeId)
        else:
            result = self._processMallPurchase(gameconst.MallStoreType.MOUNT, storeId, cfg, self.mountsStorePurchaseNumDic)
        self.client.onBuyMallMountStoreResult(storeId, result)

    def _processMallPurchase(self, storeType, storeId, cfg, purchaseDic):
        LOG_INFO('IMallStore::_processMallPurchase:', storeType, storeId)
        limitNumber = cfg.get('limitNumber', 0)
        if limitNumber > 0:
            bought = purchaseDic.get(storeId, 0)
            if bought >= limitNumber:
                LOG_WARN('_processMallPurchase:: over limit', storeId, bought, limitNumber)
                return gameconst.MallStoreResult.COUNT_LIMIT

        costItems = cfg.get('costItem')
        if not self.isPremiumIdMonthCardExpired(MMC.datas['monthCardCostItemTypeId']['value']):
            monthCardCostItem = cfg.get('monthCardCostItem')
            if monthCardCostItem:
                costItems = monthCardCostItem

        deductWealth = dropAward.DeductWealthVal()
        for costItem in costItems:
            itemId, qty = costItem
            deductWealth.addWealthByItemId(itemId, qty)

        res = self.canDeductWealth(deductWealth)
        if not res:
            if res() == gameconst.CanDeductWealthRes.FALSE_POPUP_SECOND_PWD:
                return gameconst.MallStoreResult.FAIL
            return gameconst.MallStoreResult.ITEM_IS_NOT_ENOUGH

        rewardId = cfg.get('reward')
        awardCtx = awardContext.CommonContext(gameconst.MailConstEnum.REWARD_MAIL_ID)
        awardCtx = self.getAvatarAwardCtx(rewardId, awardCtx)
        wealthVal = dropAward.getAward(rewardId, 1, awardCtx)

        opUUID = KBEngine.genUUID64()
        detail = gameclass.AwardDetailCls()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUY_ITEMS

        if not self.canAddWealthVal(srcType, wealthVal):
            return gameconst.MallStoreResult.BAG_IS_FULL
        
        self.deductWealth(srcType, deductWealth, opUUID, detail)
        self.addWealth(srcType, wealthVal, opUUID, detail, awardCtx=awardCtx)

        if limitNumber > 0:
            purchaseDic[storeId] = purchaseDic.get(storeId, 0) + 1
        limitType = cfg.get('limitType', 0)
        boughtNum = purchaseDic.get(storeId, 0)
        LogTrackingMgr.LogTrackingMgr.Gift_Buy(self.gbID, self.accountEntity.clientDistinctId, self.gbID, storeId, opUUID, limitType, limitNumber, boughtNum)
        return gameconst.MallStoreResult.SUCCESS

    def _resetMallLimits(self, storeType, configDatas, purchaseDic, limitType):
        LOG_INFO('IMallStore::_resetMallLimits:', storeType, limitType)
        hasChanged = False
        for storeId, bought in purchaseDic.items():
            cfg = configDatas.get(storeId)
            if cfg and cfg.get('limitType') == limitType and bought > 0:
                purchaseDic[storeId] = 0
                hasChanged = True

        if hasChanged:
            if storeType == gameconst.MallStoreType.GIFT:
                self.sendMallGiftStoreLimit()
            elif storeType == gameconst.MallStoreType.MOUNT:
                self.sendMallMountStoreLimit()

    def _onMallPurchaseDailyUpdate(self, *args):
        LOG_INFO('IMallStore::_onMallPurchaseDailyUpdate:', args)
        self._resetMallLimits(gameconst.MallStoreType.GIFT, MGS.datas, self.giftStorePurchaseNumDic, gameconst.MallLimitType.Daily)
        self._resetMallLimits(gameconst.MallStoreType.MOUNT, MMS.datas, self.mountsStorePurchaseNumDic, gameconst.MallLimitType.Daily)

    def _onMallPurchaseWeeklyUpdate(self, *args):
        LOG_INFO('IMallStore::_onMallPurchaseWeeklyUpdate:', args)
        self._resetMallLimits(gameconst.MallStoreType.GIFT, MGS.datas, self.giftStorePurchaseNumDic, gameconst.MallLimitType.Weekly)
        self._resetMallLimits(gameconst.MallStoreType.MOUNT, MMS.datas, self.mountsStorePurchaseNumDic, gameconst.MallLimitType.Weekly)

    def _onMallPurchaseMonthlyUpdate(self, *args):
        LOG_INFO('IMallStore::_onMallPurchaseMonthlyUpdate:', args)
        self._resetMallLimits(gameconst.MallStoreType.GIFT, MGS.datas, self.giftStorePurchaseNumDic, gameconst.MallLimitType.Monthly)
        self._resetMallLimits(gameconst.MallStoreType.MOUNT, MMS.datas, self.mountsStorePurchaseNumDic, gameconst.MallLimitType.Monthly)

    def getStoreLimitDatas(self, dic):
        LOG_INFO('IMallStore::getStoreLimitDatas:', dic)
        storeIds = []
        usedCounts = []
        for storeId, usedCount in dic.items():
            storeIds.append(storeId)
            usedCounts.append(usedCount)
        return storeIds, usedCounts

    def sendMallGiftStoreLimit(self):
        LOG_INFO('IMallStore::sendMallGiftStoreLimit')
        storeIds, usedCounts = self.getStoreLimitDatas(self.giftStorePurchaseNumDic)
        self.client.onMallGiftStoreLimit(storeIds, usedCounts)

    def sendMallMountStoreLimit(self):
        LOG_INFO('IMallStore::sendMallMountStoreLimit')
        storeIds, usedCounts = self.getStoreLimitDatas(self.mountsStorePurchaseNumDic)
        self.client.onMallMountStoreLimit(storeIds, usedCounts)
