# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameengine
import gametimer
import gameconst
import formula
import utils
import StaticSpaceVal

import branchData_branchData as B_BD


class ILineSpaceStub(object):
    def __init__(self):
        pass

    def createLines(self):
        for ln in range(utils.fetchLineMaxNumber(self.lineType)):
            lineMaxCnt = B_BD.datas[self.lineType]['N1']
            spaceWeight = utils.calcSpaceWeight(0, False, gameconst.EntNumPerPlayerInAOI.worldLine, lineMaxCnt/10)
            self.addTimerCB(ln*0.2, '_createLineSpaceRemote', (ln,spaceWeight), gametimer.TIMER_TAG_CREATE_LINE_SPACE_REMOTE)

    def doNext(self):
        if hasattr(super(), 'doNext'):
            super().doNext()
        self.createLines()

    def newLineSpaceVal(self, lineType, lineNo):
        return StaticSpaceVal.StaticSpaceVal(lineType, lineNo)

    def getLineSpaceVal(self, lineNo):
        lineNo = min(len(self.lineSpaces)-1, lineNo)
        return self.lineSpaces[lineNo]

    def createCellEntityInSpace(self, spaceNo, className, bornPosition, bornDirection, params):
        lineNo = formula.parseLineNo(spaceNo)
        _spaceVal = self.getLineSpaceVal(lineNo)
        params['spaceMgrId'] = _spaceVal.spaceMgrBoxCell.id

        _spaceVal.lineSpaceBox.cell.createCellLocally(className, bornPosition, bornDirection, params)

    def _createLineSpaceRemote(self, lineNo, spaceWeight=10):
        _spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)

        self.lineSpaces[lineNo] = self.newLineSpaceVal(self.lineType, lineNo)

        cellappIndx = lineNo + 1 + gameconst.getWorldLineCellIdx(self.lineType)
        LOG_INFO('zt: create line', lineNo, _spaceNo, spaceWeight, self.lineType, cellappIndx)
        KBEngine.createEntityAnywhere('Space',
                                      {
                                          'spaceno': _spaceNo,
                                          'spaceNo': _spaceNo,
                                          'position': gameconst.SPACE_FIX_POS,
                                          'spaceWeight': spaceWeight,
                                          'cellappIndex': cellappIndx
                                      },
                                      lambda spaceBox, spaceNo=_spaceNo:
                                      self._onCreateLineSpace(spaceBox, spaceNo)
                                      )

    def _onCreateLineSpace(self, spaceBox, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        sVal = self.getLineSpaceVal(lineNo)
        sVal.lineSpaceBox = spaceBox

    def isSpaceReadyEnter(self, lineType, lineNo):
        sVal = self.getLineSpaceVal(lineNo)
        return sVal.isReadyEnter()
    
    def getSpaceAvatarNo(self, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        linePlayers = self.allPlayers.getLinePlayers(lineNo)
        return 0 if not linePlayers else len(linePlayers)

    def onSpaceLineReady(self, spaceNo):
        LOG_INFO('onSpaceLineReady', spaceNo)
        lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces[lineNo].lineSpaceReady()
        
        # spaceVal = self.getLineSpaceVal(lineNo)
        # spaceVal.lineSpaceBox.cell.doLoadEntities(0)

    def onSpaceMgrReady(self, spaceNo, spaceMgrCell):
        LOG_DBG("iLineSpaceStub onSpaceMgrReady", spaceNo, spaceMgrCell)
        lineNo = formula.parseLineNo(spaceNo)
        spaceVal = self.getLineSpaceVal(lineNo)
        spaceVal.setSpaceMgrBoxCell(spaceMgrCell)

    def onLoadEntitiesEnd(self, spaceNo):
        LOG_DBG("iLineSpaceStub onLoadEntitiesEnd", spaceNo)
        lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces[lineNo].lineEntitiesReady()
        self.batchlyCall(self.sendLineInfoOnSpaceChanged(), 50)

        gameengine.callBaseApps('gameglobal.onLineEntityReady', (spaceNo,))

    def handleCellappDeath(self, groupOrder):
        LOG_INFO('handleCellappDeath', self.id, groupOrder)
        if groupOrder not in self.deadApps:
            self.deadApps.append(groupOrder)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        LOG_ERR('onLineSpaceGone', spaceNo, groupOrder)
        _lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces.pop(_lineNo, None)
        self.collectionSharedLimitDic.pop(spaceNo, None)
        self.missedLines[_lineNo] = groupOrder

    def onCellappRelive(self, groupOrder):
        if groupOrder not in self.relivedCellapps:
            self.relivedCellapps.append(groupOrder)
        LOG_INFO('LineStub:onCellappRelive', groupOrder, self.deadApps, self.relivedCellapps)

        self._doRecoverLines()

    def _doRecoverLines(self):
        if len(self.relivedCellapps) == len(self.deadApps):
            LOG_INFO('recove lines:', self.missedLines)
            _delay = 0
            for ln, order in self.missedLines.items():
                self.willRecoverLine(ln)
                self.addTimerCB(
                    _delay, 
                    '_createLineSpaceRemote', 
                    (ln,), 
                    gametimer.TIMER_TAG_CREATE_LINE_SPACE_REMOTE)
                _delay += 0.2

            self.relivedCellapps = []
            self.deadApps = []
            self.missedLines.clear()

    def checkAllLineSpaceReady(self, box, callback, args):
        if len(self.lineSpaces) == utils.fetchLineMaxNumber(self.lineType):
            _allLineReady = all([sVal.isSpaceReady() for sVal in self.lineSpaces.values()])
        else:
            _allLineReady = False

        getattr(box, callback)(self.lineType, _allLineReady, *args)

    def willRecoverLine(self, lineNo):
        pass

    def createCellEntityInLine(self, box, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        sVal = self.getLineSpaceVal(lineNo)
        if not sVal:
            LOG_ERR('createCellEntityInLine: invalid spaceNo', box.id, spaceNo)
            return

        if not sVal.lineSpaceBox:
            LOG_ERR('createCellEntityInLine: invalid spaceBox', box.id, spaceNo)
            return

        sVal.lineSpaceBox.createCellNearSelf(box)

    def getLineNoReadyForEnter(self):
        return sorted([_lineNo for _lineNo, sVal in self.lineSpaces.items() if sVal.isReadyEnter()])

    def createRefreshTimers(self):
        for lineNo, line in self.lineSpaces.items():
            spaceNo = formula.combineLineSpaceNo(gameconst.SpaceType.SpaceLine, lineNo)
            policyIdsMap = []
            self.createRefreshTimers(spaceNo, policyIdsMap)

    def onRefreshEntity(self, spaceNo, entId):
        pass

    def onCollectionBeCollectAndDestroyed(self, spaceNo, posIndex, gameEntityId):
        LOG_DBG('onCollectionBeCollectAndDestroyed::', spaceNo, posIndex, gameEntityId)

    def onLoadGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onLoadGroupEntities", info, lineNoList)
        if len(lineNoList) <= 0:
            LOG_WARN('ILineSpaceStub::onLoadGroupEntities: no lineNo found')
            return

        for lineNo in lineNoList:
            info['spaceNo'] = formula.combineLineSpaceNo(self.lineType, lineNo)
            LOG_DBG("ILineSpaceStub::onLoadGroupEntities lineNo, spaceNo", lineNo, info['spaceNo'])
            spaceVal = self.getLineSpaceVal(lineNo)
            spaceVal.lineSpaceBox.cell.callOnSpace('onLoadGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onRefreshGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onRefreshGroupEntities", info, lineNoList)
        if len(lineNoList) <= 0:
            LOG_WARN('ILineSpaceStub::onRefreshGroupEntities: no lineNo found')
            return
        lineNo = info['lineNo']
        if lineNo not in lineNoList:
            LOG_WARN('ILineSpaceStub::onRefreshGroupEntities: lineNo not found', lineNo, lineNoList)
            return

        info['spaceNo'] = formula.combineLineSpaceNo(self.lineType, lineNo)
        LOG_DBG("ILineSpaceStub::onRefreshGroupEntities lineNo, spaceNo", lineNo, info['spaceNo'])
        spaceVal = self.getLineSpaceVal(lineNo)
        spaceVal.lineSpaceBox.cell.callOnSpace('onRefreshGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onDestroyGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onDestroyGroupEntities", info, lineNoList)

        if not info.get('spaceNo', None):
            LOG_WARN('ILineSpaceStub::onDestroyGroupEntities: spaceNo not found', info, lineNoList)
            return

        spaceVal = self.getLineSpaceVal(formula.parseLineNo(info['spaceNo']))
        spaceVal.lineSpaceBox.cell.callOnSpace('onDestroyGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onGetShowMapEntityInfo(self, player, mapId, lineNo):
        LOG_DBG("ILineSpaceStub::onGetShowMapEntityInfo", mapId, lineNo)
        spaceVal = self.getLineSpaceVal(lineNo)
        spaceVal.lineSpaceBox.cell.callOnSpaceMgr('onGetShowMapEntityInfo', (player, ))
