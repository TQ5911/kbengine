# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import formula
import utils
import gameconst
import gameengine
import gametimer
import CollectionCheckContext

import mineBattle_config as MBC
import mineBattle_miningArea as MBMA

class IMineWarCell(object):
    def __init__(self):
        
        self.addListener('onDead', self.id, 'onMineWarPlayerDead')
        self.mineWarCanAttack = False
        self.scoreTimer = 0
        
        self.mineWarState = gameconst.MINE_WAR_STATE.END
        self.myMineList = {}  # mapId: factor

    # 同步矿战信息
    def syncMineWarInfo(self, state, myMineList):
        INFO_MSG('iMineWarCell.syncMineWarInfo:', self.id, 'state:', state, 'myMineList:', myMineList)
        self.mineWarState = state
        self.myMineList = myMineList
        
    def onMineWarTeleportCheck(self, lineType):
        
        if lineType not in MBMA.datas.keys():
            return True
        
        if self.mineWarState != gameconst.MINE_WAR_STATE.PREPARE:
            return True
        
        if lineType in self.myMineList:
            return True
        INFO_MSG('iMineWarCell.onMineWarTeleportCheck called for player:', self.id, lineType, self.mineWarState, self.myMineList)
        startOffset = utils.getMineWarStartOffsetSec()
        prepareNeedSec = utils.getMineWarPrepareNeedSec()
        startTime = utils.getCurrentWeekTS(offsetSec=startOffset)
        nowTime = utils.getNow()
        # if nowTime > startTime or nowTime < startTime - prepareNeedSec:
        #     return True
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

    def onEnterMineWarSpace(self):
        """
        进入矿战场景回调
        """
        
        INFO_MSG('iMineWarCell.onEnterMineWarSpace called for player:', self.id)
        self.mineWarCanAttack = True
        self.base.onMessagePre(MBC.datas['mineBattle_teleportSafeZoneMsg']['value'], [])

        takePartScore = MBC.datas['mineBattle_takePartScore']['value']
        self.scoreTimer = self.pyAddTimer(0, takePartScore[0], gametimer.MINE_WAR_PLAYER_GET_SCORE)

    def onLeaveMineWarSpace(self):
        """
        离开矿战场景回调
        """
        
        INFO_MSG('iMineWarCell.onLeaveMineWarSpace called for player:', self.id)
        self.mineWarCanAttack = False
        self.cancelMineWarScoreTimer()

    def mineWarPlayerGetScoreTick(self):
        """
        矿战玩家定时获取积分
        """
        if self.guildUUID <= 0:
            return
        if not hasattr(self.spaceMgr, 'onMineWarPlayerTakePartAward'):
            self.cancelMineWarScoreTimer()
            return
        self.spaceMgr.onMineWarPlayerTakePartAward(self)

    def cancelMineWarScoreTimer(self):
        """
        取消矿战积分定时器
        """
        if self.scoreTimer:
            self.pyDelTimer(self.scoreTimer, gametimer.MINE_WAR_PLAYER_GET_SCORE)
            self.scoreTimer = 0
    
    def getMineWarMonsterInfo(self, exposed):
         if not formula.isMineWarSpace(self.spaceNo):
            return
         
         self.spaceMgr.sendMineWarMonsterInfo(self)