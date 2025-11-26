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


class IMineWarBase(object):
    def __init__(self):
        self.myMineList = []    # 玩家拥有的矿场列表
        self.MineTimeDict = {}  # mapId: factor
        self.mineWarState = gameconst.MINE_WAR_STATE.END

    def onMineWarLogin(self):
        """
        玩家登录时调用
        """
        INFO_MSG('IMineWarBase.onMineWarLogin called for player:', self.id)
        gameengine.getGlobalBase('MineWarStub').playerGetMineWarState(self, self.guildUUIDBase)

    def onMineWarStateSync(self, state, startTime, endTime, mineList, mineTimeMap):
        """
        矿战状态获取回调
        """
        self.myMineList = mineList
        self.MineTimeDict = mineTimeMap
        INFO_MSG('Avatar.onMineWarStateSync state:', state, 'startTime:', startTime, 'endTime:', endTime, mineList, mineTimeMap)
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
        self.client.onOfficialMessage(95, content, 1, [], 0)
        
    def onMineWarEndPlayer(self, changeInfo):
        """
        MINE_WAR_STATE.END状态开始
        """
        INFO_MSG('Avatar.onMineWarEndPlayer state:', changeInfo)
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

            ownerTimeMap = info.get('ownerTimeMap', {})
            if self.guildUUIDBase in ownerTimeMap:
                self.MineTimeDict[mapId] = ownerTimeMap[self.guildUUIDBase]
        
        # 同步cell
        self.syncCellMineWarInfo(gameconst.MINE_WAR_STATE.END)

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
        self.client.onOfficialMessage(95, '测试测试', 1, [], 0)
        return 'MineWarLine{}'.format(lineType)
    
    def mineWarPrecheckCollection(self, collectionId):
        """
        矿战采集预检查
        """

        # 收集物类型检查 =====todo 不是相关物品得返回True
        
        # 不在矿场
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return True
        
        lineType = formula.getLineType(self.baseSpaceNo)
        mineKey = self.getMineWarCollectionKey(lineType)
        mineTime = self.getDailyData(mineKey, 0)

        limitTimeCfg = MBC.datas['mineBattle_miningPersonalDuration']['value']
        limitTime = limitTimeCfg[0] if lineType not in self.myMineList else limitTimeCfg[1]

        # 采矿事件检查
        if mineTime >= limitTime * 60:
            # 弹消息 todo

            return False
    
        return True
    
    def onMineWarCollectionSuccess(self, collectionId, pickTime):
        """
        矿战采集成功回调
        """
        INFO_MSG('iMineWarCell.onMineWarCollectionSuccess called for player:', self.id, 'args:', collectionId, pickTime)
        if not formula.isMineWarSpace(self.baseSpaceNo):
            return

        lineType = formula.getLineType(self.baseSpaceNo)
        mineKey = self.getMineWarCollectionKey(lineType)
        self.addDailyData(mineKey, pickTime)

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
        elif lineType in self.MineTimeDict:
            factor = self.MineTimeDict[lineType] * 0.01

        return factor