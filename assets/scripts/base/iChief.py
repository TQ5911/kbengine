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

    def onChiefWeeklyAddRewardItemNumUpdate(self, *args):
        INFO_MSG('onChiefWeeklyAddRewardItemNumUpdate::')
        self.chiefInfo.resetUseItemAddRewardWeeklyNum()
        self.chiefInfo = self.chiefInfo

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useItemToIncreaseChiefRewardNumber(self, exposed, useNum):
        INFO_MSG('useItemToIncreaseChiefRewardNumber::', useNum)
        if useNum <= 0:
            ERROR_MSG('useItemToIncreaseChiefRewardNumber:: invalid useNum', useNum)

            return
        itemId = int(RBC_CFG.datas['rewardNumItem']['value'])
        if not self.chiefInfo.isCanAddRewardByItem(useNum):
            ERROR_MSG('useItemToIncreaseChiefRewardNumber:: rewardNumber not enough')
            return

        self._useItemToIncreaseChiefRewardNumber(itemId, useNum, {})

    @gamedecorator.checkGameconfigEnable('raidDungeon')
    def useCoinToIncreaseChiefRewardNumber(self, exposed, useNum):
        INFO_MSG('useCoinToIncreaseChiefRewardNumber::', useNum)
        if useNum <= 0:
            ERROR_MSG('useCoinToIncreaseChiefRewardNumber:: invalid useNum', useNum)

            return
        if not self.chiefInfo.isCanAddRewardByCoin(useNum):
            ERROR_MSG('useCoinToIncreaseChiefRewardNumber:: rewardNumber not enough')
            return

        self._useCoinToIncreaseChiefRewardNumber(useNum, {})

    def _useItemToIncreaseChiefRewardNumber(self, itemId, itemNum, extra):
        INFO_MSG('_useItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra)

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useItemToIncreaseChiefRewardNumber::check failed')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        detail = gameclass.AwardDetail(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseChiefRewardNumber(itemId, itemNum, extra)

    def onUseItemToIncreaseChiefRewardNumber(self, itemId, itemNum, extra):
        INFO_MSG('onUseItemToIncreaseChiefRewardNumber::', itemId, itemNum, extra)
        self.chiefInfo.addRewardNumByUseSpecialItem(itemNum)
        self.chiefInfo = self.chiefInfo
        self.onMessagePre(int(RBC_CFG.datas["useShanglingdingMsg"]["value"]),
                              [str(itemNum), str(self.chiefInfo.useItemAddRewardNumber)])

    def _useCoinToIncreaseChiefRewardNumber(self, useNum, extra):
        INFO_MSG('_useCoinToIncreaseChiefRewardNumber::', useNum)

        rewardNumCoin = int(RBC_CFG.datas['rewardNumCoin']['value'])
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, rewardNumCoin * useNum)

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useCoinToIncreaseChiefRewardNumber::check failed')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_CRUSADE_ADD_REWARD
        detail = gameclass.AwardDetail()
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseCoinToIncreaseChiefRewardNumber(useNum, extra)

    def onUseCoinToIncreaseChiefRewardNumber(self, useNum, extra):
        INFO_MSG('onUseCoinToIncreaseChiefRewardNumber::', useNum, extra)
        self.chiefInfo.addRewardNumByUseCoin(useNum)
        self.chiefInfo = self.chiefInfo

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
