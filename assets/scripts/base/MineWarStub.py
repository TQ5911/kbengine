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
import dropAward
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import mineBattle_rankReward as MBRR

import mailAssistor
import mail_mail as MAMAD
import mineBattle_config as MBC
import mineBattle_miningArea as MBMA
import gamePlay_gamePlay as GGD
import itemData_itemData as IDID
import mineBattle_firstTime as MBFT
import time
import datetime
import LogTrackingMgr

MINE_WAR_RANK_CD = 5  # 排名刷新间隔时间秒

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
            # if mapId not in self.mineMapData:
            #     self.mineMapData[mapId] = MineWarInfo.MineWarMapVal(mapId)

            sceneList = MBMA.datas[mapId].get('sceneList', [])
            if len(sceneList) < 2:
                ERROR_MSG('MineWarStub.__init__ mapId:{} sceneList invalid:{}'.format(mapId, sceneList))
                continue
            self.warMapTransferDict[mapId] = sceneList[-2]  # 传送到安全区场景id
            

        # 时间配置
        self.prepareNeed = utils.getMineWarPrepareNeedSec()
        self.startOffsetSec = utils.getMineWarStartOffsetSec()
        self.endOffsetSec = utils.getMineWarEndOffsetSec()
        
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

        # 矿石结算
        for mapId, mineWarVal in self.mineMapData.items():
            mineWarVal.onCollectEnd()

    def getMineWarState(self):
        return self.state
    
    def registerMineWarSpaceMgr(self, mapId, spaceMgrbox):
        if mapId in self.warMapList:
            if mapId not in self.mineMapData:
                self.mineMapData[mapId] = MineWarInfo.MineWarMapVal(mapId)

            self.mineMapData[mapId].setSpaceMgrbox(spaceMgrbox)
            spaceMgrbox.onRegisterMineWarSpaceMgr(self.mineMapData[mapId].getGuildGbId(), self.state, self.mineMapData[mapId].getflagDestroyedTime())

    def canServerStartMineWar(self):
        serverId = gameconfig.serverId()
        serverCfg = MBFT.datas.get(serverId, {})
        serverStartTime = serverCfg.get('StartTime', '20251106')
        _startTimeStr = str(serverStartTime)
        y = _startTimeStr[:4]
        m = _startTimeStr[4:6]
        d = _startTimeStr[6:8]
        # 第一次活动开启时间
        firstTime = int(time.mktime(datetime.datetime(int(y), int(m), int(d), 0, 0, 0).timetuple()))
        if utils.getNow() < firstTime:
            return False
        
        return True
    
    def _calcState(self):
        if not self.canServerStartMineWar():
            return gameconst.MINE_WAR_STATE.END
        
        if not gameconfig.visibleConfigEnabled('mineBattle'):
        # if True:
            return gameconst.MINE_WAR_STATE.END
        
        now = utils.getNow()
        self.startOffsetSec = utils.getMineWarStartOffsetSec()
        self.endOffsetSec = utils.getMineWarEndOffsetSec()
        self.startTime = utils.getCurrentWeekTS(offsetSec=self.startOffsetSec)
        self.endTime = utils.getCurrentWeekTS(offsetSec=self.endOffsetSec)
        if self.endTime <= now:
            self.startTime += gameconst.ONE_WEEK_SECONDS
            self.endTime += gameconst.ONE_WEEK_SECONDS
        prepareTime = self.startTime - self.prepareNeed

        if now < prepareTime:
            return gameconst.MINE_WAR_STATE.END
        elif now < self.startTime:
            return gameconst.MINE_WAR_STATE.PREPARE
        elif now < self.endTime:
            if self.state == gameconst.MINE_WAR_STATE.END: # 不要跳过准备阶段
                return gameconst.MINE_WAR_STATE.PREPARE
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
        offset = max(transferTime - utils.getNow(), 0)
        self._callback(offset, '_transferMineWarPersonnel', (), gametimer.TIMER_TAG_TRANSFER_MINE_WAR_PERSONNEL)

    def _transferMineWarPersonnel(self):
        if not gameconfig.visibleConfigEnabled('mineBattle'):
            return
        self.callAllMineWarSpaceMgr('transferAllAvatarInSpace', [], {'transferMapId': True, 'guildId': True})

    # 矿战开始阶段
    def _onMineWarStart(self):
        self.state = gameconst.MINE_WAR_STATE.RUNNING

        # 开始时重置
        for mapId, mineWarVal in self.mineMapData.items():
            mineWarVal.onStartReset()

        # 广播玩家
        gameengine.broadcastBaseapp('broadcastToAllAvatar', (gameconst.BASE, 'onMineWarStartPlayer', (self.state, self.endTime), ()))
        #
        LogTrackingMgr.LogTrackingMgr.MineBattle_Start(self.startTime, {mapId: val.getGuildGbId() for mapId, val in self.mineMapData.items()})

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
                mapCfg = MBMA.datas.get(mapId, {})
                mapName = mapCfg.get('name', '')
                currGuildInfo = mineWarVal.currGuildInfo
                mineWarVal.addMineWarEvent(2, [currGuildInfo.leaderName, mapName])

            # 计算归属帮派排名
            mineWarVal.calcOwnerTime()
            guildRevenue = {}
            for guildId, guildVal in mineWarVal.guildOwnerDict.items():
                if guildId == mineWarVal.currGuildInfo.guildGbId:
                    guildVal.revenue = mineWarVal.currGuildInfo.revenue
                else:
                    guildVal.revenue = int(min((guildVal.ownerTime // timeCfg[0]) * timeCfg[1], timeCfg[2]))
                guildRevenue[guildId] = guildVal.revenue
        
            changeDict['leaderName'] = mineWarVal.currGuildInfo.leaderName
            changeDict['guildName'] = mineWarVal.currGuildInfo.guildName
            changeDict['guildRevenueRate'] = guildRevenue
            changeInfo.append(changeDict)

            ownerList = list(mineWarVal.guildOwnerDict.values())
            ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
            ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
            mineWarVal.ownerRankList = ownerList    # 暂存

            try:
                logRankList = []
                for i, guildVal in enumerate(ownerList):
                    logRankList.append({'rank': i+1, 'guildGbId': guildVal.guildGbId, 'ownerTime': guildVal.ownerTime, 'revenue': guildVal.revenue})
                LogTrackingMgr.LogTrackingMgr.MineBattle_End(self.endTime, mapId, tempguildGbId, logRankList)
            except Exception as e:
                ERROR_MSG('LogTrackingMgr.MineBattle_End error:', mapId, tempguildGbId)

        # 结算
        self.onEndRewardByScore()

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

    def doMineWarGuildDisbanded(self, guildId):
        INFO_MSG('MineWarStub.onMineWarGuildDisbanded :', 'guildId:', guildId)
        _mapIds = 0
        for mapId, mineWarVal in self.mineMapData.items():
            if mineWarVal.getGuildGbId() == guildId:
                _mapIds = mapId
                break
        if _mapIds > 0:
            spaceMgrbox = mineWarVal.getSpaceMgrbox()
            mineWarVal = MineWarInfo.MineWarMapVal(_mapIds)
            mineWarVal.setSpaceMgrbox(spaceMgrbox)
            self.mineMapData[_mapIds] = mineWarVal
            spaceMgrbox.onMineWarGuildDisbanded(mineWarVal.getGuildGbId(), self.state)

    def onRewardMineWar(self, mapId, oldGuildId, newGuildId):
        INFO_MSG('MineWarStub.onRewardMineWar mapId:', mapId, 'oldGuildId:', oldGuildId, 'newGuildId:', newGuildId)
        # 奖励矿战胜利帮派成员
        spaceMgrbox = self.mineMapData[mapId].getSpaceMgrbox()
        if spaceMgrbox:
            spaceMgrbox.rewardMineWarGuildMembers(oldGuildId, newGuildId)

    def onMineWarFlagBeKill(self, mapId, guildGbId, guildName, killerGbId, killerName):
        # 旗帜被毁
        mineWarVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        # 暂存
        mineWarVal.onFlagBeDestroyed()
        mineWarVal.addMineWarEvent(3, [guildName, killerName])
        LogTrackingMgr.LogTrackingMgr.MineBattle_KillFlag(mapId, guildGbId, killerGbId, mineWarVal.flagDestroyedNum)

        guildName = mineWarVal.currGuildInfo.guildName
        damageCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
        mineWarVal.addMineWarEvent(4, [str(mineWarVal.flagDestroyedNum), str(damageCfg[0]), guildName])
        # 帮会频道
        self._doMineWarBroadcastGuildMember(mineWarVal.currGuildInfo.guildGbId, 'doBroadcastGuildMemberBase',
                                                ('onMineWarFlagBeDestroyed', (mapId, mineWarVal.currGuildInfo.guildGbId, mineWarVal.flagDestroyedNum)))
        
        if mineWarVal.flagDestroyedNum == damageCfg[0]:
            # 战报
            mineWarVal.addMineWarEvent(5, [str(mineWarVal.flagDestroyedNum), str(damageCfg[0]), guildName])
            mineWarVal.onFlagAllDestroyed()
            # 广播
            gameengine.broadcastBaseapp('broadcastToAllAvatar', (gameconst.BASE, 'onMineWarFlagAllDestroyed', (mapId, guildName, mineWarVal.currGuildInfo.guildGbId), ()))

    def doOnMineWarKillCoreForGuild(self, mapId, box, guildInfo):
        INFO_MSG('doOnMineWarKillCoreForGuild mapId:', mapId, 'box:', box.id, 'guildInfo:', guildInfo)
        mineWarVal: MineWarInfo.MineWarMapVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        mineWarVal.onCoreBeKilled(guildInfo)

    def SyncMineWarFlagHp(self, mapId, hp):
        mineWarVal: MineWarInfo.MineWarMapVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        
        if mineWarVal.flagHp > hp:
            # 帮会频道
            INFO_MSG('SyncMineWarFlagHp flagHp change warning mapId:', mapId, 'from:', mineWarVal.flagHp, 'to:', hp)
            self._doMineWarBroadcastGuildMember(mineWarVal.currGuildInfo.guildGbId, 'doBroadcastGuildMemberBase',
                                                ('onMineWarFlagHpChangeWarning', (mapId,)))

        if mineWarVal.flagHp >= 50 and hp < 50:
            # 帮会频道
            self._doMineWarBroadcastGuildMember(mineWarVal.currGuildInfo.guildGbId, 'doBroadcastGuildMemberBase',
                                                ('onMineWarFlagHpLowWarning', (mapId,)))
            
        mineWarVal.flagHp = hp

    def _doMineWarBroadcastGuildMember(self, guildGbId, funcName, args):
        if guildGbId > 0:
            gameengine.getGlobalBase('GuildStub').callOnGuild(guildGbId, funcName, args, None, '', ())

    def playerGetMineWarState(self, playerBox, guildId):
        mineList = []
        MineRevenueDict = {}

        for mapId, Val in self.mineMapData.items():
            if guildId <= 0:
                continue
            if Val.getGuildGbId() == guildId:
                mineList.append(mapId)
                currGuildInfo = Val.currGuildInfo
                MineRevenueDict[mapId] = currGuildInfo.revenue
            elif guildId in Val.guildOwnerDict:
                guildVal = Val.guildOwnerDict[guildId]
                MineRevenueDict[mapId] = guildVal.revenue

        # 玩家获取矿战状态
        playerBox.onMineWarStateSync(self.state, self.startTime, self.endTime, mineList, MineRevenueDict)

    def playerGetMineWarInfo(self, playerBox, guildId):
        mineWarInfo = []
        for mapId, Val in self.mineMapData.items():
            info = {'mapId': mapId, 'startTime': self.startTime, 'endTime': self.endTime,}
            currGuildInfo = Val.currGuildInfo
            info['guildGbId'] = getattr(currGuildInfo, 'guildGbId', 0)
            info['guildName'] = getattr(currGuildInfo, 'guildName', '')
            info['guildIcon'] = getattr(currGuildInfo, 'guildIcon', 0)
            info['guildDspFlag'] = getattr(currGuildInfo, 'guildDspFlag', 0)
            info['guildOwnerName'] = getattr(currGuildInfo, 'leaderName', '')
            info['ownerTimeStamp'] = getattr(currGuildInfo, 'ownerTimeStamp', 0)
            info['ownerDay'] = 0
            if info['ownerTimeStamp'] > 0:
                info['ownerDay'] = utils.countIntersDay(info['ownerTimeStamp'])

            info['flagRecoverTime'] = 0
            flagDestroyedTime = Val.getflagDestroyedTime()
            if utils.isDiffDay(flagDestroyedTime, utils.getNow(), gameconst.COMMON_CYCLE_TIME):
                info['flagDestroyed'] = 0
            else:
                info['flagDestroyed'] = 1
                info['flagRecoverTime'] = utils.getCurrentDayTS(offsetSec=gameconst.COMMON_CYCLE_TIME) + gameconst.ONE_DAY_SECONDS

            # destroyCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
            # incomeCfg = (MBC.datas['mineBattle_incomeCoefficient']['value'] - 1.0) * 100
            # info['guildRevenueRate'] = int(incomeCfg) - (destroyCfg[1] if Val.flagDestroyedNum >= destroyCfg[0] else 0)
            info['guildRevenueRate'] = getattr(currGuildInfo, 'revenue', 0)

            info['revenue'] = int(Val.currCollectNum * (MBC.datas['mineBattle_extraIncome']['value'] * 0.01))
            info['allNum'] = int(Val.allCollectNum)
            info['mineEvents'] = Val.mineWarEvents
            # info['mineEvents'] = [e.toGuildEventLogSavedDict() for e in Val.mineWarEvents]

            info['flagHp'] = Val.flagHp

            mineWarInfo.append(info)

        playerBox.client.onMineWarInfo(mineWarInfo)

        INFO_MSG('MineWarStub.playerGetMineWarInfo response:', mineWarInfo)

    def doGetMineWarFlagHp(self, mapId, playerBox):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        # INFO_MSG('MineWarStub.doGetMineWarFlagHp called for player:', playerBox.id, 'mapId:', mapId, 'flagHp:', mapVal.flagHp)
        flagHp = mapVal.flagHp if self.state != gameconst.MINE_WAR_STATE.RUNNING else 0
        playerBox.client.onGetMineWarFlagHp(mapId, mapVal.flagHp)

    def doShareGuildMineWarBonusToMember(self, mapId, srcGbId, shareList, box):
        INFO_MSG('doShareGuildMineWarBonusToMember mapId:', mapId, 'srcGbId:', srcGbId, 'shareList:', shareList)
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        
        sum = 0
        for val in shareList:
            sum += val['bonusNum']
        if sum > mapVal.allCollectNum:
            DEBUG_MSG('doShareGuildMineWarBonusToMember sum > allCollectNum:', sum, '>', mapVal.allCollectNum)
            box.onMessagePre(MBC.datas['mineBattle_notEnoughStock']['value'], [])
            box.client.onMineWarShareBonusResult(False)
            return
        
        playerList = []
        bonusNumList = []
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_MINE_WAR_GUILD_SHARE
        itemId = MBC.datas['mineBattle_MoneyID']['value']
        itemName = IDID.datas[itemId]['name']
        for val in shareList:
            num = val['bonusNum']
            mapVal.allCollectNum -= num
            playerGbId = val['playerGbId']
            playerList.append(playerGbId)
            bonusNumList.append(num)
            awardVal = dropAward.MailWealthVal()
            awardVal.addWealthByItemId(itemId, num)
            mailAssistor.sendMailToPlayers([playerGbId],
                                          MBC.datas['mineBatte_dividendMail']['value'],
                                          extraAttach=awardVal,
                                          despArgs=(mapVal.currGuildInfo.leaderName, itemName),
                                          srcType=srcType, opUUID=opUUID)
            
        box.client.onMineWarShareBonusResult(True)
        # 重新拉下数据
        self.playerGetMineWarInfo(box, srcGbId)

        LogTrackingMgr.LogTrackingMgr.MineBattle_Shared(srcGbId, mapVal.getGuildGbId(), mapVal.currCollectNum, playerList, bonusNumList, opUUID)

    def doGetMineWarGuildMemberScore(self, mapId, playerBox, guildGbId):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return

        if mapVal.guildGbId != guildGbId:
            return
        
        scoreRankList = mapVal.scoreRankList
        res = []
        idx = 1
        for scoreVal in scoreRankList:
            if scoreVal.guildGbId != guildGbId:
                continue
            val = scoreVal.getScoreData()
            val['rankId'] = idx
            res.append(val)
            idx += 1

        INFO_MSG('MineWarStub.doGetMineWarGuildMemberScore response to player:', mapId, res)
        playerBox.client.onGetMineWarGuildMemberScore(mapId, res)
    
    def doGetMineWarGuildOwnerRank(self, mapId, playerBox, guildInfo, last):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        
        selfRankInfo = None
        rankList = []
        if self.state == gameconst.MINE_WAR_STATE.RUNNING:
            if last:
                ownerList = mapVal.ownerRankListLast
            elif utils.getNow() - mapVal.coreDestroyedTime > MINE_WAR_RANK_CD:
                mapVal.calcOwnerTime()
                ownerList = list(mapVal.guildOwnerDict.values())
                ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
                ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
                mapVal.ownerRankList = ownerList    # 暂存
            else:
                ownerList = mapVal.ownerRankList
        elif len(mapVal.ownerRankList) == 0:
            ownerList = list(mapVal.guildOwnerDict.values())
            ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
            ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
            mapVal.ownerRankList = ownerList    # 暂存
        else:
            ownerList = mapVal.ownerRankList

        timeCfg = MBC.datas['mineBattle_bonusIncome']['value']
        for idx, ownerVal in enumerate(ownerList):
            val = ownerVal.toSaveDict()
            val['rankId'] = idx + 1
            if self.state == gameconst.MINE_WAR_STATE.RUNNING and not last:
                val['revenue'] = int(min((val['ownerTime'] // timeCfg[0]) * timeCfg[1], timeCfg[2]))
            else:
                val['revenue'] = ownerVal.revenue
            rankList.append(val)

            if guildInfo.get('guildGbId', 0) == ownerVal.guildGbId:
                selfRankInfo = val

        if selfRankInfo is None:
            selfRankInfo = MineWarInfo.MineWarGuildVal().initFromDict(guildInfo).toSaveDict()
            selfRankInfo['rankId'] = 0
        
        # INFO_MSG('MineWarStub.doGetMineWarGuildOwnerRank response to player:', last, playerBox.id, guildInfo, selfRankInfo, rankList)
        playerBox.onMineWarGuildOwnerRankBase(selfRankInfo, rankList)

            
    def doGetMineWarGuildPlayerRank(self, mapId, playerBox, playerGbId, playerName, guildInfo, last):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        selfGuildInfo = None
        scoreDict = mapVal.playerScoreDict

        rankList = []
        if self.state == gameconst.MINE_WAR_STATE.RUNNING and not last:
            if utils.getNow() - mapVal.lastScoreRankTime > MINE_WAR_RANK_CD:
                scoreList = [val for val in scoreDict.values() if val.totalScore >= MBC.datas['mineBattle_rankScoreThreshold']['value']]
                scoreList.sort(key=lambda x: x.totalScore, reverse=True)
                mapVal.scoreRankListTemp = scoreList
                mapVal.lastScoreRankTime = utils.getNow()
            else:
                scoreList = mapVal.scoreRankListTemp
        else:
            scoreList = mapVal.scoreRankList

        scoreList = scoreList[:MBC.datas['mineBatte_rankPersonNum']['value']]
        for idx, scoreVal in enumerate(scoreList):
            if scoreVal.totalScore < MBC.datas['mineBattle_rankScoreThreshold']['value']:
                break
            val = scoreVal.getData()
            val['rankId'] = idx + 1
            if val['gbId'] == playerGbId:
                selfGuildInfo = val
            rankList.append(val)

        if selfGuildInfo is None:
            if not last and playerGbId in scoreDict:
                selfGuildInfo = scoreDict[playerGbId].getData()
            else:
                selfGuildInfo = MineWarInfo.MineWarScore(gbId=playerGbId, name=playerName, 
                                                        guildName=guildInfo.get('guildName', ''),
                                                        guildIcon=guildInfo.get('guildIcon', 0),
                                                        guildDspFlag=guildInfo.get('guildDspFlag', 0)).getData()
            selfGuildInfo['rankId'] = 0
        
        # INFO_MSG('MineWarStub.doGetMineWarGuildPlayerRank response to player:', playerBox.id, guildInfo, selfGuildInfo, rankList)
        playerBox.onMineWarGuildPlayerRankBase(selfGuildInfo, rankList)

        
    def addMineWarScore(self, mapId, playerGbId, playerName, guildGbId, guildName, guildIcon, guildDspFlag, score, scoreType):
        if self.state != gameconst.MINE_WAR_STATE.RUNNING:
            return
        
        mapVal: MineWarInfo.MineWarMapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        
        mapVal.addMineWarScoreVal(playerGbId, playerName, guildGbId, guildName, guildIcon, guildDspFlag, score, scoreType)

    def playerCollectAward(self, mapId, num):
        INFO_MSG('MineWarStub.playerCollectAward lineType:', mapId, 'num:', num)
        mineWarVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        mineWarVal.addCollectNum(num)

    def getRewardIdByRankCfg(self):
        """根据排名获取奖励ID"""
        rankCfg = {}
        for rank, cfg in MBRR.datas.items():
            minRank = cfg['rankMin']
            maxRank = cfg['rankMax']
            rewardId = cfg['rewardID']
            for r in range(minRank, maxRank + 1):
                rankCfg[r] = rewardId
                
        return rankCfg

    def onEndRewardByScore(self):
        if self.state != gameconst.MINE_WAR_STATE.END:
            return

        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_MINE_WAR_SCORE
        
        rankCfg = self.getRewardIdByRankCfg()
        for mapId, mineWarVal in self.mineMapData.items():
            scoreDict = mineWarVal.playerScoreDict
            rankList = []
            otherList = []
            guildMemberList = []
            mapCfg = MBMA.datas.get(mapId, {})
            mapName = mapCfg.get('name', '')
            for val in scoreDict.values():
                if val.totalScore >= MBC.datas['mineBattle_rankScoreThreshold']['value']:
                    rankList.append(val)
                else:
                    if val.guildGbId == mineWarVal.guildGbId:
                        guildMemberList.append(val)
                    if val.totalScore >= MBC.datas['mineBattle_rewardThreshold']['value']:
                        otherList.append(val)

            rankList.sort(key=lambda x: x.totalScore, reverse=True)
            guildMemberList.sort(key=lambda x: x.totalScore, reverse=True)
            
            mineWarVal.scoreRankList = rankList[:len(rankCfg)]
            for val in rankList[len(rankCfg):]: # 未上排行榜但积分超过限制的归属帮派玩家
                if val.guildGbId == mineWarVal.guildGbId:
                    mineWarVal.scoreRankList.append(val)
            mineWarVal.scoreRankList.extend(guildMemberList) # 加上归属帮派所有成员
            mineWarVal.playerScoreDict = {} # 清理

            if gameconfig.visibleConfigEnabled('mineBattle'):
                sendRankList = rankList[:len(rankCfg)]
                for i, obj in enumerate(sendRankList):
                    if i < len(rankCfg):
                        _addVal = dropAward.MailWealthVal()
                        _addVal.addWealthByItemId(rankCfg[i + 1], 1)
                        mailAssistor.sendMailToPlayers([obj.gbId], MBC.datas['mineBatte_scoreRankMail']['value'], 
                                                    extraAttach=_addVal, despArgs=(mapName,), srcType=srcType, opUUID=opUUID)
                        INFO_MSG('onEndRewardByScore send mail', mapId, obj.gbId, i + 1, rankCfg[i + 1])
                    else:
                        # 参与奖 
                        otherList.append(obj)
                
                _otherVal = dropAward.MailWealthVal()
                _otherVal.addWealthByItemId(MBC.datas['mineBattle_rewardParticipation']['value'], 1)
                # 参与奖
                def _sendOthers():
                    for obj in otherList:
                        playerId = obj.gbId
                        mailAssistor.sendMailToPlayers([playerId], MBC.datas['mineBatte_scoreRankMail']['value'],
                                                        extraAttach=_otherVal, despArgs=(mapName,), srcType=srcType, opUUID=opUUID)
                        yield lambda: None
                def _sendOthersDone():
                    INFO_MSG('MineWarStub.onEndRewardByScore _sendOthersDone mapId:', mapId)
                self.batchlyCall(_sendOthers(), 30, 0.2, _sendOthersDone)
            #
            try:
                logRankList = []
                for i, obj in enumerate(mineWarVal.scoreRankList[:len(rankCfg)]):
                    logRankList.append({'rank': i+1, 'playerGbId': obj.gbId, 'playerScore': obj.totalScore})
                LogTrackingMgr.LogTrackingMgr.MineBattle_End_Reward(self.endTime, mapId, logRankList)
            except Exception as e:
                ERROR_MSG('LogTrackingMgr.MineBattle_End_Reward error:', mapId)
                
        INFO_MSG('MineWarStub.onEndRewardByScore done')
