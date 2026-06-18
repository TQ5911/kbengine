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
import branchData_set as BDS

class CubeSpaceMgr(iCollectionBossForMgr.ICollectionBossForMgr, iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        iCollectionBossForMgr.ICollectionBossForMgr.__init__(self)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)

        #每分钟统计一次当前line活跃人数(5分钟内进入过战斗状态)
        self.pyAddTimer(1, 60, gametimer.STATISTIC_FIGHTING_COUNT)
        self.fightingPlayersCnt = 0

    def onTimer(self, tid, userData):
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        elif userData == gametimer.STATISTIC_FIGHTING_COUNT:
            self._statisticFightingCount()
        else:
            super(CubeSpaceMgr, self).onTimer(tid, userData)

    def initStaticSpace(self):
        super().initStaticSpace()

    def removeEntById(self, entId):
        super().removeEntById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)
        if not formula._isArenaSpace(self.spaceNo):
            return

        box.client.onArenaKing(self.cubeArena.arenaKing)

    def createTeleporterToCow(self, num, pos=None):
        if KBEngine.isShuttingDown():
            return

        _mapId = formula.fetchMapId(self.spaceNo)
        _dunData = utils.getDunStructModData(_mapId)
        if not _dunData:
            LOG_ERR("can't find dunData for mapId:%d" % _mapId)
            return

        _cubeData = _dunData.get('Cube')
        if not _cubeData:
            LOG_WARN("can't find cubeData in dunData for mapId:%d" % _mapId)
            return

        _space = gameglobal.localSpaceIDMap.get(self.spaceID)
        if not _space:
            LOG_ERR("can't find localSpace for spaceID:%d" % self.spaceID)
            return

        _gids = []
        _pools = list(_cubeData.get('Teleporter', {}).keys())
        _pools = random.sample(_pools, min(num, len(_pools)))
        for _gid in _pools:
            for i in utils.genGameEntityId(int(_gid), 1):
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
        if not formula._isArenaSpace(self.spaceNo):
            return

        self.cubeArena.onPlayerLeaveArena(playerId, self)

    def onPlayerLeave(self, gbId, playerId, box):
        super(CubeSpaceMgr, self).onPlayerLeave(gbId, playerId, box)
        if not formula._isArenaSpace(self.spaceNo):
            return

        self.cubeArena.onPlayerLeaveArena(playerId, self)

    def onPlayerEnter(self, playerEntId):
        super(CubeSpaceMgr, self).onPlayerEnter(playerEntId)
        if not formula._isArenaSpace(self.spaceNo):
            return

        _player = KBEngine.entities.get(playerEntId)
        if not _player:
            LOG_ERR('can not find player entity', playerEntId)
            return

        _buffId = self.cubeArena.getChallengerBuff(self.spaceNo)
        LOG_DBG('enter arena cube', _buffId)
        _player.addBuff(_buffId, 1, _player.id)
        _player.client.onArenaKing(self.cubeArena.arenaKing)

    def doInteractArenaKing(self, player):
        if not formula._isArenaSpace(self.spaceNo):
            return False

        return self.cubeArena.setArenaKing(player, self)

    def dealWithArenaTimer(self):
        if self.cubeArenaTimerId:
            self._cancelDatetimeCallback(self.cubeArenaTimerId, gametimer.TIMER_TAG_CUBE_ARENA)
            self.cubeArenaTimerId = 0

        _nextCBTime = self.cubeArena.getNextCBTime(self.spaceNo)
        if not _nextCBTime:
            return

        LOG_INFO('next arena cb time:', _nextCBTime)
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
        if not formula._isArenaSpace(self.spaceNo):
            return

        self.cubeArena.onArenaPlayerKillAnother(deathPlayer, killerPlayer, self)
        
    def doSendArenaKingPos(self, box):
        if not formula._isArenaSpace(self.spaceNo):
            LOG_WARN('doSendArenaKingPos', self.spaceNo)
            return

        _king = KBEngine.entities.get(self.cubeArena.arenaKing)
        if not _king:
            return

        LOG_DBG('_notifyArenaKingPos', _king.position)
        box.client.onArenaKingPos(_king.position)

    def onPlayerRelive(self, box, playerGbId):
        super(CubeSpaceMgr, self).onPlayerRelive(box, playerGbId)
        if not formula._isArenaSpace(self.spaceNo):
            return

        _boxCell = KBEngine.entities.get(box.id)
        if not _boxCell:
            LOG_WARN('can not find boxCell', box.id)
            return
        _boxCell.addBuff(self.cubeArena.getChallengerBuff(self.spaceNo), 1, _boxCell.id)

    def onChangeSafeArea(self, player, beSafe):
        if not formula._isArenaSpace(self.spaceNo):
            return
        
        self.cubeArena.onArenaChangeSafeArea(player, beSafe, self)

    # ------------------ 擂台房玩法 end --------------------------------

    # ------------------ 神秘商人 start -----------------------------------
    def destroyChanMap(self):
        _mapId = formula.fetchMapId(self.spaceNo)
        _floor = cube_room.datas[_mapId]['floor']
        _npcId = cube_floor.datas[_floor]['chapmanID']
        _waitDestroyes = []
        for _eid in self.tagEntities.get('Npc', []):
            _ent = KBEngine.entities.get(_eid)
            if not _ent:
                continue

            if _ent.npcId == _npcId:
                _waitDestroyes.append(_ent)

        for _ent in _waitDestroyes:
            _ent.safeDestroy()

    def createChapMan(self, position, direction):
        _mapId = formula.fetchMapId(self.spaceNo)
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
            'deathTime': cube_config.datas['cube_chapmanRefreshInterval']['value'] * 10 + utils.curTS(),
        }

        _space = gameglobal.localSpaceIDMap.get(self.spaceID)
        if not _space:
            LOG_ERR("can't find localSpace for spaceID:%d" % self.spaceID)
            return

        _space.createCellLocally('Npc', position, _dir, _params)
        
    # ------------------ 神秘商人 end -----------------------------------

    def _statisticFightingCount(self):
        now = utils.curTS()
        lastCnt = self.fightingPlayersCnt
        self.fightingPlayersCnt = 0
        dt = BDS.datas["Branch_activePlayer"]["value"] * 60
        for pid in self.players:
            ent = KBEngine.entities.get(pid)
            if not ent:
                continue
            #5分钟内有进入过战斗视为"活跃用户"
            if now - ent.lastFightTime < dt:
                self.fightingPlayersCnt += 1

        if lastCnt != self.fightingPlayersCnt:
            gameengine.getCubeStubBySpaceNo(self.spaceNo).onFightingPlayersCntSync(self.spaceNo, self.fightingPlayersCnt)
