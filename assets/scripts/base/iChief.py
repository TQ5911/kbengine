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
import raidBossChallenge_config as RBC_CFG
import actionContext
import utils

class IChief(object):
    def onChiefDailyRewardNumUpdate(self, *args):
        tType = args[0] if len(args) >= 1 else 0
        LOG_INFO('IChief::onChiefDailyRewardNumUpdate', tType)
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            freeLeftNum, paidLeftNum = self.leftChiefDailyUseCoinFreeNum
            LOG_INFO("IChief::onChiefDailyRewardNumUpdate", freeLeftNum, paidLeftNum)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.CHIEF, freeLeftNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.CHIEF, paidLeftNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.chiefInfo.rewardDailyCount = 0
        self.chiefInfo.resetUseCoinAddRewardDailyNum()
        self.chiefInfo = self.chiefInfo

    @property
    def leftChiefDailyUseCoinFreeNum(self):
        LOG_INFO("IChief::leftChiefDailyUseCoinFreeNum", self.chiefInfo.useCoinAddRewardNum)
        if not self.chiefInfo.useCoinAddRewardNum:
            return 0, 0
        leftFreeNum = 0
        leftPaidNum = 0
        for times in range(self.chiefInfo.useCoinAddRewardNum, 0, -1): 
            res, beFree = utils.isOriginaCoinCostBeFree(gameconst.RecoveryTicketSubType.CHIEF, times)
            if not res:
                LOG_ERR("IChief::leftChiefDailyUseCoinFreeNum error", times)
                continue
            if beFree:
                leftFreeNum += 1
            else:
                leftPaidNum += 1
        return leftFreeNum, leftPaidNum

    def updateChiefUseCoinTimesTicketInfo(self, time, level):
        self.chiefCoinTicketData.clear()
        for times in range(self.chiefInfo.rewardNumCoinDailyLimit, 0, -1): 
            itemId, itemNum, discountType = utils.getCoinCostInfo(self, gameconst.RecoveryTicketSubType.CHIEF, times, time, level)
            self.chiefCoinTicketData.append(itemId, itemNum, discountType)
        LOG_INFO("IChief::updateChiefUseCoinTimesTicketInfo", time, self.chiefInfo.useCoinAddRewardNum, level, self.chiefCoinTicketData)
        self.sendChiefUseCoinTimesTicketInfo()

    def sendChiefUseCoinTimesTicketInfo(self):
        self.client.onUseCoinTimesTicketDatas(gameconst.RecoveryTicketSubType.CHIEF, self.chiefCoinTicketData.getClientDatas())

    def tryAddChiefUseCoinTimesFreeTicket(self):
        LOG_INFO("IChief::tryAddChiefUseCoinTimesFreeTicket", self.chiefInfo.leftDailyRewardNum, self.chiefInfo.useCoinAddRewardNum)
        if self.chiefInfo.leftDailyRewardNum > 0:
            LOG_DBG("IChief::tryAddChiefUseCoinTimesFreeTicket has coin free ticket")
            return
        if self.chiefInfo.useCoinAddRewardNum <= 0:
            LOG_DBG("IChief::tryAddChiefUseCoinTimesFreeTicket chiefInfo.useCoinAddRewardNum <= 0 ")
            return
        itemId, itemNum, discountType = self.chiefCoinTicketData.getTicketInfo(self.chiefInfo.useCoinAddRewardNum)
        if not itemId:
            LOG_ERR("IChief:tryAddChiefUseCoinTimesFreeTicket error", self.chiefCoinTicketData)
            return
        if itemNum:
            LOG_DBG("IChief::tryAddChiefUseCoinTimesFreeTicket not free")
            return
        self._useCoinToIncreaseChiefRewardNumber(1, {})

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def increaseChiefRewardNumber(self, exposed, coinNum, itemNum, isExchange):
        LOG_INFO('increaseChiefRewardNumber::', coinNum, itemNum)
        retCoin, coinAddCount = self._useCoinToIncreaseChiefRewardNumber(coinNum, {}, needMsg = False, isExchange=isExchange)
        retItem = self._useItemToIncreaseChiefRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinAddCount
            if retItem:
                totalNum += itemNum
            if totalNum:
                self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useItemToIncreaseChiefRewardNumber(self, exposed, useNum):
        LOG_INFO('useItemToIncreaseChiefRewardNumber::', useNum)
        
        self._useItemToIncreaseChiefRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useCoinToIncreaseChiefRewardNumber(self, exposed, useNum, isExchange=False):
        LOG_INFO('useCoinToIncreaseChiefRewardNumber::', useNum)

        self._useCoinToIncreaseChiefRewardNumber(useNum, {}, isExchange=isExchange)

    def _useItemToIncreaseChiefRewardNumber(self, itemNum, extra, needMsg = True):
        itemId = int(RBC_CFG.datas['rewardNumItem']['value'])
        LOG_INFO('_useItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra)

        if itemNum <= 0:
            return False
        
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        res = self.canDeductWealth(deductWealthVal)
        if not res:
            LOG_WARN('_useItemToIncreaseChiefRewardNumber::check failed', res())
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        detail = gameclass.AwardDetailCls(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseChiefRewardNumber(itemId, itemNum, extra, needMsg, opUUID=opUUID)
        return True
    
    def onUseItemToIncreaseChiefRewardNumber(self, itemId, itemNum, extra, needMsg = True, opUUID = 0):
        LOG_INFO('onUseItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra, needMsg)
        self.chiefInfo.addRewardNumByUseSpecialItem(itemNum)
        self.chiefInfo = self.chiefInfo
        # 获得门票埋点：op_uuid 关联扣道具的 opUUID
        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
            self.gbID,
            self.accountEntity.clientDistinctId,
            opUUID,
            gameconst.DungeonTicketBuySrc.ITEM_BUY,
            gameconst.DungeonTicketType.ITEM,
            itemNum,
            gameconst.DungeonPlayModeEnum.CHIEF
        )
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseChiefRewardNumber(self, useNum, extra, needMsg = True, isExchange=False):
        LOG_INFO('_useCoinToIncreaseChiefRewardNumber::', useNum)
        if useNum <= 0:
            return False, 0
        
        addRewardNum = 0
        freeAddNum = 0
        paidAddNum = 0
        # 一次购买操作全程共用同一 opUUID 与 srcType（埋点 op_uuid 口径）
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        for _ in range(0, useNum):
            if not self.chiefInfo.isCanAddRewardByCoin(1):
                LOG_ERR('useCoinToIncreaseChiefRewardNumber:: rewardNumber not enough')
                break
            
            itemId, itemNum, discountType = self.chiefCoinTicketData.getTicketInfo(self.chiefInfo.useCoinAddRewardNum)
            if not itemId:
                break

            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(itemId, itemNum)

            res = self.canDeductWealth(deductWealthVal, allowMoneyCoverBindMoney=isExchange)
            if not res:
                LOG_WARN('_useCoinToIncreaseChiefRewardNumber::check failed', res())
                break

            addRewardNum += 1
            if itemNum:
                paidAddNum += 1
            else:
                freeAddNum += 1

            detail = gameclass.AwardDetailCls()
            self.deductWealth(srcType, deductWealthVal, opUUID, detail, allowMoneyCoverBindMoney=isExchange)
            self.chiefInfo.deductUsedCoinAddRewardNum(1)

        if addRewardNum > 0:
            self.onUseCoinToIncreaseChiefRewardNumber(
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
    
    def onUseCoinToIncreaseChiefRewardNumber(self, useNum, addRewardNum, extra, freeAddNum, paidAddNum, attType, needMsg, opUUID = 0):
        LOG_INFO('onUseCoinToIncreaseChiefRewardNumber::', useNum, addRewardNum, extra, freeAddNum, paidAddNum, attType, needMsg)
        if freeAddNum:
            if attType == gameconst.addTicketTimesType.RECOVERY:
                self.chiefInfo.addRewardNumByUseCommonDefault(freeAddNum)
            elif attType == gameconst.addTicketTimesType.COIN:
                self.chiefInfo.addRewardNumByDefault(freeAddNum)
        if paidAddNum:
            self.chiefInfo.addRewardNumByUseCoin(paidAddNum)
        self.chiefInfo = self.chiefInfo
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
                    gameconst.DungeonPlayModeEnum.CHIEF
                )
            if paidAddNum:
                LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Buy(
                    self.gbID,
                    self.accountEntity.clientDistinctId,
                    opUUID,
                    gameconst.DungeonTicketBuySrc.COIN_BUY,
                    gameconst.DungeonTicketType.GOLD,
                    paidAddNum,
                    gameconst.DungeonPlayModeEnum.CHIEF
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
                    gameconst.DungeonPlayModeEnum.CHIEF
                )
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(addRewardNum)])
