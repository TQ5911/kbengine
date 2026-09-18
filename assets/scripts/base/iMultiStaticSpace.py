# coding: utf-8

import KBEngine
from KBEDebug import *

import random

import iGlobal
import StaticSpaceVal
import formula
import gameconst
import gameconfig
import gametimer
import utils


class IMultiStaticSpace(iGlobal.IGlobal):
    def __init__(self):
        self.staticSpaces = {} # type: dict[int, StaticSpaceVal.StaticSpaceVal]
        self.loadWaitSet = set()

        # ===== 灾难恢复状态 (cellapp挂掉重启时使用) =====
        self.deadApps = []           # type: list[int]  挂掉的cellapp groupOrder
        self.relivedCellapps = []    # type: list[int]  恢复的cellapp groupOrder
        self.missedSpaces = {}       # type: dict[int, int]  待恢复 spaceNo -> groupOrder

    def _createStaticSpace(self, mapId, spaceWeight=10, lineNo=0):
        LOG_INFO('_createStaticSpace:', mapId, lineNo)
        _spaceNo = formula.combineLineSpaceNo(mapId, lineNo)
        # 恢复时 staticSpaces[spaceNo] 可能还有旧的占位, 先清掉
        self.staticSpaces.pop(_spaceNo, None)
        self.loadWaitSet.discard(_spaceNo)

        _spaceVal = StaticSpaceVal.StaticSpaceVal(
            mapId,
            lineNo)

        self.staticSpaces[_spaceNo] = _spaceVal
        _cellappIndx = mapId + lineNo
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
        LOG_INFO('_onCraeteLineSpace', spaceNo)
        _spaceVal = self.staticSpaces[spaceNo]
        _spaceVal.lineSpaceBox = spaceBox

    def _getSpaceMgrEntityType(self):
        raise NotImplementedError()

    def isSpaceReady(self, spaceNo):
        _spaceVal = self.staticSpaces.get(spaceNo)
        if not _spaceVal:
            return False

        return _spaceVal.spaceMgrBoxCell is not None
    
    def isSpaceReadyEnter(self, lineType, lineNo):
        spaceNo = formula.combineLineSpaceNo(lineType, lineNo)
        _spaceVal = self.staticSpaces.get(spaceNo)
        if not _spaceVal:
            return False

        return _spaceVal.isReadyEnter()

    def onStaticSpaceReady(self, spaceNo):
        LOG_INFO('onStaticSpaceReady', spaceNo)
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
        LOG_INFO('onLoadEntitiesEnd:', spaceNo)
        self.loadWaitSet.discard(spaceNo)
        if not self.loadWaitSet and not self.doNextFlag:
            self.doNextFlag = 1
            iGlobal.IGlobal.doNext(self)

    def onSpaceCellAppDeath(self, spaceNo):
        """
        cellapp挂掉导致space销毁时调用

        注意: 此时cellapp可能已经死/即将死, 直接调 _createStaticSpace
        会因 cellappIndex 指向死掉的 cellapp 而失败/错位.
        所以这里只记录, 等 cellapp 恢复后再重建.
        """
        LOG_INFO('onSpaceCellAppDeath', spaceNo)
        if spaceNo not in self.staticSpaces:
            LOG_WARN('onSpaceCellAppDeath:: spaceNo not in staticSpaces', spaceNo)
            return

        # 把老 staticSpaceVal 标记为destroy (lineSpaceBox 已经无效)
        _oldVal = self.staticSpaces.get(spaceNo)
        if _oldVal:
            _oldVal.lineDestroy()
        self.loadWaitSet.discard(spaceNo)

        # Space.onLoseCell 没有把 groupOrder 传下来, 这里暂时记 0
        self.missedSpaces[spaceNo] = 0

    # =========================================
    # 灾难恢复: handleCellappDeath / onCellappRelive

    def handleCellappDeath(self, groupOrder):
        if groupOrder not in self.deadApps:
            self.deadApps.append(groupOrder)
        LOG_INFO('IMultiStaticSpace::handleCellappDeath', groupOrder, self.deadApps)

    def onCellappRelive(self, groupOrder):
        if groupOrder not in self.relivedCellapps:
            self.relivedCellapps.append(groupOrder)
        LOG_INFO('IMultiStaticSpace::onCellappRelive', groupOrder,
                 'dead=', self.deadApps, 'relived=', self.relivedCellapps)
        self._doRecoverMissedSpaces()

    def _doRecoverMissedSpaces(self):
        # 所有死过的cellapp都恢复后, 才开始恢复missedSpaces
        if len(self.relivedCellapps) != len(self.deadApps):
            return

        LOG_INFO('IMultiStaticSpace::_doRecoverMissedSpaces', self.missedSpaces)
        _delay = 0
        for _spaceNo in list(self.missedSpaces.keys()):
            self.willRecoverSpace(_spaceNo)
            self.addTimerCB(
                _delay,
                '_recoverStaticSpaceByNo',
                (_spaceNo,),
                gametimer.TIMER_TAG_RECOVER_MULTI_STATIC_SPACE,
            )
            _delay += 0.2

        self.relivedCellapps = []
        self.deadApps = []
        self.missedSpaces.clear()

    def _recoverStaticSpaceByNo(self, spaceNo):
        if spaceNo in self.staticSpaces:
            _val = self.staticSpaces[spaceNo]
            if _val.isSpaceReady() and not _val.isLineDestroy():
                # 已经被新的回调填上了, 不用重建
                LOG_INFO('_recoverStaticSpaceByNo:: space already recovered', spaceNo)
                return

        _mapId = formula.fetchMapId(spaceNo)
        _lineNo = formula.parseLineNo(spaceNo)
        LOG_INFO('_recoverStaticSpaceByNo:', spaceNo, _mapId, _lineNo)
        self._createStaticSpace(_mapId, lineNo=_lineNo)

    def willRecoverSpace(self, spaceNo):
        """子类钩子, 可以在space恢复前做一些准备 (例如清掉旧timer, 通知玩家等)"""
        pass

    def _doBatchlyBroadcastAllSpaceMgr(self, sendList, func, args):
        for spaceNo in sendList:
            spaceVal = self.staticSpaces[spaceNo]
            if not spaceVal or not spaceVal.spaceMgrBoxCell:
                continue
            spaceVal.spaceMgrBoxCell.callOnSpaceMgr(func, args)
            yield utils.emptyFunc

    def broadcastAllSpaceMgrByTypes(self, excludeTypes, func, args):
        LOG_INFO('broadcastAllSpaceMgrByTypes:', excludeTypes, func, args)
        sendList = []
        for spaceNo in list(self.staticSpaces.keys()):
            _type = self.getStaticSpaceType(spaceNo)
            if _type in excludeTypes:
                continue
            sendList.append(spaceNo)
        if len(sendList) <= 0:
            return
        self.batchlyCall(
            self._doBatchlyBroadcastAllSpaceMgr(sendList, func, args),
            20, 0.1)
