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

class IChief(object):
    def onChiefDailyRewardNumUpdate(self, *args):
        INFO_MSG('onChiefDailyRewardNumUpdate::')
        dailyRewardNum = self.chiefInfo.dailyRewardNum
        if self.chiefInfo.rewardNumber < dailyRewardNum:
            self.chiefInfo.addRewardNumByDefault(dailyRewardNum - self.chiefInfo.rewardNumber)
        self.chiefInfo.rewardDailyCount = 0
        self.chiefInfo.resetUseCoinAddRewardDailyNum()
        self.chiefInfo = self.chiefInfo

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def increaseChiefRewardNumber(self, exposed, coinNum, itemNum):
        INFO_MSG('increaseChiefRewardNumber::', coinNum, itemNum)
        retCoin = self._useCoinToIncreaseChiefRewardNumber(coinNum, {}, needMsg = False)
        retItem = self._useItemToIncreaseChiefRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinNum
            if retItem:
                totalNum += itemNum
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useItemToIncreaseChiefRewardNumber(self, exposed, useNum):
        INFO_MSG('useItemToIncreaseChiefRewardNumber::', useNum)
        
        self._useItemToIncreaseChiefRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useCoinToIncreaseChiefRewardNumber(self, exposed, useNum):
        INFO_MSG('useCoinToIncreaseChiefRewardNumber::', useNum)

        self._useCoinToIncreaseChiefRewardNumber(useNum, {})

    def _useItemToIncreaseChiefRewardNumber(self, itemNum, extra, needMsg = True):
        itemId = int(RBC_CFG.datas['rewardNumItem']['value'])
        INFO_MSG('_useItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra)

        if itemNum <= 0:
            return False
        
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useItemToIncreaseChiefRewardNumber::check failed')
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        detail = gameclass.AwardDetail(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseChiefRewardNumber(itemId, itemNum, extra, needMsg)
        return True
    
    def onUseItemToIncreaseChiefRewardNumber(self, itemId, itemNum, extra, needMsg = True):
        INFO_MSG('onUseItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra, needMsg)
        self.chiefInfo.addRewardNumByUseSpecialItem(itemNum)
        self.chiefInfo = self.chiefInfo
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseChiefRewardNumber(self, useNum, extra, needMsg = True):
        INFO_MSG('_useCoinToIncreaseChiefRewardNumber::', useNum)
        if useNum <= 0:
            return False
        
        if not self.chiefInfo.isCanAddRewardByCoin(useNum):
            ERROR_MSG('useCoinToIncreaseChiefRewardNumber:: rewardNumber not enough')
            return False
        
        rewardNumCoin = int(RBC_CFG.datas['rewardNumCoin']['value'])
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, rewardNumCoin * useNum)

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useCoinToIncreaseChiefRewardNumber::check failed')
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        detail = gameclass.AwardDetail()
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseCoinToIncreaseChiefRewardNumber(useNum, extra, needMsg)
        return True
    
    def onUseCoinToIncreaseChiefRewardNumber(self, useNum, extra, needMsg):
        INFO_MSG('onUseCoinToIncreaseChiefRewardNumber::', useNum, extra, needMsg)
        self.chiefInfo.addRewardNumByUseCoin(useNum)
        self.chiefInfo = self.chiefInfo
        if needMsg:
            self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]), [str(useNum)])

    def onEnterChiefDungeon(self, spaceNo, dungeonNo, spaceMgrBox, extra):
        chiefInfo = self.chiefInfo
        chiefInfo.deductRewardNum()
        self.chiefInfo = chiefInfo
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(RBC_CFG.datas['raidBossChallengeActID']['value'])

        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Consume(
            extra.get('raidId'),
            gameconst.DungeonPlayModeEnum.CHIEF,
            dungeonNo,
            chiefInfo.getUsedTicketType(),
            extra.get('joinType'),
            extra.get('totalNum'),
            self.gbID,
            self.getTotalScore(),
            self.getRoleCacheAttr('level')
        )

        INFO_MSG('in onEnterChiefDungeon::', spaceNo, dungeonNo, spaceMgrBox, extra)
