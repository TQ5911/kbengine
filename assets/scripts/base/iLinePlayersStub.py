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
        pass

    def onLineSpaceReady(self, spaceNo):
        lineNo = formula.getLineNo(spaceNo)
        self.allPlayers[lineNo] = linePlayers.LinePlayers(lineNo)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        lineNo = formula.getLineNo(spaceNo)
        self.allPlayers.pop(lineNo)

        self.batchlyCall(self.sendLineInfoOnSpaceChanged(), 50)

    def handleCellappDeath(self, groupOrder):
        pass

    def onCellappRelive(self, groupOrder):
        pass

    def enterLine(self, lineNo, box, gbId, position, direction, extra):
        _linePlayers = self.allPlayers.getLinePlayers(lineNo) or ()
        INFO_MSG('enterLine', box.id, gbId, lineNo, extra, len(_linePlayers))
        ext = EnterLineExtra.new(extra, lineNo)

        isAutoSelectedLine = False
        if lineNo < 0:
            lineNo = self._autoSelectLine(box, gbId, ext)
            isAutoSelectedLine = True

        elif extra.get('isAuto'):
            ERROR_MSG('enterline: invalid args', lineNo, gbId, extra)
            return

        if formula.isWorldLineType(self.lineType) and isAutoSelectedLine and lineNo < 0:
            lineNo = random.choice(self.getLineNoReadyForEnter())

        if lineNo < 0:
            ERROR_MSG('enterLine _autoSelectLine failed:', box.id, gbId, extra)
            return

        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            ERROR_MSG('enterLine: invalid lineNo', self.lineType, lineNo, box.id, gbId)
            return

        if not extra.get('isLogin'):
            playerVal = self.allPlayers.getPlayer(-1 if lineNo < 0 else lineNo, gbId)
            if playerVal:
                WARNING_MSG('enterLine: player is already in line', lineNo, playerVal, playerVal.playerStatus)

            # 自动选出的已经check过了
            if not isAutoSelectedLine:
                checkCode = self._checkCanEnterLine(lineNo, box, gbId, ext)
                if checkCode != gameconst.EnterLineCode.CAN_ENTER:
                    INFO_MSG('enterLine fail:', lineNo, box.id, gbId, extra, checkCode)
                    # if checkCode == gameconst.EnterLineCode.FAIL_REACH_MAX_GUILD_MEMBER \
                    #         or checkCode == gameconst.EnterLineCode.FAIL_REACH_MAX_MEMBER:
                    #     box.cell.enterGuildBattleLineFailedReachMax()

                    # 跟随队长失败需要处理
                    callback = getattr(box.cell, extra.get('failCallback', ''), None)
                    failArgs = extra.get('callbackArgs', ())
                    callback and callback(checkCode, *failArgs)
                    return

        spaceNo = formula.getLineSpaceNo(self.lineType, lineNo)
        # 处理连续两次(异常)调用进入分线的情况
        self.removeLinePlayerWhenExist(gbId)
        self.addLinePlayerInLine(lineNo, box, gbId, 0, 0, linePlayers.LinePlayerVal.ENTERING, spaceNo, extra)
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)

        playerVal.playerBox.cell.beginEnterLine(self.lineType, lineNo, spaceVal.lineSpaceBox, position, direction,
                                                extra)
        playerVal.checkEnterTimer = self._callback(10, '_checkPlayerEnterLine', (lineNo, box, gbId),
                                                   gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

    # 进入分线添加playerVal前调用，保证只存在一个playerVal
    def removeLinePlayerWhenExist(self, gbId):
        for lineNo_ in self.allPlayers.keys():
            playerVal = self.allPlayers.getPlayer(lineNo_, gbId)
            if playerVal:
                # 如果存在对应timer，需要删除
                if playerVal.checkEnterTimer:
                    self._cancelCallback(playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

                self.removeLinePlayerInLine(lineNo_, gbId)
                return

    def addLinePlayerInLine(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo):
        self.allPlayers.addLinePlayer(self, lineNo, box, gbId, teamUUID, areaId, status, curSpaceNo, extraInfo)

    def removeLinePlayerInLine(self, lineNo, gbId):
        self.allPlayers.removeLinePlayer(self, lineNo, gbId)

    def _checkPlayerEnterLine(self, lineNo, box, gbId, checkCnt=0):
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            ERROR_MSG('_checkPlayerEnterLine error: player not in line', lineNo, box.id, gbId)
            return

        playerVal.checkEnterTimer = 0

        if playerVal.playerStatus != playerVal.IN_LINE:
            spaceNo = formula.getLineSpaceNo(self.lineType, lineNo)
            if checkCnt < 5:
                ERROR_MSG('_checkPlayerEnterLine fail:', lineNo, box.id, gbId, checkCnt)

            if checkCnt > 3 and not formula.spaceInWorldLine(spaceNo):
                self.removeLinePlayerInLine(lineNo, gbId)
                toSpaceNo = formula.getLineSpaceNo(self.lineType)
                box.cell.beginLeaveLine(spaceNo, toSpaceNo, formula.whatSpaceBornPoint(toSpaceNo)(0, 0, 0))
            else:
                playerVal.checkEnterTimer = self._callback(10, '_checkPlayerEnterLine', (lineNo, box, gbId,
                                                                                         checkCnt + 1),
                                                           gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)

    def _checkSelectLine(self, lineNo, box, gbId, extraInfo, exlude=None, isSwitchLine=False):
        needCnt = len(extraInfo.followers) + 1

        if exlude and lineNo in exlude:
            return gameconst.EnterLineCode.FAIL_EXLUDE

        # TODO X: validate line config
        lineMaxCnt = BBD.datas[self.lineType]['N1']
        teamEnterCnt = BBD.datas[self.lineType]['N2']
        autoEnterCnt = BBD.datas[self.lineType]['N3']
        lineMembers = self.allPlayers[lineNo]
        sVal = self.getLineSpaceVal(lineNo)

        if not sVal.isReadyEnter():
            return gameconst.EnterLineCode.FAIL_SPACE_IS_NOT_READY

        hasLeader = extraInfo.teamUUID and lineMembers.getLeaderGbId(extraInfo.teamUUID)
        hasMember = hasLeader or (extraInfo.teamUUID and lineMembers.hasTeamMember(extraInfo.teamUUID))
        failCode = gameconst.EnterLineCode.FAIL_COMMON

        playerNum = len(lineMembers) + lineMembers.getPendingEnterNum()
        if gameconfig.enableCheckEnterLineNew():
            playerNum = len(lineMembers) + lineMembers.getPendingEnterNum()
        # 单条线人数超过上限，禁止进入
        if playerNum + needCnt > lineMaxCnt:
            return gameconst.EnterLineCode.FAIL_REACH_MAX_MEMBER

        # 单线每秒人数超过上限，禁止进入(只在登录时限制)
        elif extraInfo.isLogin and lineMembers.getPendingEnterNumNowSec() >= gameconfig.loginLinePlayerNumLimit():
            return gameconst.EnterLineCode.FAIL_REACH_SEC_LIMIT
        else:
            return gameconst.EnterLineCode.CAN_ENTER

        return failCode

    def _autoSelectLine(self, box, gbId, extraInfo, exlude=None, isSwitchLine=False):
        needCnt = len(extraInfo.followers) + 1
        lineMaxCnt = BBD.datas[self.lineType]['N1']

        # 有队伍且不是队长，优先找队长
        if extraInfo.teamUUID and not extraInfo.isLeader:
            for lineNo, lineMembers in self.allPlayers.items():
                if lineMembers.getLeaderGbId(extraInfo.teamUUID) and len(lineMembers) + needCnt < lineMaxCnt + 50:
                    return lineNo

        n5list = []
        lineNoList = sorted(self.allPlayers.keys())
        if gameconfig.enableSelectLineNew():
            memberCnt1 = lineMaxCnt // 2
            lineInfoList = []
            for lineNo in lineNoList:
                _linePlayers = self.allPlayers.getLinePlayers(lineNo) or ()
                lineInfoList.append((len(_linePlayers), lineNo))

            if all([info[0] > memberCnt1 for info in lineInfoList]):
                lineNoList = [info[1] for info in sorted(lineInfoList)]
            else:
                for i, info in enumerate(lineInfoList):
                    if info[0] < memberCnt1:
                        if i != 0:
                            lineInfoList[i] = lineInfoList[0]
                            lineInfoList[0] = info
                        break

                lineNoList = [info[1] for info in lineInfoList]

        elif extraInfo.fromLineNo in lineNoList:
            lineNoList.remove(extraInfo.fromLineNo)
            lineNoList.insert(0, extraInfo.fromLineNo)

        for lineNo in lineNoList:
            checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo, exlude, isSwitchLine)
            if checkCode == gameconst.EnterLineCode.CAN_ENTER:
                return lineNo
            elif checkCode == gameconst.EnterLineCode.FAIL_REACH_AREAM_LIMIT:
                n5list.append(lineNo)
        WARNING_MSG('cannot select line', box.id, gbId, needCnt,
                    [len(lineMembers) for lineMembers in self.allPlayers.values()])

        if formula.isWorldLineType(self.lineType):
            if n5list:
                INFO_MSG('cannot select line: put to n5 area')
                return random.choice(n5list)
            else:
                INFO_MSG('cannot select line: put to random area')
                return -1
        else:
            return random.choice(self.getLineNoReadyForEnter())

    def enterLineSuccess(self, lineNo, box, gbId, succInfo):
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            ERROR_MSG('enterLineSuccess:player is not in line', lineNo)
            return

        if playerVal.checkEnterTimer:
            self._cancelCallback(playerVal.checkEnterTimer, gametimer.TIMER_TAG_CHECK_PLAYER_ENTER_LINE)
            playerVal.checkEnterTimer = 0

        playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)

    def enterLineFailed(self, lineNo, box, gbId, extra):
        INFO_MSG('enterLineFailed:', lineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            ERROR_MSG('enterLineFailed: invalid lineNo', self.lineType, lineNo, box.id, gbId)
            return

        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            ERROR_MSG('enterLineFailed:player is not in line', lineNo)
            return

        self.removeLinePlayerInLine(lineNo, gbId)

    def autoSwitchLine(self, box, gbId, fromSpaceNo, extra, cbName, cbArgs):
        ext = EnterLineExtra.new(extra, -1)
        fromLineNo = formula.getLineNo(fromSpaceNo)
        toLineNo = self._autoSelectLine(box, gbId, ext, exlude=None, isSwitchLine=True)

        if formula.isWorldLineType(self.lineType) and toLineNo < 0:
            toLineNo = random.choice(self.getLineNoReadyForEnter())
            # TODO X: valid world position config
            pos, dir = formula.whatSpaceBornPosAndDir(self.lineType)
            extra['position'] = pos

        if fromLineNo != toLineNo:
            lineMembers = self.allPlayers.getLinePlayers(toLineNo)
            if not lineMembers:
                return
            lineMembers.addPendingEnterPlayer(self, gbId)

        spaceVal = self.getLineSpaceVal(toLineNo)
        box.callMethod(cbName, (toLineNo, spaceVal.lineSpaceBox, extra.get('position', None)) + cbArgs)

    def switchLine(self, fromLineNo, toLineNo, box, gbId, extra):
        INFO_MSG('switchLine', fromLineNo, toLineNo, box.id, gbId)
        ext = EnterLineExtra.new(extra, toLineNo)
        if toLineNo < 0:
            toLineNo = self._autoSelectLine(box, gbId, ext, exlude=(fromLineNo,), isSwitchLine=True)

        if toLineNo < 0:
            ERROR_MSG('switchLine _autoSelectLine fail', fromLineNo, toLineNo, box.id, gbId, extra)
            return False

        if toLineNo == fromLineNo:
            ERROR_MSG('switchLine fail: same line')
            return False

        spaceVal = self.getLineSpaceVal(toLineNo)
        if not spaceVal:
            ERROR_MSG('switchLine: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return False

        lineMembers = self.allPlayers.getLinePlayers(fromLineNo)
        if not linePlayers:
            return False

        playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if not playerVal:
            # 可能由于某种异常跑到别的线上了
            WARNING_MSG('switchLine: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            extra['loseLine'] = -1
            for lineNo_ in self.allPlayers.keys():
                playerVal = self.allPlayers.getPlayer(lineNo_, gbId)
                if playerVal:
                    extra['loseLine'] = lineNo_
                    break

        spaceNo = formula.getLineSpaceNo(self.lineType, toLineNo)
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
        return True

    def switchLineSuccess(self, fromLineNo, toLineNo, box, gbId, extra):
        playerVal = self.allPlayers.getPlayer(toLineNo, gbId)
        if playerVal:
            playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)
        else:
            ERROR_MSG('switchLineSuccess: player is not in line', self.lineType, fromLineNo, toLineNo, box.id, gbId)

        if 'loseLine' in extra:
            if extra['loseLine'] > -1 and extra['loseLine'] != toLineNo:
                WARNING_MSG('switchLine: remove player but not in line', fromLineNo, toLineNo, extra['loseLine'],
                            box.id, gbId)
                self.removeLinePlayerInLine(extra['loseLine'], gbId)
        else:
            self.removeLinePlayerInLine(fromLineNo, gbId)

    def switchLineFailed(self, fromLineNo, toLineNo, box, gbId, extra):
        INFO_MSG('switchLineFailed:', fromLineNo, toLineNo, box.id, gbId, extra)
        spaceVal = self.getLineSpaceVal(fromLineNo)
        if not spaceVal:
            ERROR_MSG('switchLineFailed: invalid lineNo', self.lineType, fromLineNo, toLineNo, box.id, gbId)
            return

        playerVal = self.allPlayers.getPlayer(fromLineNo, gbId)
        if playerVal:
            playerVal.setPlayerStatus(linePlayers.LinePlayerVal.IN_LINE)
        else:
            ERROR_MSG('switchLineFailed: cannot find from player')

        self.removeLinePlayerInLine(toLineNo, gbId)

    def goBackLine(self, lineNo, box, gbId, dstPos, dstDir, callback, callbackArgs):
        spaceVal = self.getLineSpaceVal(lineNo)
        if not spaceVal:
            ERROR_MSG('goBackLine: invalid lineNo', self.lineType, lineNo, box.id, gbId, callback, callbackArgs)
            return

        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            ERROR_MSG('goBackLine: player is not in line', self.lineType, lineNo, box.id, gbId)
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
        INFO_MSG('leaveLine', box, gbId, fromSpaceNo, toSpaceNo)
        lineNo = formula.getLineNo(fromSpaceNo)
        self.removeLinePlayerInLine(lineNo, gbId)
        box.cell.beginLeaveLine(fromSpaceNo, toSpaceNo, toPosition, toDirection)

    def _checkCanEnterLine(self, lineNo, box, gbId, extraInfo):
        if lineNo not in self.allPlayers:
            return gameconst.EnterLineCode.FAIL_SPACE_IS_NOT_READY

        checkCode = self._checkSelectLine(lineNo, box, gbId, extraInfo)
        return checkCode

    def checkCanEnterLine(self, lineNo, box, gbId, extra, method, args):
        ext = EnterLineExtra.new(extra, lineNo)
        ret = self._checkCanEnterLine(lineNo, box, gbId, ext)
        if ret == gameconst.EnterLineCode.CAN_ENTER:
            lineMembers = self.allPlayers.getLinePlayers(lineNo)
            lineMembers.addPendingEnterPlayer(self, gbId)
        DEBUG_MSG('check enter line', lineNo, box, gbId, extra, method, ret)
        callback = getattr(box.cell, method)
        callback(ret, *args)

    def checkCanEnterLineFinallyFailed(self, lineNo, box, gbId, extra, method, args):
        WARNING_MSG("checkCanEnterLineFinallyFailed::", lineNo, box, gbId, extra, method, args)
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

    def doQueryLineInfo(self, spaceNo, box, gbId):
        res = {'lineType': self.lineType, 'info': {}}
        havePlayerLineList = [lineNo for lineNo, lineMembers in self.allPlayers.items() if len(lineMembers) > 0]
        maxPlayerLineNo = min(max(havePlayerLineList, default=0) + 1, utils.getLineMaxNumber(self.lineType) - 1)
        for lineNo, lineMembers in self.allPlayers.items():
            if lineNo > maxPlayerLineNo:
                continue

            sVal = self.getLineSpaceVal(lineNo)

            if not sVal.isReadyEnter():
                continue

            res['info'][lineNo] = len(lineMembers)

        box.client.onGetLineInfo(json.dumps(res))

    def notifyPlayerOffline(self, lineNo, gbId):
        self.removeLinePlayerInLine(lineNo, gbId)

    def removePendingEnterOnBaseDestroy(self, lineNo, gbId):
        DEBUG_MSG('ILinePlayersStub::removePendingEnterOnBaseDestroy', lineNo, gbId)
        lineMembers = self.allPlayers.getLinePlayers(lineNo)
        if not lineMembers:
            return
        lineMembers.removePendingEnterPlayer(self, gbId)

    def debugPlayerAreaInfo(self):
        pass
