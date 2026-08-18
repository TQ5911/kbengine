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

class IChief(object):
    def onChiefDailyRewardNumUpdate(self, *args):
        LOG_INFO('onChiefDailyRewardNumUpdate::')
        tType = args[0] if len(args) >= 1 else 0
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.CHIEF, self.chiefInfo.leftDailyRewardNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.CHIEF, self.chiefInfo.useCoinAddRewardNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.chiefInfo.dailyResetRewardNum()
        self.chiefInfo.rewardDailyCount = 0
        self.chiefInfo.resetUseCoinAddRewardDailyNum()
        self.chiefInfo = self.chiefInfo

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def increaseChiefRewardNumber(self, exposed, coinNum, itemNum):
        LOG_INFO('increaseChiefRewardNumber::', coinNum, itemNum)
        retCoin, coinAddCount = self._useCoinToIncreaseChiefRewardNumber(coinNum, {}, needMsg = False)
        retItem = self._useItemToIncreaseChiefRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinAddCount
            if retItem:
                totalNum += itemNum
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useItemToIncreaseChiefRewardNumber(self, exposed, useNum):
        LOG_INFO('useItemToIncreaseChiefRewardNumber::', useNum)
        
        self._useItemToIncreaseChiefRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useCoinToIncreaseChiefRewardNumber(self, exposed, useNum):
        LOG_INFO('useCoinToIncreaseChiefRewardNumber::', useNum)

        self._useCoinToIncreaseChiefRewardNumber(useNum, {})

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

        self.onUseItemToIncreaseChiefRewardNumber(itemId, itemNum, extra, needMsg)
        return True
    
    def onUseItemToIncreaseChiefRewardNumber(self, itemId, itemNum, extra, needMsg = True):
        LOG_INFO('onUseItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra, needMsg)
        self.chiefInfo.addRewardNumByUseSpecialItem(itemNum)
        self.chiefInfo = self.chiefInfo
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseChiefRewardNumber(self, useNum, extra, needMsg = True):
        LOG_INFO('_useCoinToIncreaseChiefRewardNumber::', useNum)
        if useNum <= 0:
            return False, 0
        
        addRewardNum = 0
        for _ in range(0, useNum):
            isFirst = self.chiefInfo.isFirstAddRewardNum()
            idx = 0
            if not isFirst:
                idx = 1
            cost = RBC_CFG.datas["rewardNumCoinCost"]["value"][idx]

            addRewardNum += cost[0]
            itemId = cost[1]
            itemNum = cost[2]
            
            if not self.chiefInfo.isCanAddRewardByCoin(1):
                LOG_ERR('useCoinToIncreaseChiefRewardNumber:: rewardNumber not enough')
                return False, 0
            
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(itemId, itemNum)

            res = self.canDeductWealth(deductWealthVal)
            if not res:
                LOG_WARN('_useCoinToIncreaseChiefRewardNumber::check failed', res())
                return False, 0

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
            detail = gameclass.AwardDetailCls()
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            self.chiefInfo.deductUsedCoinAddRewardNum(1)

        if addRewardNum > 0:
            self.onUseCoinToIncreaseChiefRewardNumber(useNum, addRewardNum, extra, needMsg)
        return True, addRewardNum
    
    def onUseCoinToIncreaseChiefRewardNumber(self, useNum, addRewardNum, extra, needMsg):
        LOG_INFO('onUseCoinToIncreaseChiefRewardNumber::', useNum, addRewardNum, extra, needMsg)
        self.chiefInfo.addRewardNumByUseCoin(addRewardNum)
        self.chiefInfo = self.chiefInfo
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(addRewardNum)])

    def onEnterChiefDungeon(self, spaceUUID, spaceNo, dungeonNo, spaceMgrBox, extra):
        LOG_INFO('onEnterChiefDungeon::', spaceUUID, spaceNo, dungeonNo, spaceMgrBox, extra)
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(RBC_CFG.datas['raidBossChallengeActID']['value'])

        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Consume(
            self.gbID,
            self.accountEntity.clientDistinctId,
            extra.get('raidId'),
            gameconst.DungeonPlayModeEnum.CHIEF,
            dungeonNo,
            spaceNo, 
            spaceUUID,
            self.chiefInfo.getUsedTicketType(),
            extra.get('joinType'),
            extra.get('totalNum'),
            self.gbID,
            self.getTotalScore(),
            self.getRoleCacheAttr('level')
        )

        LogTrackingMgr.LogTrackingMgr.Dungeon_Entrance(
                self.gbID,
                self.accountEntity.clientDistinctId,
                extra.get('raidId'),
                gameconst.DungeonPlayModeEnum.CHIEF,
                dungeonNo,
                spaceUUID,
                spaceNo,
                self.gbID,
                self.chiefInfo.getUsedTicketType(),
                extra.get('joinType'),
                self.getTotalScore(),
                self.getRoleCacheAttr('level'),
                self.getRoleCacheAttr('name'),
            )
        
        LOG_INFO('in onEnterChiefDungeon::', spaceNo, dungeonNo, spaceMgrBox, extra)
