# coding: utf-8

from KBEDebug import *

import KBEngine
import utils
import buyCredit_buyCreditConst as BCBCCD
import buyCredit_buyCredit as BCBCD
import time
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import gameclass

class IMonthCard(object):
    def __init__(self):
        pass

    def isMonthCardExpired(self):
        return self.monthCardExpireTime < utils.getNow()
    
    def addMonthCardByItem(self, monthCardId, opUUID, ctx):
        seconds = BCBCCD.datas['durationHours']['value'] * 3600
        if not self.checkCanAddMonthCard():
            self.cell.onPendingUseItem(ctx.pendingOpId, gameconst.UseItem.FALSE)
            self.onMessagePre(BCBCCD.datas["durationHoursLimitMsg"]["value"], [])
            return
        self.doAddMonthCard(seconds, monthCardId)
        self.cell.onPendingUseItem(ctx.pendingOpId, gameconst.UseItem.TRUE)

    def checkCanAddMonthCard(self):
        durationHoursLimit = BCBCCD.datas['durationHoursLimit']['value']
        maxTime = utils.getNow() + 3600 * durationHoursLimit
        INFO_MSG("checkCanAddMonthCard", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(maxTime)),
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))
        if self.monthCardExpireTime > maxTime:
            return False
        return True

    #只要调用了这个，就会发一次月卡获得奖励
    def doAddMonthCard(self, seconds, monthCardId):
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, 'unlock by action: doAddMonthCard')
        INFO_MSG("before add month card", self.monthCardExpireTime, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))
        if self.isMonthCardExpired():
            self.monthCardExpireTime = utils.getNow() + seconds
        else:
            self.monthCardExpireTime += seconds
        INFO_MSG("after add month card", self.monthCardExpireTime, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))

        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT_MONTHCARD
        _awardVal = dropAward.AwardVal()
        for rewardId in BCBCD.datas[monthCardId]['reward']:
            _ctx = self._getAvatarAwardCtx(rewardId, None)
            _awardVal += dropAward.getAwardOne(
                rewardId,
                _ctx
            )
        self.addWealth(_src, _awardVal, KBEngine.genUUID64(), _detail)
        self.checkMonthCardAward()

        return True
    

    def tryGetMonthCardDailyReward(self, exposed):
        self.checkMonthCardAward()

    #检查并发放月卡每日奖励
    def checkMonthCardAward(self):
        INFO_MSG("start checkMonthCardAward")
        if self.isMonthCardExpired():
            return
        
        if not utils.isDiffDay(self.lastMonthCardDailyRewardTime, utils.getNow(), gameconst.COMMON_CYCLE_TIME):
            INFO_MSG("checkMonthCardAward", "not diff day",
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardDailyRewardTime)),
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.getNow())))
            return
        
        INFO_MSG("checkMonthCardAward", "get daily reward",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardDailyRewardTime)),
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.getNow())))
        self.lastMonthCardDailyRewardTime = utils.getNow()
        
        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_MONTHCARD_DAILY
        _awardVal = dropAward.AwardVal()
        rewardId = BCBCCD.datas['dailyRewards']['value']
        _ctx = self._getAvatarAwardCtx(rewardId, None)
        _awardVal += dropAward.getAwardOne(
            rewardId,
            _ctx
        )
        self.addWealth(_src, _awardVal, KBEngine.genUUID64(), _detail)