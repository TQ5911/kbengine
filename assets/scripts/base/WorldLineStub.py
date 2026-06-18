# -*- coding: utf-8 -*-

import random

import KBEngine
from KBEDebug import *

import iGlobal
import iBaseNoCell
import iTimer
import iLinePlayersStub
import iLineStubBase
import linePlayers

import gameengine
import gametimer
import utils
import gameconst
import gameconfig

import formula
import branchData_set


class WorldLineStub(iGlobal.IGlobal, iBaseNoCell.IBaseNoCell, iTimer.ITimer, \
                    iLineStubBase.ILineStubBase):
    def __init__(self):
        iLineStubBase.ILineStubBase.__init__(self)
        self.initDatetimeTimerTick()
        self.allPlayers = linePlayers.AllLinePlayers(self.lineType)
        self.clearTimeOutIter = None

        interval = 60 * branchData_set.datas["Branch_mergeInterval"]["value"]
        waitTime = 60 * branchData_set.datas["Branch_mergeWaitingTime"]["value"]

        self.pyAddTimer(interval, interval, gametimer.CHECK_LINE_MERGE)
        self.pyAddTimer(interval + waitTime, interval, gametimer.DO_LINE_MERGE)
        self.pyAddTimer(5, 5, gametimer.CLEAR_WORLDLINE_ENTER_TIME_OUT)

    def doNext(self):
        LOG_DBG('WorldLine doNext', self.lineType)
        super().doNext()
        return

    def onTimer(self, tid, userArg):
        if userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
            self._onDatetimeTimerTick()
        elif userArg == gametimer.CHECK_LINE_MERGE:
            self._checkLineMerge()
        elif userArg == gametimer.DO_LINE_MERGE:
            self._doLineMerge()
        elif userArg == gametimer.CLEAR_WORLDLINE_ENTER_TIME_OUT:
            self.onClearEnterTimeOut(gameconst.WORLDLINE_ENTER_TIME_OUT_DUR)

        super().onTimer(tid, userArg)

    def onLoadEntitiesEnd(self, spaceNo):
        LOG_DBG("WorldLineStub onLoadEntitiesEnd", spaceNo)
        iLineStubBase.ILineStubBase.onLoadEntitiesEnd(self, spaceNo)

    def onLineSpaceGone(self, spaceNo, groupOrder):
        iLineStubBase.ILineStubBase.onLineSpaceGone(self, spaceNo, groupOrder)
        lineNo = formula.parseLineNo(spaceNo)

        # 所有线都没了，暂时禁止登录
        if not self.lineSpaces:
            import gmCommand
            import gmGroup
            import gmAdmin
            agent = gmCommand.GMAgent(gmAdmin.DUMMY_SU, '', None, gmGroup.MANAGER_GROUP_GOD)
            gmCommand.doCommandInside(agent, "$setcachecfg interfaceEnableLogin 0")

    def willRecoverLine(self, lineNo):
        if lineNo not in self.lineReadRecoverList:
            self.lineReadRecoverList.append(lineNo)

    def onLineSpaceReady(self, spaceNo):
        LOG_INFO('onLineSpaceReady', spaceNo)
        iLineStubBase.ILineStubBase.onLineSpaceReady(self, spaceNo)
        lineNo = formula.parseLineNo(spaceNo)

        if lineNo in self.lineReadRecoverList:
            self.lineReadRecoverList.remove(lineNo)

    def onCellappRelive(self, groupOrder):
        super(WorldLineStub, self).onCellappRelive(groupOrder)

    def enterLineSuccess(self, lineNo, box, gbId, succInfo):
        LOG_INFO('enterLineSuccess', lineNo, box.id, gbId, succInfo)
        super(WorldLineStub, self).enterLineSuccess(lineNo, box, gbId, succInfo)
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('enterLineSuccess:cannot find player:', self.lineType, lineNo, gbId, box.id)
            return

        _linePlayers = self.allPlayers.getLinePlayers(lineNo)

        teamUUID = succInfo.get('teamUUID', 0)
        isLeader = succInfo.get('isLeader', False)

        _linePlayers.onPlayerTeamChanged(gbId, 0, teamUUID, isLeader)
        # _linePlayers.onPlayerAreaChanged(gbId, areaId)
        if abs(len(_linePlayers) - _linePlayers.lastUpPlayerNum) >= gameconst.WORLD_LINE_UPDATE_WEIGHT_VAL:
            _linePlayers.lastUpPlayerNum = len(_linePlayers)
            spaceVal = self.getLineSpaceVal(lineNo)
            spaceVal.lineSpaceBox.cell.updateSpaceWeight(utils.calcSpaceWeight(_linePlayers.lastUpPlayerNum, False,
                                                                               gameconst.EntNumPerPlayerInAOI.worldLine,
                                                                               gameconst.WORLD_LINE_BASE_WEIGHT))

    def updateLinePlayerInfo(self, lineNo, box, gbId, infoDict):
        super(WorldLineStub, self).updateLinePlayerInfo(lineNo, box, gbId, infoDict)
        playerVal = self.allPlayers.getPlayer(lineNo, gbId)
        if not playerVal:
            LOG_ERR('updateLinePlayerInfo:cannot find player:', self.lineType, lineNo, gbId, box.id, infoDict)
            return

        linePlayers = self.allPlayers.getLinePlayers(lineNo)
        if not linePlayers:
            return

        if 'areaId' in infoDict:
            newVal = infoDict['areaId']
            linePlayers.onPlayerAreaChanged(gbId, newVal)

    def checkAutoSwitchLine(self, box, gbId, spaceNo):
        pass

    def _requestCollectionPostionByCollId(self, collectionId, spaceNo):
        _m_coll = self.getCollectionSharedColl(spaceNo, collectionId, default=())
        if not _m_coll:
            LOG_WARN("_requestCollectionPostionByCollId:: coll not found", collectionId, spaceNo)
            return (0, None), False

        _m_gameEntityId = random.choice(list(_m_coll))
        _m_gid = utils.parseGidFromGameEntityId(_m_gameEntityId)
        _m_sGid = str(_m_gid)

        m_datas = utils.getDunModuleData(formula.fetchMapId(spaceNo))
        if _m_sGid not in m_datas:
            LOG_WARN("_requestCollectionPostionByCollId:: gid not in data", _m_sGid, collectionId, spaceNo)
            return (0, None), False

        _m_prm = m_datas[_m_sGid]
        _m_pos = (_m_prm['PosX'], _m_prm['PosY'], _m_prm['PosZ'])
        return (_m_gameEntityId, _m_pos), True

    def leaveLine(self, box, gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection):
        super(WorldLineStub, self).leaveLine(box, gbId, fromSpaceNo, toSpaceNo, toPosition, toDirection)
        lineNo = formula.parseLineNo(fromSpaceNo)
        _linePlayers = self.allPlayers.getLinePlayers(lineNo)
        # 进入副本，大世界需要继续占坑位
        if abs(len(_linePlayers) - _linePlayers.lastUpPlayerNum) >= gameconst.WORLD_LINE_UPDATE_WEIGHT_VAL:
            _linePlayers.lastUpPlayerNum = len(_linePlayers)
            spaceVal = self.getLineSpaceVal(lineNo)
            spaceVal.lineSpaceBox.cell.updateSpaceWeight(utils.calcSpaceWeight(_linePlayers.lastUpPlayerNum, False,
                                                                               gameconst.EntNumPerPlayerInAOI.worldLine,
                                                                               gameconst.WORLD_LINE_BASE_WEIGHT))

    def switchLineSuccess(self, fromLineNo, toLineNo, box, gbId, extra):
        super(WorldLineStub, self).switchLineSuccess(fromLineNo, toLineNo, box, gbId, extra)
        for lineNo in (fromLineNo, toLineNo):
            _linePlayers = self.allPlayers.getLinePlayers(lineNo)
            if abs(len(_linePlayers) - _linePlayers.lastUpPlayerNum) >= gameconst.WORLD_LINE_UPDATE_WEIGHT_VAL:
                _linePlayers.lastUpPlayerNum = len(_linePlayers)
                spaceVal = self.getLineSpaceVal(lineNo)
                spaceVal.lineSpaceBox.cell.updateSpaceWeight(utils.calcSpaceWeight(_linePlayers.lastUpPlayerNum, False,
                                                                                   gameconst.EntNumPerPlayerInAOI.worldLine,
                                                                                   gameconst.WORLD_LINE_BASE_WEIGHT))

    def debugPlayerAreaInfo(self):
        lines = self.getLineNoReadyForEnter()
        LOG_DBG('!!!!!!!========== debug player area info start ==========')
        import worldConfig_Area as wcad
        count = 0
        for areaid in iter(wcad.datas):
            info = wcad.datas[areaid]
            LOG_DBG(
                '!!!!!!!area: {}, N4:{}, N5:{}'.format(info.get('Areaname', ''), info.get('N4', 0), info.get('N5', 0)))
            linen = [0] * len(lines)
            for lineNo in lines:
                linePlayers = self.allPlayers.getLinePlayers(lineNo)
                areaPlayers = linePlayers.playersInArea(areaid)
                num = len(areaPlayers)
                if num: LOG_DBG('!!!!!!!        line: {}, num: {}'.format(lineNo, num))
                linen[lineNo] = num
                count += num

            n5 = wcad.datas[areaid]['N5']
            maxx = max(linen)
            flag = False if maxx > n5 else True
            LOG_DBG('!!!!!!!        check area player num under hard limit', flag)
            LOG_DBG('!!!!!!!--------')

        LOG_DBG('!!!!!!!player area num count:', count)
        LOG_DBG('!!!!!!!========== debug player area info end ==========')

    def notifyPlayerOffline(self, lineNo, gbId):
        super(WorldLineStub, self).notifyPlayerOffline(lineNo, gbId)
        _linePlayers = self.allPlayers.getLinePlayers(lineNo)
        if not _linePlayers:
            return
        if abs(len(_linePlayers) - _linePlayers.lastUpPlayerNum) >= gameconst.WORLD_LINE_UPDATE_WEIGHT_VAL:
            _linePlayers.lastUpPlayerNum = len(_linePlayers)
            spaceVal = self.getLineSpaceVal(lineNo)
            spaceVal.lineSpaceBox.cell.updateSpaceWeight(utils.calcSpaceWeight(_linePlayers.lastUpPlayerNum, False,
                                                                               gameconst.EntNumPerPlayerInAOI.worldLine,
                                                                               gameconst.WORLD_LINE_BASE_WEIGHT))

    def onLoadGroupEntities(self, info):
        LOG_DBG("WorldLineStub::onLoadGroupEntities", info)
        super(WorldLineStub, self).onLoadGroupEntities(info)

    def onRefreshGroupEntities(self, info):
        LOG_DBG("WorldLineStub::onRefreshGroupEntities", info)
        super(WorldLineStub, self).onRefreshGroupEntities(info)

    def onDestroyGroupEntities(self, info):
        LOG_DBG("WorldLineStub::onDestroyGroupEntities", info)
        super(WorldLineStub, self).onDestroyGroupEntities(info)

    def notifyCreateWorldBoss(self, spaceNo):
        _lineNo = formula.parseLineNo(spaceNo)
        spaceVal = self.getLineSpaceVal(_lineNo)
        spaceVal.lineSpaceBox.cell.callOnSpaceMgr('doCreateWorldBoss', ())
