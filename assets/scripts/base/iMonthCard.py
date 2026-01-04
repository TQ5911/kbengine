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

class IMonthCard(object):
    def __init__(self):
        self.offlineHangupChecked = False
        self.pyAddTimer(60, 60, gametimer.MONTH_CARD_CHECK_TIMER)

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
        self.updateRedisVIPFlag()

        LogTrackingMgr.LogTrackingMgr.MonthCard_Invoke(
            self.gbID,
            self.getAvatarLevel(),
            utils.getNow(),
            self.monthCardExpireTime
        )
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
        self.addWealth(_src, _awardVal, KBEngine.genUUID64(), _detail)

        #挂机时长奖励
        self.checkAndGetHangupTime()

    #领取挂机时长
    def checkAndGetHangupTime(self):
        if self.isMonthCardExpired():
            return
        
        if not utils.isDiffDay(self.lastMonthCardHangupGetTime, utils.getNow(), gameconst.COMMON_CYCLE_TIME):
            return
        
        INFO_MSG("lastMonthCardHangupGetTime:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.lastMonthCardHangupGetTime)),
                 "->", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.getNow())))
        INFO_MSG("remainHangupMinutes:", self.remainHangupMinutes, "->", BCBCCD.datas['dailyBaseTime']['value'])
        self.lastMonthCardHangupGetTime = utils.getNow()
        self.remainHangupMinutes = BCBCCD.datas['dailyBaseTime']['value']
        return True

    def _checkAndAddIdleIncome(self, minutes):
        self._deductRemainHangupMinutes(minutes)
        self._doAddIdleIncome(minutes)
    
    def _deductRemainHangupMinutes(self, minutes):
        INFO_MSG("_deductRemainHangupMinutes", "minutes", minutes, "remainHangupMinutes", self.remainHangupMinutes)
        if minutes > self.remainHangupMinutes:
            ERROR_MSG("deductRemainHangupMinutes", "minutes > remainHangupMinutes", minutes, self.remainHangupMinutes)
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
            ERROR_MSG("onMonthCardTimer", "invalid powerRange", totalScore, level, G_EXP_EXP.datas[level]['powerRange'])
            return 0 

        income = G_EXP_EXP.datas[level]['idleIncome'][idx] * expPercent * minutes
        income = int(income)
        INFO_MSG("_calcIdleIncome", "level", level, "idx", idx, "expPercent", expPercent, "minutes", minutes, "income", income)
        return income

    def _doAddIdleIncome(self, minutes):
        INFO_MSG("_doAddIdleIncome", "minutes", minutes)
        income = self._calcIdleIncome(minutes)
        
        _opUUID = KBEngine.genUUID64()
        _detail = gameclass.AwardDetail()
        _src = AAC_AACDD.datas.BONUS_SRC_HANG_UP_INCOME
        _awardVal = dropAward.AwardVal()

        _awardVal.addWealthByItemId(gameconst.ItemId.EXP, income)

        awardCtx = self._getAvatarAwardCtx(0, None)
        self.addWealth(_src, _awardVal, _opUUID, _detail, awardCtx)

    #主城、等级到达、有月卡 = 有挂机收益
    def _onMonthCardTimer(self):
        #主城挂机收益
        if self.isMonthCardExpired():
            return
        
        if self.getAvatarLevel() < CC.datas["offlineTriggerMin"]["value"]:
            return
        
        mapId = formula.getDungeonNoBySpaceNo(self.baseSpaceNo)
        if not formula.isWorldLineType(mapId):
            return
        
        mapData = G_GP.datas.get(mapId)
        if not mapData:
            WARNING_MSG("onMonthCardTimer", "mapData invalid:", mapId)
            return
        
        #分线大世界 and 安全区 = 主城，有挂机收益
        if mapData['ifSafeArea'] != 1:
            return
        
        if self.remainHangupMinutes > 0:
            self._checkAndAddIdleIncome(1)

    #结算挂机收益
    def checkOfflineHangup(self):
        if self.offlineHangupChecked:
            return
        self.offlineHangupChecked = True
        
        if self.getAvatarLevel() < CC.datas["offlineTriggerMin"]["value"]:
            return

        endTime = min(self.monthCardExpireTime, utils.getNow())
        if endTime <= self.tLastOfflineBase + BCBCCD.datas['offlineTimeLimit']['value'] * 60:
            return

        totalMinutes = 0
        #上次离线，没有跨天
        if not utils.isDiffDay(self.tLastOfflineBase, endTime, gameconst.COMMON_CYCLE_TIME):
            #先尝试领取挂机时长
            self.checkAndGetHangupTime()

            timeDelta = (endTime - self.tLastOfflineBase) // 60
            timeDelta = min(timeDelta, self.remainHangupMinutes)
            if timeDelta > 0:
                totalMinutes += timeDelta
                self._deductRemainHangupMinutes(timeDelta)
        else:
            accumulateTime = CC.datas['maxAccumulateTime']['value']
            lastRemainHangupMinutes = self.remainHangupMinutes
            self.checkAndGetHangupTime()

            #计算最早那天的收益
            #那天的挂机时长有浪费
            timeDelta = lastRemainHangupMinutes
            if utils.isDiffDay(self.tLastOfflineBase, self.tLastOfflineBase + lastRemainHangupMinutes * 60, gameconst.COMMON_CYCLE_TIME):
                timeDelta = (utils.getCurrentDayTS(self.tLastOfflineBase + lastRemainHangupMinutes * 60, gameconst.COMMON_CYCLE_TIME) - self.tLastOfflineBase) // 60

            timeDelta = min(timeDelta, accumulateTime)
            totalMinutes += timeDelta
            accumulateTime -= timeDelta
            INFO_MSG("checkOfflineHangup begin", "timeDelta", timeDelta, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime, "tLastOfflineBase", self.tLastOfflineBase, "endTime", endTime)

            #中间天数
            dayDelta = utils.getCurrentDayTS(endTime, gameconst.COMMON_CYCLE_TIME) - \
                       utils.getCurrentDayTS(self.tLastOfflineBase, gameconst.COMMON_CYCLE_TIME) - 1
            if dayDelta > 0:
                minutes = min(accumulateTime, BCBCCD.datas['dailyBaseTime']['value'] * dayDelta)
                totalMinutes += minutes
                accumulateTime -= minutes
            INFO_MSG("checkOfflineHangup middle", "dayDelta", dayDelta, "minutes", minutes, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime)

            #今天
            minutes = min((endTime - utils.getCurrentDayTS(endTime, gameconst.COMMON_CYCLE_TIME)) // 60, self.remainHangupMinutes)
            minutes = min(minutes, accumulateTime)
            totalMinutes += minutes
            INFO_MSG("checkOfflineHangup end", "minutes", minutes, "totalMinutes", totalMinutes, "accumulateTime", accumulateTime)

            #今天的要扣掉今天的时长
            self._deductRemainHangupMinutes(minutes)

        self.totalOfflineExp = self._calcIdleIncome(totalMinutes)
        self.totalOfflineMinute = totalMinutes
        INFO_MSG("checkOfflineHangup", "totalMinutes", totalMinutes, "totalOfflineExp", self.totalOfflineExp)
        return True

    def reqOfflineHangupData(self, exposed):
        if self.totalOfflineExp != 0:
            self.client.onOfflineHangupData(self.totalOfflineMinute, self.totalOfflineExp)
    
    def reqGetOfflineExp(self, exposed):
        INFO_MSG("reqGetOfflineExp", self.totalOfflineExp)
        if self.totalOfflineExp == 0:
            WARNING_MSG("reqGetOfflineExp", "totalOfflineExp is 0")
            return
        
        exp = self.totalOfflineExp
        self.totalOfflineExp = 0
        self.totalOfflineMinute = 0
        _src = AAC_AACDD.datas.BONUS_SRC_HANG_UP_INCOME
        self.cell.addExpByMonthCard(exp, KBEngine.genUUID64(), _src, "")

    #如果在线时没有领取离线收益，离线后会转化成邮件
    def _checkMonthCardOfflineExpMail(self):
        if self.totalOfflineExp == 0:
            return
        
        exp = self.totalOfflineExp
        self.totalOfflineExp = 0
        self.totalOfflineMinute = 0
        INFO_MSG("_checkMonthCardOfflineExpMail", "totalOfflineExp", exp)
        _addVal = dropAward.MailWealthVal()
        _addVal.addWealthByItemId(gameconst.ItemId.EXP, exp)
        mailAssistor.sendMailToPlayers([self.gbID], CC.datas['offlineMail']['value'], extraAttach=_addVal)

    #更新redis的特权标识(排队优先)
    def updateRedisVIPFlag(self):
        redisUtils.RedisUtils.checkAndSetSVIP(gameconst.PrivilegeRedisKey.SVIP + self.accountName, self._onUpdateRedisSVIPFlag)

        if self.isMonthCardExpired():
            return
        
        redisUtils.SetUtils.setMaxNumber(gameconst.PrivilegeRedisKey.VIP + self.accountName, self.monthCardExpireTime, self._onUpdateRedisVIPFlag)

    def _onUpdateRedisVIPFlag(self, cid, err, res):
        INFO_MSG("_onUpdateRedisVIPFlag", "cid", cid, "err", err, "res", res)

    def _onUpdateRedisSVIPFlag(self, cid, err, res):
        INFO_MSG("_onUpdateRedisSVIPFlag", "cid", cid, "err", err, "res", res)

