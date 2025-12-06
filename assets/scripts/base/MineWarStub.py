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
            spaceMgrbox.onRegisterMineWarSpaceMgr(self.mineMapData[mapId].getGuildGbId(), self.state)
    
    def _calcState(self):
        now = utils.getNow()
        self.startOffsetSec = utils.getMineWarStartOffsetSec()
        self.endOffsetSec = utils.getMineWarEndOffsetSec()
        self.startTime = utils.getCurrentWeekTS(offsetSec=self.startOffsetSec)
        self.endTime = utils.getCurrentWeekTS(offsetSec=self.endOffsetSec)
        if self.endTime <= now:
            self.startTime += gameconst.ONE_WEEK_SECONDS
            self.endTime += gameconst.ONE_WEEK_SECONDS
        prepareTime = self.startTime - self.prepareNeed

        if self.gmDisableMineWar:
        # if True:
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
        # self._transferMineWarPersonnel()

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
                mapCfg = GGD.datas.get(mapId, {})
                mapName = mapCfg.get('name', '')
                currGuildInfo = mineWarVal.currGuildInfo
                mineWarVal.addMineWarEvent(2, [currGuildInfo.leaderName, mapName])

            guildRevenue = {}
            for guildId, guildVal in mineWarVal.guildOwnerDict.items():
                if guildId == mineWarVal.currGuildInfo.guildGbId:
                    guildVal.revenue = mineWarVal.currGuildInfo.revenue
                else:
                    guildVal.revenue = int(min((guildVal.ownerTime // timeCfg[0]) * timeCfg[1], timeCfg[2]))
                guildRevenue[guildId] = guildVal.revenue
        
            changeDict['leaderName'] = mineWarVal.currGuildInfo.leaderName
            changeDict['guildRevenueRate'] = guildRevenue
            changeInfo.append(changeDict)

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

    def onRewardMineWar(self, mapId, oldGuildId, newGuildId):
        INFO_MSG('MineWarStub.onRewardMineWar mapId:', mapId, 'oldGuildId:', oldGuildId, 'newGuildId:', newGuildId)
        # 奖励矿战胜利帮派成员
        spaceMgrbox = self.mineMapData[mapId].getSpaceMgrbox()
        if spaceMgrbox:
            spaceMgrbox.rewardMineWarGuildMembers(oldGuildId, newGuildId)

    def onMineWarFlagBeKill(self, mapId, guildName, killerName):
        # 旗帜被毁
        mineWarVal = self.mineMapData.get(mapId, None)
        if mineWarVal is None:
            return
        # 暂存
        mineWarVal.onFlagBeDestroyed()
        mineWarVal.addMineWarEvent(3, [guildName, killerName])

        guildInfo = mineWarVal.guildOwnerDict.get(mineWarVal.getGuildGbId(), None)
        guildName = getattr(guildInfo, 'guildName', '')
        
        damageCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
        mineWarVal.addMineWarEvent(4, [str(mineWarVal.flagDestroyedNum), str(damageCfg[0]), guildName])
        # 战报
        if mineWarVal.flagDestroyedNum == damageCfg[0]:
            mineWarVal.addMineWarEvent(5, [str(mineWarVal.flagDestroyedNum), str(damageCfg[0]), guildName])
            mineWarVal.onFlagAllDestroyed()


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
        mineWarVal.flagHp = hp

    def playerGetMineWarState(self, playerBox, guildId):
        mineList = []
        MineRevenueDict = {}

        for mapId, Val in self.mineMapData.items():
            if Val.getGuildGbId() == guildId:
                mineList.append(mapId)
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
            box.base.onMessagePre(MBC.datas['mineBattle_notEnoughStock']['value'], [])
            box.client.onMineWarShareBonusResult(False)
            return
        
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_MINE_WAR_GUILD_SHARE
        itemId = MBC.datas['mineBattle_MoneyID']['value']
        for val in shareList:
            num = val['bonusNum']
            mapVal.allCollectNum -= num
            playerGbId = val['playerGbId']
            awardVal = dropAward.MailWealthVal()
            awardVal.addWealthByItemId(itemId, num)
            mailAssistor.sendMailToPlayers([playerGbId],
                                          MBC.datas['mineBatte_dividendMail']['value'],
                                          extraAttach=awardVal,
                                          srcType=srcType, opUUID=opUUID)
            
        box.client.onMineWarShareBonusResult(True)
        # 重新拉下数据
        self.playerGetMineWarInfo(box, srcGbId)

    
    def doGetMineWarGuildOwnerRank(self, mapId, playerBox, guildInfo):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        
        selfRankInfo = None
        rankList = []
        if self.state == gameconst.MINE_WAR_STATE.RUNNING and utils.getNow() - mapVal.coreDestroyedTime > 5:
            mapVal.calcOwnerTime()
            ownerList = list(mapVal.guildOwnerDict.values())
            ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
            ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
            mapVal.ownerRankList = ownerList    # 暂存
        elif len(mapVal.ownerRankList) == 0:
            ownerList = list(mapVal.guildOwnerDict.values())
            ownerList.sort(key=lambda x: x.ownerTime, reverse=True)
            ownerList = ownerList[:MBC.datas['mineBatte_rankGuildNum']['value']]
            mapVal.ownerRankList = ownerList    # 暂存
        else:
            ownerList = mapVal.ownerRankList

        for idx, ownerVal in enumerate(ownerList):
            val = ownerVal.toSaveDict()
            val['rankId'] = idx + 1
            rankList.append(val)

            if guildInfo['guildGbId'] == ownerVal.guildGbId:
                selfRankInfo = val

        if selfRankInfo is None:
            selfRankInfo = MineWarInfo.MineWarGuildVal().initFromDict(guildInfo).toSaveDict()
            selfRankInfo['rankId'] = 0
        
        INFO_MSG('MineWarStub.doGetMineWarGuildOwnerRank response to player:', playerBox.id, guildInfo, selfRankInfo, rankList)
        playerBox.client.onMineWarGuildOwnerRank(selfRankInfo, rankList)

            
    def doGetMineWarGuildPlayerRank(self, mapId, playerBox, playerGbId, playerName, guildInfo):
        mapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        selfGuildInfo = None
        scoreDict = mapVal.playerScoreDict

        rankList = []
        if self.state == gameconst.MINE_WAR_STATE.RUNNING:
            scoreList = list(scoreDict.values())
            scoreList.sort(key=lambda x: x.totalScore, reverse=True)
            scoreList = scoreList[:MBC.datas['mineBatte_rankPersonNum']['value']]
            mapVal.scoreRankList = scoreList
        else:
            scoreList = mapVal.scoreRankList
        for idx, val in enumerate(scoreList):
            val = val.getData()
            val['rankId'] = idx + 1
            rankList.append(val)
            if val['gbId'] == playerGbId:
                selfGuildInfo = val

        if selfGuildInfo is None:
            if playerGbId in scoreDict:
                selfGuildInfo = scoreDict[playerGbId].getData()
            else:
                selfGuildInfo = MineWarInfo.MineWarScore(gbId=playerGbId, name=playerName, 
                                                        guildName=guildInfo.get('guildName', ''),
                                                        guildIcon=guildInfo.get('guildIcon', 0),
                                                        guildDspFlag=guildInfo.get('guildDspFlag', 0)).getData()
            selfGuildInfo['rankId'] = 0
        
        INFO_MSG('MineWarStub.doGetMineWarGuildPlayerRank response to player:', playerBox.id, guildInfo, selfGuildInfo, rankList)
        playerBox.client.onMineWarGuildPlayerRank(selfGuildInfo, rankList)

        
    def addMineWarScore(self, mapId, playerGbId, playerName, guildName, guildIcon, guildDspFlag, score, scoreType):
        if self.state != gameconst.MINE_WAR_STATE.RUNNING:
            return
        
        mapVal: MineWarInfo.MineWarMapVal = self.mineMapData.get(mapId, None)
        if mapVal is None:
            return
        
        mapVal.addMineWarScoreVal(playerGbId, playerName, guildName, guildIcon, guildDspFlag, score, scoreType)

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
            mapCfg = GGD.datas.get(mapId, {})
            mapName = mapCfg.get('name', '')
            for val in scoreDict.values():
                if val.totalScore >= MBC.datas['mineBattle_rankScoreThreshold']['value']:
                    rankList.append(val)
                elif val.totalScore >= MBC.datas['mineBattle_rewardThreshold']['value']:
                    otherList.append(val)
            rankList.sort(key=lambda x: x.totalScore, reverse=True)

            rankList = rankList[:len(rankCfg)]
            mineWarVal.scoreRankList = rankList
            mineWarVal.playerScoreDict = {} # 清理
            res = []
            for i, obj in enumerate(rankList):
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
            for obj in otherList:
                playerId = obj.gbId
                mailAssistor.sendMailToPlayers([playerId], MBC.datas['mineBatte_scoreRankMail']['value'],
                                                extraAttach=_otherVal, despArgs=(mapName,), srcType=srcType, opUUID=opUUID)
                
        INFO_MSG('MineWarStub.onEndRewardByScore done')
