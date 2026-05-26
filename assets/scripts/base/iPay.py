# coding: utf-8
from KBEDebug import *
import KBEngine

import utils
import dropAward
import gameconst
import awardContext
import gameclass

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import buyCredit_buyCredit as BC_BCD
import buyCredit_buyCreditConst as BC_BCCD
import gamedecorator
import gameconfig
import LogTrackingMgr
import message_Message_def as MMD

class BuyCreditLimitType:
    Once = 1
    Daily = 2
    Weekly = 3
    Monthly = 4

class IPay(object):
    def __init__(self):
        self.tlogArgsDic = {}

    @gamedecorator.checkGameconfigEnable('monthCard')
    def clientBuyMonthCard(self, buyCreditId):
        cfgData = BC_BCD.datas.get(buyCreditId)
        if not self.checkCanAddMonthCard():
            self.onMessagePre(BC_BCCD.datas["durationHoursLimitMsg"]["value"], [])
            return
        priceID = cfgData.get('priceID')
        quantity = cfgData.get('quantity')
        if priceID and quantity:
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(priceID, quantity)

            if not self.canDeductWealth(deductWealthVal):
                LOG_WARN('clientBuyGoods: items not enough:', deductWealthVal)
                return

            detail = gameclass.AwardDetail(buyCreditId=buyCreditId)
            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_BUY_CURRENCY_GIFT
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        monthCardId = cfgData.get('ID')
        seconds = BC_BCCD.datas['durationHours']['value'] * 3600
        opUUID = self.doAddMonthCard(seconds, monthCardId)
        LogTrackingMgr.LogTrackingMgr.Gift_Buy(
            self.gbID,
            buyCreditId,
            opUUID
        )
        return True

    @gamedecorator.checkGameconfigEnable('pay')
    def clientBuyGoods(self, exposed, buyCreditId):
        LOG_INFO('clientBuyGoods', buyCreditId)
        cfgData = BC_BCD.datas.get(buyCreditId)
        if not cfgData:
            LOG_ERR('clientBuyGoods buyCreditId not in config', buyCreditId)
            return
        
        if not gameconfig.payConfigEnable("pay", buyCreditId):
            LOG_WARN('clientBuyGoods payConfigEnable is False', buyCreditId)
            return
        
        creditType = cfgData.get('type')
        
        if not gameconfig.payConfigEnable("buyCreditType", creditType):
            LOG_WARN('clientBuyGoods payConfigEnable is False, buyCreditType', creditType)
            self.onMessagePre(MMD.datas.systemSwitchClose, [])
            return

        price = cfgData.get('price')
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT
        if creditType == gameconst.BuyCreditType.money:
            wealthVal = dropAward.AwardVal()
            credit = cfgData.get('credit')
            if credit:
                wealthVal.addWealthByItemId(gameconst.ItemId.MONEY, credit)
            # 只有直充点券需要额外赠送玉贝
            if buyCreditId not in self.firstBuyCreditDic:
                self.firstBuyCreditDic[buyCreditId] = utils.curTS()
                self.client.onAddFirstBuyCredit(buyCreditId)
                extraItemId = cfgData['firstBuyExRewardType']
                extraItemNum = BC_BCD.datas[buyCreditId]['firstBuyExReward']
                wealthVal.addWealthByItemId(extraItemId, extraItemNum)
                detail = gameclass.AwardDetail(buyCreditId=buyCreditId)
            else:
                extraItemId = BC_BCD.datas[buyCreditId]['normalBuyExRewardType']
                extraItemNum = BC_BCD.datas[buyCreditId]['normalBuyExReward']
                wealthVal.addWealthByItemId(extraItemId, extraItemNum)
                detail = gameclass.AwardDetail(buyCreditId=buyCreditId)
            ctx = self._getAvatarAwardCtx(0, None)
            self.addWealth(srcType, wealthVal, opUUID, detail=detail, awardCtx=ctx)
            LogTrackingMgr.LogTrackingMgr.Gift_Buy(
                self.gbID,
                buyCreditId,
                opUUID
            )
        elif creditType == gameconst.BuyCreditType.PermanentGift:
            priceID = cfgData.get('priceID')
            quantity = cfgData.get('quantity')
            if priceID and quantity:
                deductWealthVal = dropAward.DeductWealthVal()
                deductWealthVal.addWealthByItemId(priceID, quantity)

                if not self.canDeductWealth(deductWealthVal):
                    LOG_WARN('clientBuyGoods: items not enough:', deductWealthVal)
                    return

                detail = gameclass.AwardDetail(buyCreditId=buyCreditId)
                opUUID = KBEngine.genUUID64()
                srcType = AAC_AACDD.datas.BONUS_SRC_BUY_CURRENCY_GIFT
                self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            limitNumber = cfgData.get('limitNumber')
            if limitNumber:
                buyNum = self.buyCreditNumDic.get(buyCreditId, 0)
                if buyNum >= limitNumber:
                    LOG_ERR('clientBuyGoods over limitNumber', buyCreditId, buyNum, limitNumber)
                    return
                self.buyCreditNumDic[buyCreditId] = buyNum+1
                self.client.onUpdateCreditNum([buyCreditId], [buyNum+1])
                self._addCreditConfigReward(buyCreditId, opUUID, srcType, cfgData)
        elif creditType == gameconst.BuyCreditType.holidayGift:
            if not self.checkHolidayPayCond(buyCreditId):
                return
            priceID = cfgData.get('priceID')
            quantity = cfgData.get('quantity')
            if priceID and quantity:
                deductWealthVal = dropAward.DeductWealthVal()
                deductWealthVal.addWealthByItemId(priceID, quantity)

                if not self.canDeductWealth(deductWealthVal):
                    LOG_WARN('clientBuyGoods: items not enough:', deductWealthVal)
                    return

                detail = gameclass.AwardDetail(buyCreditId=buyCreditId)
                opUUID = KBEngine.genUUID64()
                srcType = AAC_AACDD.datas.BONUS_SRC_BUY_CURRENCY_GIFT
                self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            self.holidayPaySuccess(buyCreditId)
            self._addCreditConfigReward(buyCreditId, opUUID, srcType, cfgData)
        elif creditType == gameconst.BuyCreditType.monthCard:
            if not self.clientBuyMonthCard(buyCreditId):
                LOG_WARN('clientBuyMonthCard failed', buyCreditId)
                return

        self.client.onBuyCreditSuccess(buyCreditId)
        self.midasTotalPay += price

    def _addCreditConfigReward(self, buyCreditId, opUUID, src, cfgData=None):
        cfgData = cfgData or BC_BCD.datas[buyCreditId]
        reward = cfgData['reward']
        reward = reward or []
        detail = gameclass.AwardDetail(itemId=buyCreditId)
        for rewardId in reward:
            awardCtx = awardContext.CommonContext(gameconst.MailConstID.REWARD_MAIL_ID)
            self.addAwards(src, rewardId, 1, opUUID, detail, awardCtx)
        LogTrackingMgr.LogTrackingMgr.Gift_Buy(
            self.gbID,
            buyCreditId,
            opUUID
        )

    @property
    def totalPayMoney(self):
        return self.midasTotalPay + self.idipTotalPay

    def sendPlayerPayInfo(self):
        self._sendPlayerPayInfo()

    def _sendPlayerPayInfo(self):
        clientData = []
        for key, val in self.buyCreditNumDic.items():
            clientData.append({'creditId': key, 'buyNum': val})
        self.client.onGetPlayerPayInfo(self.totalPayMoney,
                                       list(self.firstBuyCreditDic.keys()), clientData)

    def reqQueryPlayerPayInfo(self):
        self._sendPlayerPayInfo()

    def _onBuyCreditDailyUpdate(self, *args):
        clientBuyCreditIds = []
        clientBuyCreditNums = []
        for buyCreditId, buyNum in self.buyCreditNumDic.items():
            if buyCreditId in BC_BCD.datas:
                limitType = BC_BCD.datas[buyCreditId]['limitType']
                if limitType == BuyCreditLimitType.Daily and buyNum:
                    self.buyCreditNumDic[buyCreditId] = 0
                    clientBuyCreditIds.append(buyCreditId)
                    clientBuyCreditNums.append(0)
        self.client.onUpdateCreditNum(clientBuyCreditIds, clientBuyCreditNums)

    def _onBuyCreditWeeklyUpdate(self, *args):
        clientBuyCreditIds = []
        clientBuyCreditNums = []
        for buyCreditId, buyNum in self.buyCreditNumDic.items():
            if buyCreditId in BC_BCD.datas:
                limitType = BC_BCD.datas[buyCreditId]['limitType']
                if limitType == BuyCreditLimitType.Weekly and buyNum:
                    self.buyCreditNumDic[buyCreditId] = 0
                    clientBuyCreditIds.append(buyCreditId)
                    clientBuyCreditNums.append(0)
        self.client.onUpdateCreditNum(clientBuyCreditIds, clientBuyCreditNums)

    def _onBuyCreditMonthlyUpdate(self, *args):
        clientBuyCreditIds = []
        clientBuyCreditNums = []
        for buyCreditId, buyNum in self.buyCreditNumDic.items():
            if buyCreditId in BC_BCD.datas:
                limitType = BC_BCD.datas[buyCreditId]['limitType']
                if limitType == BuyCreditLimitType.Monthly and buyNum:
                    self.buyCreditNumDic[buyCreditId] = 0
                    clientBuyCreditIds.append(buyCreditId)
                    clientBuyCreditNums.append(0)
        self.client.onUpdateCreditNum(clientBuyCreditIds, clientBuyCreditNums)

