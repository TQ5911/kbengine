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
        #     LOG_ERR('Barrier.__init__:: add Engine airwall failed')
        #     import traceback
        #     traceback.print_exc()

        spaceMgr = self.spaceMgr
        if formula.inDungeonScene(self.spaceNo):
            gid = utils.parseGidFromGameEntityId(self.gameEntityId)
            dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
            if spaceMgr:
                spaceMgr.addEntity(self.id, (str(self.fbEntityId), str(self.barrierId),
                                             'gid_{}'.format(gid), self.__class__.__name__,))
            # large entity
            entityMaxLength = self._getBarrierLargeEntLength(dungeonNo, gid)
            if entityMaxLength > gameconst.DEFAULT_AOI:
                self.setBodySize((entityMaxLength*1.414, entityMaxLength*1.414))
        elif formula.inSiegeWarScene(self.spaceNo):
            if spaceMgr:
                spaceMgr.addEntity(self.id, ('', self.__class__.__name__,))

    def _getBarrierLargeEntLength(self, dungeonNo, gid):
        dunAllDatas = utils.getDunModuleData(dungeonNo)
        dunData = dunAllDatas[str(gid)]
        dunPropsData = dunData["Props"]
        _areaType = dunPropsData["AreaType"]
        _maxLength = 0
        if _areaType == gameconst.DungeonCustomAreaType.CIRCLE:
            _maxLength = gameconst.DungeonCustomAreaType.fetchCircleRadius(dunPropsData) * 2
        elif _areaType == gameconst.DungeonCustomAreaType.RECTANGLE:
            _maxLength = max(gameconst.DungeonCustomAreaType.fetchRectVal(dunPropsData))
        elif _areaType == gameconst.DungeonCustomAreaType.LINE:
            _maxLength = gameconst.DungeonCustomAreaType.fetchLineVal(dunPropsData)
        return _maxLength

    @property
    def pointId(self):
        """use for battle field dungeon space controller"""
        return self.barrierId

    def getTmxName(self):
        def _getTmxName():
            return utils.getDunModuleName(formula.fetchMapId(self.spaceNo))

        dunName = _getTmxName()
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        dunFileName = '{}_{}.tmx'.format(dunName, gid)

        return dunFileName

    def getTmxAnchorPoint(self):
        def _getTmxModuleData():
            return utils.getDunModuleData(formula.fetchMapId(self.spaceNo))

        data = _getTmxModuleData()
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        props = data[str(gid)]['Props']
        return int(props['MPosX']), int(props['MPosZ'])

    def addEngineAirWall(self):
        name = self.getTmxName()
        x, y = self.getTmxAnchorPoint()
        LOG_DBG('~~~~~~~~ CREATE BARRIER AIR WALL ENGINE MARK', name, x, y)
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
        LOG_DBG('_preSafeDestory::')
        self.removeEngineAirWall()

    # def _preDelaySafeDestroy(self, delay):
    #     LOG_DBG('_preDelaySafeDestroy::', delay)
    #     self.removeEngineAirWall()

    def removeEngineAirWall(self):
        try:
            x, y = self.getTmxAnchorPoint()
            LOG_DBG('~~~~~~~~ DESTROY BARRIER AIR WALL ENGINE MARK', x, y)
            # KBEngine.removeLayerOneTilesGeometryMapping(self.spaceID, x, y)
        except:
            LOG_ERR('Barrier._preDelaySafeDestroy:: remove Engine airwall failed')
            import traceback
            traceback.print_exc()

    def safeDestroy(self, forceDestroy=False):
        self.unsetBodySize()
        super(Barrier, self).safeDestroy(forceDestroy)

