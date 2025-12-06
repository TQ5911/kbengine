# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import os

import gameengine
import gameconst
import gametimer
import formula
import utils

import iCell
import iTimer
import iLargeEnt
import iFubenSpace
import iGameEntity

import NPC_airWall as NPA


class Barrier(iCell.ICell, iTimer.ITimer, iFubenSpace.IFubenSpace,
              iGameEntity.IGameEntity, iLargeEnt.ILargeEnt):
    IsMonster = False
    IsCombatUnit = False

    def __init__(self):
        iCell.ICell.__init__(self)
        iGameEntity.IGameEntity.__init__(self)

        # try:
        #     # raise error if fail to init engine airwall
        #     self.addEngineAirWall()
        # except:
        #     ERROR_MSG('Barrier.__init__:: add Engine airwall failed')
        #     import traceback
        #     traceback.print_exc()

        spaceMgr = self.spaceMgr
        if formula.isDungeonSpace(self.spaceNo):
            gid = utils.getGidFromGameEntityId(self.gameEntityId)
            dungeonNo = formula.getDungeonNoBySpaceNo(self.spaceNo)
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.barrierId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))
            # large entity
            entityMaxLength = self._getBarrierLargeEntLength(dungeonNo, gid)
            if entityMaxLength > gameconst.DEFAULT_AOI:
                self.setBodySize((entityMaxLength*1.414, entityMaxLength*1.414))
        elif formula.isSiegeWarSpace(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, ('', self.__class__.__name__,))

    def _getBarrierLargeEntLength(self, dungeonNo, gid):
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        dunData = dunAllDatas[str(gid)]
        dunPropsData = dunData["Props"]
        _areaType = dunPropsData["AreaType"]
        _maxLength = 0
        if _areaType == gameconst.DungeonCustomAreaType.CIRCLE:
            _maxLength = gameconst.DungeonCustomAreaType.getCircleRadius(dunPropsData) * 2
        elif _areaType == gameconst.DungeonCustomAreaType.RECTANGLE:
            _maxLength = max(gameconst.DungeonCustomAreaType.getRectangleVal(dunPropsData))
        elif _areaType == gameconst.DungeonCustomAreaType.LINE:
            _maxLength = gameconst.DungeonCustomAreaType.getLineVal(dunPropsData)
        return _maxLength

    @property
    def pointId(self):
        """use for battle field dungeon space controller"""
        return self.barrierId

    def getTmxName(self):
        def _getTmxName():
            return utils.getDunModuleName(formula.getMapId(self.spaceNo))

        dunName = _getTmxName()
        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        dunFileName = '{}_{}.tmx'.format(dunName, gid)

        return dunFileName

    def getTmxAnchorPoint(self):
        def _getTmxModuleData():
            return utils.getDunModuleData(formula.getMapId(self.spaceNo))

        data = _getTmxModuleData()
        gid = utils.getGidFromGameEntityId(self.gameEntityId)
        props = data[str(gid)]['Props']
        return int(props['MPosX']), int(props['MPosZ'])

    def addEngineAirWall(self):
        name = self.getTmxName()
        x, y = self.getTmxAnchorPoint()
        DEBUG_MSG('~~~~~~~~ CREATE BARRIER AIR WALL ENGINE MARK', name, x, y)
        # KBEngine.addLayerOneTilesById(self.spaceID, x, y, name)

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(Barrier, self).onTimer(tid, userData)

    def onGetWitness(self):
        pass

    def onLoseWitness(self):
        pass

    def _preSafeDestory(self):
        DEBUG_MSG('_preSafeDestory::')
        self.removeEngineAirWall()

    # def _preDelaySafeDestroy(self, delay):
    #     DEBUG_MSG('_preDelaySafeDestroy::', delay)
    #     self.removeEngineAirWall()

    def removeEngineAirWall(self):
        try:
            x, y = self.getTmxAnchorPoint()
            DEBUG_MSG('~~~~~~~~ DESTROY BARRIER AIR WALL ENGINE MARK', x, y)
            # KBEngine.removeLayerOneTilesGeometryMapping(self.spaceID, x, y)
        except:
            ERROR_MSG('Barrier._preDelaySafeDestroy:: remove Engine airwall failed')
            import traceback
            traceback.print_exc()

    def safeDestroy(self, forceDestroy=False):
        self.unsetBodySize()
        super(Barrier, self).safeDestroy(forceDestroy)

