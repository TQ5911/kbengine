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
import gametimer
import formula
import gamePlay_gamePlay as G_GP
import experience_config as G_EXP
import experience_exp as G_EXP_EXP
import random
import const_const as CC
import mailAssistor
import itemData_set as IDSD
import redisUtils
import LogTrackingMgr
import gamedecorator
import gameconfig
import gameengine

class IMonthCard(object):
    def __init__(self):
        self.offlineHangupChecked = False
        self.tempLastDayRemainHangupMinutes = 0
        self.monthCardTimer = 0
        self.lastMonthcardLoginTime = self.tLoginBase
        if not self.isMonthCardExpired():
            LOG_INFO("init month card timer", self.monthCardExpireTime)
            self.monthCardTimer = self.pyAddTimer(60, 60, gametimer.MONTH_CARD_CHECK_TIMER)

    def isMonthCardExpired(self):
        if not gameconfig.visibleConfigEnabled('monthCard'):
            return True
        return self.monthCardExpireTime < utils.curTS()
    
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
        maxTime = utils.curTS() + 3600 * durationHoursLimit
        LOG_INFO("checkCanAddMonthCard", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(maxTime)),
                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))
        if self.monthCardExpireTime > maxTime:
            return False
        if not gameconfig.visibleConfigEnabled('monthCard'):
            return False
        return True

    #只要调用了这个，就会发一次月卡获得奖励
    def doAddMonthCard(self, seconds, monthCardId):
        self.unlockBag(gameconst.BagType.BAG_TYPE_NORMAL, 'unlock by action: doAddMonthCard')
        LOG_INFO("before add month card", self.monthCardExpireTime, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))
        if self.isMonthCardExpired():
            self.monthCardExpireTime = utils.curTS() + seconds
        else:
            self.monthCardExpireTime += seconds
        LOG_INFO("after add month card", self.monthCardExpireTime, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.monthCardExpireTime)))

        if not self.monthCardTimer:
            LOG_INFO("add month card timer", self.monthCardExpireTime)
            self.monthCardTimer = self.pyAddTimer(60, 60, gametimer.MONTH_CARD_CHECK_TIMER)

        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_BUYCREDIT_MONTHCARD
        _awardVal = dropAward.AwardVal()
        for rewardId in BCBCD.datas[monthCardId]['reward']:
            _ctx = self._getAvatarAwardCtx(rewardId, None)
            _awardVal += dropAward.getAwardOne(
                rewardId,
                _ctx
            )
        awardCtx = self._getAvatarAwardCtx(0, None)
        opUUID = KBEngine.genUUID64()
        self.addWealth(_src, _awardVal, opUUID, _detail, awardCtx)
        self.checkMonthCardAward()
        self.updateRedisVIPFlag()

        LogTrackingMgr.LogTrackingMgr.MonthCard_Invoke(
            self.gbID,
            self.getAvatarLevel(),
            utils.curTS(),
            self.monthCardExpireTime,
            opUUID
        )
        return opUUID
    

    def tryGetMonthCardDailyReward(self, exposed):
        self.checkMonthCardAward()

    #检查并发放月卡每日奖励
    def checkMonthCardAward(self, *args):
        LOG_INFO("start checkMonthCardAward")
        if self.isMonthCardExpired():
            return
        
        if not utils.checkDiffDay(self.lastMonthCardDailyRewardTime, utils.curTS(), gameconst.GENERAL_CYCLE_TIME):
            LOG_INFO("checkMonthCardAward", "not diff day",
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardDailyRewardTime)),
                     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.curTS())))
            return
        
        LOG_INFO("checkMonthCardAward", "get daily reward",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardDailyRewardTime)),
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.curTS())))
        self.lastMonthCardDailyRewardTime = utils.curTS()
        
        #道具奖励
        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_MONTHCARD_DAILY
        _awardVal = dropAward.AwardVal()
        rewardId = BCBCCD.datas['dailyRewards']['value']
        _ctx = self._getAvatarAwardCtx(rewardId, None)
        _awardVal += dropAward.getAwardOne(
            rewardId,
            _ctx
        )
        awardCtx = self._getAvatarAwardCtx(0, None)
        self.addWealth(_src, _awardVal, KBEngine.genUUID64(), _detail, awardCtx)

        #挂机时长奖励
        self.checkAndGetHangupTime()

    #领取挂机时长
    def checkAndGetHangupTime(self):
        if self.isMonthCardExpired():
            return
        
        if not utils.checkDiffDay(self.lastMonthCardHangupGetTime, utils.curTS(), gameconst.GENERAL_CYCLE_TIME):
            return
        
        LOG_INFO("lastMonthCardHangupGetTime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardHangupGetTime)),
                 "->", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.curTS())))
        LOG_INFO("remainHangupMinutes:", self.remainHangupMinutes, "->", BCBCCD.datas['dailyBaseTime']['value'])
        self.lastMonthCardHangupGetTime = utils.curTS()
        self.tempLastDayRemainHangupMinutes = self.remainHangupMinutes
        self.remainHangupMinutes = BCBCCD.datas['dailyBaseTime']['value']
        return True

    def _checkAndAddIdleIncome(self, minutes):
        self._deductRemainHangupMinutes(minutes)
        self._doAddIdleIncome(minutes)
    
    def _deductRemainHangupMinutes(self, minutes):
        LOG_INFO("_deductRemainHangupMinutes", "minutes", minutes, "remainHangupMinutes", self.remainHangupMinutes)
        if minutes > self.remainHangupMinutes:
            LOG_ERR("deductRemainHangupMinutes", "minutes > remainHangupMinutes", minutes, self.remainHangupMinutes)
            minutes = self.remainHangupMinutes
        self.remainHangupMinutes -= minutes

    def _calcIdleIncome(self, minutes):
        level = self.getAvatarLevel()
        
        l, r = G_EXP.datas["offlineExpFluctuate"]["value"]
        expPercent = random.uniform(l, r)
        
        totalScore = self.getTotalScore()

        idx = -1
        for i in range(len(G_EXP_EXP.datas[level]['powerRange'])):
            powerRange = G_EXP_EXP.datas[level]['powerRange'][i]
            if len(powerRange) == 1:
                if totalScore >= powerRange[0]:
                    idx = i
                    break
            elif len(powerRange) == 2:
                if totalScore >= powerRange[0] and totalScore <= powerRange[1]:
                    idx = i
                    break
        
        if idx == -1:
            LOG_ERR("onMonthCardTimer", "invalid powerRange", totalScore, level, G_EXP_EXP.datas[level]['powerRange'])
            return 0 

        income = G_EXP_EXP.datas[level]['idleIncome'][idx] * expPercent * minutes
        income = int(income)
        LOG_INFO("_calcIdleIncome", "level", level, "idx", idx, "expPercent", expPercent, "minutes", minutes, "income", income)
        return income

    def _doAddIdleIncome(self, minutes):
        LOG_INFO("_doAddIdleIncome", "minutes", minutes)
        income = self._calcIdleIncome(minutes)
        
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_MAP_HANG_UP_INCOME
        _awardVal = dropAward.AwardVal()

        _awardVal.addWealthByItemId(gameconst.ItemId.EXP, income)

        awardCtx = self._getAvatarAwardCtx(0, None)
        self.addWealth(_src, _awardVal, _opUUID, _detail, awardCtx)

        LogTrackingMgr.LogTrackingMgr.MonthCard_Afk(
            self.gbID,
            self.remainHangupMinutes,
            minutes,
            _opUUID
        )

    #主城、等级到达、有月卡 = 有挂机收益
    def _onMonthCardTimer(self):
        #主城挂机收益
        if self.isMonthCardExpired():
            return
        
        if self.getAvatarLevel() < CC.datas["offlineTriggerMin"]["value"]:
            return
        
        mapId = formula.parseDungeonNoBySpaceNo(self.baseSpaceNo)
        if not formula.checkWorldLineType(mapId):
            return
        
        mapData = G_GP.datas.get(mapId)
        if not mapData:
            LOG_WARN("onMonthCardTimer", "mapData invalid:", mapId)
            return
        
        #分线大世界 and 安全区 = 主城，有挂机收益
        if mapData['isMainCity'] != 1:
            return
        
        if self.remainHangupMinutes > 0:
            self._checkAndAddIdleIncome(1)

    #结算挂机收益
    def checkOfflineHangup(self):
        if self.isCrossServer:
            return
        
        if not gameconfig.visibleConfigEnabled('monthCard'):
            LOG_WARN("checkOfflineHangup", "monthCard not enabled", self.gbID, self.tsLastOfflineBase, self.offlineHangupChecked)
            return

        if self.offlineHangupChecked:
            return
        self.offlineHangupChecked = True
        
        if self.getAvatarLevel() < CC.datas["offlineTriggerMin"]["value"]:
            return

        endTime = min(self.monthCardExpireTime, utils.curTS())
        if endTime <= self.tsLastOfflineBase + BCBCCD.datas['offlineTimeLimit']['value'] * 60:
            return
        
        if self.tsLastOfflineBase <= 0:
            LOG_WARN("checkOfflineHangup", "tsLastOfflineBase <= 0", self.tsLastOfflineBase, endTime)
            return
        
        if self.lastMonthcardLoginTime >= self.tsLastOfflineBase:
            LOG_WARN("checkOfflineHangup", "lastMonthcardLoginTime >= tsLastOfflineBase", self.lastMonthcardLoginTime, self.tsLastOfflineBase)
            return

        totalMinutes = 0
        #上次离线，没有跨天
        if not utils.checkDiffDay(self.tsLastOfflineBase, endTime, gameconst.GENERAL_CYCLE_TIME):
            #先尝试领取挂机时长
            self.checkAndGetHangupTime()

            timeDelta = (endTime - self.tsLastOfflineBase) // 60
            timeDelta = min(timeDelta, self.remainHangupMinutes)
            if timeDelta > 0:
                totalMinutes += timeDelta
                self._deductRemainHangupMinutes(timeDelta)
        else:
            self.checkAndGetHangupTime()
            accumulateTime = CC.datas['maxAccumulateTime']['value']
            lastRemainHangupMinutes = self.tempLastDayRemainHangupMinutes
            self.tempLastDayRemainHangupMinutes = 0

            #计算最早那天的收益
            #那天的挂机时长有浪费
            timeDelta = lastRemainHangupMinutes
            if utils.checkDiffDay(self.tsLastOfflineBase, self.tsLastOfflineBase + lastRemainHangupMinutes * 60, gameconst.GENERAL_CYCLE_TIME):
                timeDelta = (utils.getCurDayTS(self.tsLastOfflineBase + lastRemainHangupMinutes * 60, gameconst.GENERAL_CYCLE_TIME) - self.tsLastOfflineBase) // 60

            timeDelta = min(timeDelta, accumulateTime)
            totalMinutes += timeDelta
            accumulateTime -= timeDelta
            LOG_INFO("checkOfflineHangup begin", "timeDelta", timeDelta, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime, "tsLastOfflineBase", self.tsLastOfflineBase, "endTime", endTime)

            #中间天数
            dayDelta = (utils.getCurDayTS(endTime - gameconst.GENERAL_CYCLE_TIME, gameconst.GENERAL_CYCLE_TIME) - \
                       utils.getCurDayTS(self.tsLastOfflineBase - gameconst.GENERAL_CYCLE_TIME, gameconst.GENERAL_CYCLE_TIME)) // gameconst.ONE_DAY_COST_SECONDS - 1
            if dayDelta > 0:
                minutes = min(accumulateTime, BCBCCD.datas['dailyBaseTime']['value'] * dayDelta)
                totalMinutes += minutes
                accumulateTime -= minutes
                LOG_INFO("checkOfflineHangup middle", "dayDelta", dayDelta, "minutes", minutes, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime)

            #今天
            minutes = min((endTime - utils.getCurDayTS(endTime - gameconst.GENERAL_CYCLE_TIME, gameconst.GENERAL_CYCLE_TIME)) // 60, self.remainHangupMinutes)
            minutes = min(minutes, accumulateTime)
            totalMinutes += minutes
            LOG_INFO("checkOfflineHangup end", "minutes", minutes, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime)

            #今天的要扣掉今天的时长
            self._deductRemainHangupMinutes(minutes)

        self.totalOfflineExp = self._calcIdleIncome(totalMinutes)
        self.totalOfflineMinute = totalMinutes
        LOG_INFO("checkOfflineHangup", "totalMinutes", totalMinutes, "totalOfflineExp", self.totalOfflineExp,
                 "lastMonthcardLoginTime", self.lastMonthcardLoginTime, "tsLastOfflineBase", self.tsLastOfflineBase)
        LogTrackingMgr.LogTrackingMgr.MonthCard_Offline(
            self.gbID,
            self.remainHangupMinutes,
            totalMinutes
        )
        return True

    def reqOfflineHangupData(self, exposed):
        LOG_INFO("reqOfflineHangupData")
        self.checkOfflineHangup()
        if self.totalOfflineExp != 0:
            LOG_INFO("send offlineHangupData")
            self.client.onOfflineHangupData(self.totalOfflineMinute, self.totalOfflineExp)
    
    def reqGetOfflineExp(self, exposed):
        LOG_INFO("reqGetOfflineExp", self.totalOfflineExp)
        if self.totalOfflineExp == 0:
            LOG_WARN("reqGetOfflineExp", "totalOfflineExp is 0")
            return
        
        exp = self.totalOfflineExp
        self.totalOfflineExp = 0
        self.totalOfflineMinute = 0
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_HANG_UP_INCOME
        wealthVal = dropAward.AwardVal()
        wealthVal.addWealthByItemId(gameconst.ItemId.EXP, exp)
        awardCtx = self._getAvatarAwardCtx(0, None)
        _detail = gameclass.AwardDetail()
        self.addWealth(srcType, wealthVal, opUUID, _detail, awardCtx)
        
        LogTrackingMgr.LogTrackingMgr.MonthCard_OfflineReward(
            self.gbID,
            1,
            opUUID
        )

    #如果在线时没有领取离线收益，离线后会转化成邮件
    def _checkMonthCardOfflineExpMail(self):
        if self.totalOfflineExp == 0:
            return
        
        exp = self.totalOfflineExp
        self.totalOfflineExp = 0
        self.totalOfflineMinute = 0
        LOG_INFO("_checkMonthCardOfflineExpMail", "totalOfflineExp", exp)
        _addVal = dropAward.MailWealthVal()
        _addVal.addWealthByItemId(gameconst.ItemId.EXP, exp)
        opUUID = KBEngine.genUUID64()
        mailAssistor.sendMailToPlayers([self.gbID], CC.datas['offlineMail']['value'], extraAttach=_addVal,
                                       srcType=AAC_AACDD.datas.BONUS_SRC_MONTHCARD_OFFLINE_BONUS, opUUID=opUUID)
        LogTrackingMgr.LogTrackingMgr.MonthCard_OfflineReward(
            self.gbID,
            2,
            opUUID
        )

    #更新redis的特权标识(排队优先)
    def updateRedisVIPFlag(self):
        redisUtils.RedisUtils.checkAndSetSVIP(gameconst.PrivilegeRedisKey.SVIP + self.accountName, self._onUpdateRedisSVIPFlag)

        if self.isMonthCardExpired():
            return
        
        redisUtils.SetUtils.setMaxNumber(gameconst.PrivilegeRedisKey.VIP + self.accountName, self.monthCardExpireTime, self._onUpdateRedisVIPFlag)

    def _onUpdateRedisVIPFlag(self, cid, err, res):
        LOG_INFO("_onUpdateRedisVIPFlag", "cid", cid, "err", err, "res", res)

    def _onUpdateRedisSVIPFlag(self, cid, err, res):
        LOG_INFO("_onUpdateRedisSVIPFlag", "cid", cid, "err", err, "res", res)
        if res and res == 1:
            stubs = gameengine.getLoginStubsByAccountName(self.accountName)
            gameclass.DuplicatedCallList(stubs).incSVIPOnlineNumBySetSVIP()
