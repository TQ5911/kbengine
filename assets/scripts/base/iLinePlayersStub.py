# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import gameengine
import gametimer
import gameconfig
import gameglobal
import formula
import gameconst
import utils
import random

import linePlayers
import json

import branchData_branchData as B_BD
import gamePlay_gamePlay as GGD
import branchData_set as BDS


class EnterLineExtra(object):
    @classmethod
    def new(cls, dataDic, lineNo):
        _ret = cls()
        _ret.__dict__.update(dataDic)

        _ret.isAuto = (lineNo < 0)
        _ret.isLeader = 'followers' in dataDic
        _ret.fromLineNo = dataDic.get('fromLineNo', -1)

        return _ret

    def __init__(self):
        self.teamUUID = 0
        self.followers = []
        self.isLeader = False
        self.isAuto = False
        self.position = None
        self.guildUUID = 0
        self.isLogin = 0
        self.fromLineNo = -1

#分线相关，不改父类属性
class IBranchLineStub(object):
    def __init__(self):
        self.mergeRes = {}
        self.fightingPlayersCntBase = {}
        self.lastChooseLineNo = 0

    def _checkSelectLine(self, lineNo, box, gbId, extraInfo, exlude=None, isSwitchLine=False, lineType=None, checkCellAvatarCount=True):
        LOG_DBG("checkSelectLine", lineNo, box, gbId, extraInfo, exlude, isSwitchLine, lineType)
        lineType = lineType or self.lineType
        needCnt = len(extraInfo.followers) + 1

        if exlude and lineNo in exlude:
            return gameconst.EnterLineCodeEnum.ERR_EXLUDE

        # TODO X: validate line config
        lineMaxCnt = B_BD.datas[lineType]['N1']
        N2Cnt = B_BD.datas[lineType]['N2']
        N3Cnt = B_BD.datas[lineType]['N3']
        
        if not self.isSpaceReadyEnter(lineType, lineNo):
            return gameconst.EnterLineCodeEnum.ERR_SPACE_IS_NOT_READY
            
        allPlayers = self.getMapBranchLinePlayers(lineType)
        lineMembers = allPlayers[lineNo]

        _hasLeader = extraInfo.teamUUID and lineMembers.getLeaderGbId(extraInfo.teamUUID)
        hasMember = _hasLeader or (extraInfo.teamUUID and lineMembers.hasTeamMember(extraInfo.teamUUID))

        playerNum = len(lineMembers) + lineMembers.getPendingEnterNum()

        # 单条线人数超过上限，禁止进入
        if playerNum + needCnt > lineMaxCnt:
            return gameconst.EnterLineCodeEnum.ERR_REACH_MAX_MEMBER

        # 单线每秒人数超过上限，禁止进入(只在登录时限制)
        if extraInfo.isLogin and lineMembers.getPendingEnterNumNowSec() >= gameconfig.loginLinePlayerNumLimit():
            return gameconst.EnterLineCodeEnum.ERR_REACH_SEC_LIMIT
        
        # 人数 > N2 且 该线没有队友
        if playerNum > N2Cnt and not hasMember:
            return gameconst.EnterLineCodeEnum.ERR_ONLY_TEAM_MEMBER
        
        # 人数 > N3 且 是自动就不能进了
        if playerNum > N3Cnt and extraInfo.isAuto and not hasMember:
            return gameconst.EnterLineCodeEnum.ERR_CANNOT_AUTO_ENTER
        
        mergeRes = self.mergeRes.get(lineType, None)
        if mergeRes:
            for i, res in mergeRes:
                if lineNo in res:
                    return gameconst.EnterLineCodeEnum.ERR_MERGE_LINE

        if checkCellAvatarCount:
            if formula.checkWorldLineType(lineType):
                cellappIndx = (lineNo + 1 + gameconst.getWorldLineCellIdx(lineType)) % gameconfig.cellAppCount()
                if cellappIndx == 0:
                    cellappIndx = gameconfig.cellAppCount()
                cellAvatarCount = gameglobal.cellAvatarCountDict.get(cellappIndx, 0)
                LOG_INFO("checkmaxCellAvatarCount", cellappIndx, cellAvatarCount)
                if cellAvatarCount >= gameconfig.maxCellAvatarCount():
                    return gameconst.EnterLineCodeEnum.ERR_REACH_MAX_AVATAR_COUNT

        return gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS

    def _autoSelectLine(self, box, gbId, extraInfo, exlude=None, isSwitchLine=False, lineType=None):
        lineType = lineType or self.lineType
        needCnt = len(extraInfo.followers) + 1
        lineMaxCnt = B_BD.datas[lineType]['N1']
        allPlayers = self.getMapBranchLinePlayers(lineType)

        # 有队伍且不是队长，优先找队长
        if extraInfo.teamUUID and not extraInfo.isLeader:
            for lineNo, lineMembers in allPlayers.items():
                if lineMembers.getLeaderGbId(extraInfo.teamUUID) and len(lineMembers) + needCnt <= lineMaxCnt:
                    return lineNo

        n5list = []
        lineNoList = sorted(allPlayers.keys())
        if BDS.datas["Branch_allocationPlan"]["value"] == 1:
            newLineNoList = []
            usedLineNoSet = set()
            lineInfo = self._calculateLineInfo(lineType)
            if gameconfig.switchLineUselastLineNo():
                if self.lastChooseLineNo in allPlayers:
                    maxNum = 0
                    for k, v in lineInfo['info'].items():
                        if k != self.lastChooseLineNo:
                            maxNum = max(maxNum, v)
                    LOG_INFO("lastChooseLineNo", self.lastChooseLineNo, lineInfo, maxNum)
                    if len(allPlayers[self.lastChooseLineNo]) <= maxNum + BDS.datas["Branch_mergeFloatRange"]["value"]:
                        newLineNoList.append(self.lastChooseLineNo)
                        if self.lastChooseLineNo in lineInfo['info']:
                            lineInfo['info'].pop(self.lastChooseLineNo)
            newLineNoList.extend(sorted(lineInfo['info'], key=lambda x: lineInfo['info'][x]))
            for lineNo in newLineNoList:
                usedLineNoSet.add(lineNo)
            for lineNo in lineNoList:
                if lineNo not in usedLineNoSet:
                    newLineNoList.append(lineNo)
            lineNoList = newLineNoList
            LOG_INFO("lineNoList", lineNoList)

        for lineNo in lineNoList:
            checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo, exlude, isSwitchLine, lineType)
            if checkCode == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
                return lineNo
            elif checkCode == gameconst.EnterLineCodeEnum.ERR_REACH_MAX_AVATAR_COUNT:
                n5list.append(lineNo)
        
        if n5list:
            LOG_INFO("give n5 list", n5list[0])
            return n5list[0]
        LOG_WARN('cannot select line', box.id, gbId, needCnt,
                    [len(lineMembers) for lineMembers in allPlayers.values()])

        return -1

    def _calculateLineInfo(self, lineType=None):
        if lineType is None:
            lineType = self.lineType

        res = {'lineType': lineType, 'info': {}}
        if lineType not in B_BD.datas:
            return res
        
        baseLineNum = B_BD.datas[lineType]['num']
        maxLineNum = gameconst.getBranchLineCnt(lineType)
        addRequired = B_BD.datas[lineType]['AddRequired']

        needNewLine = True
        for lineNo in range(gameconst.getBranchLineCnt(lineType)):
            cnt = self.getSpaceAvatarNo(formula.combineLineSpaceNo(lineType, lineNo))
            LOG_INFO("calculateLineInfo", lineType, lineNo, cnt)
            if not self.isSpaceReadyEnter(lineType, lineNo):
                continue

            if lineNo < baseLineNum or cnt > 0:
                res['info'][lineNo] = cnt

                ifSafeArea = GGD.datas[lineType]['ifSafeArea']
                activeCnt = cnt if ifSafeArea else self.fightingPlayersCntBase.get(lineType, {}).get(lineNo, 0)
                if activeCnt < addRequired:
                    needNewLine = False
                continue

        if needNewLine:
            for i in range(1, maxLineNum):
                if i not in res['info']:
                    res['info'][i] = self.getSpaceAvatarNo(formula.combineLineSpaceNo(lineType, i))
                    break

        return res

    def _checkLineMerge(self, lineType=None):
        lineType = lineType or self.lineType
        LOG_DBG('_checkLineMerge', lineType)
        baseLineNum = B_BD.datas[lineType]['num']
        mergeRequired = B_BD.datas[lineType]['MergeRequired']
        allPlayers = self.getMapBranchLinePlayers(lineType)
        
        sortedData = []
        for lineNo, lineMembers in allPlayers.items():
            if lineNo >= baseLineNum and len(lineMembers) > 0:
                sortedData.append((lineNo, len(lineMembers)))
        
        sortedData = sorted(sortedData, key=lambda x: x[1])

        if not sortedData:
            return
        LOG_DBG('sortedData', sortedData)

        idx = 0

        if lineType not in self.mergeRes:
            self.mergeRes[lineType] = []
        #将下标j的线合到下标i的线
        for i in range(len(allPlayers)):
            sumCnt = len(allPlayers[i])
            res = []
            for j in range(idx, len(sortedData)):
                #要合的线no大于当前的，就结算
                if i >= sortedData[j][0]:
                    break

                num = sortedData[j][1]
                if sumCnt + num <= mergeRequired:
                    res.append(sortedData[j][0])
                    sumCnt += num
                    idx = j + 1
                else:
                    break
            if res:
                self.mergeRes[lineType].append((i, res))

        if not self.mergeRes[lineType]:
            return

        LOG_DBG('mergeRes', self.mergeRes[lineType])
        msgID = BDS.datas["Branch_mergeNoticeMsg"]["value"]
        for i, res in self.mergeRes[lineType]:
            for lineNo in res:
                lineMembers = allPlayers[lineNo]
                for gbId in list(lineMembers.keys()):
                    _pVal = lineMembers.get(gbId)
                    if not _pVal:
                        continue
                    if not _pVal.playerBox:
                        continue
                    _pVal.playerBox.onMessagePre(msgID, [])

    def _doLineMerge(self, lineType=None):
        lineType = lineType or self.lineType
        if lineType in self.mergeRes:
            LOG_DBG('_doLineMerge', lineType)
            for i, res in self.mergeRes[lineType]:
                self.mergeLine(i, res, lineType)
            self.mergeRes.pop(lineType)

    def mergeLine(self, i, res, lineType=None):
        lineType = lineType or self.lineType
        LOG_DBG('mergeLine', i, res, lineType)
        mergeRequired = B_BD.datas[lineType]['MergeRequired']
        allPlayers = self.getMapBranchLinePlayers(lineType)
        for fromLineNo in res:
            lineMembers = allPlayers[fromLineNo]
            if len(lineMembers) > mergeRequired:
                continue
            for gbId in list(lineMembers.keys()):
                _pVal = lineMembers.get(gbId)
                if not _pVal:
                    continue
                if not _pVal.playerBox:
                    continue
                _pVal.playerBox.cell.onMergeLine(i)

    def onFightingPlayersCntSync(self, spaceNo, cnt):
        lineNo = formula.parseLineNo(spaceNo)
        lineType = formula.parseLineType(spaceNo)
        self.fightingPlayersCntBase.setdefault(lineType, {})
        self.fightingPlayersCntBase[lineType][lineNo] = cnt
        LOG_DBG("onFightingPlayersCntSync", lineType, lineNo, cnt)

class ILinePlayersStub(IBranchLineStub):
    def __init__(self):
        super(ILinePlayersStub, self).__init__()

    def onSpaceLineReady(self, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        self.allPlayers[lineNo] = linePlayers.LinePlayers(lineNo)

    def getMapBranchLinePlayers(self, lineType=None):
        return self.allPlayers

    def genClearTimeOutIter(self):
        for lineNo in list(self.allPlayers.keys()):
            yield lineNo

    def onClearEnterTimeOut(self, timeOutDuration):
        if self.clearTimeOutIter is None:
            self.clearTimeOutIter = self.genClearTimeOutIter()

        lineNo = next(self.clearTimeOutIter, None)
        if lineNo is None:
            self.clearTimeOutIter = self.genClearTimeOutIter()
            return

        _linePlayers = self.allPlayers.get(lineNo)

        _timeoutTime = utils.curTS() - timeOutDuration
        if not _linePlayers:
            LOG_WARN('onClearEnterTimeOut:spaceNo={}, _linePlayers is None'.format(lineNo))
            return

        _clearList = _linePlayers.clearTimeOutInfo(_timeoutTime)
        if _clearList:
            LOG_ERR('onClearEnterTimeOut:spaceNo={}, clearList={}'.format(lineNo, _clearList))
            for _gbId in _clearList:
                self.allPlayers.pop(_gbId, None)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        lineNo = formula.parseLineNo(spaceNo)
        self.allPlayers.pop(lineNo)

        self.batchlyCall(self.sendLineInfoOnSpaceChanged(), 50)

    def onCellappRelive(self, groupOrder):
        pass

    def handleCellappDeath(self, groupOrder):
        pass

    def enterLine(self, lineNo, box, gbId, position, direction, extra):
        _linePlayers = self.allPlayers.getLinePlayers(lineNo) or ()
        LOG_INFO('enterLine', box.id, gbId, lineNo, extra, len(_linePlayers))
        _ext = EnterLineExtra.new(extra, lineNo)

        isAutoSelectedLine = False
        if lineNo < 0:
            lineNo = self._autoSelectLine(box, gbId, _ext)
            isAutoSelectedLine = True

        elif extra.get('isAuto'):
            LOG_ERR('enterline: invalid args', lineNo, gbId, extra)
            return

        if formula.checkWorldLineType(self.lineType) and isAutoSelectedLine and lineNo < 0:
            if 'telToMainCityWhenFull' in extra:
                isTel = extra['telToMainCityWhenFull']
                if not isTel:
                    box.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
                    mpFailCb = extra.get('mpFailCb', None)
                    mpFailCbArgs = extra.get('mpFailCbArgs', (1,))
                    isBase = extra.get('isBase', True)
                    if mpFailCb:
                        if isBase:
                            box.callMethod(mpFailCb, mpFailCbArgs)
                        else:
                            box.cell.callMethod(mpFailCb, mpFailCbArgs)
                else:
                    #目标场景满人了，回到主城
                    returnMapID = GGD.datas[self.lineType]["returnMapID"]
                    extra['isForceEnter'] = True
                    extra.pop('telToMainCityWhenFull')
                    position, direction = formula.getSpaceBornPosAndDir(returnMapID)
                    LOG_DBG('enterLine: telToMainCityWhenFull')
                    gameengine.getLineStub(returnMapID).enterLine(-1, box, gbId, position, direction, extra)
                return
            
            #突破上限强行进入，主城满人的时候再进入才会发生
            if extra.get('isLogin') or extra.get('isForceEnter'):
                LOG_ERR('enterLine: reach max member', box.id, gbId, extra)
                lineNo = random.choice(self.getLineNoReadyForEnter())
            else:
                #没处理到的enterline
                box.onMessagePre(BDS.datas["Branch_fullCapacityMsg"]["value"], [])
                gameengine.panicStack('enterLine: unexpected error', box.id, gbId, extra)
                return

        if lineNo < 0:
            LOG_ERR('enterLine _autoSelectLine failed:', box.id, gbId, extra)
            return

        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            LOG_ERR('enterLine: invalid lineNo', self.lineType, lineNo, box.id, gbId)
            return

        if not extra.get('isLogin'):
            _playerVal = self.allPlayers.getPlayer(-1 if lineNo < 0 else lineNo, gbId)
            if _playerVal:
                LOG_WARN('enterLine: player is already in line', lineNo, _playerVal, _playerVal.playerStatus)

            # 自动选出的已经check过了
            if not isAutoSelectedLine:
                checkCode = self._checkEnterLine(lineNo, box, gbId, _ext)
                if checkCode != gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
                    LOG_INFO('enterLine fail:', lineNo, box.id, gbId, extra, checkCode)

                    # 跟随队长失败需要处理
                    _callback = getattr(box.cell, extra.get('failCallback', ''), None)
                    failArgs = extra.get('callbackArgs', ())
                    if _callback:
                        _callback(checkCode, *failArgs)
                    return

        _spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)
        # 处理连续两次(异常)调用进入分线的情况
        self.removeLinePlayerWhenExist(gbId)
        self.addLinePlayerToLine(lineNo, box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, _spaceNo, extra)
        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)

        _playerVal.playerBox.cell.beginEnterLine(self.lineType, lineNo, spaceVal.lineSpaceBox, position, direction,
                                                extra)
        _playerVal.checkEnterTimer = self.addTimerCB(10, '_checkPlayerEnterLine', (lineNo, box, gbId),
                                                   gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)
        
        LOG_INFO("lastChooseLineNo", self.lastChooseLineNo, "->", lineNo)
        self.lastChooseLineNo = lineNo

    # 进入分线添加playerVal前调用，保证只存在一个playerVal
    def removeLinePlayerWhenExist(self, gbId):
        for lineNo_ in self.allPlayers.keys():
            _playerVal = self.allPlayers.getPlayer(lineNo_, gbId)
            if _playerVal:
                # 如果存在对应timer，需要删除
                if _playerVal.checkEnterTimer:
                    self.cancelTimerCB(_playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

                self.removeLinePlayerFromLine(lineNo_, gbId)
                return

    def removeLinePlayerFromLine(self, lineNo, gbId):
        self.allPlayers.removeLinePlayer(self, lineNo, gbId)

    def addLinePlayerToLine(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extra):
        self.allPlayers.addLinePlayer(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extra)

    def _checkPlayerEnterLine(self, lineNo, box, gbId, checkCnt=0):
        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not _playerVal:
            LOG_ERR('_checkPlayerEnterLine error: player not in line', lineNo, box.id, gbId)
            return

        _playerVal.checkEnterTimer = 0

        if _playerVal.playerStatus != _playerVal.INLINE:
            spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)
            if checkCnt < 5:
                LOG_ERR('_checkPlayerEnterLine fail:', lineNo, box.id, gbId, checkCnt)

            if checkCnt > 3 and not formula.inWorldLineScene(spaceNo):
                self.removeLinePlayerFromLine(lineNo, gbId)
                toSpaceNo = formula.combineLineSpaceNo(self.lineType)
                box.cell.beginLeaveLine(spaceNo, toSpaceNo, formula.getSpaceBornPoint(toSpaceNo)(0, 0, 0))
            else:
                _playerVal.checkEnterTimer = self.addTimerCB(10, '_checkPlayerEnterLine', (lineNo, box, gbId,
                                                                                         checkCnt + 1),
                                                           gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

    def enterLineSuccess(self, lineNo, box, gbId, succInfo):
        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not _playerVal:
            LOG_ERR('enterLineSuccess:player is not in line', lineNo)
            return

        if _playerVal.checkEnterTimer:
            self.cancelTimerCB(_playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)
            _playerVal.checkEnterTimer = 0

        _playerVal.setPlayerStatus(linePlayers.LinePlayerVal.INLINE)

    def enterLineFailed(self, lineNo, box, gbId, extra):
        LOG_INFO('enterLineFailed:', lineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            LOG_ERR('enterLineFailed: invalid lineNo', self.lineType, lineNo, box.id, gbId)
            return

        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not _playerVal:
            LOG_ERR('enterLineFailed:player is not in line', lineNo)
            return

        self.removeLinePlayerFromLine(lineNo, gbId)

    def autoSwitchLine(self, box, gbId, fromSpaceNo, extra, cbName, cbArgs):
        _ext = EnterLineExtra.new(extra, -1)
        fromLineNo = formula.parseLineNo(fromSpaceNo)
        toLineNo = self._autoSelectLine(box, gbId, _ext, exlude=None, isSwitchLine=True)

        if formula.checkWorldLineType(self.lineType) and toLineNo < 0:
            toLineNo = -1
            
            pos, dir = formula.getSpaceBornPosAndDir(self.lineType)
            extra['position'] = pos
            spaceVal = self.getLineSpaceVal(0)

        if fromLineNo != toLineNo and toLineNo != -1:
            lineMembers = self.allPlayers.getLinePlayers(toLineNo)
            if not lineMembers:
                LOG_ERR("autoSwitchLine: toLineNo is not in line", toLineNo)
                return
            lineMembers.addPendingEnterPlayer(self, gbId)

        spaceVal = self.getLineSpaceVal(toLineNo) if toLineNo != -1 else self.getLineSpaceVal(0)
        box.callMethod(cbName, (toLineNo, spaceVal.lineSpaceBox, extra.get('position', None)) + cbArgs)

    #目标线全满了回主城
    def autoSwitchLineToMainCity(self, box, gbId, fromSpaceNo, extra, cbName, cbArgs):
        LOG_DBG("autoSwitchLineToMainCity", box, gbId, fromSpaceNo, extra, cbName, cbArgs)
        ext = EnterLineExtra.new(extra, -1)
        fromLineNo = formula.parseLineNo(fromSpaceNo)
        toLineNo = self._autoSelectLine(box, gbId, ext, exlude=None, isSwitchLine=True)
        pos, dir = formula.getSpaceBornPosAndDir(self.lineType)
        extra['position'] = pos

        if formula.checkWorldLineType(self.lineType) and toLineNo < 0:
            toLineNo = random.choice(self.getLineNoReadyForEnter())

        if fromLineNo != toLineNo:
            _lineMembers = self.allPlayers.getLinePlayers(toLineNo)
            if not _lineMembers:
                LOG_ERR("autoSwitchLineToMainCity: toLineNo is not in line", toLineNo)
                return
            _lineMembers.addPendingEnterPlayer(self, gbId)

        _spaceVal = self.getLineSpaceVal(toLineNo)
        box.callMethod(cbName, (toLineNo, _spaceVal.lineSpaceBox, extra.get('position', None)) + cbArgs)

    def doSwitchLine(self, fromLineNo, toLineNo, box, gbId, extraData):
        LOG_INFO('doSwitchLine', fromLineNo, toLineNo, box.id, gbId)
        _ext = EnterLineExtra.new(extraData, toLineNo)
        if toLineNo < 0:
            toLineNo = self._autoSelectLine(box, gbId, _ext, exlude=(fromLineNo,), isSwitchLine=True)

        if toLineNo < 0:
            LOG_ERR('doSwitchLine _autoSelectLine fail', fromLineNo, toLineNo, box.id, gbId, extraData)
            return False

        if toLineNo == fromLineNo:
            LOG_ERR('doSwitchLine fail: same line')
            return False

        spaceVal = self.getLineSpaceVal(toLineNo)
        if not spaceVal:
            LOG_ERR('doSwitchLine: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return False

        _lineMembers = self.allPlayers.getLinePlayers(fromLineNo)
        if not linePlayers:
            return False

        _playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if not _playerVal:
            # 可能由于某种异常跑到别的线上了
            LOG_WARN('doSwitchLine: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            extraData['loseLine'] = -1
            for _lineNo in self.allPlayers.keys():
                _playerVal = self.allPlayers.getPlayer(_lineNo, gbId)
                if _playerVal:
                    extraData['loseLine'] = _lineNo
                    break

        spaceNo = formula.combineLineSpaceNo(self.lineType, toLineNo)
        if _playerVal:
            if _playerVal.playerStatus != linePlayers.LinePlayerVal.INLINE:
                return False

            _playerVal.setPlayerStatus(linePlayers.LinePlayerVal.SWITCHING, {'toLineNo': toLineNo})

            _isTeamLeader = _lineMembers.isTeamLeader(_playerVal.teamUUID, _playerVal.gbId)
            if _isTeamLeader is not None:
                extraData['isLeader'] = _isTeamLeader

            if 'loseLine' not in extraData or extraData['loseLine'] != toLineNo:
                self.addLinePlayerToLine(toLineNo, box, gbId, _playerVal.teamUUID, _playerVal.areaId,
                                         linePlayers.LinePlayerVal.SWITCHING, spaceNo, extraData)
        else:
            self.addLinePlayerToLine(toLineNo, box, gbId, 0, 0, linePlayers.LinePlayerVal.SWITCHING, spaceNo, extraData)

        box.cell.beginSwitchLine(self.lineType, fromLineNo, toLineNo, spaceVal.lineSpaceBox, extraData)
        LOG_INFO("lastChooseLineNo", self.lastChooseLineNo, "->", toLineNo)
        self.lastChooseLineNo = toLineNo
        return True

    def switchLineSuccess(self, fromLineNo, toLineNo, box, gbId, extraData):
        _playerVal = self.allPlayers.getPlayer(toLineNo, gbId)
        if _playerVal:
            _playerVal.setPlayerStatus(linePlayers.LinePlayerVal.INLINE)
        else:
            LOG_ERR('switchLineSuccess: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)

        if 'loseLine' in extraData:
            if extraData['loseLine'] > -1 and extraData['loseLine'] != toLineNo:
                LOG_WARN('doSwitchLine: remove player but not in line', fromLineNo, toLineNo, extraData['loseLine'],
                            box.id, gbId)
                self.removeLinePlayerFromLine(extraData['loseLine'], gbId)
        else:
            self.removeLinePlayerFromLine(fromLineNo, gbId)

    def switchLineFailed(self, fromLineNo, toLineNo, box, gbId, extra):
        LOG_INFO('switchLineFailed:', fromLineNo, toLineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(fromLineNo)
        if not spaceVal:
            LOG_ERR('switchLineFailed: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return

        _playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if _playerVal:
            _playerVal.setPlayerStatus(linePlayers.LinePlayerVal.INLINE)
        else:
            LOG_ERR('switchLineFailed: cannot find from player')

        self.removeLinePlayerFromLine(toLineNo, gbId)

    def goBackLine(self, lineNo, box, gbId, dstPos, dstDir, callback, callbackArgs):
        _spaceVal = self.getLineSpaceVal(lineNo)
        if not _spaceVal:
            LOG_ERR('goBackLine: invalid lineNo', self.lineType, lineNo, box.id, gbId, callback, callbackArgs)
            return

        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not _playerVal:
            LOG_ERR('goBackLine: player is not in line', self.lineType, lineNo, box.id, gbId)
            return

        box.cell.beginGoBackLine(_spaceVal.getSpaceNo(), _spaceVal.lineSpaceBox, dstPos, dstDir, callback, callbackArgs)

    def updateLinePlayerInfo(self, lineNo, box, gbId, infoDic):
        _playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not _playerVal:
            return

        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not lineMembers:
            return

        if 'spaceNo' in infoDic:
            _playerVal.curSpaceNo = infoDic['spaceNo']

        if 'changeTeam' in infoDic:
            _oldVal, _newVal, _isLeader = infoDic['changeTeam']
            lineMembers.onPlayerTeamChanged(gbId, _oldVal, _newVal, _isLeader)

        if 'changeLeader' in infoDic:
            teamUUID, isLeader = infoDic['changeLeader']
            lineMembers.onPlayerTeamChanged(gbId, teamUUID, teamUUID, isLeader)

        if _playerVal.playerStatus == linePlayers.LinePlayerVal.SWITCHING and _playerVal.statusArgs:
            toLineNo = _playerVal.statusArgs.get('toLineNo')
            toLineNo and self.updateLinePlayerInfo(toLineNo, box, gbId, infoDic)

    def leaveLine(self, box, gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        LOG_INFO('leaveLine', box, gbId, fromSpaceNo, toSpaceNo)
        _lineNo = formula.parseLineNo(fromSpaceNo)
        self.removeLinePlayerFromLine(_lineNo, gbId)
        box.cell.beginLeaveLine(fromSpaceNo, toSpaceNo, toPosition, toDirection)

    def _checkEnterLine(self, lineNo, box, gbId, extraInfo):
        if lineNo not in self.allPlayers:
            return gameconst.EnterLineCodeEnum.ERR_SPACE_IS_NOT_READY

        checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo, checkCellAvatarCount=False)
        return checkCode

    def checkCanEnterLine(self, lineNo, box, gbId, extra, method, args):
        _ext = EnterLineExtra.new(extra, lineNo)
        ret = self._checkEnterLine(lineNo, box, gbId, _ext)
        if ret == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            if extra["needPending"]:
                lineMembers = self.allPlayers.getLinePlayers(lineNo)
                lineMembers.addPendingEnterPlayer(self, gbId)
        LOG_DBG('check enter line', lineNo, box, gbId, extra, method, ret)
        _callback = getattr(box.cell, method)
        _callback(ret, *args)

    def checkCanEnterLineFinallyFailed(self, lineNo, box, gbId, extra, method, args):
        LOG_WARN("checkCanEnterLineFinallyFailed::", lineNo, box, gbId, extra, method, args)
        _lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not _lineMembers:
            return

        _lineMembers.removePendingEnterPlayer(self, gbId)

        if method:
            callback = getattr(box.cell, method)
            callback and callback(*args)

    def sendLineInfoOnSpaceChanged(self):
        for _ln in list(self.allPlayers.keys()):
            lineMembers = self.allPlayers.getLinePlayers(_ln)
            for gbId in list(lineMembers.keys()):
                _pVal = lineMembers.get(gbId)
                if not _pVal:
                    continue
                if not _pVal.playerBox:
                    continue
                yield lambda: self._doSendLineInfoOnSpaceChanged(gbId, _ln)

    def _doSendLineInfoOnSpaceChanged(self, gbId, lineNo):
        if lineNo not in self.allPlayers:
            return

        _lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if gbId not in _lineMembers:
            return

        _pVal = _lineMembers[gbId]
        if not _pVal.playerBox:
            return

        self.doQueryLineInfo(0, _pVal.playerBox, gbId)

    def doQueryLineInfo(self, spaceNo, box, gbId):
        res = self._calculateLineInfo()

        LOG_DBG('doQueryLineInfo', res)
        box.client.onGetLineInfo(json.dumps(res))

    def notifyPlayerOffline(self, lineNo, gbId):
        self.removeLinePlayerFromLine(lineNo, gbId)

    def removePendingEnterOnBaseDestroy(self, lineNo, gbId):
        LOG_DBG('ILinePlayersStub::removePendingEnterOnBaseDestroy', lineNo, gbId)
        _lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not _lineMembers:
            return
        _lineMembers.removePendingEnterPlayer(self, gbId)

    def debugPlayerAreaInfo(self):
        pass
