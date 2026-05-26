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
        if not _linePlayers:
            LOG_WARN('onClearEnterTimeOut:spaceNo={}, _linePlayers is None'.format(_spaceNo))
            return
        
        _clearList = _linePlayers.clearTimeOutInfo(_timeoutTime)
        if _clearList:
            LOG_ERR('onClearEnterTimeOut:spaceNo={}, clearList={}'.format(_spaceNo, _clearList))
            for _gbId in _clearList:
                self.allPlayers.pop(_gbId, None)

    def getSpaceAvatarNo(self, spaceNo):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            return 0

        return len(_linePlayers) + len(_linePlayers.pendingEnterPlayers)

    def canSpaceEnter(self, spaceNo):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            return True

        _curNum = len(_linePlayers) + len(_linePlayers.pendingEnterPlayers)
        return _curNum < self.maxEnterNum

    def addPendingEnterPlayer(self, spaceNo, gbId):
        _linePlayers = self.allLines.get(spaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(spaceNo))
            self.allLines[spaceNo] = _linePlayers

        _linePlayers.addPendingEnterPlayer(None, gbId)

    def addEnterPlayer(self, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        if gbId in self.allPlayers:
            LOG_ERR('addEnterPlayer:already in allPlayers', gbId)
            return

        _linePlayers = self.allLines.get(curSpaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(curSpaceNo))
            self.allLines[curSpaceNo] = _linePlayers

        _linePlayers.doAddLinePlayer(None, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo)
        self.allPlayers[gbId] = _linePlayers[gbId]

    def removePlayer(self, gbId):
        _playerVal = self.allPlayers.pop(gbId, None)
        if not _playerVal:
            return

        _linePlayers = self.allLines.get(_playerVal.curSpaceNo)
        if not _linePlayers:
            LOG_ERR('removePlayer:linePlayers not found', _playerVal.curSpaceNo)
            return

        _linePlayers.doRemoveLinePlayer(None, gbId)

    def switchStaticSpace(self, gbId, toSpaceNo):
        _playerVal = self.allPlayers.get(gbId)
        if not _playerVal:
            LOG_ERR('switchStaticSpace:player not found', gbId)
            return

        if _playerVal.curSpaceNo == toSpaceNo:
            LOG_ERR('switchStaticSpace:spaceNo same', toSpaceNo)
            return

        _isLeader = False
        _linePlayers = self.allLines.get(_playerVal.curSpaceNo)
        if _playerVal.teamUUID:
            _isLeader = _linePlayers.teamPlayers.get(_playerVal.teamUUID, {}).get(gbId, False)

        _linePlayers.doRemoveLinePlayer(None, gbId)

        _playerVal.curSpaceNo = toSpaceNo
        _linePlayers = self.allLines.get(toSpaceNo)
        if not _linePlayers:
            _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(toSpaceNo))
            self.allLines[toSpaceNo] = _linePlayers

        _linePlayers.doAddLinePlayerVal(_playerVal, _isLeader)

    def getMapBranchLinePlayers(self, lineType):
        LOG_INFO('getMapBranchLinePlayers', lineType)
        ret = {}
        if lineType not in B_BD.datas:
            LOG_ERR('getMapBranchLinePlayers:lineType not found', lineType)
            return ret
        for lineNo in range(gameconst.getBranchLineCnt(lineType)):
            _spaceNo = formula.combineLineSpaceNo(lineType, lineNo)
            _linePlayers = self.allLines.get(_spaceNo)
            if not _linePlayers:
                _linePlayers = linePlayers.LinePlayers(formula.parseLineNo(_spaceNo))
                self.allLines[_spaceNo] = _linePlayers
            ret[lineNo] = _linePlayers
            LOG_INFO('getMapBranchLinePlayers:lineNo={}, linePlayers={}'.format(lineNo, _linePlayers))

        return ret
