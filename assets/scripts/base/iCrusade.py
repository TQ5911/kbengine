# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import dataUtils
import dropAward
import gameclass
import gamedecorator
import LogTrackingMgr

import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import teamDunChallenge_config as TDC_CFG
import gameconst
import actionContext
import utils

class ICrusade(object):
    def onCrusadeDailyRewardNumUpdate(self, *args):
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO('ICrusade::onCrusadeDailyRewardNumUpdate', tType)
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            freeLeftNum, paidLeftNum = self.leftCrusadDailyUseCoinFreeNum
            LOG_INFO("ICrusade::onCrusadeDailyRewardNumUpdate", freeLeftNum, paidLeftNum)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.CRUSADE, freeLeftNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.CRUSADE, paidLeftNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.crusadeInfo.rewardDailyCount = 0
        self.crusadeInfo.resetUseCoinAddRewardDailyNum()
        self.crusadeInfo = self.crusadeInfo

    @property
    def leftCrusadDailyUseCoinFreeNum(self):
        LOG_INFO("ICrusade::leftCrusadDailyUseCoinFreeNum", self.crusadeInfo.useCoinAddRewardNum)
        if not self.crusadeInfo.useCoinAddRewardNum:
            return 0, 0
        leftFreeNum = 0
        leftPaidNum = 0
        for times in range(self.crusadeInfo.useCoinAddRewardNum, 0, -1): 
            res, beFree = utils.isOriginaCoinCostBeFree(gameconst.RecoveryTicketSubType.CRUSADE, times)
            if not res:
                LOG_ERR("ICrusade::leftCrusadDailyUseCoinFreeNum error", times)
                continue
            if beFree:
                leftFreeNum += 1
            else:
                leftPaidNum += 1
        return leftFreeNum, leftPaidNum

    def updateCrusadeUseCoinTimesTicketInfo(self, time, level):
        self.crusadeCoinTicketData.clear()
        for times in range(self.crusadeInfo.rewardNumCoinDailyLimit, 0, -1): 
            itemId, itemNum, discountType = utils.getCoinCostInfo(self, gameconst.RecoveryTicketSubType.CRUSADE, times, time, level)
            self.crusadeCoinTicketData.append(itemId, itemNum, discountType)
        LOG_INFO("ICrusade::updateCrusadeUseCoinTimesTicketInfo", time, self.crusadeInfo.useCoinAddRewardNum, level, self.crusadeCoinTicketData)
        self.sendCrusadeUseCoinTimesTicketInfo()

    def sendCrusadeUseCoinTimesTicketInfo(self):
        self.client.onUseCoinTimesTicketDatas(gameconst.RecoveryTicketSubType.CRUSADE, self.crusadeCoinTicketData.getClientDatas())

    def tryAddCrusadeUseCoinTimesFreeTicket(self):
        LOG_INFO("ICrusade::tryAddCrusadeUseCoinTimesFreeTicket", self.crusadeInfo.leftDailyRewardNum, self.crusadeInfo.useCoinAddRewardNum)
        if self.crusadeInfo.leftDailyRewardNum > 0:
            LOG_DBG("ICrusade::tryAddCrusadeUseCoinTimesFreeTicket has coin free ticket")
            return
        if self.crusadeInfo.useCoinAddRewardNum <= 0:
            LOG_DBG("ICrusade::tryAddCrusadeUseCoinTimesFreeTicket crusadeInfo.useCoinAddRewardNum <= 0 ")
            return
        itemId, itemNum, discountType = self.crusadeCoinTicketData.getTicketInfo(self.crusadeInfo.useCoinAddRewardNum)
        if not itemId:
            LOG_ERR("ICrusade:tryAddCrusadeUseCoinTimesFreeTicket error", self.crusadeCoinTicketData)
            return
        if itemNum:
            LOG_DBG("ICrusade::tryAddCrusadeUseCoinTimesFreeTicket not free")
            return
        self._useCoinToIncreaseCrusadeRewardNumber(1, {})

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def increaseCrusadeRewardNumber(self, exposed, coinNum, itemNum, isExchange):
        LOG_INFO('increaseCrusadeRewardNumber::', coinNum, itemNum)
        retCoin, coinAddCount = self._useCoinToIncreaseCrusadeRewardNumber(coinNum, {}, needMsg = False, isExchange=isExchange)
        retItem = self._useItemToIncreaseCrusadeRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinAddCount
            if retItem:
                totalNum += itemNum
            if totalNum:
                self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useItemToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        LOG_INFO('useItemToIncreaseCrusadeRewardNumber::', useNum)
        self._useItemToIncreaseCrusadeRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useCoinToIncreaseCrusadeRewardNumber(self, exposed, useNum, isExchange=False):
        LOG_INFO('useCoinToIncreaseCrusadeRewardNumber::', useNum)

        self._useCoinToIncreaseCrusadeRewardNumber(useNum, {}, isExchange=isExchange)

    def _useItemToIncreaseCrusadeRewardNumber(self, itemNum, extra, needMsg = True):
        itemId = int(TDC_CFG.datas['rewardNumItem']['value'])
        LOG_INFO('_useItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra, needMsg)
        if itemNum <= 0:
            return False

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('_useItemToIncreaseCrusadeRewardNumber::check failed', res())
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        detail = gameclass.AwardDetailCls(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseCrusadeRewardNumber(itemId, itemNum, extra, needMsg, opUUID=opUUID)
        return True
    
    def onUseItemToIncreaseCrusadeRewardNumber(self, itemId, itemNum, extra, needMsg = True, opUUID = 0):
        LOG_INFO('onUseItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra)
        self.crusadeInfo.addRewardNumByUseSpecialItem(itemNum)
        self.crusadeInfo = self.crusadeInfo
        # 获得门票埋点：op_uuid 关联扣道具的 opUUID
        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            gameconst.DungeonTicketBuySrc.ITEM_BUY,
            gameconst.DungeonTicketType.ITEM,
            itemNum,
            gameconst.DungeonPlayModeEnum.CRUSADE
        )
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseCrusadeRewardNumber(self, useNum, extra, needMsg = True, isExchange=False):
        LOG_INFO('_useCoinToIncreaseCrusadeRewardNumber::', useNum, extra, needMsg)
        if useNum <= 0:
            return False, 0
        addRewardNum = 0
        freeAddNum = 0
        paidAddNum = 0
        # 一次购买操作全程共用同一 opUUID 与 srcType（埋点 op_uuid 口径）
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        for _ in range(0, useNum):
            if not self.crusadeInfo.isCanAddRewardByCoin(1):
                LOG_ERR('useCoinToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
                break
            
            itemId, itemNum, discountType = self.crusadeCoinTicketData.getTicketInfo(self.crusadeInfo.useCoinAddRewardNum)
            if not itemId:
                break

            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(itemId, itemNum)

            res = self.canDeductWealth(deductWealthVal, allowMoneyCoverBindMoney=isExchange)
            if not res:
                LOG_WARN('_useCoinToIncreaseCrusadeRewardNumber::check failed', res())
                break

            addRewardNum += 1
            if itemNum:
                paidAddNum += 1
            else:
                freeAddNum += 1

            detail = gameclass.AwardDetailCls()
            self.deductWealth(srcType, deductWealthVal, opUUID, detail, allowMoneyCoverBindMoney=isExchange)
            self.crusadeInfo.deductUsedCoinAddRewardNum(1)

        if addRewardNum > 0:
            self.onUseCoinToIncreaseCrusadeRewardNumber(
                useNum,
                addRewardNum,
                extra,
                freeAddNum,
                paidAddNum,
                gameconst.addTicketTimesType.COIN,
                needMsg,
                opUUID=opUUID
            )
        return True, addRewardNum
    
    def onUseCoinToIncreaseCrusadeRewardNumber(self, useNum, addRewardNum, extra, freeAddNum, paidAddNum, attType, needMsg = True, opUUID = 0):
        LOG_INFO('onUseCoinToIncreaseCrusadeRewardNumber::', useNum, addRewardNum, extra, freeAddNum, paidAddNum, attType)
        if freeAddNum:
            if attType == gameconst.addTicketTimesType.RECOVERY:
                self.crusadeInfo.addRewardNumByUseCommonDefault(freeAddNum)
            elif attType == gameconst.addTicketTimesType.COIN:
                self.crusadeInfo.addRewardNumByDefault(freeAddNum)
        if paidAddNum:
            self.crusadeInfo.addRewardNumByUseCoin(paidAddNum)
        self.crusadeInfo = self.crusadeInfo
        # 获得门票埋点：按桶拆分上报，同一操作共用 opUUID
        if attType == gameconst.addTicketTimesType.COIN:
            if freeAddNum:
                LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
                    self.gbID,
                    self.accountEntity.clientDistinctId,
                    opUUID,
                    gameconst.DungeonTicketBuySrc.COIN_BUY,
                    gameconst.DungeonTicketType.NORMAL,
                    freeAddNum,
                    gameconst.DungeonPlayModeEnum.CRUSADE
                )
            if paidAddNum:
                LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
                    self.gbID,
                    self.accountEntity.clientDistinctId,
                    opUUID,
                    gameconst.DungeonTicketBuySrc.COIN_BUY,
                    gameconst.DungeonTicketType.GOLD,
                    paidAddNum,
                    gameconst.DungeonPlayModeEnum.CRUSADE
                )
        elif attType == gameconst.addTicketTimesType.RECOVERY:
            if freeAddNum:
                LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
                    self.gbID,
                    self.accountEntity.clientDistinctId,
                    opUUID,
                    gameconst.DungeonTicketBuySrc.RECOVERY,
                    gameconst.DungeonTicketType.COMMON,
                    freeAddNum,
                    gameconst.DungeonPlayModeEnum.CRUSADE
                )
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(addRewardNum)])
