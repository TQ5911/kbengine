# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gameengine
import math
import gameconst
import cube_room
import random
import gametimer
import formula
import utils
import gameglobal
import cube_config
import iStaticSpaceMgr
import iCollectionBossForMgr
import cube_floor
import NPC_NPC as N_ND


class CubeSpaceMgr(iCollectionBossForMgr.ICollectionBossForMgr, iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        iCollectionBossForMgr.ICollectionBossForMgr.__init__(self)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)

    def onTimer(self, tid, userData):
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(CubeSpaceMgr, self).onTimer(tid, userData)

    def initStaticSpace(self):
        super().initStaticSpace()

    def removeEntityById(self, entId):
        super().removeEntityById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)
        if not self._isArenaSpace():
            return

        box.client.onArenaKing(self.cubeArena.arenaKing)

    def createTeleporterToCow(self, num, pos=None):
        if KBEngine.isShuttingDown():
            return

        _mapId = formula.getMapId(self.spaceNo)
        _dunData = utils.getDunStructureModuleData(_mapId)
        if not _dunData:
            ERROR_MSG("can't find dunData for mapId:%d" % _mapId)
            return

        _cubeData = _dunData.get('Cube')
        if not _cubeData:
            WARNING_MSG("can't find cubeData in dunData for mapId:%d" % _mapId)
            return

        _space = gameglobal.localSpaceIDMap.get(self.spaceID)
        if not _space:
            ERROR_MSG("can't find localSpace for spaceID:%d" % self.spaceID)
            return

        _gids = []
        _pools = list(_cubeData.get('Teleporter', {}).keys())
        _pools = random.sample(_pools, min(num, len(_pools)))
        for _gid in _pools:
            for i in utils.generateGameEntityId(int(_gid), 1):
                _gids.append(int(i))

        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, _gids, _entityProps)
        _ttl = cube_config.datas['cube_cowRoomEntranceTime']['value'] * 60
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            _params['ttl'] = _ttl
            if pos is not None:
                _params['position'] = pos
                _pos = pos

            _space.createCellLocally(_className, _pos, _dir, _params)

    # ------------------ 擂台房玩法 start --------------------------------

    def onPlayerOffline(self, playerId, playerGbId):
        super(CubeSpaceMgr, self).onPlayerOffline(playerId, playerGbId)
        if not self._isArenaSpace():
            return

        self.cubeArena.onPlayerLeaveArena(playerId, self)

    def onPlayerLeave(self, gbId, playerId, box):
        super(CubeSpaceMgr, self).onPlayerLeave(gbId, playerId, box)
        if not self._isArenaSpace():
            return

        self.cubeArena.onPlayerLeaveArena(playerId, self)

    def onPlayerEnter(self, playerEntId):
        super(CubeSpaceMgr, self).onPlayerEnter(playerEntId)
        if not self._isArenaSpace():
            return

        _player = KBEngine.entities.get(playerEntId)
        if not _player:
            ERROR_MSG('can not find player entity', playerEntId)
            return

        _buffId = self.cubeArena.getChallengerBuff(self.spaceNo)
        DEBUG_MSG('enter arena cube', _buffId)
        _player.addBuff(_buffId, 1, _player.id)
        _player.client.onArenaKing(self.cubeArena.arenaKing)

    def _isArenaSpace(self):
        _mapId = formula.getMapId(self.spaceNo)
        return cube_room.datas[_mapId]['sign'] == gameconst.CUBE_SIGN_ARENA

    def doInteractArenaKing(self, player):
        if not self._isArenaSpace():
            return False

        return self.cubeArena.setArenaKing(player, self)

    def dealWithArenaTimer(self):
        if self.cubeArenaTimerId:
            self._cancelDatetimeCallback(self.cubeArenaTimerId, gametimer.TIMER_TAG_CUBE_ARENA)
            self.cubeArenaTimerId = 0

        _nextCBTime = self.cubeArena.getNextCBTime(self.spaceNo)
        if not _nextCBTime:
            return

        INFO_MSG('next arena cb time:', _nextCBTime)
        self.cubeArenaTimerId = self._datetimeCallback(
            _nextCBTime, 
            '_onArenaCB', 
            (self.cubeArena.arenaStage,),
            gametimer.TIMER_TAG_CUBE_ARENA,
            'cubeArenaTimerId'
        )

    def _onArenaCB(self, curStage):
        self.cubeArena.doAddStage(curStage, self)

    def onPlayerKillAnother(self, deathPlayer, killerPlayer):
        if not self._isArenaSpace():
            return

        self.cubeArena.onArenaPlayerKillAnother(deathPlayer, killerPlayer, self)
        
    def doSendArenaKingPos(self, box):
        if not self._isArenaSpace():
            WARNING_MSG('doSendArenaKingPos', self.spaceNo)
            return

        _king = KBEngine.entities.get(self.cubeArena.arenaKing)
        if not _king:
            return

        DEBUG_MSG('_notifyArenaKingPos', _king.position)
        box.client.onArenaKingPos(_king.position)

    def onPlayerRelive(self, box, playerGbId):
        super(CubeSpaceMgr, self).onPlayerRelive(box, playerGbId)
        if not self._isArenaSpace():
            return

        _boxCell = KBEngine.entities.get(box.id)
        if not _boxCell:
            WARNING_MSG('can not find boxCell', box.id)
            return
        _boxCell.addBuff(self.cubeArena.getChallengerBuff(self.spaceNo), 1, _boxCell.id)

    # ------------------ 擂台房玩法 end --------------------------------

    # ------------------ 神秘商人 start -----------------------------------
    def destroyChanMap(self):
        _mapId = formula.getMapId(self.spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        _npcId = cube_floor.datas[_floor]['chapmanID']
        _waitDestroyes = []
        for _eid in self.taggedEntities.get('Npc', []):
            _ent = KBEngine.entities.get(_eid)
            if not _ent:
                continue

            if _ent.npcId == _npcId:
                _waitDestroyes.append(_ent)

        for _ent in _waitDestroyes:
            _ent.safeDestroy()

    def createChapMan(self, position, direction):
        _mapId = formula.getMapId(self.spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        _npcId = cube_floor.datas[_floor]['chapmanID']

        _dir = (0.0, 0.0, direction * math.pi / 180)
        _params = {
            'spaceNo': self.spaceNo,
            'spaceno': self.spaceNo,
            'spaceMgrId': self.id,
            'direction': _dir,
            'position': position,
            'npcId': _npcId,
            'name': N_ND.datas[_npcId]['name'],
            'deathTime': cube_config.datas['cube_chapmanRefreshInterval']['value'] * 10 + utils.getNow(),
        }

        _space = gameglobal.localSpaceIDMap.get(self.spaceID)
        if not _space:
            ERROR_MSG("can't find localSpace for spaceID:%d" % self.spaceID)
            return

        _space.createCellLocally('Npc', position, _dir, _params)
        
    # ------------------ 神秘商人 end -----------------------------------
