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

class ICrusade(object):
    def onCrusadeDailyRewardNumUpdate(self, *args):
        INFO_MSG('onCrusadeDailyRewardNumUpdate::')
        dailyRewardNum = self.crusadeInfo.dailyRewardNum
        if self.crusadeInfo.rewardNumber < dailyRewardNum:
            self.crusadeInfo.addRewardNumByDefault(dailyRewardNum - self.crusadeInfo.rewardNumber)
        self.crusadeInfo.rewardDailyCount = 0
        self.crusadeInfo.resetUseCoinAddRewardDailyNum()
        self.crusadeInfo = self.crusadeInfo

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def increaseCrusadeRewardNumber(self, exposed, coinNum, itemNum):
        INFO_MSG('increaseCrusadeRewardNumber::', coinNum, itemNum)
        retCoin = self._useCoinToIncreaseCrusadeRewardNumber(coinNum, {}, needMsg = False)
        retItem = self._useItemToIncreaseCrusadeRewardNumber(itemNum, {}, needMsg = False)
        if retCoin or retItem:
            totalNum = 0
            if retCoin:
                totalNum += coinNum
            if retItem:
                totalNum += itemNum
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(totalNum)])

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useItemToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        INFO_MSG('useItemToIncreaseCrusadeRewardNumber::', useNum)
        self._useItemToIncreaseCrusadeRewardNumber(useNum, {})

    @gamedecorator.checkGameconfigEnable('teamDungeon')
    def useCoinToIncreaseCrusadeRewardNumber(self, exposed, useNum):
        INFO_MSG('useCoinToIncreaseCrusadeRewardNumber::', useNum)
        self._useCoinToIncreaseCrusadeRewardNumber(useNum, {})

    def _useItemToIncreaseCrusadeRewardNumber(self, itemNum, extra, needMsg = True):
        itemId = int(TDC_CFG.datas['rewardNumItem']['value'])
        INFO_MSG('_useItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra, needMsg)
        if itemNum <= 0:
            return False

        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(itemId, itemNum, dataUtils.getItemDefaultBindType())

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useItemToIncreaseCrusadeRewardNumber::check failed')
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        detail = gameclass.AwardDetail(itemId=itemId, itemNum=itemNum)
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseItemToIncreaseCrusadeRewardNumber(itemId, itemNum, extra, needMsg)
        return True
    
    def onUseItemToIncreaseCrusadeRewardNumber(self, itemId, itemNum, extra, needMsg = True):
        INFO_MSG('onUseItemToIncreaseCrusadeRewardNumber::', itemId, itemNum, extra)
        self.crusadeInfo.addRewardNumByUseSpecialItem(itemNum)
        self.crusadeInfo = self.crusadeInfo
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(itemNum)])

    def _useCoinToIncreaseCrusadeRewardNumber(self, useNum, extra, needMsg = True):
        INFO_MSG('_useCoinToIncreaseCrusadeRewardNumber::', useNum, extra, needMsg)
        if useNum <= 0:
            return False
        
        if not self.crusadeInfo.isCanAddRewardByCoin(useNum):
            ERROR_MSG('_useCoinToIncreaseCrusadeRewardNumber:: rewardNumber not enough')
            return False
        
        rewardNumCoin = int(TDC_CFG.datas['rewardNumCoin']['value'])
        deductWealthVal = dropAward.DeductWealthVal()
        deductWealthVal.addWealthByItemId(gameconst.ItemId.MONEY, rewardNumCoin * useNum)

        if not self.canDeductWealth(deductWealthVal):
            ERROR_MSG('_useCoinToIncreaseCrusadeRewardNumber::check failed')
            return False

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_TEAMDUN_ADD_REWARD
        detail = gameclass.AwardDetail()
        self.deductWealth(srcType, deductWealthVal, opUUID, detail)

        self.onUseCoinToIncreaseCrusadeRewardNumber(useNum, extra, needMsg)
        return True
    
    def onUseCoinToIncreaseCrusadeRewardNumber(self, useNum, extra, needMsg = True):
        INFO_MSG('onUseCoinToIncreaseCrusadeRewardNumber::', useNum, extra)
        self.crusadeInfo.addRewardNumByUseCoin(useNum)
        self.crusadeInfo = self.crusadeInfo
        if needMsg:
            self.onMessagePre(int(TDC_CFG.datas["useShanglingdingMsg"]["value"]), [str(useNum)])

    def onEnterCrusadeDungeon(self, spaceNo, dungeonNo, spaceMgrBox, extra):
        crusadeInfo = self.crusadeInfo
        crusadeInfo.deductRewardNum()
        self.crusadeInfo = crusadeInfo
        self.onEnterDungeon(spaceNo, spaceMgrBox, extra)
        self.activityComplete(TDC_CFG.datas['teamDunChallengeActID']['value'])

        LogTrackingMgr.LogTrackingMgr.Dungeon_Ticket_Consume(
            extra.get('teamUUID'),
            gameconst.DungeonPlayModeEnum.CRUSADE,
            dungeonNo,
            crusadeInfo.getUsedTicketType(),
            extra.get('joinType'),
            extra.get('totalNum'),
            self.gbID,
            self.getTotalScore(),
            self.getRoleCacheAttr('level')
        )
        
        INFO_MSG('in onEnterCrusadeDungeon::', spaceNo, dungeonNo, spaceMgrBox, extra)
