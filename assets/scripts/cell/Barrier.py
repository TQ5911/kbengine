# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gameconst
import formula
import utils

import iCell
import iTimer
import iLargeEnt
import iFubenSpace
import iGameEntity


class Barrier(iCell.ICell, iTimer.ITimer, iFubenSpace.IFubenSpace,
              iGameEntity.IGameEntity, iLargeEnt.ILargeEnt):
    IsCombatUnit = False
    IsMonster = False

    def __init__(self, **kwargs):
        iCell.ICell.__init__(self)
        iGameEntity.IGameEntity.__init__(self)

        _spaceMgr = self.spaceMgr
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        if formula.inDungeonScene(self.spaceNo):
            dungeonNo = formula.parseDungeonNoBySpaceNo(self.spaceNo)
            if _spaceMgr:
                _spaceMgr.addEntity(self.id, (
                    str(self.barrierId),
                    str(self.fbEntityId), 
                    'gid_{}'.format(gid), 
                    self.__class__.__name__,
                ))
            # large entity
            _entityMaxLength = self._getBarrierLargeEntLength(dungeonNo, gid)
            if _entityMaxLength > gameconst.DEFAULT_AOI:
                self.setBodySize((_entityMaxLength*1.414, _entityMaxLength*1.414))
        elif formula.inSiegeWarScene(self.spaceNo):
            if _spaceMgr:
                _spaceMgr.addEntity(self.id, ('', self.__class__.__name__,))

        _area = self._getNavArea()
        if _area:
            LOG_INFO('addAirwallAreas', self.spaceID, _area)
            KBEngine.addAirwallAreas(self.spaceID, [_area])

    def _getNavArea(self):
        gid = utils.parseGidFromGameEntityId(self.gameEntityId)
        _mapId = formula.fetchMapId(self.spaceNo)
        _airData = utils.getAirWallModuleData(_mapId)

        return _airData.get(gid, 0)

    def _getBarrierLargeEntLength(self, dungeonNo, gid):
        _dunAllDatas = utils.getDunModuleData(dungeonNo)
        _dunData = _dunAllDatas[str(gid)]
        dunPropsData = _dunData["Props"]
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
        _props = data[str(gid)]['Props']
        return int(_props['MPosX']), int(_props['MPosZ'])

    def addEngineAirWall(self):
        name = self.getTmxName()
        x, y = self.getTmxAnchorPoint()
        LOG_DBG('~~~~~~~~ CREATE BARRIER AIR WALL ENGINE MARK', name, x, y)
        # KBEngine.addLayerOneTilesById(self.spaceID, x, y, name)

    def onTimer(self, tid, userData):
        self._onTimerTrigger(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(Barrier, self).onTimer(tid, userData)

    def onLoseWitness(self):
        pass

    def onGetWitness(self):
        pass

    def _preSafeDestory(self):
        LOG_DBG('_preSafeDestory::')
        _area = self._getNavArea()
        if _area:
            LOG_INFO('removeAirwallAreas', self.spaceID, _area)
            KBEngine.removeAirwallAreas(self.spaceID, [_area])

    def safeDestroy(self, forceDestroy=False):
        self.unsetBodySize()
        super(Barrier, self).safeDestroy(forceDestroy)

