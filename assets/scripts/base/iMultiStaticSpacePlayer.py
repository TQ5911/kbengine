# coding: utf-8
import KBEngine
from KBEDebug import *

import formula
import random
import gameconst
import linePlayers
import utils
import branchData_branchData as B_BD


class IMultiStaticSpacePlayer(object):
    def __init__(self, maxEnterNum):
        self.maxEnterNum = maxEnterNum
        self.allLines = {}
        self.allPlayers = {}
        self.clearTimeOutIter = None

    def genClearTimeOutIter(self):
        for _spaceNo in list(self.allLines.keys()):
            yield _spaceNo

    def onClearEnterTimeOut(self, timeOutDuration):
        if self.clearTimeOutIter is None:
            self.clearTimeOutIter = self.genClearTimeOutIter()

        _spaceNo = next(self.clearTimeOutIter, None)
        if _spaceNo is None:
            self.clearTimeOutIter = self.genClearTimeOutIter()
            return

        _linePlayers = self.allLines.get(_spaceNo)

        _timeoutTime = utils.curTS() - timeOutDuration
        _lineCtx = formula.lineInfo(spaceNo=_spaceNo)
        if not _linePlayers:
            LOG_WARN('onClearEnterTimeOut: _linePlayers is None', _lineCtx)
            return
        
        _clearList = _linePlayers.clearTimeOutInfo(_timeoutTime)
        if _clearList:
            LOG_ERR('onClearEnterTimeOut: clear timeout players', _lineCtx, 'clearList', _clearList)
            for _gbId in _clearList:
                self.allPlayers.pop(_gbId, None)

    def getSpaceAvatarNo(self, spaceNo):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            return 0

        return len(_linePlayers) + len(_linePlayers.pendingEnterPlayersDic)

    def canSpaceEnter(self, spaceNo):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            return True

        _curNum = len(_linePlayers) + len(_linePlayers.pendingEnterPlayersDic)
        return _curNum < self.maxEnterNum

    def addPendingEnterPlayer(self, spaceNo, gbId):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(spaceNo))
            self.allLines[spaceNo] = _linePlayers

        _linePlayers.doAddPendingEnterPlayer(None, gbId)

    def addEnterPlayer(self, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        if gbId in self.allPlayers:
            LOG_ERR('addEnterPlayer:already in allPlayers', formula.lineInfo(spaceNo=curSpaceNo), gbId)
            return

        _linePlayers = self.allLines.get(curSpaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(curSpaceNo))
            self.allLines[curSpaceNo] = _linePlayers

        _linePlayers.doAddLinePlayer(None, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo)
        self.allPlayers[gbId] = _linePlayers[gbId]

    def enterSpaceFailed(self, gbId, spaceNo):
        LOG_WARN('enterSpaceFailed', formula.lineInfo(spaceNo=spaceNo), gbId)
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            return

        if not _linePlayers.doEnterSpaceFailed(gbId):
            # 可能只是pending中pop掉了，没必要pop全局的
            return
        
        self.allPlayers.pop(gbId, None)

    def removePlayer(self, gbId):
        _playerVal = self.allPlayers.pop(gbId, None)
        if not _playerVal:
            return

        _linePlayers = self.allLines.get(_playerVal.curSpaceNo)
        if not _linePlayers:
            LOG_ERR('removePlayer:linePlayers not found', formula.lineInfo(spaceNo=_playerVal.curSpaceNo), gbId)
            return

        _linePlayers.doRemoveLinePlayer(gbId)

    def switchStaticSpace(self, gbId, toSpaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('switchStaticSpace:player not found', formula.lineInfo(spaceNo=toSpaceNo), gbId)
            return

        if _playerVal.curSpaceNo == toSpaceNo:
            LOG_ERR('switchStaticSpace:spaceNo same', formula.lineInfo(spaceNo=toSpaceNo), gbId)
            return

        _isLeader = False
        _linePlayers = self.allLines.get(_playerVal.curSpaceNo)
        if _playerVal.teamUUID:
            _isLeader = _linePlayers.teamPlayersDic.get(_playerVal.teamUUID, {}).get(gbId, False)

        _linePlayers.doRemoveLinePlayer(gbId)

        _playerVal.curSpaceNo = toSpaceNo
        _linePlayers = self.allLines.get(toSpaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(toSpaceNo))
            self.allLines[toSpaceNo] = _linePlayers

        _linePlayers.doAddLinePlayerVal(_playerVal, _isLeader)

    def getMapBranchLinePlayers(self, lineType):
        LOG_INFO('getMapBranchLinePlayers', formula.lineInfo(lineType))
        ret = {}
        if lineType not in B_BD.datas:
            LOG_ERR('getMapBranchLinePlayers:lineType not found', formula.lineInfo(lineType))
            return ret
        for lineNo in range(gameconst.getBranchLineCnt(lineType)):
            _spaceNo = formula.combineLineSpaceNo(lineType, lineNo)
            _linePlayers = self.allLines.get(_spaceNo)
            if not _linePlayers:
                _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(_spaceNo))
                self.allLines[_spaceNo] = _linePlayers
            ret[lineNo] = _linePlayers
            LOG_DBG('getMapBranchLinePlayers', formula.lineInfo(lineType, lineNo), _linePlayers)

        return ret
