# -*- coding: utf-8 -*-
import KBEngine

import utils
import sMath
import gameconst
from KBEDebug import *
import iCell
import iTimer
import iGameEntity
import iFubenSpace

import NPC_teleporter as NPC_T
import gameglobal
import gametimer
import formula
import utils

import dungeonSrc


class Teleporter(iCell.ICell, iTimer.ITimer, iGameEntity.IGameEntity,
                 iFubenSpace.IFubenSpace):
    IsTeleporter = True

    TELEPORT_TRAP = 1

    def __init__(self):
        super(Teleporter, self).__init__()
        if not self.name:
            self.name = NPC_T.datas[self.teleporterId].get('name', '未知传送门')

        spaceMgr = self.spaceMgr
        if formula.isDungeonSpace(self.spaceNo):
            gid = utils.getGidFromGameEntityId(self.gameEntityId)
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.teleporterId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))

        # 【【任务】【程序自主】【组队跟随-远距离寻路优化】传送门相关迭代】
        gameglobal.teleporterGIDToEntIdMap.setdefault(self.spaceNo, {}).setdefault(
            self.teleporterId, (self.id, self.gameEntityId))

        if self.ttl:
            self.pyAddTimer(self.ttl, 0, gametimer.TIMER_CELL_TTL_DESTROY)

    # self._callback(1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)

    def _postSafeDestory(self):
        gameglobal.teleporterGIDToEntIdMap.get(self.spaceNo, {}).pop(self.teleporterId, None)

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.TIMER_CELL_TTL_DESTROY:
            if not self.isDestroyed:
                self._ttlDestroy()
        else:
            super(Teleporter, self).onTimer(tid, userData)

    def _addTrap(self):
        teleportData = NPC_T.datas[self.teleporterId]
        if teleportData.get('activateType', 0) == 3:
            telRange = teleportData.get('activateParam')
            self.addProximity(telRange, 0.0, self.TELEPORT_TRAP)

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if userArg == self.TELEPORT_TRAP:
            pass

    def userDoTeleport(self, userId, desTelId, lineNo=-1, src=None):
        INFO_MSG("selfDoTeleport::", userId, desTelId, lineNo, src)
        user = KBEngine.entities.get(userId)
        if self._checkBadEnt(user):
            return
        self._doTeleport(user, desTelId, lineNo, src)

    def doTeleport(self, exposed, desTelId, lineNo=-1):
        INFO_MSG('doTeleport::~', exposed, desTelId, lineNo)
        user = KBEngine.entities.get(exposed)
        if self._checkBadEnt(user):
            return

        if self.teleportType == gameconst.TeleporterType.CUBE_HALL:
            user.enterCubeByFloorConfig()
            return

        elif self.teleportType == gameconst.TeleporterType.CUBE_BACK:
            user.backOriginRoomFromCow()
            return

        elif self.teleportType == gameconst.TeleporterType.TO_CUBE_MAP_ID:
            user.enterCubeByMapIds([self.getMapIdByCustomId()])
            return

        src = dungeonSrc.DungeonFromClientSrc(user.base, user.gbId)
        lineType = utils.getLineTypeFromCfgGameEntityId(desTelId)

        spaceNo = formula.getLineSpaceNo(lineType, 0)
        if formula.isCubeSpace(spaceNo):
            user.enterCubeByMapIds([lineType])
            return

        self._doTeleport(user, desTelId, lineType, lineNo, src)

    def getMapIdByCustomId(self):
        customeId, _ = utils.getCustomIdAndGid(self.spaceNo, self.gameEntityId)
        if not customeId:
            return 0

        return int(customeId)

    def _doTeleport(self, user, desTelId, lineType, lineNo=-1, src=None):
        DEBUG_MSG('_doTeleport:', user, src, desTelId, lineType, lineNo)
        user.teleportByTeleporter(desTelId, self.cfgGameEntityId, self, lineNo, lineType, src)

    def _checkBadEnt(self, ent):
        if not ent or ent.isDestroyed:
            INFO_MSG('Teleporter._checkBadEnt: invalid entity')
            return True

        if not ent.IsAvatar:
            INFO_MSG('Teleporter._checkBadEnt: not Avatar')
            return True

        if ent.spaceNo != self.spaceNo:
            INFO_MSG('Teleporter._checkBadEnt: not in same space')
            return True
