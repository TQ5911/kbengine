# coding: utf-8

from KBEDebug import *

import KBEngine
import gameclass
import gameengine
import gameconfig
import gameconst
import utils
import formula
import mailAssistor

import mail_mail as MAMAD
import mineBattle_config as MBC
import gamePlay_gamePlay as GGD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import gamedecorator
import mineBattle_miningArea as MBMA
import gametimer
import NPC_Pick as NPD
import LogTrackingMgr

class IMineWarBase(object):
    def __init__(self):
        self.myMineListBase = []    # 玩家拥有的矿场列表
        self.MineRevenueDict = {}  # mapId: factor
        self.mineWarStateBase = gameconst.MINE_WAR_STATE.END
        self.myGuildInfoBase = {}

    def onMineWarLogin(self):
        """
        玩家登录时调用
        """
        LOG_IFO('IMineWarBase.onMineWarLogin called for player:', self.id)
        self.reqSyncGuildData()

    def reqSyncGuildData(self):
        """
        同步帮派数据
        """
        # LOG_IFO('IMineWarBase.reqSyncGuildData called for player:', self.id)
        gameengine.getGlobalBase('MineWarStub').playerGetMineWarState(self, self.guildUUIDBase)

        self.reqGuildInfo()

    def reqGuildInfo(self):
        if self.guildUUIDBase > 0 and self.guildBox is not None:
            self.guildBox.playerGetGuildInfo(self)
        else:
            self.onPlayerGetGuildInfo({
                'guildGbId': 0,
                'guildName': '',
                'guildIcon': 0,
                'guildDspFlag': 0,
                'leaderGbId': 0,
                'leaderName': '',
            })

    def onPlayerGetGuildInfo(self, guildInfo):
        """
        获取帮派信息回调
        """
        # 检查帮派解散
        if self.myGuildInfoBase and guildInfo.get('guildGbId', 0) == 0 and self.myGuildInfoBase.get('leaderGbId', 0) == self.gbID:
            gameengine.getGlobalBase('MineWarStub').doMineWarGuildDisbanded(self.myGuildInfoBase.get('guildGbId', 0))  

        self.myGuildInfoBase = guildInfo
        LOG_IFO('IMineWarBase.onPlayerGetGuildInfo called for player:', self.id, guildInfo)

        self.cell.onCellPlayerGetGuildInfo(guildInfo)

    def onMineWarStateSync(self, state, startTime, endTime, mineList, MineRevenueDict):
        """
        矿战状态获取回调
        """
        self.myMineListBase = mineList
        self.MineRevenueDict = MineRevenueDict
        LOG_IFO('Avatar.onMineWarStateSync state:', state, 'startTime:', startTime, 'endTime:', endTime, mineList, MineRevenueDict)
        if state == gameconst.MINE_WAR_STATE.PREPARE:
            self.onMineWarPreparePlayer(state, startTime)
        elif state == gameconst.MINE_WAR_STATE.RUNNING:
            self.onMineWarStartPlayer(state, endTime)

        self.mineWarStateBase = state

        self.syncCellMineWarInfo(state)

    def onMineWarGuildChange(self):
        """
        帮派变更回调
        """
        # LOG_IFO('IMineWarBase.onGuildChange called for player:', self.id)

        # 重新请求
        self.reqSyncGuildData()

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarPreparePlayer(self, state, startTime):
        """
        MINE_WAR_STATE.PREPARE状态开始
        """
        LOG_IFO('Avatar.onMineWarPreparePlayer state:', state, 'startTime:', startTime)
        self.client.showMineWarPrepare(state, startTime - utils.curTS())

        self.syncCellMineWarInfo(state)

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarStartPlayer(self, state, endTime):
        """
        MINE_WAR_STATE.RUNNING状态开始
        """
        LOG_IFO('Avatar.onMineWarStartPlayer state:', state, 'endTime:', endTime)
        self.client.showMineWarStart(state, endTime - utils.curTS())
        
        self.informPlayerStart(endTime)

        self.syncCellMineWarInfo(state)
        
    def informPlayerStart(self, endTime):
        """
        矿战开始通知玩家
        """
        LOG_IFO('Avatar.informPlayerStart endTime:', endTime)
        key = 'MineWarInformFlag'
        if self.getWeeklyData(key):
            return
            # pass
        self.setWeeklyData(key, 1)
        
        # 邮件
        mailId = MBC.datas['mineBatte_startMail']['value']
        title = MAMAD.datas[mailId]['title']
        content = MAMAD.datas[mailId]['content']
        mailAssistor.sendMailToPlayers(
            [self.gbID],
            mailId,
            opUUID=KBEngine.genUUID64(),
            title=title, cont=content,
        )
        
        # 跑马灯
        msgId = MBC.datas['mineBatte_chatChannelMsg1']['value']
        self.onMessagePre(msgId, [])

    def onMineWarEndPlayer(self, changeInfo):
        """
        MINE_WAR_STATE.END状态开始
        """
        LOG_IFO('Avatar.onMineWarEndPlayer state:', changeInfo)
        msgId = MBC.datas['mineBatte_chatChannelMsg2']['value']

        for info in changeInfo:
            mapId = info['mapId']
            oldGuildId = info['oldGuildId']
            newGuildId = info['newGuildId']
            if newGuildId == 0:
                if mapId in self.myMineListBase:
                    self.myMineListBase.remove(mapId)
                continue
            if oldGuildId == self.guildUUIDBase and newGuildId != oldGuildId and mapId in self.myMineListBase:
                self.myMineListBase.remove(mapId)
            elif newGuildId == self.guildUUIDBase and mapId not in self.myMineListBase:
                self.myMineListBase.append(mapId)
                LOG_IFO('Avatar.onMineWarEndPlayer won mine:', self.id, mapId)

            guildRevenueRate = info.get('guildRevenueRate', {})
            if self.guildUUIDBase in guildRevenueRate:
                self.MineRevenueDict[mapId] = guildRevenueRate[self.guildUUIDBase]

            if gameconfig.visibleConfigEnabled('mineBattle'):
                # 跑马灯
                mapCfg = MBMA.datas.get(mapId, {})
                mapName = mapCfg.get('name', '')
                self.onMessagePre(utils.getTranslatedMsgId(msgId), [info['guildName'], info['leaderName'], utils.getTranslatedArg(mapName), str(info.get('leaderGbId', 0))])

                # 邮件
                mailId = MBC.datas['mineBatte_occupyMail']['value']
                title = MAMAD.datas[mailId]['title']
                content = MAMAD.datas[mailId]['content']
                mailAssistor.sendMailToPlayers(
                    [self.gbID],
                    mailId,
                    despArgs=(info['guildName'], info['leaderName'], mapName),
                    opUUID=KBEngine.genUUID64(),
                    title=title, cont=content,
                )

        # 同步cell
        self.syncCellMineWarInfo(gameconst.MINE_WAR_STATE.END)
        # 同步client
        if gameconfig.visibleConfigEnabled('mineBattle'):
            self.client.showMineWarEnd()

        # 重新拉数据
        if formula.inMineWarScene(self.baseSpaceNo):
            self.getMineWarInfo()

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarFlagBeDestroyed(self, mapId, guildGbId, destroyNum, lostMineNum):
        """
        矿战荣誉旗帜被破坏回调
        """
        #
        if self.guildUUIDBase != guildGbId:
            return
            # 
        mapName = MBMA.datas[mapId]['name']
        damageCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
        guildMsgId = MBC.datas['mineBatte_chatChannelMsg4']['value']
        self.onMessagePre(utils.getTranslatedMsgId(guildMsgId), [utils.getTranslatedArg(mapName), str(destroyNum), str(damageCfg[0])])

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarFlagAllDestroyed(self, mapId, guildName, guildGbId):
        """
        矿战荣誉旗帜被全部破坏回调
        """
        mapName = MBMA.datas[mapId]['name']
        # 帮派消息
        if self.guildUUIDBase == guildGbId:
            # 
            damageCfg = MBC.datas['mineBattle_flagDamageEffect']['value']
            guildMsgId = MBC.datas['mineBatte_chatChannelMsg5']['value']
            self.onMessagePre(utils.getTranslatedMsgId(guildMsgId), [utils.getTranslatedArg(mapName), str(damageCfg[0]), str(damageCfg[0])])
            # 减掉收益
            if mapId in self.MineRevenueDict:
                del self.MineRevenueDict[mapId]

        # 跑马灯
        msgId = MBC.datas['mineBatte_chatChannelMsg7']['value']
        self.onMessagePre(utils.getTranslatedMsgId(msgId), [guildName, utils.getTranslatedArg(mapName)])

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarFlagHpChangeWarning(self, mapId):
        """
        矿战荣誉旗帜血量变化预警回调
        """
        mapName = MBMA.datas[mapId]['name']
        msgId = MBC.datas['mineBatte_chatChannelMsg3']['value']
        self.onMessagePre(utils.getTranslatedMsgId(msgId), [utils.getTranslatedArg(mapName)])

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarFlagHpLowWarning(self, mapId):
        """
        矿战荣誉旗帜血量过低预警回调
        """
        mapName = MBMA.datas[mapId]['name']
        msgId = MBC.datas['mineBatte_chatChannelMsg6']['value']
        self.onMessagePre(utils.getTranslatedMsgId(msgId), [utils.getTranslatedArg(mapName)])

    def onMineWarLeaveGuild(self):
        """
        玩家离开帮派时调用
        """
        LOG_IFO('IMineWarBase.onMineWarLeaveGuild called for player:', self.id)
        # gameengine.getGlobalBase('MineWarStub').playerLeaveMineWarGuild(self)
        

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onMineWarHpWarning(self, spaceNo, percent):
        """
        矿战核心血量预警
        """
        if spaceNo != self.baseSpaceNo or self.guildUUIDBase <= 0:
            return
        LOG_IFO('IMineWarBase.onMineWarHpWarning called for player:', self.id, 'spaceNo:', spaceNo, 'percent:', percent)
        self.onMessagePre(MBC.datas['mineBattle_coreHpInsufficientMsg']['value'], [])
        
    def syncCellMineWarInfo(self, state):
        """
        同步矿战信息到cell
        """
        self.cell.syncMineWarInfo(state, self.myMineListBase)

    # ======================== 采矿 ========================
    def getMineWarCollectionKey(self, lineType):
        """
        获取矿战采集Key
        """
        return 'MineWarLine{}'.format(lineType)
    
    def getMineWarCollectionTime(self, lineType):
        """
        获取矿战采集时间
        """
        mineTime = 0
        limitTimeCfg = MBC.datas['mineBattle_miningPersonalDuration']['value']
        limitTime = limitTimeCfg[0]
        battleMapId = formula.getMineWarBattleArea(self.baseSpaceNo)
        if battleMapId > 0 and battleMapId in self.myMineListBase:
            limitTime = limitTimeCfg[1]
            
        mineKey = self.getMineWarCollectionKey(battleMapId)
        mineTime = self.getDailyData(mineKey, 0)
        # LOG_IFO('iMineWarBase.getMineWarCollectionTime :', self.id, battleMapId, mineTime, limitTime, mineKey)

        return limitTime * 60 - mineTime
    
    def isMineralType(self, collectionId):
        """
        是否矿战采集物
        """
        collectionCfg = NPD.datas.get(collectionId, {})
        if collectionCfg.get('type', 0) == gameconst.CollectionType.MINERAL:
            return True
        return False
    
    def mineWarPrecheckCollection(self, collectionId):
        """
        矿战采集预检查
        """
        # 不在矿场区域
        if not formula.isMineWarMineArea(self.baseSpaceNo):
            return True
        
        lineType = formula.parseLineType(self.baseSpaceNo)
        collectionList = MBC.datas['mineBattle_flagDropCollectionId']['value']
        # LOG_IFO('iMineWarBase.mineWarPrecheckCollection :', self.id, collectionId, collectionList, lineType, self.myMineListBase)
        # 矿战宝箱检查
        if collectionId in collectionList and lineType in self.myMineListBase:
            self.onMessagePre(MBC.datas['mineBattle_notPickableMsg']['value'], [])
            return False
            
        if self.isMineralType(collectionId):
            leftTime = self.getMineWarCollectionTime(lineType)
            # 采矿时间检查
            if leftTime <= 0:
                # 弹消息
                self.onMessagePre(MBC.datas['mineBattle_noEnoughTime']['value'], [])
                return False
        return True
    
    def onMineWarCollectionSuccess(self, collectionId, pickTime):
        """
        矿战采集成功回调
        """
        
        if not formula.isMineWarMineArea(self.baseSpaceNo) or not self.isMineralType(collectionId):
            return

        battleMapId = formula.getMineWarBattleArea(self.baseSpaceNo)
        if battleMapId > 0:
            mineKey = self.getMineWarCollectionKey(battleMapId)
            self.addDailyData(mineKey, pickTime)
        
            LOG_IFO('iMineWarCell.onMineWarCollectionSuccess :', self.id, 'args:', collectionId, pickTime, battleMapId, self.getDailyData(mineKey, 0))

    def onMineWarCollectionReward(self, srcType, awardId, awardVal, awardCtx):
        """
        矿战采集奖励回调
        """
        # 月卡过期
        if self.isMonthCardExpired():
            return
        battleMapId = formula.getMineWarBattleArea(self.baseSpaceNo)
        if battleMapId <= 0 or srcType != AAC_AACDD.datas.BONUS_SRC_GATHER:
            return

        num = 0
        darkIron = getattr(awardVal, 'darkIron', None)
        if darkIron:
            num = int(darkIron.data)
        LOG_IFO('iMineWarCell.onMineWarCollectionReward :', self.id, 'darkIron num:', num)
        if num > 0:
            gameengine.getGlobalBase('MineWarStub').playerCollectAward(battleMapId, num)

    def getMineWarFactor(self, collectionId=0):
        """
        获取矿战奖励加成系数
        """
        factor = 0.0
        if not formula.isMineWarMineArea(self.baseSpaceNo):
            return factor
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return factor
        if collectionId > 0 and not self.isMineralType(collectionId):
            return factor
        
        currLineType = formula.parseLineType(self.baseSpaceNo)
        for lineType, lineCfg in MBMA.datas.items():
            if currLineType in lineCfg['sceneList']:
                factor = self.MineRevenueDict.get(lineType, 0) * 0.01
                break
        # LOG_IFO('iMineWarCell.getMineWarFactor :', self.id, 'lineType:', lineType, 'factor:', factor)
        return factor
    
    # ======================== 客户端请求 ========================
    @gamedecorator.checkGameconfigEnable('mineBattle')
    @gamedecorator.limitcall(2)
    def reqMineWarInfo(self, exposed):
        """
        客户端请求矿战信息
        """
        LOG_IFO('iMineWarBase.reqMineWarInfo called for player:', self.id)
        self.getMineWarInfo()
        
    def getMineWarInfo(self):
        """"""
        gameengine.getGlobalBase('MineWarStub').playerGetMineWarInfo(self, self.guildUUIDBase)
        
    @gamedecorator.checkGameconfigEnable('mineBattle')
    def reqMineWarShareBonus(self, exposed, mapId, shareList):
        """
        客户端请求矿战分享奖励
        """
        LOG_IFO('iMineWarBase.reqMineWarShareBonus called for player:', self.id, 'mapId:', mapId, shareList)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return
        
        self.guildBox.reqShareBonusFromMineWar(mapId, self.gbID, shareList, self)

    @gamedecorator.checkGameconfigEnable('mineBattle')
    @gamedecorator.limitcall(2)
    def reqMineWarGuildMemberScore(self, exposed, lineType):
        """
        客户端请求矿战帮派成员积分
        """
        LOG_IFO('iMineWarBase.reqMineWarGuildMemberScore called for player:', self.id, 'lineType:', lineType)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return

        gameengine.getGlobalBase('MineWarStub').doGetMineWarGuildMemberScore(lineType, self, self.guildUUIDBase)
        
    @gamedecorator.checkGameconfigEnable('mineBattle')
    @gamedecorator.limitcall(5)
    def reqMineWarGuildOwnerRank(self, exposed, mapId, last):
        """
        客户端请求矿战帮派占领排名
        """
        LOG_IFO('iMineWarBase.reqMineWarGuildOwnerRank called for player:', self.id, 'mapId:', mapId, last)
        # if not formula.inMineWarScene(self.baseSpaceNo):
        #     return
        gameengine.getGlobalBase('MineWarStub').doGetMineWarGuildOwnerRank(mapId, self, self.myGuildInfoBase, last)
                
    @gamedecorator.checkGameconfigEnable('mineBattle')
    @gamedecorator.limitcall(5)
    def reqMineWarGuildPlayerRank(self, exposed, mapId, lastRank):
        """
        客户端请求矿战个人贡献排名
        """
        LOG_IFO('iMineWarBase.reqMineWarGuildPlayerRank called for player:', self.id, 'mapId:', mapId, lastRank)
        # if not formula.inMineWarScene(self.baseSpaceNo):
        #     return

        gameengine.getGlobalBase('MineWarStub').doGetMineWarGuildPlayerRank(mapId, self, self.gbID, self.getRoleCacheAttr('name'), self.myGuildInfoBase, lastRank)
        
    def onMineWarKillCore(self, lineType):
        """
        矿战摧毁核心回调
        """
        LOG_IFO('iMineWarBase.onMineWarKillCore called for player:', self.id, 'mapId:', lineType)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return
        
        if not self.myGuildInfoBase:
            self.addTimerCB(0.2, 'onMineWarKillCore', (lineType), gametimer.TIMER_TAG_MINE_WAR_KILL_CORE_DALAY)
            LOG_IFO('onMineWarKillCore no guild info, retry later:', self.id, self.guildUUIDBase)
            return

        gameengine.getGlobalBase('MineWarStub').doOnMineWarKillCoreForGuild(lineType, self, self.myGuildInfoBase)

        LogTrackingMgr.LogTrackingMgr.MineBattle_KillCore(lineType, self.guildUUIDBase, self.gbID)

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def reqMineWarCollectInfo(self, exposed):
        if not formula.isMineWarMineArea(self.baseSpaceNo):
            return
        lineType = formula.parseLineType(self.baseSpaceNo)
        leftTime = self.getMineWarCollectionTime(lineType)
        revenue = self.getMineWarFactor() * 100

        self.client.onGetMineWarCollectInfo(leftTime, revenue)

    def reqMineWarFlagHp(self, exposed, mapId):
        """
        客户端请求矿战荣誉旗帜血量
        """
        # LOG_IFO('iMineWarBase.reqMineWarFlagHp called for player:', self.id, 'mapId:', mapId)
        gameengine.getGlobalBase('MineWarStub').doGetMineWarFlagHp(mapId, self)

    # ======================================  客户端回调 ======================================

    def onMineWarGuildOwnerRankBase(self, selfGuildInfo, rankList):
        """
        处理矿战帮派占领排名回调
        """
        if not rankList:
            self.client.onMineWarGuildOwnerRank(selfGuildInfo, rankList)
            return
        
        batchNum = gameconst.GUILD_MEMBER_SEND_MAX
        def _iter(_datas):
            while _datas:
                sendList = _datas[:batchNum]
                _datas = _datas[batchNum:]
                # LOG_IFO('onMineWarGuildOwnerRank send rank to player:', selfGuildInfo, sendList)
                self.client.onMineWarGuildOwnerRank(selfGuildInfo, sendList)
                yield lambda: None
        self._addPacketSendTask(_iter(rankList))

    def onMineWarGuildPlayerRankBase(self, selfGuildInfo, rankList):
        """
        处理矿战所有成员排名回调
        """
        if not rankList:
            self.client.onMineWarGuildPlayerRank(selfGuildInfo, rankList)
            return
        
        batchNum = gameconst.GUILD_MEMBER_SEND_MAX
        def _iter(_datas):
            while _datas:
                sendList = _datas[:batchNum]
                _datas = _datas[batchNum:]
                # LOG_IFO('onMineWarGuildPlayerRank send rank to player:', selfGuildInfo, sendList)
                self.client.onMineWarGuildPlayerRank(selfGuildInfo, sendList)
                yield lambda: None
        self._addPacketSendTask(_iter(rankList))
