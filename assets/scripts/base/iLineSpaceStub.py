# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameengine
import iGlobal
import iBaseNoCell
import iTimer
import iCycleEvent
import gametimer
import gameconfig
import asyncore
import gmCommand
import gameglobal
import gameconst
import formula
import random
import utils
import StaticSpaceVal

import branchData_branchData as BBD

import lineSpace
import iMapRefresher


class ILineSpaceStub(object):
    def __init__(self):
        pass

    def doNext(self):
        if hasattr(super(), 'doNext'):
            super().doNext()
        self.createLines()

    def createLines(self):
        for ln in range(utils.fetchLineMaxNumber(self.lineType)):
            lineMaxCnt = BBD.datas[self.lineType]['N1']
            spaceWeight = utils.calcSpaceWeight(0, False, gameconst.EntNumPerPlayerInAOI.worldLine, lineMaxCnt/10)
            self.addTimerCB(ln*0.2, '_createLineSpaceRemote', (ln,spaceWeight), gametimer.TIMER_TAG_CREATE_LINE_SPACE_REMOTE)

    def newLineSpaceVal(self, lineType, lineNo):
        # return lineSpace.LineSpaceVal(lineType, lineNo, lineSpace.LineSpaceVal.LINE_CREATING)
        return StaticSpaceVal.StaticSpaceVal(lineType, lineNo)

    def getLineSpaceVal(self, lineNo):
        #TODO临时改动，等正式策划案出来再正式改
        lineNo = min(len(self.lineSpaces)-1, lineNo)
        return self.lineSpaces[lineNo]

    def createCellEntityInSpace(self, spaceNo, className, bornPosition, bornDirection, params):
        lineNo = formula.parseLineNo(spaceNo)
        spaceVal = self.getLineSpaceVal(lineNo)
        params['spaceMgrId'] = spaceVal.spaceMgrBoxCell.id

        spaceVal.lineSpaceBox.cell.createCellLocally(className, bornPosition, bornDirection, params)

    def _createLineSpaceRemote(self, lineNo, spaceWeight=10):
        spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)

        self.lineSpaces[lineNo] = self.newLineSpaceVal(self.lineType, lineNo)

        cellappIndx = lineNo + 1 + gameconst.getWorldLineCellIdx(self.lineType)
        LOG_IFO('zt: create line', lineNo, spaceNo, spaceWeight, self.lineType, cellappIndx)
        KBEngine.createEntityAnywhere('Space',
                                      {
                                          'spaceno': spaceNo,
                                          'spaceNo': spaceNo,
                                          'position': gameconst.SPACE_FIX_POS,
                                          'spaceWeight': spaceWeight,
                                          'cellappIndex': cellappIndx
                                      },
                                      lambda spaceBox, spaceNo=spaceNo:
                                      self._onCreateLineSpace(spaceBox, spaceNo)
                                      )

    def _createLineSpaceLocal(self, lineNo, spaceWeight=10):
        spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)
        LOG_IFO('zt: create line locally', lineNo, spaceNo, spaceWeight)

        self.lineSpaces[lineNo] = self.newLineSpaceVal(self.lineType, lineNo)

        cellappIndx = lineNo + 1
        s = KBEngine.createEntityLocally('Space',
                                         {
                                             'spaceno': spaceNo,
                                             'spaceNo': spaceNo,
                                             'lineStubIdx': self.lineStubIdx,
                                             'position': gameconst.SPACE_FIX_POS,
                                             'spaceWeight': spaceWeight,
                                             'cellappIndex': cellappIndx
                                         })
        self._onCreateLineSpace(s, spaceNo)

    def _onCreateLineSpace(self, spaceBox, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        sVal = self.getLineSpaceVal(lineNo)
        sVal.lineSpaceBox = spaceBox

    def onLineSpaceReady(self, spaceNo):
        LOG_IFO('onLineSpaceReady', spaceNo)
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
        LOG_IFO('handleCellappDeath', groupOrder)
        if groupOrder not in self.deadApps:
            self.deadApps.append(groupOrder)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        LOG_ERR('onLineSpaceGone', spaceNo, groupOrder)
        lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces.pop(lineNo, None)
        self.collectionSharedLimitDic.pop(spaceNo, None)
        self.missedLines[lineNo] = groupOrder

    def onCellappRelive(self, groupOrder):
        if groupOrder not in self.relivedCellapps:
            self.relivedCellapps.append(groupOrder)
        LOG_IFO('LineStub:onCellappRelive', groupOrder, self.deadApps, self.relivedCellapps)

        self._tryRecoverLines()

    def _tryRecoverLines(self):
        if len(self.relivedCellapps) == len(self.deadApps):
            LOG_IFO('recove lines:', self.missedLines)
            delay = 0
            for ln, order in self.missedLines.items():
                self.willRecoverLine(ln)
                self.addTimerCB(delay, '_createLineSpaceRemote', (ln,), gametimer.TIMER_TAG_CREATE_LINE_SPACE_REMOTE)
                delay += 0.2

            self.relivedCellapps = []
            self.deadApps = []
            self.missedLines.clear()

    def willRecoverLine(self, lineNo):
        pass

    def checkAllLineSpaceReady(self, box, callback, args):
        if len(self.lineSpaces) == utils.fetchLineMaxNumber(self.lineType):
            allLineReady = all([sVal.isSpaceReady() for sVal in self.lineSpaces.values()])
        else:
            allLineReady = False

        getattr(box, callback)(self.lineType, allLineReady, *args)

    def getLineNoReadyForEnter(self):
        return sorted([lineNo for lineNo, sVal in self.lineSpaces.items() if sVal.isReadyEnter()])

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

    def createRefreshTimers(self):
        for lineNo, line in self.lineSpaces.items():
            spaceNo = formula.combineLineSpaceNo(gameconst.SpaceType.SpaceLine, lineNo)
            policyIdsMap = []
            self.createRefreshTimers(spaceNo, policyIdsMap)

    def onRefreshEntity(self, spaceNo, entId):
        pass

    def onCollectionBeCollectAndDestroyed(self, spaceNo, posIndex, gameEntityId):
        LOG_DBG('onCollectionBeCollectAndDestroyed::', spaceNo, posIndex, gameEntityId)

    def loadSingleEntity(self, spaceNo, clsName, needCreateBase, pos, direction, props):
        # LOG_DBG("--- iLineSpaceStub loadSingleEntity", spaceNo, clsName, pos, direction, props)
        if needCreateBase:
            props.update({
                'spaceNo': spaceNo,
                'pos': pos,
                'direction': direction
            })
            e = KBEngine.createEntityLocally(
                clsName,
                props
            )
            if not e:
                LOG_ERR("loadSingleEntity base entity failed", clsName)
            if clsName == 'MonsterGrp':
                e.createMonstersFromGrp(props)
        else:
            self.createCellEntityInSpace(spaceNo, clsName, pos, direction, props)

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
