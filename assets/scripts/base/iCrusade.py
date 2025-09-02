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

import message_Message_def as MMD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import teamDunChallenge_config as TDC_CFG
import gameconst

class ICrusade(object):
    def onCrusadeDailyRewardNumUpdate(self, *args):
        DEBUG_MSG('onCrusadeDailyRewardNumUpdate::')
        dailyRewardNum = int(TDC_CFG.datas['dailyRewardNum']['value'])
        if self.crusadeInfo.rewardNumber < dailyRewardNum:
            self.crusadeInfo.addRewardNum(dailyRewardNum - self.crusadeInfo.rewardNumber)
        self.crusadeInfo.rewardDailyCount = 0
        self.crusadeInfo.useCoinAddRewardNum = int(TDC_CFG.datas['rewardNumCoinDailyLimit']['value'])
        self.crusadeInfo = self.crusadeInfo

    def onCrusadeWeeklyAddRewardItemNumUpdate(self, *args):
        DEBUG_MSG('onCrusadeWeeklyAddRewardItemNumUpdate::')
        self.crusadeInfo.resetUseItemAddRewardNumber()
        self.crusadeInfo = self.crusadeInfo

    def useItemToIncreaseCrusadeRewardNumber(self, useNum):
        DEBUG_MSG('useItemToIncreaseCrusadeRewardNumber::', useNum)
        if useNum <= 0:
            ERROR_MSG('useItemToIncreaseCrusadeRewardNumber:: invalid useNum', useNum)

            return
        itemId = int(TDC_CFG.datas['rewardNumItem']['value'])
        if not self.crusadeInfo.isCanAddRewardByItem(useNum):
            ERROR_MSG('useItemToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
            return

        self._useItemToIncreaseCrusadeRewardNumber(itemId, useNum, {})

    def useCoinToIncreaseCrusadeRewardNumber(self, useNum):
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
        detail = gameclass.AwardDetail
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseCoinToIncreaseCrusadeRewardNumber(useNum, extra)

    def onUseCoinToIncreaseCrusadeRewardNumber(self, useNum, extra):
        DEBUG_MSG('onUseCoinToIncreaseCrusadeRewardNumber::', useNum, extra)
        self.crusadeInfo.addRewardNumByUseCoin(useNum)
        self.crusadeInfo = self.crusadeInfo

    def onEnterCrusadeDungeon(self, spaceNo, spaceMgrBox, extra):
        DEBUG_MSG('in onEnterCrusadeDungeon::', spaceNo, spaceMgrBox, extra)
        crusadeInfo = self.crusadeInfo
        crusadeInfo.addRewardNum(-1)
        self.crusadeInfo = crusadeInfo
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(TDC_CFG.datas['teamDunChallengeActID']['value'])

    def setCrusadeDungeonAutoConfirmConfig(self, storyLevel):
        self.setPersistentMiscProp(gameconst.AvatarProps.CrusadeDunAutoConfirmConfig, storyLevel)
        self.client.onSetCrusadeDungeonAutoConfirmConfig(storyLevel)

    def getCrusadeDungeonAutoConfirmConfig(self):
        return self.getPersistentMiscProp(gameconst.AvatarProps.CrusadeDunAutoConfirmConfig, 1)

    def sendCrusadeDungeonAutoConfirmConfig(self):
        storyLevel = self.getCrusadeDungeonAutoConfirmConfig()
        self.client.onSetCrusadeDungeonAutoConfirmConfig(storyLevel)
