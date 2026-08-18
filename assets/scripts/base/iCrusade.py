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

class ICrusade(object):
    def onCrusadeDailyRewardNumUpdate(self, *args):
        LOG_INFO('onCrusadeDailyRewardNumUpdate::')
        tType = args[0] if len(args) >= 1 else 0
        if tType == gameconst.CycleEventTriggerType.UPDATE:
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.FREE_TICKET, gameconst.RecoveryTicketSubType.CRUSADE, self.crusadeInfo.leftDailyRewardNum, gameconst.FreeTicketUpdateType.UPDATE)
            self.updateFreeTicketInfo(gameconst.RecoveryTicketType.PAID_TICKET, gameconst.RecoveryTicketSubType.CRUSADE, self.crusadeInfo.useCoinAddRewardNum, gameconst.FreeTicketUpdateType.UPDATE)

        self.crusadeInfo.dailyResetRewardNum()
        self.crusadeInfo.rewardDailyCount = 0
        self.crusadeInfo.resetUseCoinAddRewardDailyNum()
        self.crusadeInfo = self.crusadeInfo

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def increaseCrusadeRewardNumber(self, exposed, coinNum, itemNum):
        LOG_INFO('increaseCrusadeRewardNumber::', coinNum, itemNum)
        retCoin, coinAddCount = self._useCoinToIncreaseCrusadeRewardNumber(coinNum, {}, needMsg = False)
        retItem = self._useItemToIncreaseCrusadeRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinAddCount
            if retItem:
                totalNum += itemNum
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useItemToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        LOG_INFO('useItemToIncreaseCrusadeRewardNumber::', useNum)
        self._useItemToIncreaseCrusadeRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useCoinToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        LOG_INFO('useCoinToIncreaseCrusadeRewardNumber::', useNum)
        self._useCoinToIncreaseCrusadeRewardNumber(useNum, {})

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

        self.onUseItemToIncreaseCrusadeRewardNumber(itemId, itemNum, extra, needMsg)
        return True
    
    def onUseItemToIncreaseCrusadeRewardNumber(self, itemId, itemNum, extra, needMsg = True):
        LOG_INFO('onUseItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra)
        self.crusadeInfo.addRewardNumByUseSpecialItem(itemNum)
        self.crusadeInfo = self.crusadeInfo
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseCrusadeRewardNumber(self, useNum, extra, needMsg = True):
        LOG_INFO('_useCoinToIncreaseCrusadeRewardNumber::', useNum, extra, needMsg)
        if useNum <= 0:
            return False, 0
        addRewardNum = 0
        for _ in range(0, useNum):
            isFirst = self.crusadeInfo.isFirstAddRewardNum()
            idx = 0
            if not isFirst:
                idx = 1
            cost = TDC_CFG.datas["rewardNumCoinCost"]["value"][idx]

            addRewardNum += cost[0]
            itemId = cost[1]
            itemNum = cost[2]

            if not self.crusadeInfo.isCanAddRewardByCoin(1):
                LOG_ERR('_useCoinToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
                return False, 0
            
            deductWealthVal = dropAward.DeductWealthVal()
            deductWealthVal.addWealthByItemId(itemId, itemNum)

            res = self.canDeductWealth(deductWealthVal)
            if not res:
                LOG_WARN('_useCoinToIncreaseCrusadeRewardNumber::check failed', res())
                return False, 0

            opUUID = KBEngine.genUUID64()
            srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
            detail = gameclass.AwardDetailCls()
            self.deductWealth(srcType, deductWealthVal, opUUID, detail)
            self.crusadeInfo.deductUsedCoinAddRewardNum(1)

        if addRewardNum > 0:
            self.onUseCoinToIncreaseCrusadeRewardNumber(useNum, addRewardNum, extra, needMsg)
        return True, addRewardNum
    
    def onUseCoinToIncreaseCrusadeRewardNumber(self, useNum, addRewardNum, extra, needMsg = True):
        LOG_INFO('onUseCoinToIncreaseCrusadeRewardNumber::', useNum, addRewardNum, extra)
        self.crusadeInfo.addRewardNumByUseCoin(addRewardNum)
        self.crusadeInfo = self.crusadeInfo
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(addRewardNum)])

    def onEnterCrusadeDungeon(self, spaceUUID, spaceNo, dungeonNo, spaceMgrBox, extra):
        LOG_INFO('onEnterCrusadeDungeon::', spaceUUID, spaceNo, dungeonNo, spaceMgrBox, extra)
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(TDC_CFG.datas['teamDunChallengeActID']['value'])

        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Consume(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            extra.get('teamUUID'),
            gameconst.DungeonPlayModeEnum.CRUSADE,
            dungeonNo,
            spaceNo, 
            spaceUUID,
            self.crusadeInfo.getUsedTicketType(),
            extra.get('joinType'),
            extra.get('totalNum'),
            self.gbID,
            self.getTotalScore(),
            self.getRoleCacheAttr('level')
        )
        
        LogTrackingMgr.LogTrackingMgr.Dungeon_Entrance(
                self.gbID,
                self.accountEntity.clientDistinctId,
                extra.get('teamUUID'),
                gameconst.DungeonPlayModeEnum.CRUSADE,
                dungeonNo,
                spaceUUID,
                spaceNo,
                self.gbID,
                self.crusadeInfo.getUsedTicketType(),
                extra.get('joinType'),
                self.getTotalScore(),
                self.getRoleCacheAttr('level'),
                self.getRoleCacheAttr('name'),
            )
        LOG_INFO('in onEnterCrusadeDungeon::', spaceNo, dungeonNo, spaceMgrBox, extra)
