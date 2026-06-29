# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *

import formula
import gameconst
import gameengine
import utils
import gameconfig
import gameconst

import iCell
import iFubenSpace
import iTimer
import gameglobal
import kbeUtils
import iEntityLoader
import iGroupEntityLoader


class SpaceEntityGenerateMixin(object):

    def removeEntById(self, gameEntityId):
        gameEntityId = int(gameEntityId)

        for _, _ent in KBEngine.entities.items():
            if not hasattr(_ent, 'gameEntityId'):
                continue

            if _ent.gameEntityId == gameEntityId:
                _ent.safeDestroy()


class Space(iCell.ICell, iTimer.ITimer, SpaceEntityGenerateMixin, iEntityLoader.IEntityLoader, iGroupEntityLoader.IGroupEntityLoader, iFubenSpace.IFubenSpace):
    def __init__(self):
        LOG_INFO("Space#__init__", self.spaceNo, self.spaceID, self.dungeonId, KBEngine.getComponentGroupOrder())
        iEntityLoader.IEntityLoader.__init__(self)
        iGroupEntityLoader.IGroupEntityLoader.__init__(self)
        gameglobal.localSpaceNoMap[self.spaceNo] = self
        gameglobal.localSpaceIDMap[self.spaceID] = self
        gameglobal.cellSpaceDungeonMap[self.spaceNo] = self.dungeonId

        super(Space, self).__init__()

        self.base.initCellField(self.spaceID)

        # 完整地图用包含了navmesh/tmx的目录路径
        self.spaceMap = formula.getSpaceMap(self.spaceNo)
        # 多个tmx拼接时给定具体tmx文件的路径
        if not self.spaceMap and self.spaceNo:
            gameengine.panicStack("space map is empty! %s %s" % (self.spaceNo, self.spaceID))

        if self.spaceMap:
            # KBEngine.addSpaceGeometryMapping(self.spaceID, None, self.spaceMap)
            kbeUtils.addSpaceGeometryMapping(self.spaceID, None, self.spaceMap)

        if formula.inWorldLineScene(self.spaceNo) and gameconfig.cellAppCount() > utils.fetchLineMaxNumber(
                formula.parseLineType(self.spaceNo)) * 2:
            pass
            # KBEngine.setAppFlags(KBEngine.APP_FLAGS_NOT_PARTCIPATING_LOAD_BALANCING|flags)
        elif not gameglobal.staticCell:
            gameglobal.staticCell = self

        if formula.inWorldLineScene(self.spaceNo):
            _pos = gameconst.SPACE_FIX_POS
            _dir = (0, 0, 0)
            _params = {
                'spaceNo': self.spaceNo,
                'position': _pos,
                'direction': _dir,
            }

            self.spaceMgrId = self.createCellLocally(
                'WorldLineSpaceMgr',
                _pos,
                _dir,
                _params
            ).id

    def onSpaceGone(self):
        gameglobal.localSpaceNoMap.pop(self.spaceNo, None)
        gameglobal.localSpaceIDMap.pop(self.spaceID, None)
        gameglobal.cellSpaceDungeonMap.pop(self.spaceNo, None)
        self.destroy()
        return

    def createCellLocally(self, entType, pos, direction, properties):
        if KBEngine.isShuttingDown():
            return

        direction = (float(direction[0]), float(direction[1]), float(direction[2]))
        LOG_DBG('createCellLocally~~~~~~~~~~', pos, direction)
        properties['spaceNo'] = self.spaceNo
        _entity = KBEngine.createEntity(entType, self.spaceID, pos, direction, properties)
        LOG_DBG('after createCellLocally~~~~~~~~~~', _entity)
        return _entity

    def onDestroy(self):
        super(Space, self).onDestroy()
        gameglobal.localSpaceNoMap.pop(self.spaceNo, None)
        gameglobal.localSpaceIDMap.pop(self.spaceID, None)
        gameglobal.cellSpaceDungeonMap.pop(self.spaceNo, None)

    def destroyMySpace(self):
        self.destroySpace()
        return

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)

    def onEntireConstruct(self):
        LOG_INFO('zt: onEntireConstruct', self.id, self.spaceNo)

    def calculateSpawnTime(self):
        # space only have default spawnspan
        return 0

    def updateSpaceWeight(self, spaceWeight):
        LOG_INFO('updateSpaceWeight', self.spaceID, spaceWeight)
        self.setSpaceWeight(self.spaceID, spaceWeight)

    def callOnSpaceMgr(self, func, args):
        if not self.spaceMgr:
            LOG_ERR('callOnSpaceMgr: spaceMgr is None', func, args)
            return

        getattr(self.spaceMgr, func)(*args)

    def callOnSpace(self, func, args):
        getattr(self, func)(*args)
