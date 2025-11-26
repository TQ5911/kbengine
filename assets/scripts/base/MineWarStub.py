# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import gameengine
import gametimer
import utils
import gameconst
import gameconfig
import formula
import iCycleEvent
import gameglobal
import MineWarInfo

import mailAssistor
import mail_mail as MAMAD
import mineBattle_config as MBC
import mineBattle_miningArea as MBMA


class MineWarStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, iCycleEvent.ICycleEvent):
    def __init__(self):
        iBaseNoCell.IBaseNoCell.__init__(self)
        iTimer.ITimer.__init__(self)
        iCycleEvent.ICycleEvent.__init__(self)
        
        self.gmDisableMineWar = False
        self.state = gameconst.MINE_WAR_STATE.END
        self.startTime = 0
        self.endTime = 0

        self.warMapTransferDict = {}

        self.warMapList = MBMA.datas.keys()
        for mapId in self.warMapList:
            if mapId not in self.mineMapData:
                self.mineMapData[mapId] = MineWarInfo.MineWarMapVal(mapId)

            sceneList = MBMA.datas[mapId].get('sceneList', [])
            if len(sceneList) < 2:
                ERROR_MSG('MineWarStub.__init__ mapId:{} sceneList invalid:{}'.format(mapId, sceneList))
                continue
            self.warMapTransferDict[mapId] = sceneList[-2]  # 传送到安全区场景id
            

        # 时间配置
        self.prepareNeed = MBC.datas['mineBattle_interfacePromptTime']['value'] * 60  # 准备时间需要提前多少时间

        self.warStartWeekDay = MBC.datas['mineBattle_startTime']['value'][0]  # 每周几
        self.warStartHour = MBC.datas['mineBattle_startTime']['value'][1]  // 100   # 几点开始
        self.warStartMin = MBC.datas['mineBattle_startTime']['value'][1]  % 100    # 几分开始
        self.startOffsetSec = offset = ((self.warStartWeekDay - 1) * 24 + self.warStartHour) * 3600 + self.warStartMin * 60

        self.warEndHour = MBC.datas['mineBattle_startTime']['value'][2]  // 100   # 几点结束
        self.warEndMin = MBC.datas['mineBattle_startTime']['value'][2]  % 100    # 几分结束
        self.endOffsetSec = ((self.warStartWeekDay - 1) * 24 + self.warEndHour) * 3600 + self.warEndMin * 60
        
    def doNext(self):

        self.pyAddTimer(1, 1, gametimer.MINE_WAR_STATE_CHECK)

        self.registerDailyEvent('_onMineWarDailyEvent')
        self.onDailyEvent()

        super(MineWarStub, self).doNext()
        
    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        elif userArg == gametimer.MINE_WAR_STATE_CHECK:
            self._calcCurState()
            
        elif userArg == gametimer.CYCLE_EVENT_TICK_TIMER:
            self.onCycleEventTick()
        else:
            self._onTimer(tid, userArg)

    def _onMineWarDailyEvent(self):
        #
        self.callAllMineWarSpaceMgr('onMineWarDayChange', [], {'guildId': True, 'flagDestroyedTime': True})


    def getMineWarState(self):
        return self.state
    
    def registerMineWarSpaceMgr(self, mapId, spaceMgrbox):
        if mapId in self.mineMapData:
            self.mineMapData[mapId].setSpaceMgrbox(spaceMgrbox)
            spaceMgrbox.onRegisterMineWarSpaceMgr(self.mineMapData[mapId].getGuildGbId(), self.state)
    
    def _calcState(self):
        now = utils.getNow()
        self.startTime = utils.getCurrentWeekTS(offsetSec=self.startOffsetSec)
        self.endTime = utils.getCurrentWeekTS(offsetSec=self.endOffsetSec)
        prepareTime = self.startTime - self.prepareNeed

        # if self.gmDisableMineWar:
        if True:
            return gameconst.MINE_WAR_STATE.END

        if now < prepareTime:
            return gameconst.MINE_WAR_STATE.END
        elif now < self.startTime:
            return gameconst.MINE_WAR_STATE.PREPARE
        elif now < self.endTime:
            return gameconst.MINE_WAR_STATE.RUNNING
        else:
            return gameconst.MINE_WAR_STATE.END
        
    def _calcCurState(self):
        # 计算当前状态
        curState = self._calcState()
        if curState != self.state:
            self._onStateChange(self.state, curState)
            
    def _onStateChange(self, oldState, newState):
        INFO_MSG('MineWarStub.onStateChange oldState:', oldState, 'newState:', newState)
        if newState == gameconst.MINE_WAR_STATE.PREPARE:
            self._onMineWarPrepare()
        elif newState == gameconst.MINE_WAR_STATE.RUNNING:
            self._onMineWarStart()
        elif newState == gameconst.MINE_WAR_STATE.END:
            self._onMineWarEnd()

        # 同步各 spacemgr state
        self.callAllMineWarSpaceMgr('onMineWarStateChange', [oldState, newState], {'guildId': True})


    # 矿战准备阶段
    def _onMineWarPrepare(self):
        self.state = gameconst.MINE_WAR_STATE.PREPARE
        
        # 广播
        gameengine.broadcastBaseapp('broadcastToAllAvatar', (gameconst.BASE, 'onMineWarPreparePlayer', (self.state, self.startTime), ()))

        # 注册定时器传送到上一层
        transferTime = self.startTime - MBC.datas['mineBattle_transferPersonnelTime']['value'] * 60
        offset = transferTime - utils.getNow()
        if offset > 0:
            self._callback(offset, '_transferMineWarPersonnel', (), gametimer.TIMER_TAG_TRANSFER_MINE_WAR_PERSONNEL)


    def _transferMineWarPersonnel(self):
        self.callAllMineWarSpaceMgr('transferAllAvatarInSpace', [], {'transferMapId': True, 'guildId': True})

    # 矿战开始阶段
    def _onMineWarStart(self):
        self.state = gameconst.MINE_WAR_STATE.RUNNING

        # ============================= lxq测试用 
        self._transferMineWarPersonnel()

        # 开始时重置
        for mapId, mineWarVal in self.mineMapData.items():
            mineWarVal.onStartReset()

        # 广播玩家
        gameengine.broadcastBaseapp('broadcastToAllAvatar', (gameconst.BASE, 'onMineWarStartPlayer', (self.state, self.endTime), ()))


    # 矿战结束阶段
    def _onMineWarEnd(self):
        self.state = gameconst.MINE_WAR_STATE.END

        changeInfo = []
        timeCfg = MBC.datas['mineBattle_bonusIncome']['value']
        # 切换帮派归属
        for mapId, mineWarVal in self.mineMapData.items():
            guildGbId = mineWarVal.getGuildGbId()
            tempguildGbId = mineWarVal.getTempGuildGbId()
            changeDict = {'mapId': mapId, 'oldGuildId': guildGbId, 'newGuildId': tempguildGbId}
            

            if mineWarVal.onMineWarEnd():
                # self.onRewardMineWar(mapId, guildGbId, tempguildGbId) # 放到spacemgr自己去处理
                INFO_MSG('MineWarStub._onMineWarEnd mapId:', mapId, 'oldGuildId:', guildGbId, 'newGuildId:', tempguildGbId)
                # 记录帮派近期战事 === todo=

            guildMap = {}
            for guildId, ownerTime in mineWarVal.guildOwnerTime.items():
                guildMap[guildId] = min((ownerTime // timeCfg[0]) * timeCfg[1], timeCfg[2])
        
            changeDict['ownerTimeMap'] = guildMap
            changeInfo.append(changeDict)

        # 广播玩家
        gameengine.broadcastBaseapp('broadcastToAllAvatar', (gameconst.BASE, 'onMineWarEndPlayer', (changeInfo,), ()))


    def callAllMineWarSpaceMgr(self, funcName, args=[], kwargs={}):
        INFO_MSG('callAllMineWarSpaceMgr with:', funcName, 'args:', args, 'kwargs:', kwargs)
        for mapId, mineWarVal in self.mineMapData.items():
            arg = []
            spaceMgrbox = mineWarVal.getSpaceMgrbox()
            if spaceMgrbox is None:
                continue
            if kwargs.get('transferMapId', False):
                arg.append(self.warMapTransferDict.get(mapId, 0))
            if kwargs.get('guildId', False):
                arg.append(mineWarVal.getGuildGbId())
            if kwargs.get('flagDestroyedTime', False):
                arg.append(mineWarVal.getflagDestroyedTime())
            arg.extend(args)
            getattr(spaceMgrbox, funcName)(*arg)

    def onRewardMineWar(self, mapId, oldGuildId, newGuildId):
        INFO_MSG('MineWarStub.onRewardMineWar mapId:', mapId, 'oldGuildId:', oldGuildId, 'newGuildId:', newGuildId)
        # 奖励矿战胜利帮派成员
        spaceMgrbox = self.mineMapData[mapId].getSpaceMgrbox()
        if spaceMgrbox:
            spaceMgrbox.rewardMineWarGuildMembers(oldGuildId, newGuildId)

    def onMineWarFlagBeKill(self, mapId):
        # 旗帜被毁
        mineWarVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        # 暂存
        mineWarVal.onFlagBeDestroyed()

    def onMineWarCoreBeKill(self, mapId, killerId, killerGuildId):
        # 杀死核心
        mineWarVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        # 暂存
        mineWarVal.onCoreBeKilled(killerGuildId)


    def playerGetMineWarState(self, playerBox, guildId):
        mineList = []
        mineTimeMap = {}
        timeCfg = MBC.datas['mineBattle_bonusIncome']['value']

        for mapId, Val in self.mineMapData.items():
            if Val.getGuildGbId() == guildId:
                mineList.append(mapId)
            elif guildId in Val.guildOwnerTime:
                timeVal = Val.guildOwnerTime[guildId]
                mineTimeMap[mapId] = min((timeVal // timeCfg[0]) * timeCfg[1], timeCfg[2])

        # 玩家获取矿战状态
        playerBox.onMineWarStateSync(self.state, self.startTime, self.endTime, mineList, mineTimeMap)

        

