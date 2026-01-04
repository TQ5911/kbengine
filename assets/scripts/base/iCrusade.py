# coding: utf-8
from KBEDebug import *
import KBEngine

import gameconst
import gameengine
import utils
import formula
import dataUtils
import dungeonPlayMode
import dropAward
import gameclass
import gametlog
import gamedecorator

import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import teamDunChallenge_config as TDC_CFG
import gameconst

class ICrusade(object):
    def onCrusadeDailyRewardNumUpdate(self, *args):
        DEBUG_MSG('onCrusadeDailyRewardNumUpdate::')
        dailyRewardNum = self.crusadeInfo.dailyRewardNum
        if self.crusadeInfo.rewardNumber < dailyRewardNum:
            self.crusadeInfo.addRewardNumByDefault(dailyRewardNum - self.crusadeInfo.rewardNumber)
        self.crusadeInfo.rewardDailyCount = 0
        self.crusadeInfo.resetUseCoinAddRewardDailyNum()
        self.crusadeInfo = self.crusadeInfo

    def onCrusadeWeeklyAddRewardItemNumUpdate(self, *args):
        DEBUG_MSG('onCrusadeWeeklyAddRewardItemNumUpdate::')
        self.crusadeInfo.resetUseItemAddRewardWeeklyNum()
        self.crusadeInfo = self.crusadeInfo

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useItemToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        DEBUG_MSG('useItemToIncreaseCrusadeRewardNumber::', useNum)
        if useNum <= 0:
            ERROR_MSG('useItemToIncreaseCrusadeRewardNumber:: invalid useNum', useNum)

            return
        itemId = int(TDC_CFG.datas['rewardNumItem']['value'])
        if not self.crusadeInfo.isCanAddRewardByItem(useNum):
            ERROR_MSG('useItemToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
            return

        self._useItemToIncreaseCrusadeRewardNumber(itemId, useNum, {})

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useCoinToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        DEBUG_MSG('useCoinToIncreaseCrusadeRewardNumber::', useNum)
        if useNum <= 0:
            ERROR_MSG('useCoinToIncreaseCrusadeRewardNumber:: invalid useNum', useNum)

            return
        if not self.crusadeInfo.isCanAddRewardByCoin(useNum):
            ERROR_MSG('useCoinToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
            return

        self._useCoinToIncreaseCrusadeRewardNumber(useNum, {})

    def _useItemToIncreaseCrusadeRewardNumber(self, itemId, itemNum, extra):
        DEBUG_MSG('_useItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra)

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useItemToIncreaseCrusadeRewardNumber::check failed')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        detail = gameclass.AwardDetail(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseCrusadeRewardNumber(itemId, itemNum, extra)

    def onUseItemToIncreaseCrusadeRewardNumber(self, itemId, itemNum, extra):
        DEBUG_MSG('onUseItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra)
        self.crusadeInfo.addRewardNumByUseSpecialItem(itemNum)
        self.crusadeInfo = self.crusadeInfo
        self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]),
                              [str(itemNum), str(self.crusadeInfo.useItemAddRewardNumber)])

    def _useCoinToIncreaseCrusadeRewardNumber(self, useNum, extra):
        DEBUG_MSG('_useCoinToIncreaseCrusadeRewardNumber::', useNum)

        rewardNumCoin = int(TDC_CFG.datas['rewardNumCoin']['value'])
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, rewardNumCoin * useNum)

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useCoinToIncreaseCrusadeRewardNumber::check failed')
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        detail = gameclass.AwardDetail()
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseCoinToIncreaseCrusadeRewardNumber(useNum, extra)

    def onUseCoinToIncreaseCrusadeRewardNumber(self, useNum, extra):
        DEBUG_MSG('onUseCoinToIncreaseCrusadeRewardNumber::', useNum, extra)
        self.crusadeInfo.addRewardNumByUseCoin(useNum)
        self.crusadeInfo = self.crusadeInfo

    def onEnterCrusadeDungeon(self, spaceNo, dungeonNo, spaceMgrBox, extra):
        crusadeInfo = self.crusadeInfo
        crusadeInfo.deductRewardNum()
        self.crusadeInfo = crusadeInfo
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(TDC_CFG.datas['teamDunChallengeActID']['value'])
        INFO_MSG('in onEnterCrusadeDungeon::', spaceNo, dungeonNo, spaceMgrBox, extra)
