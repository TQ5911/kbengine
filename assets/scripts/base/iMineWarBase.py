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


class IMineWarBase(object):
    def __init__(self):
        self.myMineList = []    # 玩家拥有的矿场列表
        self.MineRevenueDict = {}  # mapId: factor
        self.mineWarState = gameconst.MINE_WAR_STATE.END

    def onMineWarLogin(self):
        """
        玩家登录时调用
        """
        INFO_MSG('IMineWarBase.onMineWarLogin called for player:', self.id)
        gameengine.getGlobalBase('MineWarStub').playerGetMineWarState(self, self.guildUUIDBase)

    def onMineWarStateSync(self, state, startTime, endTime, mineList, MineRevenueDict):
        """
        矿战状态获取回调
        """
        self.myMineList = mineList
        self.MineRevenueDict = MineRevenueDict
        INFO_MSG('Avatar.onMineWarStateSync state:', state, 'startTime:', startTime, 'endTime:', endTime, mineList, MineRevenueDict)
        if state == gameconst.MINE_WAR_STATE.PREPARE:
            self.onMineWarPreparePlayer(state, startTime)
        elif state == gameconst.MINE_WAR_STATE.RUNNING:
            self.onMineWarStartPlayer(state, endTime)


    def onMineWarPreparePlayer(self, state, startTime):
        """
        MINE_WAR_STATE.PREPARE状态开始
        """
        INFO_MSG('Avatar.onMineWarPreparePlayer state:', state, 'startTime:', startTime)
        self.client.showMineWarPrepare(state, startTime - utils.getNow())
        
        self.syncCellMineWarInfo(state)

    def onMineWarStartPlayer(self, state, endTime):
        """
        MINE_WAR_STATE.RUNNING状态开始
        """
        INFO_MSG('Avatar.onMineWarStartPlayer state:', state, 'endTime:', endTime)
        self.client.showMineWarStart(state, endTime - utils.getNow())
        
        self.syncCellMineWarInfo(state)
        
        self.informPlayerStart(endTime)
        
    def informPlayerStart(self, endTime):
        """
        矿战开始通知玩家
        """
        INFO_MSG('Avatar.informPlayerStart endTime:', endTime)
        key = 'MineWarInformFlag'
        if self.getWeeklyData(key):
            # return
            pass
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
        INFO_MSG('Avatar.onMineWarEndPlayer state:', changeInfo)
        msgId = MBC.datas['mineBatte_chatChannelMsg2']['value']

        for info in changeInfo:
            mapId = info['mapId']
            oldGuildId = info['oldGuildId']
            newGuildId = info['newGuildId']
            if newGuildId == 0:
                if mapId in self.myMineList:
                    self.myMineList.remove(mapId)
                continue
            if oldGuildId == self.guildUUIDBase and newGuildId != oldGuildId and mapId in self.myMineList:
                self.myMineList.remove(mapId)
            elif newGuildId == self.guildUUIDBase and mapId not in self.myMineList:
                self.myMineList.append(mapId)
                INFO_MSG('Avatar.onMineWarEndPlayer won mine:', self.id, mapId)

            guildRevenueRate = info.get('guildRevenueRate', {})
            if self.guildUUIDBase in guildRevenueRate:
                self.MineRevenueDict[mapId] = guildRevenueRate[self.guildUUIDBase]

            mapCfg = GGD.datas.get(mapId, {})
            mapName = mapCfg.get('name', '')
            self.onMessagePre(utils.getNeedTranslateMsgId(msgId), [info['leaderName'], mapName])
        
        # 同步cell
        self.syncCellMineWarInfo(gameconst.MINE_WAR_STATE.END)
        # 同步client
        self.client.showMineWarEnd()

        # 重新拉数据
        if formula.isMineWarSpace(self.baseSpaceNo):
            self.getMineWarInfo()

    def onMineWarLeaveGuild(self):
        """
        玩家离开帮派时调用
        """
        INFO_MSG('IMineWarBase.onMineWarLeaveGuild called for player:', self.id)
        # gameengine.getGlobalBase('MineWarStub').playerLeaveMineWarGuild(self)
        

    def onMineWarHpWarning(self, spaceNo, percent):
        """
        矿战核心血量预警
        """
        if spaceNo != self.baseSpaceNo or self.guildUUIDBase <= 0:
            return
        INFO_MSG('IMineWarBase.onMineWarHpWarning called for player:', self.id, 'spaceNo:', spaceNo, 'percent:', percent)
        self.onMessagePre(MBC.datas['mineBattle_coreHpInsufficientMsg']['value'], [])
        
    def syncCellMineWarInfo(self, state):
        """
        同步矿战信息到cell
        """
        self.cell.syncMineWarInfo(state, self.myMineList)

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
        mineKey = self.getMineWarCollectionKey(lineType)
        mineTime = self.getDailyData(mineKey, 0)
        limitTimeCfg = MBC.datas['mineBattle_miningPersonalDuration']['value']
        limitTime = limitTimeCfg[0] if lineType not in self.myMineList else limitTimeCfg[1]

        return limitTime * 60 - mineTime
    
    def mineWarPrecheckCollection(self, collectionId):
        """
        矿战采集预检查
        """

        # 收集物类型检查 =====todo 不是相关物品得返回True
        
        # 不在矿场
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return True
        
        lineType = formula.getLineType(self.baseSpaceNo)
        # 矿战宝箱检查  # ==todo
        if collectionId == 1000001 and lineType in self.myMineList:
            self.onMessagePre(MBC.datas['mineBattle_notPickableMsg']['value'], [])
            return False
            
        leftTime = self.getMineWarCollectionTime(lineType)
        # 采矿时间检查
        if leftTime <= 0:
            # 弹消息
            self.onMessagePre(MBC.datas['mineBattle_notEnoughTime']['value'], [])
            return False
    
        return True
    
    def onMineWarCollectionSuccess(self, collectionId, pickTime):
        """
        矿战采集成功回调
        """
        
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return

        lineType = formula.getLineType(self.baseSpaceNo)
        mineKey = self.getMineWarCollectionKey(lineType)
        self.addDailyData(mineKey, pickTime)

        INFO_MSG('iMineWarCell.onMineWarCollectionSuccess :', self.id, 'args:', collectionId, pickTime, self.getDailyData(mineKey, 0))

    def onMineWarCollectionReward(self, srcType, awardId, awardVal, awardCtx):
        """
        矿战采集奖励回调
        """
        # 月卡过期
        # if self.isMonthCardExpired():
        #     return
        
        if not formula.isMineWarSpace(self.baseSpaceNo) or srcType != AAC_AACDD.datas.BONUS_SRC_GATHER:
            return

        num = 0
        darkIron = getattr(awardVal, 'darkIron', None)
        if darkIron:
            num = int(darkIron.data)
        INFO_MSG('iMineWarCell.onMineWarCollectionReward :', self.id, 'darkIron num:', num)
        if num > 0:
            gameengine.getGlobalBase('MineWarStub').playerCollectAward(formula.getLineType(self.baseSpaceNo), num)

    def getMineWarFactor(self):
        """
        获取矿战奖励加成系数
        """
        factor = 0.0
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return factor
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return factor
        
        lineType = formula.getLineType(self.baseSpaceNo)
        if lineType in self.myMineList:
            factor = MBC.datas['mineBattle_incomeCoefficient']['value'] - 1.0
        elif lineType in self.MineRevenueDict:
            factor = self.MineRevenueDict[lineType] * 0.01
        # INFO_MSG('iMineWarCell.getMineWarFactor :', self.id, 'lineType:', lineType, 'factor:', factor)
        return factor
    
    # ======================== 客户端请求 ========================
    def reqMineWarInfo(self, exposed):
        """
        客户端请求矿战信息
        """
        INFO_MSG('iMineWarBase.reqMineWarInfo called for player:', self.id)
        self.getMineWarInfo()
        
    def getMineWarInfo(self):
        """"""
        gameengine.getGlobalBase('MineWarStub').playerGetMineWarInfo(self, self.guildUUIDBase)
        
    def reqMineWarShareBonus(self, exposed, mapId, shareList):
        """
        客户端请求矿战分享奖励
        """
        INFO_MSG('iMineWarBase.reqMineWarShareBonus called for player:', self.id, 'mapId:', mapId, shareList)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return
        
        self.guildBox.reqShareBonusFromMineWar(mapId, self.gbID, shareList, self)
        
        
    def reqMineWarGuildOwnerRank(self, exposed, mapId):
        """
        客户端请求矿战帮派占领排名
        """
        INFO_MSG('iMineWarBase.reqMineWarGuildOwnerRank called for player:', self.id, 'mapId:', mapId)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return
        # gameengine.getGlobalBase('MineWarStub').doGetMineWarGuildOwnerRank(mapId, self, {})
        
        self.guildBox.getMineWarGuildOwnerRank(mapId, self)
        
    def reqMineWarGuildPlayerRank(self, exposed, mapId):
        """
        客户端请求矿战个人贡献排名
        """
        INFO_MSG('iMineWarBase.reqMineWarGuildPlayerRank called for player:', self.id, 'mapId:', mapId)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return

        self.guildBox.getMineWarGuildPlayerRank(mapId, self, self.gbID, self.getRoleCacheAttr('name'))
        
    def onMineWarKillCore(self, lineType):
        """
        矿战摧毁核心回调
        """
        INFO_MSG('iMineWarBase.onMineWarKillCore called for player:', self.id, 'mapId:', lineType)
        if self.guildUUIDBase <= 0 or self.guildBox is None:
            return
        
        self.guildBox.onMineWarKillCoreForGuild(lineType, self)

    def reqMineWarCollectInfo(self, exposed):
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return
        lineType = formula.getLineType(self.baseSpaceNo)
        leftTime = self.getMineWarCollectionTime(lineType)
        revenue = self.getMineWarFactor() * 100

        self.client.onGetMineWarCollectInfo(leftTime, revenue)