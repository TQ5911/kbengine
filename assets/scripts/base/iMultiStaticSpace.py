# coding: utf-8

import KBEngine
from KBEDebug import *

import random

import iGlobal
import StaticSpaceVal
import formula
import gameconst
import gameconfig
import iEntityLoaderInBase


class IMultiStaticSpace(iEntityLoaderInBase.IEntityLoaderInBase, iGlobal.IGlobal):
    def __init__(self):
        iEntityLoaderInBase.IEntityLoaderInBase.__init__(self)
        self.staticSpaces = {} # type: dict[int, StaticSpaceVal.StaticSpaceVal]
        self.loadWaitSet = set()

    def _createStaticSpace(self, mapId, spaceWeight=10, lineNo=0):
        _spaceNo = formula.getLineSpaceNo(mapId, lineNo)
        _spaceVal = StaticSpaceVal.StaticSpaceVal(
            mapId,
            lineNo)

        self.staticSpaces[_spaceNo] = _spaceVal
        _cellappIndx = random.randint(1, gameconfig.cellAppCount())
        _spaceBox = KBEngine.createEntityLocally('Space',
            {
                'spaceno': _spaceNo,
                'spaceNo': _spaceNo,
                'position': gameconst.SPACE_FIX_POS,
                'spaceWeight': spaceWeight,
                'cellappIndex': _cellappIndx
            })

        self._onCraeteLineSpace(_spaceBox, _spaceNo)
        self.loadWaitSet.add(_spaceNo)

    def _onCraeteLineSpace(self, spaceBox, spaceNo):
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.lineSpaceBox = spaceBox

    def _getSpaceMgrEntityType(self):
        raise NotImplementedError()

    def onStaticSpaceReady(self, spaceNo):
        self.staticSpaces[spaceNo].lineSpaceReady()

        _pos = gameconst.SPACE_FIX_POS
        _dir = (0, 0, 0)
        _params = {
            'spaceNo': spaceNo,
            'position': _pos,
            'direction': _dir,
        }
        self.createCellEntityInSpace(spaceNo, self._getSpaceMgrEntityType(), _pos, _dir, _params)

    def createCellEntityInSpace(self, spaceNo, className, bornPosition, bornDirection, params):
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.lineSpaceBox.cell.createCellLocally(className, bornPosition, bornDirection, params)

    def onSpaceMgrReady(self, spaceNo, spaceMgrCell):
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.setSpaceMgrBoxCell(spaceMgrCell)
        _spaceVal.spaceMgrBoxCell.initStaticSpace()

    def loadEntitiesInMulti(self, spaceNo):
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.lineSpaceBox.cell.doLoadEntities(_spaceVal.spaceMgrBoxCell.id)

    def loadSingleEntity(self, spaceNo, clsName, needCreateBase, pos, direction, props):
        # DEBUG_MSG("--- iLineSpaceStub loadSingleEntity", spaceNo, clsName, pos, direction, props)
        _spaceVal = self.staticSpaces[spaceNo]
        props['spaceMgrId'] = _spaceVal.spaceMgrBoxCell.id

        self.createCellEntityInSpace(spaceNo, clsName, pos, direction, props)

    def onLoadGroupEntities(self, info):
        spaceNoList = list(self.staticSpaces.keys())
        DEBUG_MSG("IMultiStaticSpace::onLoadGroupEntities", info, spaceNoList)
        if len(spaceNoList) <= 0:
            WARNING_MSG('IMultiStaticSpace::onLoadGroupEntities: no spaceNo found')
            return
        else:
            mapId = formula.getMapId(info['id'])
            for spaceNo in spaceNoList:
                if formula.getMapId(spaceNo) == mapId:
                    info['spaceNo'] = spaceNo
                    break
            if not info.get('spaceNo', None):
                WARNING_MSG('IMultiStaticSpace::onLoadGroupEntities: spaceNo not found', mapId, spaceNoList)
                return

        DEBUG_MSG("IMultiStaticSpace::onLoadGroupEntities spaceNo", info['spaceNo'])
        super(IMultiStaticSpace, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        spaceNoList = list(self.staticSpaces.keys())
        DEBUG_MSG("IMultiStaticSpace::onRefreshGroupEntities", info, spaceNoList)
        if len(spaceNoList) <= 0:
            WARNING_MSG('IMultiStaticSpace::onRefreshGroupEntities: no spaceNo found')
            return
        else:
            lineNo = info['lineNo']
            mapId = formula.getMapId(info['id'])
            for spaceNo in spaceNoList:
                if formula.getMapId(spaceNo) == mapId:
                    info['spaceNo'] = spaceNo
                    break
            if not info.get('spaceNo', None):
                WARNING_MSG('IMultiStaticSpace::onRefreshGroupEntities: spaceNo not found', mapId, spaceNoList)
                return

        DEBUG_MSG("IMultiStaticSpace::onRefreshGroupEntities spaceNo", info['spaceNo'])
        super(IMultiStaticSpace, self).onRefreshGroupEntities(info)

    def onLoadEntitiesEnd(self, spaceNo):
        INFO_MSG('onLoadEntitiesEnd:', spaceNo)
        self.loadWaitSet.remove(spaceNo)
        if not self.loadWaitSet:
            iGlobal.IGlobal.doNext(self)

    def onSpaceCellAppDeath(self, spaceNo):
        INFO_MSG('onSpaceCellAppDeath', spaceNo)
        _mapId = formula.getMapId(spaceNo)
        self._createStaticSpace(_mapId)

