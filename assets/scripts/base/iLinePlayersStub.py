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
import formula
import gameconst
import utils
import random

import linePlayers
import json

import branchData_branchData as BBD
import gamePlay_gamePlay as GGD
import branchData_set as BDS


class EnterLineExtra(object):
    @classmethod
    def new(cls, dataDic, lineNo):
        ret = cls()
        ret.__dict__.update(dataDic)

        ret.isAuto = (lineNo < 0)
        ret.isLeader = 'followers' in dataDic
        ret.fromLineNo = dataDic.get('fromLineNo', -1)

        return ret

    def __init__(self):
        self.teamUUID = 0
        self.followers = []
        self.isAuto = False
        self.isLeader = False
        self.position = None
        self.guildUUID = 0
        self.isLogin = 0
        self.fromLineNo = -1


class ILinePlayersStub(object):
    def __init__(self):
        self.mergeRes = []
        self.fightingPlayersCntBase = {}
        self.lastChooseLineNo = 0

    def onLineSpaceReady(self, spaceNo):
        lineNo = formula.parseLineNo(spaceNo)
        self.allPlayers[lineNo] = linePlayers.LinePlayers(lineNo)

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

    def handleCellappDeath(self, groupOrder):
        pass

    def onCellappRelive(self, groupOrder):
        pass

    def enterLine(self, lineNo, box, gbId, position, direction, extra):
        _linePlayers = self.allPlayers.getLinePlayers(lineNo) or ()
        LOG_IFO('enterLine', box.id, gbId, lineNo, extra, len(_linePlayers))
        ext = EnterLineExtra.new(extra, lineNo)

        isAutoSelectedLine = False
        if lineNo < 0:
            lineNo = self._autoSelectLine(box, gbId, ext)
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
                    if mpFailCb:
                        box.callMethod(mpFailCb, (1,))
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
            playerVal = self.allPlayers.getPlayer(-1 if lineNo < 0 else lineNo, gbId)
            if playerVal:
                LOG_WARN('enterLine: player is already in line', lineNo, playerVal, playerVal.playerStatus)

            # 自动选出的已经check过了
            if not isAutoSelectedLine:
                checkCode = self._checkCanEnterLine(lineNo, box, gbId, ext)
                if checkCode != gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
                    LOG_IFO('enterLine fail:', lineNo, box.id, gbId, extra, checkCode)
                    # if checkCode == gameconst.EnterLineCodeEnum.ERR_REACH_MAX_GUILD_MEMBER \
                    #         or checkCode == gameconst.EnterLineCodeEnum.ERR_REACH_MAX_MEMBER:
                    #     box.cell.enterGuildBattleLineFailedReachMax()

                    # 跟随队长失败需要处理
                    callback = getattr(box.cell, extra.get('failCallback', ''), None)
                    failArgs = extra.get('callbackArgs', ())
                    callback and callback(checkCode, *failArgs)
                    return

        spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)
        # 处理连续两次(异常)调用进入分线的情况
        self.removeLinePlayerWhenExist(gbId)
        self.addLinePlayerInLine(lineNo, box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, spaceNo, extra)
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)

        playerVal.playerBox.cell.beginEnterLine(self.lineType, lineNo, spaceVal.lineSpaceBox, position, direction,
                                                extra)
        playerVal.checkEnterTimer = self.addTimerCB(10, '_checkPlayerEnterLine', (lineNo, box, gbId),
                                                   gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)
        
        LOG_IFO("lastChooseLineNo", self.lastChooseLineNo, "->", lineNo)
        self.lastChooseLineNo = lineNo

    # 进入分线添加playerVal前调用，保证只存在一个playerVal
    def removeLinePlayerWhenExist(self, gbId):
        for lineNo_ in self.allPlayers.keys():
            playerVal = self.allPlayers.getPlayer(lineNo_, gbId)
            if playerVal:
                # 如果存在对应timer，需要删除
                if playerVal.checkEnterTimer:
                    self.cancelTimerCB(playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

                self.removeLinePlayerInLine(lineNo_, gbId)
                return

    def addLinePlayerInLine(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        self.allPlayers.addLinePlayer(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo)

    def removeLinePlayerInLine(self, lineNo, gbId):
        self.allPlayers.removeLinePlayer(self, lineNo, gbId)

    def _checkPlayerEnterLine(self, lineNo, box, gbId, checkCnt=0):
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('_checkPlayerEnterLine error: player not in line', lineNo, box.id, gbId)
            return

        playerVal.checkEnterTimer = 0

        if playerVal.playerStatus != playerVal.IN_LINE:
            spaceNo = formula.combineLineSpaceNo(self.lineType, lineNo)
            if checkCnt < 5:
                LOG_ERR('_checkPlayerEnterLine fail:', lineNo, box.id, gbId, checkCnt)

            if checkCnt > 3 and not formula.inWorldLineScene(spaceNo):
                self.removeLinePlayerInLine(lineNo, gbId)
                toSpaceNo = formula.combineLineSpaceNo(self.lineType)
                box.cell.beginLeaveLine(spaceNo, toSpaceNo, formula.getSpaceBornPoint(toSpaceNo)(0, 0, 0))
            else:
                playerVal.checkEnterTimer = self.addTimerCB(10, '_checkPlayerEnterLine', (lineNo, box, gbId,
                                                                                         checkCnt + 1),
                                                           gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

    def _checkSelectLine(self, lineNo, box, gbId, extraInfo, exlude=None, isSwitchLine=False):
        LOG_DBG("checkSelectLine", lineNo, box, gbId, extraInfo, exlude, isSwitchLine)
        needCnt = len(extraInfo.followers) + 1

        if exlude and lineNo in exlude:
            return gameconst.EnterLineCodeEnum.ERR_EXLUDE

        # TODO X: validate line config
        lineMaxCnt = BBD.datas[self.lineType]['N1']
        N2Cnt = BBD.datas[self.lineType]['N2']
        N3Cnt = BBD.datas[self.lineType]['N3']
        lineMembers = self.allPlayers[lineNo]
        sVal = self.getLineSpaceVal(lineNo)

        if not sVal.isReadyEnter():
            return gameconst.EnterLineCodeEnum.ERR_SPACE_IS_NOT_READY

        hasLeader = extraInfo.teamUUID and lineMembers.getLeaderGbId(extraInfo.teamUUID)
        hasMember = hasLeader or (extraInfo.teamUUID and lineMembers.hasTeamMember(extraInfo.teamUUID))
        failCode = gameconst.EnterLineCodeEnum.ERR_COMMON

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
        
        for i, res in self.mergeRes:
            if lineNo in res:
                return gameconst.EnterLineCodeEnum.ERR_MERGE_LINE

        cellappIndx = (lineNo + 1 + gameconst.getWorldLineCellIdx(self.lineType)) % gameconfig.cellAppCount()
        cellAvatarCount = gameglobal.cellAvatarCountDict.get(cellappIndx, 0)
        LOG_IFO("checkmaxCellAvatarCount", cellappIndx, cellAvatarCount)
        if cellAvatarCount >= gameconfig.maxCellAvatarCount():
            return gameconst.EnterLineCodeEnum.ERR_REACH_MAX_AVATAR_COUNT

        return gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS

    def _autoSelectLine(self, box, gbId, extraInfo, exlude=None, isSwitchLine=False):
        needCnt = len(extraInfo.followers) + 1
        lineMaxCnt = BBD.datas[self.lineType]['N1']

        # 有队伍且不是队长，优先找队长
        if extraInfo.teamUUID and not extraInfo.isLeader:
            for lineNo, lineMembers in self.allPlayers.items():
                if lineMembers.getLeaderGbId(extraInfo.teamUUID) and len(lineMembers) + needCnt <= lineMaxCnt:
                    return lineNo

        n5list = []
        lineNoList = sorted(self.allPlayers.keys())
        if BDS.datas["Branch_allocationPlan"]["value"] == 1:
            newLineNoList = []
            usedLineNoSet = set()
            lineInfo = self._calculateLineInfo()
            if gameconfig.switchLineUselastLineNo():
                if self.lastChooseLineNo in self.allPlayers:
                    LOG_IFO("lastChooseLineNo", self.lastChooseLineNo, lineInfo)
                    if len(self.allPlayers[self.lastChooseLineNo]) <= max(lineInfo['info'].values()) + BDS.datas["Branch_mergeFloatRange"]["value"]:
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
            LOG_IFO("lineNoList", lineNoList)

        for lineNo in lineNoList:
            checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo, exlude, isSwitchLine)
            if checkCode == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
                return lineNo
            elif checkCode == gameconst.EnterLineCodeEnum.ERR_REACH_AREAM_LIMIT:
                n5list.append(lineNo)
        LOG_WARN('cannot select line', box.id, gbId, needCnt,
                    [len(lineMembers) for lineMembers in self.allPlayers.values()])

        if formula.checkWorldLineType(self.lineType):
            if n5list:
                LOG_IFO('cannot select line: put to n5 area')
                return random.choice(n5list)
            else:
                LOG_IFO('cannot select line: put to random area')
                return -1
        else:
            return random.choice(self.getLineNoReadyForEnter())

    def enterLineSuccess(self, lineNo, box, gbId, succInfo):
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('enterLineSuccess:player is not in line', lineNo)
            return

        if playerVal.checkEnterTimer:
            self.cancelTimerCB(playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)
            playerVal.checkEnterTimer = 0

        playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)

    def enterLineFailed(self, lineNo, box, gbId, extra):
        LOG_IFO('enterLineFailed:', lineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            LOG_ERR('enterLineFailed: invalid lineNo', self.lineType, lineNo, box.id, gbId)
            return

        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('enterLineFailed:player is not in line', lineNo)
            return

        self.removeLinePlayerInLine(lineNo, gbId)

    def autoSwitchLine(self, box, gbId, fromSpaceNo, extra, cbName, cbArgs):
        ext = EnterLineExtra.new(extra, -1)
        fromLineNo = formula.parseLineNo(fromSpaceNo)
        toLineNo = self._autoSelectLine(box, gbId, ext, exlude=None, isSwitchLine=True)

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
            lineMembers = self.allPlayers.getLinePlayers(toLineNo)
            if not lineMembers:
                LOG_ERR("autoSwitchLineToMainCity: toLineNo is not in line", toLineNo)
                return
            lineMembers.addPendingEnterPlayer(self, gbId)

        spaceVal = self.getLineSpaceVal(toLineNo)
        box.callMethod(cbName, (toLineNo, spaceVal.lineSpaceBox, extra.get('position', None)) + cbArgs)

    def switchLine(self, fromLineNo, toLineNo, box, gbId, extra):
        LOG_IFO('switchLine', fromLineNo, toLineNo, box.id, gbId)
        ext = EnterLineExtra.new(extra, toLineNo)
        if toLineNo < 0:
            toLineNo = self._autoSelectLine(box, gbId, ext, exlude=(fromLineNo,), isSwitchLine=True)

        if toLineNo < 0:
            LOG_ERR('switchLine _autoSelectLine fail', fromLineNo, toLineNo, box.id, gbId, extra)
            return False

        if toLineNo == fromLineNo:
            LOG_ERR('switchLine fail: same line')
            return False

        spaceVal = self.getLineSpaceVal(toLineNo)
        if not spaceVal:
            LOG_ERR('switchLine: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return False

        lineMembers = self.allPlayers.getLinePlayers(fromLineNo)
        if not linePlayers:
            return False

        playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if not playerVal:
            # 可能由于某种异常跑到别的线上了
            LOG_WARN('switchLine: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            extra['loseLine'] = -1
            for lineNo_ in self.allPlayers.keys():
                playerVal = self.allPlayers.getPlayer(lineNo_, gbId)
                if playerVal:
                    extra['loseLine'] = lineNo_
                    break

        spaceNo = formula.combineLineSpaceNo(self.lineType, toLineNo)
        if playerVal:
            if playerVal.playerStatus != linePlayers.LinePlayerVal.IN_LINE:
                return False

            playerVal.setPlayerStatus(linePlayers.LinePlayerVal.SWITCHING, {'toLineNo': toLineNo})

            isTeamLeader = lineMembers.isTeamLeader(playerVal.teamUUID, playerVal.gbId)
            if isTeamLeader is not None:
                extra['isLeader'] = isTeamLeader

            if 'loseLine' not in extra or extra['loseLine'] != toLineNo:
                self.addLinePlayerInLine(toLineNo, box, gbId, playerVal.teamUUID, playerVal.areaId,
                                         linePlayers.LinePlayerVal.SWITCHING, spaceNo, extra)
        else:
            self.addLinePlayerInLine(toLineNo, box, gbId, 0, 0, linePlayers.LinePlayerVal.SWITCHING, spaceNo, extra)

        box.cell.beginSwitchLine(self.lineType, fromLineNo, toLineNo, spaceVal.lineSpaceBox, extra)
        LOG_IFO("lastChooseLineNo", self.lastChooseLineNo, "->", toLineNo)
        self.lastChooseLineNo = toLineNo
        return True

    def switchLineSuccess(self, fromLineNo, toLineNo, box, gbId, extra):
        playerVal = self.allPlayers.getPlayer(toLineNo, gbId)
        if playerVal:
            playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)
        else:
            LOG_ERR('switchLineSuccess: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)

        if 'loseLine' in extra:
            if extra['loseLine'] > -1 and extra['loseLine'] != toLineNo:
                LOG_WARN('switchLine: remove player but not in line', fromLineNo, toLineNo, extra['loseLine'],
                            box.id, gbId)
                self.removeLinePlayerInLine(extra['loseLine'], gbId)
        else:
            self.removeLinePlayerInLine(fromLineNo, gbId)

    def switchLineFailed(self, fromLineNo, toLineNo, box, gbId, extra):
        LOG_IFO('switchLineFailed:', fromLineNo, toLineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(fromLineNo)
        if not spaceVal:
            LOG_ERR('switchLineFailed: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return

        playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if playerVal:
            playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)
        else:
            LOG_ERR('switchLineFailed: cannot find from player')

        self.removeLinePlayerInLine(toLineNo, gbId)

    def goBackLine(self, lineNo, box, gbId, dstPos, dstDir, callback, callbackArgs):
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            LOG_ERR('goBackLine: invalid lineNo', self.lineType, lineNo, box.id, gbId, callback, callbackArgs)
            return

        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('goBackLine: player is not in line', self.lineType, lineNo, box.id, gbId)
            return

        box.cell.beginGoBackLine(spaceVal.getSpaceNo(), spaceVal.lineSpaceBox, dstPos, dstDir, callback, callbackArgs)

    def updateLinePlayerInfo(self, lineNo, box, gbId, infoDict):
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            return

        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not lineMembers:
            return

        if 'spaceNo' in infoDict:
            playerVal.curSpaceNo = infoDict['spaceNo']

        if 'changeTeam' in infoDict:
            oldVal, newVal, isLeader = infoDict['changeTeam']
            lineMembers.onPlayerTeamChanged(gbId, oldVal, newVal, isLeader)

        if 'changeLeader' in infoDict:
            teamUUID, isLeader = infoDict['changeLeader']
            lineMembers.onPlayerTeamChanged(gbId, teamUUID, teamUUID, isLeader)

        if playerVal.playerStatus == linePlayers.LinePlayerVal.SWITCHING and playerVal.statusArgs:
            toLineNo = playerVal.statusArgs.get('toLineNo')
            toLineNo and self.updateLinePlayerInfo(toLineNo, box, gbId, infoDict)

    def leaveLine(self, box, gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        LOG_IFO('leaveLine', box, gbId, fromSpaceNo, toSpaceNo)
        lineNo = formula.parseLineNo(fromSpaceNo)
        self.removeLinePlayerInLine(lineNo, gbId)
        box.cell.beginLeaveLine(fromSpaceNo, toSpaceNo, toPosition, toDirection)

    def _checkCanEnterLine(self, lineNo, box, gbId, extraInfo):
        if lineNo not in self.allPlayers:
            return gameconst.EnterLineCodeEnum.ERR_SPACE_IS_NOT_READY

        checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo)
        return checkCode

    def checkCanEnterLine(self, lineNo, box, gbId, extra, method, args):
        ext = EnterLineExtra.new(extra, lineNo)
        ret = self._checkCanEnterLine(lineNo, box, gbId, ext)
        if ret == gameconst.EnterLineCodeEnum.ENTER_CHECK_SUCCESS:
            if extra["needPending"]:
                lineMembers = self.allPlayers.getLinePlayers(lineNo)
                lineMembers.addPendingEnterPlayer(self, gbId)
        LOG_DBG('check enter line', lineNo, box, gbId, extra, method, ret)
        callback = getattr(box.cell, method)
        callback(ret, *args)

    def checkCanEnterLineFinallyFailed(self, lineNo, box, gbId, extra, method, args):
        LOG_WARN("checkCanEnterLineFinallyFailed::", lineNo, box, gbId, extra, method, args)
        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not lineMembers:
            return

        lineMembers.removePendingEnterPlayer(self, gbId)

        if method:
            callback = getattr(box.cell, method)
            callback and callback(*args)

    def sendLineInfoOnSpaceChanged(self):
        for ln in list(self.allPlayers.keys()):
            lineMembers = self.allPlayers.getLinePlayers(ln)
            for gbId in list(lineMembers.keys()):
                pVal = lineMembers.get(gbId)
                if not pVal:
                    continue
                if not pVal.playerBox:
                    continue
                yield lambda: self._doSendLineInfoOnSpaceChanged(gbId, ln)

    def _doSendLineInfoOnSpaceChanged(self, gbId, lineNo):
        if lineNo not in self.allPlayers:
            return

        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if gbId not in lineMembers:
            return

        pVal = lineMembers[gbId]
        if not pVal.playerBox:
            return

        self.doQueryLineInfo(0, pVal.playerBox, gbId)

    def _calculateLineInfo(self):
        res = {'lineType': self.lineType, 'info': {}}
        
        baseLineNum = BBD.datas[self.lineType]['num']
        maxLineNum = gameconst.getBranchLineCnt(self.lineType)
        addRequired = BBD.datas[self.lineType]['AddRequired']

        needNewLine = True
        for lineNo, lineMembers in self.allPlayers.items():
            sVal = self.getLineSpaceVal(lineNo)

            if not sVal.isReadyEnter():
                continue

            if lineNo < baseLineNum or len(lineMembers) > 0:
                res['info'][lineNo] = len(lineMembers)

                ifSafeArea = GGD.datas[self.lineType]['ifSafeArea']
                activeCnt = len(lineMembers) if ifSafeArea else self.fightingPlayersCntBase.get(lineNo, 0)
                if activeCnt < addRequired:
                    needNewLine = False
                continue

        if needNewLine:
            for i in range(1, maxLineNum):
                if i not in res['info']:
                    linePlayers = self.allPlayers.getLinePlayers(i)
                    res['info'][i] = 0 if not linePlayers else len(linePlayers)
                    break

        return res

    def doQueryLineInfo(self, spaceNo, box, gbId):
        res = self._calculateLineInfo()

        LOG_DBG('doQueryLineInfo', res)
        box.client.onGetLineInfo(json.dumps(res))

    def notifyPlayerOffline(self, lineNo, gbId):
        self.removeLinePlayerInLine(lineNo, gbId)

    def removePendingEnterOnBaseDestroy(self, lineNo, gbId):
        LOG_DBG('ILinePlayersStub::removePendingEnterOnBaseDestroy', lineNo, gbId)
        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not lineMembers:
            return
        lineMembers.removePendingEnterPlayer(self, gbId)

    def debugPlayerAreaInfo(self):
        pass

    def _checkLineMerge(self):
        LOG_DBG('_checkLineMerge')
        baseLineNum = BBD.datas[self.lineType]['num']
        mergeRequired = BBD.datas[self.lineType]['MergeRequired']
        
        sortedData = []
        for lineNo, lineMembers in self.allPlayers.items():
            if lineNo >= baseLineNum and len(lineMembers) > 0:
                sortedData.append((lineNo, len(lineMembers)))
        
        sortedData = sorted(sortedData, key=lambda x: x[1])

        if not sortedData:
            return
        LOG_DBG('sortedData', sortedData)

        self.mergeRes = []
        idx = 0

        #将下标j的线合到下标i的线
        for i in range(len(self.allPlayers)):
            sumCnt = len(self.allPlayers.getLinePlayers(i))
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
                self.mergeRes.append((i, res))

        if not self.mergeRes:
            return

        LOG_DBG('mergeRes', self.mergeRes)
        msgID = BDS.datas["Branch_mergeNoticeMsg"]["value"]
        for i, res in self.mergeRes:
            for lineNo in res:
                lineMembers = self.allPlayers.getLinePlayers(lineNo)
                for gbId in list(lineMembers.keys()):
                    pVal = lineMembers.get(gbId)
                    if not pVal:
                        continue
                    if not pVal.playerBox:
                        continue
                    pVal.playerBox.onMessagePre(msgID, [])

    def _doLineMerge(self):
        if self.mergeRes:
            LOG_DBG('_doLineMerge')
            for i, res in self.mergeRes:
                self.mergeLine(i, res)
            self.mergeRes = []

    def mergeLine(self, i, res):
        LOG_DBG('mergeLine', i, res)
        mergeRequired = BBD.datas[self.lineType]['MergeRequired']
        for fromLineNo in res:
            lineMembers = self.allPlayers.getLinePlayers(fromLineNo)
            if len(lineMembers) > mergeRequired:
                continue
            for gbId in list(lineMembers.keys()):
                pVal = lineMembers.get(gbId)
                if not pVal:
                    continue
                if not pVal.playerBox:
                    continue
                pVal.playerBox.cell.onMergeLine(i)

    def onFightingPlayersCntSync(self, lineNo, cnt):
        self.fightingPlayersCntBase[lineNo] = cnt
        LOG_DBG("onFightingPlayersCntSync", lineNo, cnt)