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
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.FreeTicketSubType.CUBE, dateTime, curNum):
            needUpdateSubType.add(gameconst.FreeTicketSubType.CUBE)

        curNum = WLC.datas['dailyWonderLandNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.FreeTicketSubType.WONDER_LAND, dateTime, curNum):
            needUpdateSubType.add(gameconst.FreeTicketSubType.WONDER_LAND)

        curNum = ABC.datas['abyssDailyNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.FreeTicketSubType.ABYSS, dateTime, curNum):
            needUpdateSubType.add(gameconst.FreeTicketSubType.ABYSS)
            
        curNum = TDC_CFG.datas['dailyRewardNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.FreeTicketSubType.CRUSADE, dateTime, curNum):
            needUpdateSubType.add(gameconst.FreeTicketSubType.CRUSADE)

        curNum = RBC_CFG.datas['dailyRewardNum']['value']
        if self.recoveryData.ftRecoveryItem.update(now, gameconst.FreeTicketSubType.CHIEF, dateTime, curNum):
            needUpdateSubType.add(gameconst.FreeTicketSubType.CHIEF)

        if beInit:
            needUpdateSubType.add(gameconst.FreeTicketSubType.CUBE)
            needUpdateSubType.add(gameconst.FreeTicketSubType.WONDER_LAND)
            needUpdateSubType.add(gameconst.FreeTicketSubType.ABYSS)
            needUpdateSubType.add(gameconst.FreeTicketSubType.CRUSADE)
            needUpdateSubType.add(gameconst.FreeTicketSubType.CHIEF)
        LOG_DBG('ResourceRecoveryStub::checkFreeTicketNumConfigCallback', needUpdateSubType)

        if not needUpdateSubType:
            return

        dateNumInfo = {}
        for subType in needUpdateSubType:
            dateNumInfo[subType] = self.recoveryData.ftRecoveryItem.getData(subType)
        LOG_DBG('ResourceRecoveryStub::checkFreeTicketNumConfigCallback', dateNumInfo)
        gameengine.callBaseApps('gameengine.updateFreeTicketNumConfig', (dateNumInfo,))
        self.writeToDB()
