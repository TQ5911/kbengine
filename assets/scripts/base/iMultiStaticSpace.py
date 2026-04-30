# coding: utf-8

import KBEngine
from KBEDebug import *

import random

import iGlobal
import StaticSpaceVal
import formula
import gameconst
import gameconfig


class IMultiStaticSpace(iGlobal.IGlobal):
    def __init__(self):
        self.staticSpaces = {} # type: dict[int, StaticSpaceVal.StaticSpaceVal]
        self.loadWaitSet = set()

    def _createStaticSpace(self, mapId, spaceWeight=10, lineNo=0):
        LOG_IFO('_createStaticSpace:', mapId, lineNo)
        _spaceNo = formula.combineLineSpaceNo(mapId, lineNo)
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
        LOG_IFO('_onCraeteLineSpace', spaceNo)
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.lineSpaceBox = spaceBox

    def _getSpaceMgrEntityType(self):
        raise NotImplementedError()

    def isSpaceReady(self, spaceNo):
        _spaceVal = self.staticSpaces.get(spaceNo)
        if not _spaceVal:
            return False

        return _spaceVal.spaceMgrBoxCell is not None

    def onStaticSpaceReady(self, spaceNo):
        LOG_IFO('onStaticSpaceReady', spaceNo)
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
        # LOG_DBG("--- iLineSpaceStub loadSingleEntity", spaceNo, clsName, pos, direction, props)
        _spaceVal = self.staticSpaces[spaceNo]
        props['spaceMgrId'] = _spaceVal.spaceMgrBoxCell.id

        self.createCellEntityInSpace(spaceNo, clsName, pos, direction, props)

    def onLoadGroupEntities(self, info):
        spaceNoList = list(self.staticSpaces.keys())
        LOG_DBG("IMultiStaticSpace::onLoadGroupEntities", info, spaceNoList)
        if len(spaceNoList) <= 0:
            LOG_WARN('IMultiStaticSpace::onLoadGroupEntities: no spaceNo found')
            return
        else:
            mapId = formula.fetchMapId(info['id'])
            for spaceNo in spaceNoList:
                if formula.fetchMapId(spaceNo) == mapId:
                    info['spaceNo'] = spaceNo
                    break
            if not info.get('spaceNo', None):
                LOG_WARN('IMultiStaticSpace::onLoadGroupEntities: spaceNo not found', mapId, spaceNoList)
                return

        LOG_DBG("IMultiStaticSpace::onLoadGroupEntities spaceNo", info['spaceNo'])
        _spaceVal = self.staticSpaces[info['spaceNo']]
        _spaceVal.lineSpaceBox.cell.callOnSpace('onLoadGroupEntities', (info, _spaceVal.spaceMgrBoxCell.id))

    def onRefreshGroupEntities(self, info):
        spaceNoList = list(self.staticSpaces.keys())
        LOG_DBG("IMultiStaticSpace::onRefreshGroupEntities", info, spaceNoList)
        if len(spaceNoList) <= 0:
            LOG_WARN('IMultiStaticSpace::onRefreshGroupEntities: no spaceNo found')
            return
        else:
            lineNo = info['lineNo']
            mapId = formula.fetchMapId(info['id'])
            for spaceNo in spaceNoList:
                if formula.fetchMapId(spaceNo) == mapId:
                    info['spaceNo'] = spaceNo
                    break
            if not info.get('spaceNo', None):
                LOG_WARN('IMultiStaticSpace::onRefreshGroupEntities: spaceNo not found', mapId, spaceNoList)
                return

        LOG_DBG("IMultiStaticSpace::onRefreshGroupEntities spaceNo", info['spaceNo'])
        _spaceVal = self.staticSpaces[info['spaceNo']]
        _spaceVal.lineSpaceBox.cell.callOnSpace('onRefreshGroupEntities', (info, _spaceVal.spaceMgrBoxCell.id))

    def onDestroyGroupEntities(self, info):
        spaceNoList = list(self.staticSpaces.keys())
        LOG_DBG("IMultiStaticSpace::onDestroyGroupEntities", info, spaceNoList)

        if not info.get('spaceNo', None):
            LOG_WARN('IMultiStaticSpace::onDestroyGroupEntities: spaceNo not found', info, spaceNoList)
            return

        _spaceVal = self.staticSpaces[info['spaceNo']]
        _spaceVal.lineSpaceBox.cell.callOnSpace('onDestroyGroupEntities', (info, _spaceVal.spaceMgrBoxCell.id))

    def onLoadEntitiesEnd(self, spaceNo):
        LOG_IFO('onLoadEntitiesEnd:', spaceNo)
        self.loadWaitSet.remove(spaceNo)
        if not self.loadWaitSet and not self.doNextFlag:
            self.doNextFlag = 1
            iGlobal.IGlobal.doNext(self)

    def onSpaceCellAppDeath(self, spaceNo):
        LOG_IFO('onSpaceCellAppDeath', spaceNo)
        _mapId = formula.fetchMapId(spaceNo)
        self._createStaticSpace(_mapId)

