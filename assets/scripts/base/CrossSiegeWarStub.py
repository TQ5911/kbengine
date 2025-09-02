# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import iGlobal
import iBaseNoCell
import iTimer
import traceback
import gameconfig
import gameconst
import iRouter
import time
import datetime
import gametimer
import utils
import cityBattle_firstTime as CBFT
import serverList_serverList as SLSL
import cityBattle_config as CBC
import gameengine
import iCityOwnerMgr
import iCycleEvent
import calendar

#城战
class CrossSiegeWarStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCityOwnerMgr.ICityOwnerMgr, iCycleEvent.ICycleEvent):
    def __init__(self):
        self.crossServerGroupID = 2
        if gameconfig.serverId() in SLSL.datas:
            self.crossServerGroupID = SLSL.datas[gameconfig.serverId()]['groupID']
        else:
            WARNING_MSG('[lj]cross siege war stub init, server id not found:', gameconfig.serverId())
        self.GroupServerList = SLSL.group2ServerIds[self.crossServerGroupID]
        self.siegeWarStateChanged = True
        self.biddingTime = CBC.datas['cityBattle_biddingTime']['value'] * 24 * 60 * 60
        self.needBroadcastBiddingData = False
        self.lastBroadcastBiddingDataTime = 0
        self.biddingIncrease = 1 + CBC.datas['cityBattle_biddingIncrease']['value'] / 100.0
        self.biddingBasePrice = CBC.datas['cityBattle_biddingBasePrice']['value']
        self.startDayEveryMonth = CBC.datas['cityBattle_FirstStartTime']['value']

        self.firstTime, self.firstTimeValid, self.limitTime = utils.getSiegeWarFirstTimeInfo()
        self.nextBiddingStartTime = utils.getNextBiddingStartTime()
        DEBUG_MSG('[lj]init group id:', self.crossServerGroupID, 'first time:', self.firstTime, '(%s)' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.firstTime)),
                  'valid:', self.firstTimeValid)
        DEBUG_MSG('[lj]next bidding start time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.nextBiddingStartTime)))

        self.updateSystemSwitch()

        #竞拍加时
        self.signUpDelayTime = 0
        self.biddingDelayData = CBC.datas['cityBattle_biddingDelayed']['value']
        self.biddingDelayInvokeTime = self.biddingDelayData[0] * 60
        self.biddingDelayIncrease = self.biddingDelayData[1] * 60
        self.biddingDelayMaxTime = self.biddingDelayData[2] * 60

        #宣战倒计时相关
        self.countDownTime = CBC.datas['cityBattle_countdownBattle']['value'] * 24 * 60 * 60
        self.officialStartHour = CBC.datas['cityBattle_startTime']['value'][0] // 100
        self.officialStartMinute = CBC.datas['cityBattle_startTime']['value'][0] % 100
        self.officialEndHour = CBC.datas['cityBattle_startTime']['value'][1] // 100
        self.officialEndMinute = CBC.datas['cityBattle_startTime']['value'][1] % 100

        #gm相关
        self.gmDisableStateAutoChange = False
        if gameconfig.disableSiegeWarStateAutoChange():
            self.gmDisableStateAutoChange = True
            WARNING_MSG('[lj]gm disable siege war state auto change!!!!')

        #数据库初始值是0，要计算下当前状态
        if self.siegeWarState == gameconst.SiegeWarState.NOT_OPEN:
            self.updateSiegeWarStateAndEndTime()

        iCityOwnerMgr.ICityOwnerMgr.__init__(self)
        iCycleEvent.ICycleEvent.__init__(self)
        
        self.registerDailyEvent('_onCityOwnerDailyEvent')
        self.onDailyEvent()

    def doNext(self):
        if gameconfig.isCrossServer():
            crossSiegeWarServerInfo = gameconfig.crossSiegeWarServerInfo()
            self.pyAddTimer(1, 1, gametimer.CROSS_SIEGE_WAR_STATE_CHECK)
            DEBUG_MSG('[lj]do next', crossSiegeWarServerInfo)
        super().doNext()

    def onTimer(self, timer, userData):
        self._onTimer(timer, userData)
        if userData == gametimer.CROSS_SIEGE_WAR_STATE_CHECK:
            self.checkBroadcastBiddingData()
            self.checkBattleStart()
            self.cityOwnerMgrTick()
            self.onCrossSiegeWarStateCheck()
        elif userData == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()

    def getFirstMonthlyStartTime(self):
        y, m, d = time.strftime("%Y-%m-%d", time.localtime(self.limitTime)).split('-')
        nextStartTime = int(time.mktime(datetime.datetime(int(y), int(m), self.startDayEveryMonth, 0, 0, 0).timetuple()))
        if nextStartTime < self.limitTime:
            m = int(m) + 1
            if m > 12:
                y = int(y) + 1
                m = 1
            nextStartTime = int(time.mktime(datetime.datetime(int(y), int(m), self.startDayEveryMonth, 0, 0, 0).timetuple()))
        # DEBUG_MSG('[lj]next monthly start time:', time.strftime("%Y-%m-%d", time.localtime(nextStartTime)), 'limit time:',
        #           time.strftime("%Y-%m-%d", time.localtime(self.limitTime)))
        return nextStartTime
    
    #获取当前月度报名开始时间(保证now在当前周期)
    def getNowMonthlyStartTime(self):
        now = utils.getNow()
        y, m, d = time.strftime("%Y-%m-%d", time.localtime(now)).split('-')
        nowStartTime = int(time.mktime(datetime.datetime(int(y), int(m), self.startDayEveryMonth, 0, 0, 0).timetuple()))
        if now < nowStartTime:
            m = int(m) - 1
            if m < 1:
                y = int(y) - 1
                m = 12
            nowStartTime = int(time.mktime(datetime.datetime(int(y), int(m), self.startDayEveryMonth, 0, 0, 0).timetuple()))
        return nowStartTime
    
    #开关关闭、首次活动开启前为活动未开放状态
    def checkIsOpen(self):
        if self.systemSwitch == 0:
            return False
        if utils.getNow() < self.firstTime:
            return False
        if not self.firstTimeValid:
            if utils.getNow() < self.getFirstMonthlyStartTime():
                return False
        return True
    
    #检查是否在报名时间段
    def checkIsSignUpTime(self):
        now = utils.getNow()
        y, m, d = time.strftime("%Y-%m-%d", time.localtime(now)).split('-')
        biddingStartHour = CBC.datas['cityBattle_BiddingStartTime']['value'] * 60 * 60
        biddingEndHour = CBC.datas['cityBattle_BiddingEndTime']['value'] * 60 * 60

        #在第一次开服时间内
        #DEBUG_MSG('[lj]check is sign up time', now, self.firstTime, self.firstTime + self.biddingTime + self.signUpDelayTime)
        if now > self.firstTime + biddingStartHour and now < self.firstTime + self.biddingTime + self.signUpDelayTime + biddingEndHour:
            return True, self.firstTime + self.biddingTime + self.signUpDelayTime + biddingEndHour
        
        #在月度报名时间内
        nowMonthlyStartTime = self.getNowMonthlyStartTime()
        if now > nowMonthlyStartTime + biddingStartHour and now < nowMonthlyStartTime + self.biddingTime + self.signUpDelayTime + biddingEndHour:
            return True, nowMonthlyStartTime + self.biddingTime + self.signUpDelayTime + biddingEndHour
        return False, 0
    
    def resetSignUpData(self):
        self.nowBiddingCnt = self.biddingBasePrice
        self.biddingGuildList = []
        self.biddingNameList = []
        self.biddingCntList = []
        self.firstBiddingGuildName = ''
        self.firstBiddingGuildUUID = 0
        self.firstBiddingAvatarName = ''
        self.firstBiddingPrice = 0
        self.firstBiddingServerName = ''
        self.secondBiddingGuildName = ''
        self.secondBiddingGuildUUID = 0
        self.signUpDelayTime = 0
        self.avatarGBID = 0
        self.nextBiddingStartTime = utils.getNextBiddingStartTime()
        self.needBroadcastBiddingData = True

    #计算当前状态
    def updateSiegeWarStateAndEndTime(self):
        #gm禁止了自动切阶段
        if self.gmDisableStateAutoChange:
            return

        if not self.checkIsOpen():
            if self.siegeWarState != gameconst.SiegeWarState.NOT_OPEN:
                DEBUG_MSG('[lj]state change:', self.siegeWarState, '->', gameconst.SiegeWarState.NOT_OPEN)
                self.siegeWarState = gameconst.SiegeWarState.NOT_OPEN
                self.siegeWarStateChanged = True
            #未开放
            return
        
        ret, endTime = self.checkIsSignUpTime()
        if ret:
            self.siegeWarStateEndTime = endTime
            #DEBUG_MSG('[lj]signUp update end time:', self.siegeWarStateEndTime)
            if self.siegeWarState != gameconst.SiegeWarState.SIGN_UP:
                DEBUG_MSG('[lj]state change:', self.siegeWarState, '->', gameconst.SiegeWarState.SIGN_UP)
                self.siegeWarState = gameconst.SiegeWarState.SIGN_UP
                self.siegeWarStateChanged = True
                self.resetSignUpData()
                DEBUG_MSG('[lj]next bidding start time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.nextBiddingStartTime)))

            #还在报名阶段
            return

        #报名->准备宣战阶段
        if self.siegeWarState == gameconst.SiegeWarState.SIGN_UP:
            DEBUG_MSG('[lj]state change:', self.siegeWarState, '->', gameconst.SiegeWarState.PREPARE_WAR)
            self.siegeWarState = gameconst.SiegeWarState.PREPARE_WAR

            now = utils.getNow()
            localTime = time.localtime(now)
            year, month = localTime.tm_year, localTime.tm_mon
            lastDay = calendar.monthrange(year, month)[1]
            for i in range(5):
                targetTime = int(time.mktime(datetime.datetime(year, month, lastDay, self.officialStartHour, self.officialStartMinute, 0).timetuple()))
                if self.isInspecialBlackDay(targetTime):
                    lastDay -= 1
                else:
                    break

            limitDay = lastDay - CBC.datas['cityBattle_countdownBattle']['value']
            limitTime = int(time.mktime(datetime.datetime(year, month, limitDay, 23, 59, 59).timetuple()))
            
            self.siegeWarStateEndTime = limitTime
            self.siegeWarStateChanged = True

            DEBUG_MSG('[lj]prepare war end time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.siegeWarStateEndTime)))

            #处理竞拍结果
            self.handleBiddingResult()
            return
        
        #宣战倒计时阶段
        if self.siegeWarState == gameconst.SiegeWarState.WAR_COUNT_DOWN:
            remainTime = self.officialWarStartTime - utils.getNow()
            self.siegeWarStateEndTime = self.officialWarStartTime
            #DEBUG_MSG('[lj]countdown update remain time:', remainTime)
            if remainTime <= 0:
                self.siegeWarState = gameconst.SiegeWarState.WAR
                self.siegeWarStateEndTime = self.officialWarStartTime + CBC.datas['cityBattle_fightTime']['value'] * 60
                self.siegeWarStateChanged = True
            return
        
        #时间到了强制宣战
        if self.siegeWarState == gameconst.SiegeWarState.PREPARE_WAR:
            if len(self.biddingGuildList) > 0:
                if utils.getNow() >= self.siegeWarStateEndTime:
                    DEBUG_MSG('[lj]force declare war', self.firstBiddingGuildName, self.firstBiddingGuildUUID, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(utils.getNow())))
                    self.onSiegeWarDeclareWar(0, 0, True, 0, self.firstBiddingGuildName, self.firstBiddingGuildUUID, "", "")

    def onCrossSiegeWarStateCheck(self):
        self.updateSiegeWarStateAndEndTime()
        if self.siegeWarStateChanged or utils.getNow() % 60 == 0:
            if self.siegeWarStateChanged:
                DEBUG_MSG('[lj]do write to db')
                self.writeToDB()
            self.broadcastSiegeWarState()
            self.siegeWarStateChanged = False

    #开关热更todo
    def updateSystemSwitch(self):
        self.systemSwitch = CBC.datas['cityBattle_systemSwitch']['value']
        DEBUG_MSG('[lj]update system switch:', self.systemSwitch)

    #游戏服请求跨服城战状态
    def getSiegeWarState(self, srcServerId):
        DEBUG_MSG('[lj]get war state, src server id:', srcServerId)
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        _stub.setSiegeWarState(self.siegeWarState, self.siegeWarStateEndTime)

    def calOfficialWarStartTime(self):
        y, m, d = time.strftime("%Y-%m-%d", time.localtime(self.declareWarTime)).split('-')
        startDay = int(time.mktime(datetime.datetime(int(y), int(m), int(d), 0, 0, 0).timetuple()))
        self.officialWarStartTime = startDay + self.officialStartHour * 60 * 60 + self.officialStartMinute * 60 + self.countDownTime
        DEBUG_MSG('[lj]cal official war start time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.officialWarStartTime)))

    #状态变更广播
    def broadcastSiegeWarState(self):
        DEBUG_MSG('[lj]broadcast war state:', self.siegeWarState, 'servers:', self.GroupServerList)
        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.setSiegeWarState(self.siegeWarState, self.siegeWarStateEndTime)

    #跨服竞拍逻辑处理
    def doBidding(self, srcServerId, avatarGBID, name, cnt, guildName, guildUUID, serverName):
        DEBUG_MSG('[lj]do bidding', avatarGBID, name, cnt, guildName, guildUUID)
        _stub = iRouter.RemoteServerStubEntityCall(srcServerId, 'SiegeWarStub')
        if self.siegeWarState != gameconst.SiegeWarState.SIGN_UP:
            WARNING_MSG('[lj]do bidding failed, wrong state:', self.siegeWarState)
            _stub.onBiddingResult(guildUUID, cnt, False, 0)
            return
        
        nextBiddingMinValue = int(self.nowBiddingCnt * self.biddingIncrease)
        #第一次不乘
        if len(self.biddingGuildList) == 0:
            nextBiddingMinValue = self.biddingBasePrice
        if cnt < nextBiddingMinValue:
            DEBUG_MSG('[lj]do bidding failed, cnt:', cnt, 'min value:', nextBiddingMinValue)
            _stub.onBiddingResult(guildUUID, cnt, False, 1)
            return
        
        if len(self.biddingGuildList) > 0 and self.biddingGuildList[-1] == guildName:
            DEBUG_MSG('[lj]do bidding failed, guild name is same as last:', guildName, self.biddingGuildList[-1])
            _stub.onBiddingResult(guildUUID, cnt, False, 2)
            return
        
        #竞拍成功
        DEBUG_MSG('[lj]do bidding success', self.nowBiddingCnt, '->', cnt, "avatar:", self.avatarGBID, self.avatarName, "->", avatarGBID, name)

        #返还上任竞拍
        if self.avatarGBID != 0:
            lastStub = iRouter.RemoteServerStubEntityCall(self.avatarServerID, 'SiegeWarStub')
            lastStub.onBiddingResult(self.firstBiddingGuildUUID, self.nowBiddingCnt, False, 3)

        self.biddingGuildList.append(guildName)
        self.biddingNameList.append(name)
        self.biddingCntList.append(cnt)

        self.avatarServerID = srcServerId
        self.avatarGBID = avatarGBID
        self.avatarName = name
        self.nowBiddingCnt = cnt
        self.secondBiddingGuildName = self.firstBiddingGuildName
        self.secondBiddingGuildUUID = self.firstBiddingGuildUUID
        self.firstBiddingGuildName = guildName
        self.firstBiddingGuildUUID = guildUUID
        self.firstBiddingAvatarName = name
        self.firstBiddingPrice = cnt
        self.firstBiddingServerName = serverName
        DEBUG_MSG('[lj]first:', self.firstBiddingGuildName, self.firstBiddingGuildUUID, "second:", self.secondBiddingGuildName, self.secondBiddingGuildUUID)
        _stub.onBiddingResult(guildUUID, cnt, True, 0)

        #竞拍延时
        if self.siegeWarStateEndTime - utils.getNow() < self.biddingDelayInvokeTime:
            if self.signUpDelayTime < self.biddingDelayMaxTime:
                self.signUpDelayTime += self.biddingDelayIncrease
                self.siegeWarStateChanged = True

        #广播
        self.needBroadcastBiddingData = True
        self.checkBroadcastBiddingData()


    def checkBroadcastBiddingData(self):
        if not self.needBroadcastBiddingData:
            return
        if utils.getNow() - self.lastBroadcastBiddingDataTime < 1:
            return
        self.lastBroadcastBiddingDataTime = utils.getNow()
        self.needBroadcastBiddingData = False
        DEBUG_MSG('[lj]broadcast bidding data len:', len(self.biddingGuildList))
        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onSiegeWarBiddingDataUpdate(self.biddingGuildList, self.biddingNameList, self.biddingCntList, self.signUpDelayTime, self.avatarGBID, self.firstBiddingGuildUUID)

    def handleBiddingResult(self):
        if self.firstBiddingGuildUUID == 0:
            self.resetCityOwnerOrderRemainTimes()

        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.handleBiddingResult(self.firstBiddingGuildName, self.firstBiddingGuildUUID, self.firstBiddingAvatarName, self.firstBiddingPrice, self.firstBiddingServerName)

    def isInspecialBlackDay(self, ts):
        y, nowMonth, nowDay = time.strftime("%Y-%m-%d", time.localtime(ts)).split('-')
        for data in CBC.datas['cityBattle_specialTimeBlacklist']['value']:
            dayM = data // 100
            dayD = data % 100
            if int(nowMonth) == dayM and int(nowDay) == dayD:
                return True
        return False

    def onSiegeWarDeclareWar(self, srcServerId, box, isOffensive, gbId, guildName, guildUUID, declaration, srcName):
        DEBUG_MSG('[lj]on siege war declare war', srcServerId, box, isOffensive, gbId, guildName, guildUUID, declaration, srcName)
        _stub = iRouter.RemoteServerStubEntityCall(int(srcServerId), 'SiegeWarStub') if srcServerId != 0 else None

        if self.siegeWarState != gameconst.SiegeWarState.PREPARE_WAR:
            DEBUG_MSG('[lj]declare war failed, now state:', self.siegeWarState)
            if _stub:
                _stub.onSiegeWarDeclareWarCrossServerResult(box, False, gameconst.SiegeWarDeclareWarResult.WRONG_TIME)
            return
        
        if self.isInspecialBlackDay(utils.getNow()):
            DEBUG_MSG('[lj]declare war failed, now is special time:', time.strftime("%Y-%m-%d", time.localtime(utils.getNow())))
            if _stub:
                _stub.onSiegeWarDeclareWarCrossServerResult(box, False, gameconst.SiegeWarDeclareWarResult.SPECIAL_DAY)
            return
        
        DEBUG_MSG('[lj]declare war, src server id:', srcServerId)
        self.declareWarTime = utils.getNow()
        if self.declareWarTime > self.siegeWarStateEndTime:
            self.declareWarTime = self.siegeWarStateEndTime
            DEBUG_MSG('[lj]force declare war time:', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.declareWarTime)))
        self.calOfficialWarStartTime()
        self.siegeWarState = gameconst.SiegeWarState.WAR_COUNT_DOWN
        self.siegeWarStateChanged = True

        #进攻防守方
        if self.cityOwnerGuildName != '':
            self.warOffensiveGuildUUID = guildUUID
            self.warOffensiveGuildName = guildName
            self.warDefensiveGuildUUID = self.cityOwnerGuildUUID
            self.warDefensiveGuildName = self.cityOwnerGuildName
            DEBUG_MSG('[lj]declare war, city owner:', self.cityOwnerGuildName, self.cityOwnerGuildUUID)
        else:
            if isOffensive:
                self.warOffensiveGuildUUID = guildUUID
                self.warOffensiveGuildName = guildName
                self.warDefensiveGuildUUID = self.secondBiddingGuildUUID
                self.warDefensiveGuildName = self.secondBiddingGuildName
            else:
                self.warOffensiveGuildUUID = self.secondBiddingGuildUUID
                self.warOffensiveGuildName = self.secondBiddingGuildName
                self.warDefensiveGuildUUID = guildUUID
                self.warDefensiveGuildName = guildName
            DEBUG_MSG('[lj]declare war, no city owner')
        DEBUG_MSG('[lj]declare war, offensive:', self.warOffensiveGuildName, self.warOffensiveGuildUUID,
                  'defensive:', self.warDefensiveGuildName, self.warDefensiveGuildUUID)
        
        self.changeDeclaration(False, 0, declaration)
            
        if _stub:
            _stub.onSiegeWarDeclareWarCrossServerResult(box, True, gameconst.SiegeWarDeclareWarResult.SUCCESS)

        #广播邮件
        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onSiegeWarDeclareWarOfficial(guildName, guildUUID, self.warOffensiveGuildUUID, self.warDefensiveGuildUUID, self.warOffensiveGuildName, self.warDefensiveGuildName, self.officialWarStartTime, srcName)

    def doResetSpace(self):
        gameengine.getGlobalBase("SiegeWarSpaceStub").resetSiegeWarData({
            "offenseGuildUUID": self.warOffensiveGuildUUID,
            "offenseGuildName": self.warOffensiveGuildName,
            "defenseGuildUUID": self.warDefensiveGuildUUID,
            "defenseGuildName": self.warDefensiveGuildName,
            "sceneOpenTime": self.officialWarStartTime - CBC.datas['cityBattle_prepareTime']['value'] * 60,
            "offensiveJunXuQiXieLevelData": self.offensiveJunXuQiXieLevelData,
            "defensiveJunXuQiXieLevelData": self.defensiveJunXuQiXieLevelData
        })

    def checkBattleStart(self):
        if self.gmDisableStateAutoChange:
            return
        if self.siegeWarState != gameconst.SiegeWarState.WAR_COUNT_DOWN:
            self.hasResetSpace = False
            return
        if self.hasResetSpace:
            return
        if utils.getNow() >= self.officialWarStartTime - CBC.datas['cityBattle_prepareTime']['value'] * 60:
            DEBUG_MSG("[lj]checkBattleStart: reset siege war data", self.warOffensiveGuildUUID, self.warOffensiveGuildName, self.warDefensiveGuildUUID, self.warDefensiveGuildName)
            self.doResetSpace()
            self.hasResetSpace = True

    #跨服通知争夺战结束todo
    def onCrossSiegeWarEnd(self, combatResult, winnerGuildUUID):
        DEBUG_MSG('[lj]cross siege war end', combatResult)
        self.siegeWarState = gameconst.SiegeWarState.WAR_END
        self.siegeWarStateChanged = True

        #广播
        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.onCrossSiegeWarEnd(combatResult, winnerGuildUUID, self.cityOwnerGuildUUID)

    def gmChangeSiegeWarState(self, state, endTime, *args):
        DEBUG_MSG('[lj]gm change siege war state', state, endTime, args)
        if self.siegeWarState == state and args[0] == 0:
            WARNING_MSG('[lj]gm change siege war state failed, state is same:', self.siegeWarState)
            return

        endTime = utils.getNow() + 60 * 60 * 24
        WARNING_MSG('[lj]gm change siege war state:', self.siegeWarState, '->', state, "end time:", endTime, "args:", args)
        self.gmDisableStateAutoChange = True
        WARNING_MSG('[lj]set gmDisableStateAutoChange:', self.gmDisableStateAutoChange)
        if state == gameconst.SiegeWarState.WAR_COUNT_DOWN:
            self.onSiegeWarDeclareWar(0, 0, True, 0, self.firstBiddingGuildName, self.firstBiddingGuildUUID, "", "")
        elif state == gameconst.SiegeWarState.WAR:
            self.siegeWarState = state
            self.siegeWarStateChanged = True
            if args[0] > 0:
                self.siegeWarStateEndTime -= args[0] * 60
                #只改时间
                return
            else:
                self.siegeWarStateEndTime = utils.getNow() + CBC.datas['cityBattle_fightTime']['value'] * 60
        else:
            self.siegeWarState = state
            self.siegeWarStateChanged = True
            self.siegeWarStateEndTime = endTime

        #各阶段具体处理
        if state == gameconst.SiegeWarState.SIGN_UP:
            self.resetSignUpData()
        elif state == gameconst.SiegeWarState.PREPARE_WAR:
            self.handleBiddingResult()
        elif state == gameconst.SiegeWarState.WAR:
            self.officialWarStartTime = utils.getNow()
            self.doResetSpace()

    def onSyncJunXuQiXieLevel(self, offensiveData, defensiveData):
        DEBUG_MSG('[lj]onSyncJunXuQiXieLevel', offensiveData, defensiveData)
        if offensiveData:
            self.offensiveJunXuQiXieLevelData = offensiveData
        if defensiveData:
            self.defensiveJunXuQiXieLevelData = defensiveData

    def changeDeclaration(self, isDefense, srcGbId, declaration):
        if isDefense:
            if srcGbId != self.cityOwnerId:
                DEBUG_MSG('[lj]changeDeclaration not city owner', srcGbId)
                return
            self.cityDefenseDeclaration = declaration
        else:
            self.cityOffensiveDeclaration = declaration

        for serverID in self.GroupServerList:
            _stub = iRouter.RemoteServerStubEntityCall(int(serverID), 'SiegeWarStub')
            _stub.changeDeclaration(isDefense, srcGbId, declaration)