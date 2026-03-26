# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import utils
import gameconst
import gameengine
import gametimer
import CollectionCheckContext
import gamedecorator
import math
import random
import dungeonSrc
import gamePlay_set as GP_SD

import mineBattle_config as MBC
import mineBattle_miningArea as MBMA

import outsideRecord

class IMineWarCell(object):
    def __init__(self):
        
        self.addListener('onDead', self.id, 'onMineWarPlayerDead')
        self.mineWarCanAttack = False
        self.scoreTimer = 0
        
        self.mineWarState = gameconst.MINE_WAR_STATE.END
        self.myMineList = []  # mapId: factor

        self.myGuildInfo = {}

    def onCellPlayerGetGuildInfo(self, guildInfo):
        """
        获取矿战公会信息回调
        """
        self.myGuildInfo = guildInfo
        INFO_MSG('iMineWarCell.onCellPlayerGetGuildInfo called for player:', self.id, guildInfo)

    # 同步矿战信息
    def syncMineWarInfo(self, state, myMineList):
        INFO_MSG('iMineWarCell.syncMineWarInfo:', self.id, 'state:', state, 'myMineList:', myMineList)
        self.mineWarState = state
        self.myMineList = myMineList

        # 同步怪物信息
        if formula.isMineWarSpace(self.spaceNo):
            self._callback(1, 'syncMineWarMonsterInfo', (), gametimer.TIMER_TAG_MINE_WAR_SYNC_MONSTER)
            if state == gameconst.MINE_WAR_STATE.RUNNING:
                self.spaceMgr.checkAndChangeCamp(self)

        self.mineWarCanAttack = state == gameconst.MINE_WAR_STATE.RUNNING

    def syncMineWarMonsterInfo(self):
        """
        同步矿战怪物信息
        """
        if not formula.isMineWarSpace(self.spaceNo):
            DEBUG_MSG('iMineWarCell.syncMineWarMonsterInfo called for player:', self.id, self.spaceNo)
            return
        self.spaceMgr.sendMineWarMonsterInfo(self)
        
    def onMineWarTeleportCheck(self, lineType):
        
        if lineType not in MBMA.datas.keys():
            return True
        
        if self.mineWarState != gameconst.MINE_WAR_STATE.PREPARE:
            return True
        
        if lineType in self.myMineList:
            return True
        
        startOffset = utils.getMineWarStartOffsetSec()
        prepareNeedSec = MBC.datas['mineBattle_transferPersonnelTime']['value'] * 60
        startTime = utils.getCurrentWeekTS(offsetSec=startOffset)
        nowTime = utils.getNow()
        if nowTime > startTime or nowTime < startTime - prepareNeedSec:
            return True
        # INFO_MSG('iMineWarCell.onMineWarTeleportCheck called for player:', self.id, lineType, self.mineWarState, self.myMineList)
        # 通知
        self.base.onMessagePre(MBC.datas['mineBattle_forbidTeleportMsg']['value'], [])
        return False

    def onMineWarPlayerDead(self, event, *callbackArgs):
        """
        矿战玩家死亡回调
        """
        
        if not formula.isMineWarSpace(self.spaceNo):
            return
        
        killerId = event.triggerRoleId
        selfId = event.targetRoleId
        INFO_MSG('iMineWarCell.onMineWarPlayerDead called for player:', selfId, 'killerId:', killerId)
        if killerId == selfId:
            return
        # 通知矿战stub
        self.spaceMgr.onMineWarPlayerBeKill(killerId, selfId)

    @gamedecorator.checkGameconfigEnable('mineBattle')
    def onEnterMineWarSpace(self):
        """
        进入矿战场景回调（战斗期间）
        """
        
        INFO_MSG('iMineWarCell.onEnterMineWarSpace called for player:', self.id)
        # self.base.onMessagePre(MBC.datas['mineBattle_teleportSafeZoneMsg']['value'], [])
        takePartScore = MBC.datas['mineBattle_takePartScore']['value']
        self.scoreTimer = self.pyAddTimer(0, takePartScore[0], gametimer.MINE_WAR_PLAYER_GET_SCORE)

    def onLeaveMineWarSpace(self):
        """
        离开矿战场景回调
        """
        
        INFO_MSG('iMineWarCell.onLeaveMineWarSpace called for player:', self.id, self.spaceNo)
        self.cancelMineWarScoreTimer()

    def mineWarPlayerGetScoreTick(self):
        """
        矿战玩家定时获取积分
        """
        if not formula.isMineWarSpace(self.spaceNo):
            return
        if not hasattr(self.spaceMgr, 'onMineWarPlayerTakePartAward'):
            self.cancelMineWarScoreTimer()
            return
        # 重新拉数据
        if not self.myGuildInfo:
            self.base.reqSyncGuildData()

        self.spaceMgr.onMineWarPlayerTakePartAward(self)

    def cancelMineWarScoreTimer(self):
        """
        取消矿战积分定时器
        """
        if hasattr(self, 'scoreTimer'):
            if self.scoreTimer:
                DEBUG_MSG('iMineWarCell.cancelMineWarScoreTimer called for player:', self.id, self.spaceNo)
                self.pyDelTimer(self.scoreTimer, gametimer.MINE_WAR_PLAYER_GET_SCORE)
                self.scoreTimer = 0

    def getMineWarRebornPos(self, mapId, posType):
        """
        矿战复活点
        """
        dunSData = utils.getDunStructureModuleData(mapId)
        if posType not in dunSData:
            return None, None
        _data = random.choice(list(dunSData[posType].values()))
        _enterPos, _enterDir = formula.bornPosFromData(_data), (0, 0, _data['Dir'])
        if _enterDir is not None:
            _enterDir = (0, 0, _enterDir[2] * math.pi / 180)

        return _enterPos, _enterDir
    
    def mineWarTryRelive(self):
        """
        矿战尝试复活
        """
        if not formula.isMineWarSpace(self.spaceNo):
            return False
        _mapId = formula.getMapId(self.spaceNo)
        reliveHp = int(self.fullHp * GP_SD.datas['resurrectHP']['value'] / 100)
        if self.spaceMgr.mineWarGuildId > 0 and self.myGuildInfo.get('guildGbId', 0) == self.spaceMgr.mineWarGuildId:
            _pos, _dir = self.getMineWarRebornPos(_mapId, 'RebornPos')
            if not _pos:
                return False
            self.reliveToPos(_pos, _dir, reliveHp, None)
            return True
        else:
            mineWarArea = formula.getMineWarMineArea(self.spaceNo)
            if not mineWarArea:
                return False
            destSceneId = mineWarArea[-2]
            _pos, _dir = self.getMineWarRebornPos(destSceneId, 'AttackRebornPos')
            if not _pos:
                return False
            _src = dungeonSrc.BasicDungeonSrc()
            self.doEnterWorldLine(destSceneId, 0, _src, 0, _pos, _dir)
            return True
        
    def mineWarChangeOutsideRecord(self, _m_records):
        """
        退出到矿战场景，做转换
        """
        # 非战斗期间
        startOffset = utils.getMineWarStartOffsetSec()
        startTime = utils.getCurrentWeekTS(offsetSec=startOffset)
        endOffset = utils.getMineWarEndOffsetSec()
        endTime = utils.getCurrentWeekTS(offsetSec=endOffset)
        prepareNeedSec = MBC.datas['mineBattle_transferPersonnelTime']['value'] * 60
        nowTime = utils.getNow()
        if nowTime < startTime - prepareNeedSec or nowTime > endTime:
            return

        mapId = None
        for i_mapId in reversed(list(_m_records)):
            # 大世界分线
            if i_mapId in gameconst.MapIdDef.mapWorldSet and i_mapId in MBMA.datas.keys():
                mapId = i_mapId
                break

        if not mapId:
            return
        destSpaceNo = formula.getLineSpaceNo(i_mapId)
        mineWarArea = formula.getMineWarMineArea(destSpaceNo)
        if not mineWarArea:
            return
        destSceneId = mineWarArea[-2]
        _pos, _dir = self.getMineWarRebornPos(destSceneId, 'AttackRebornPos')
        record = _m_records[mapId]
        _m_records[destSceneId] = outsideRecord.OutsideRecord(
            formula.getLineSpaceNo(destSceneId), _pos, _dir, record.hp, record.mp, record.isDie
        )
        _m_records.pop(mapId)
        self.base.onMessagePre(MBC.datas['mineBattle_teleportMsg']['value'], [])
    
    @gamedecorator.checkGameconfigEnable('mineBattle')
    def getMineWarMonsterInfo(self, exposed):
        if not formula.isMineWarSpace(self.spaceNo):
            return
         
        self.spaceMgr.sendMineWarMonsterInfo(self)

    def mineWarCellPrecheckCollection(self, collectionId):
        """
        矿战采集预检查
        """
        if not formula.isMineWarMineArea(self.spaceNo):
            return True
        
        collectionList = MBC.datas['mineBattle_flagDropCollectionId']['value']
        #  
        # 矿战宝箱检查
        if collectionId in collectionList and self.mineWarCamp == gameconst.MINE_WAR_CAMP.CAMP_DEFEND:
            self.base.onMessagePre(MBC.datas['mineBattle_notPickableMsg']['value'], [])
            return False
        
        return True