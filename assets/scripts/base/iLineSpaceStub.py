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
import worldBoss_base as WB_BASE
import creep_base as CBD
import creep_title as CTD


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
        LOG_INFO('zt: create line', formula.lineInfo(self.lineType, lineNo, _spaceNo), spaceWeight, cellappIndx)
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
        LOG_INFO('onSpaceLineReady', formula.lineInfo(self.lineType, spaceNo=spaceNo))
        lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces[lineNo].lineSpaceReady()
        
        # spaceVal = self.getLineSpaceVal(lineNo)
        # spaceVal.lineSpaceBox.cell.doLoadEntities(0)

    def onSpaceMgrReady(self, spaceNo, spaceMgrCell):
        LOG_DBG("iLineSpaceStub onSpaceMgrReady", formula.lineInfo(self.lineType, spaceNo=spaceNo), spaceMgrCell)
        lineNo = formula.parseLineNo(spaceNo)
        spaceVal = self.getLineSpaceVal(lineNo)
        spaceVal.setSpaceMgrBoxCell(spaceMgrCell)

    def onLoadEntitiesEnd(self, spaceNo):
        LOG_DBG("iLineSpaceStub onLoadEntitiesEnd", formula.lineInfo(self.lineType, spaceNo=spaceNo))
        lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces[lineNo].lineEntitiesReady()
        self.batchlyCall(self.sendLineInfoOnSpaceChanged(), 50)

        gameengine.callBaseApps('gameglobal.onLineEntityReady', (spaceNo,))

    def handleCellappDeath(self, cellId):
        # cellId 为死亡 cellapp 的 cid(componentID)。每个 baseapp 都会收到
        # onCellAppDeath 并转发到本 stub, 但只有 cid 在所有进程间一致,
        # 用 groupOrder 去重会把一次死亡记成多个不同 cellapp。
        if cellId not in self.deadApps:
            self.deadApps.append(cellId)
        LOG_INFO('handleCellappDeath', self.id, cellId, self.deadApps)

    def onLineSpaceGone(self, spaceNo):
        LOG_ERR('onLineSpaceGone', formula.lineInfo(self.lineType, spaceNo=spaceNo))
        _lineNo = formula.parseLineNo(spaceNo)
        self.lineSpaces.pop(_lineNo, None)
        self.collectionSharedLimitDic.pop(spaceNo, None)
        # 只需要记录哪些 line 丢了, 恢复时按 key(lineNo) 重建, 值不再使用
        self.missedLines[_lineNo] = 0

    def onCellappRelive(self, cellId):
        if cellId not in self.relivedCellapps:
            self.relivedCellapps.append(cellId)
        LOG_INFO('LineStub:onCellappRelive', cellId, self.deadApps, self.relivedCellapps)

        self._doRecoverLines()

    def _doRecoverLines(self):
        if len(self.relivedCellapps) == len(self.deadApps):
            LOG_INFO('recove lines:', formula.lineInfo(self.lineType), self.missedLines)
            _delay = 0
            for ln in self.missedLines:
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
            LOG_ERR('createCellEntityInLine: invalid spaceNo', formula.lineInfo(self.lineType, spaceNo=spaceNo), box.id)
            return

        if not sVal.lineSpaceBox:
            LOG_ERR('createCellEntityInLine: invalid spaceBox', formula.lineInfo(self.lineType, spaceNo=spaceNo), box.id)
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

    def onLoadGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onLoadGroupEntities", formula.lineInfo(self.lineType), info, lineNoList)
        if len(lineNoList) <= 0:
            LOG_WARN('ILineSpaceStub::onLoadGroupEntities: no lineNo found', formula.lineInfo(self.lineType))
            return

        for lineNo in lineNoList:
            info['spaceNo'] = formula.combineLineSpaceNo(self.lineType, lineNo)
            LOG_DBG("ILineSpaceStub::onLoadGroupEntities", formula.lineInfo(self.lineType, lineNo, info['spaceNo']))
            spaceVal = self.getLineSpaceVal(lineNo)
            if not spaceVal or not spaceVal.lineSpaceBox:
                LOG_ERR('ILineSpaceStub::onLoadGroupEntities invalid lineNo', formula.lineInfo(self.lineType, lineNo))
                continue
            spaceVal.lineSpaceBox.cell.callOnSpace('onLoadGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onRefreshGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onRefreshGroupEntities", formula.lineInfo(self.lineType), info, lineNoList)
        if len(lineNoList) <= 0:
            LOG_WARN('ILineSpaceStub::onRefreshGroupEntities: no lineNo found', formula.lineInfo(self.lineType))
            return
        lineNo = info['lineNo']
        if lineNo not in lineNoList:
            LOG_WARN('ILineSpaceStub::onRefreshGroupEntities: lineNo not found', formula.lineInfo(self.lineType, lineNo), lineNoList)
            return

        info['spaceNo'] = formula.combineLineSpaceNo(self.lineType, lineNo)
        LOG_DBG("ILineSpaceStub::onRefreshGroupEntities", formula.lineInfo(self.lineType, lineNo, info['spaceNo']))
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal or not spaceVal.lineSpaceBox:
            LOG_ERR('ILineSpaceStub::onRefreshGroupEntities invalid lineNo', formula.lineInfo(self.lineType, lineNo))
            return
        spaceVal.lineSpaceBox.cell.callOnSpace('onRefreshGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onDestroyGroupEntities(self, info):
        lineNoList = list(self.lineSpaces.keys())
        LOG_DBG("ILineSpaceStub::onDestroyGroupEntities", formula.lineInfo(self.lineType), info, lineNoList)

        if not info.get('spaceNo', None):
            LOG_WARN('ILineSpaceStub::onDestroyGroupEntities: spaceNo not found', formula.lineInfo(self.lineType), info, lineNoList)
            return

        spaceVal = self.getLineSpaceVal(formula.parseLineNo(info['spaceNo']))
        if not spaceVal or not spaceVal.lineSpaceBox:
            LOG_ERR('ILineSpaceStub::onDestroyGroupEntities invalid lineNo', formula.lineInfo(self.lineType, spaceNo=info['spaceNo']))
            return
        spaceVal.lineSpaceBox.cell.callOnSpace('onDestroyGroupEntities', (info, spaceVal.spaceMgrBoxCell.id))

    def onGetShowMapEntityInfo(self, player, mapId, lineNo):
        LOG_DBG("ILineSpaceStub::onGetShowMapEntityInfo", formula.lineInfo(mapId, lineNo))
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal or not spaceVal.lineSpaceBox:
            LOG_ERR('ILineSpaceStub::onGetShowMapEntityInfo invalid lineNo', formula.lineInfo(mapId, lineNo))
            return
        spaceVal.lineSpaceBox.cell.callOnSpaceMgr('onGetShowMapEntityInfo', (player, ))

    def checkSpecialLineTypeCrossWorld(self, isCross):
        LOG_DBG("ILineSpaceStub::checkSpecialLineTypeCrossWorld", isCross)
        if self.lineType not in B_BD.datas:
            return False
        
        bossSIds = WB_BASE.allCross2BossSId if isCross else WB_BASE.allLocal2BossSId
        bossSId = bossSIds.get(self.lineType, 0)
        dataCfg = WB_BASE.datas.get(bossSId, None)
        if not dataCfg:
            LOG_DBG("ILineSpaceStub::checkSpecialLineTypeCrossWorld invalid bossSId", bossSIds, self.lineType)
            return False
        bossEIdkey = 'crossBossID' if isCross else 'localBossID'
        bossEId = dataCfg[bossEIdkey]

        dunData = utils.getDunModuleData(self.lineType)
        if not dunData:
            LOG_ERR('ILineSpaceStub::checkSpecialLineTypeCrossWorld invalid mapId', self.lineType)
            return False
        posData = dunData[str(bossEId)]
        entityId = posData['EntityID']

        nameSuffixID = -1
        if entityId in CBD.datas:
            nameSuffixID = CBD.datas[entityId]['nameSuffixID']

        if CTD.datas.get(nameSuffixID, {}).get('ifBranchRefresh', 1):
            return False
        
        LOG_INFO("ILineSpaceStub::checkSpecialLineTypeCrossWorld True")
        return True

    def onCrossWorld(self, extra):
        LOG_INFO("ILineSpaceStub::onCrossWorld", formula.lineInfo(self.lineType), extra)

        isCross = extra.get('isCross', False)
        lineNoList = []
        if self.checkSpecialLineTypeCrossWorld(isCross):
            lineNoList.append(0)
        else:
            lineNoList = list(self.lineSpaces.keys())

        line = extra.get('lineNo', None)
        if line == None:
            pass
        elif line not in lineNoList:
            lineNoList = []
        else:
            lineNoList = [line]

        for lineNo in lineNoList:
            spaceVal = self.getLineSpaceVal(lineNo)
            if not spaceVal:
                LOG_ERR('ILineSpaceStub::onCrossWorld invalid lineNo1', formula.lineInfo(self.lineType, lineNo))
                continue
            LOG_INFO("ILineSpaceStub::onCrossWorld", formula.lineInfo(self.lineType, lineNo), spaceVal, spaceVal.isSpaceReady(), spaceVal.lineStatus)
            if spaceVal.spaceMgrBoxCell:
                spaceVal.spaceMgrBoxCell.callOnSpaceMgr('onCrossWorld', (extra, ))
            elif spaceVal.lineSpaceBox:
                spaceVal.lineSpaceBox.cell.callOnSpaceMgr('onCrossWorld', (extra, ))
            else:
                LOG_ERR('ILineSpaceStub::onCrossWorld invalid lineNo2', formula.lineInfo(self.lineType, lineNo))