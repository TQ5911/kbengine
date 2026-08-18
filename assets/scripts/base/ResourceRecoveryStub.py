import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gameconst
import gametimer
import utils
import gameengine
import LogTrackingMgr
import message_Message_def as MMD
import const_const as CONST
import userType
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import wonderLand_config as WLC
import cube_config as CC
import abyss_config as ABC
import teamDunChallenge_config as TDC_CFG
import raidBossChallenge_config as RBC_CFG
from datetime import datetime
import gameconfig


class ResourceRecoveryStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer):
    def __init__(self):
        LOG_INFO("ResourceRecoveryStub::__init__")
        super(ResourceRecoveryStub, self).__init__()
        self.initDatetimeTimerTick()
        self.checkFreeTicketNumConfigTimerId = 0

    def doNext(self):
        super().doNext()
        LOG_INFO("ResourceRecoveryStub::doNext")
        self.checkFreeTicketNumConfigCallback(True)

    def startCheckFreeTicketNumConfigTimer(self):
        now = utils.curTS()
        dateTimeSt = datetime.fromtimestamp(now)
        nextDateTimeSt = dateTimeSt.replace(second=0, microsecond=0)
        preTimestamp = int(nextDateTimeSt.timestamp())
        nextTimestamp = preTimestamp + 60
        if self.checkFreeTicketNumConfigTimerId:
            self._cancelDatetimeCallback(self.checkFreeTicketNumConfigTimerId, gametimer.TIMER_TAG_CHECK_FREE_TICKET_NUM_CONFIG_TIMER)
            self.checkFreeTicketNumConfigTimerId = 0
        self.checkFreeTicketNumConfigTimerId = self._datetimeCallback(nextTimestamp, 'checkFreeTicketNumConfigCallback', (False,), gametimer.TIMER_TAG_CHECK_FREE_TICKET_NUM_CONFIG_TIMER, 'checkFreeTicketNumConfigTimerId')

    def onTimer(self, timerID, userData):
        self._onTimerTrigger(timerID, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(timerID)
        elif userData == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()

    def checkFreeTicketNumConfigCallback(self, beInit):
        self.startCheckFreeTicketNumConfigTimer()

        now = utils.curTS()
        serverOpenTimestamp = gameconfig.serverOpenTime()
        if serverOpenTimestamp > now:
            LOG_WARN("ResourceRecoveryStub::checkFreeTicketNumConfigCallback not serverOpenTime")
            return

        dateTime = utils.getIntDateTime(now)

        needUpdateSubType = set()

        curNum = CC.datas['dailyCubeNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CUBE, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CUBE)
        curNum = CC.datas['cubeNumCoinDailyLimit']['value']
        if self.recoveryData.ptRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CUBE, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CUBE)

        curNum = WLC.datas['dailyWonderLandNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.RecoveryTicketSubType.WONDER_LAND, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.WONDER_LAND)
        curNum = WLC.datas['wonderLandNumCoinDailyLimit']['value']
        if self.recoveryData.ptRecoveryItem.update(now, gameconst.RecoveryTicketSubType.WONDER_LAND, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.WONDER_LAND)

        curNum = ABC.datas['abyssDailyNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.RecoveryTicketSubType.ABYSS, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.ABYSS)
        curNum = ABC.datas['abyssNumCoinDailyLimit']['value']
        if self.recoveryData.ptRecoveryItem.update(now, gameconst.RecoveryTicketSubType.ABYSS, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.ABYSS)
            
        curNum = TDC_CFG.datas['dailyRewardNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CRUSADE, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CRUSADE)
        curNum = TDC_CFG.datas['rewardNumCoinDailyLimit']['value']
        if self.recoveryData.ptRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CRUSADE, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CRUSADE)

        curNum = RBC_CFG.datas['dailyRewardNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CHIEF, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CHIEF)
        curNum = RBC_CFG.datas['rewardNumCoinDailyLimit']['value']
        if self.recoveryData.ptRecoveryItem.update(now, gameconst.RecoveryTicketSubType.CHIEF, dateTime, curNum):
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CHIEF)

        if beInit:
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CUBE)
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.WONDER_LAND)
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.ABYSS)
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CRUSADE)
            needUpdateSubType.add(gameconst.RecoveryTicketSubType.CHIEF)
        LOG_DBG('ResourceRecoveryStub::checkFreeTicketNumConfigCallback', needUpdateSubType)

        if not needUpdateSubType:
            return

        dateNumInfo = {}
        for subType in needUpdateSubType:
            dateNumInfo[gameconst.RecoveryTicketType.FREE_TICKET * 100 + subType] = self.recoveryData.ftRecoveryItem.getData(subType)
            dateNumInfo[gameconst.RecoveryTicketType.PAID_TICKET * 100 + subType] = self.recoveryData.ptRecoveryItem.getData(subType)
        LOG_DBG('ResourceRecoveryStub::checkFreeTicketNumConfigCallback', dateNumInfo)
        gameengine.callBaseApps('gameengine.updateFreeTicketNumConfig', (dateNumInfo,))
        self.writeToDB()
