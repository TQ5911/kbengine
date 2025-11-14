# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import gameengine
import formula
import utils
import gameglobal
import cube_config
import iStaticSpaceMgr
import iCollectionBossForMgr

class CubeSpaceMgr(iCollectionBossForMgr.ICollectionBossForMgr, iStaticSpaceMgr.IStaticSpaceMgr):
    def __init__(self):
        iStaticSpaceMgr.IStaticSpaceMgr.__init__(self)
        iCollectionBossForMgr.ICollectionBossForMgr.__init__(self)
        gameengine.getCubeStubBySpaceNo(self.spaceNo).onSpaceMgrReady(self.spaceNo, self)

    def initStaticSpace(self):
        super().initStaticSpace()

    def removeEntityById(self, entId):
        super().removeEntityById(entId)

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)

    def createTeleporterToCow(self, pos=None):
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
        for _gid in _cubeData.get('Teleporter', {}).keys():
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

