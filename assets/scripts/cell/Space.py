# -*- coding: utf-8 -*-

import zlib
import random

import KBEngine
from KBEDebug import *

import formula
import gameconst
import gameengine
import utils
import os
import json
import gametimer
import gameconfig
import gameconst

import iCell
import iFubenSpace
import iTimer
import iEntityRefresh
import gameglobal
import ResMgr
import kbeUtils
import iEntityLoader
import iGroupEntityLoader


class SpaceEntityGenerateMixin(object):

    def removeEntById(self, gameEntityId):
        gameEntityId = int(gameEntityId)

        for _, _en in KBEngine.entities.items():
            if not hasattr(_en, 'gameEntityId'):
                continue

            if _en.gameEntityId == gameEntityId:
                _en.safeDestroy()
                # do we need multi gameEntityId in single space?
                # break


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
        entity = KBEngine.createEntity(entType, self.spaceID, pos, direction, properties)
        LOG_DBG('after createCellLocally~~~~~~~~~~', entity)
        return entity

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

    def homeEntityProxyCall(self, entId, func, args):
        if entId not in KBEngine.entities:
            return

        ent = KBEngine.entities[entId]
        if hasattr(ent, func):
            getattr(ent, func)(*args)

    def setHomeCompByteMap(self, box, x, z, height, width, byteMap):
        LOG_DBG('ckz: setHomeCompByteMap', x, z, height, width)
        byteMap = bytes(byteMap)
        KBEngine.addLayerOneTilesFromBytes(self.spaceID, x, z, height, width, byteMap)
        box.onHomeByteMapSet(self.spaceNo)

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
