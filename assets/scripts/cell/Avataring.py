# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import math
import gameconst
import gameglobal
import gametimer
import utils
import gameconfig
import sMath
import const_const as CONST

import iTimer
import posture_posture as PP
import performanceLevel_set as PLSD


class AvataringStateRef(object):
    """Avataring 状态位参考定义"""
    Idle        = 0
    Moving      = 1
    Jump        = 21
    DoubleJump  = 22
    Fall        = 23
    Posture     = 47


class Avataring(KBEngine.Entity, iTimer.ITimer):
    IsAvatar = True

    def __init__(self):
        LOG_INFO("Avataring::__intit__~")
        KBEngine.Entity.__init__(self)
        iTimer.ITimer.__init__(self)

        self.emoteId = 0
        self.playTimerId = 0

        # AOI 相关初始化（参考 Avatar）
        self.isWitnessComplete = gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL
        self.showCompleteNum = utils.fetchShowCompleteModelNum()
        self.lastSetCompleteNumTime = 0
        self.showCompleteNumTimer = 0
        self.viewMgr = KBEngine.getNewViewManager()

    def onTimer(self, tid, userArg):
        if utils.isBelongTimerTag(userArg):
            self._onTimerCallback(tid)
        else:
            self._onTimerTrigger(tid, userArg)

    def onBaseGetCell(self):
        LOG_INFO('Avataring::onBaseGetCell~')
        self.base.onGetCellSpaceNo(self.spaceNo)

    def onGetWitness(self, chn):
        LOG_INFO('Avataring::onGetWitness~', chn)
        self.base.onCellGetWitness(chn)

    def onDestroy(self):
        LOG_INFO('Avataring::onDestroy~')

    # ----------------------------
    # 状态位基础操作（服务器只同步，不处理语义和冲突）
    # ----------------------------
    def hasAvataringState(self, stateIdx):
        """查询某状态位是否置位，仅服务器内部使用。"""
        if stateIdx < 0 or stateIdx >= 128:
            return False
        if stateIdx < 64:
            return (self.state >> stateIdx) & 1 > 0
        return (self.state2 >> (stateIdx - 64)) & 1 > 0

    def setAvataringState(self, stateIdx):
        """设置某状态位。"""
        if stateIdx < 0 or stateIdx >= 128:
            LOG_ERR('Avataring::setAvataringState invalid stateIdx', stateIdx)
            return
        if stateIdx < 64:
            self.state |= (1 << stateIdx)
        else:
            self.state2 |= (1 << (stateIdx - 64))

    def removeAvataringState(self, stateIdx):
        """取消某状态位。"""
        if stateIdx < 0 or stateIdx >= 128:
            LOG_ERR('Avataring::removeAvataringState invalid stateIdx', stateIdx)
            return
        if stateIdx < 64:
            self.state &= ~(1 << stateIdx)
        else:
            self.state2 &= ~(1 << (stateIdx - 64))

    # ----------------------------
    # 客户端请求入口
    # ----------------------------
    @utils.isMyself
    def clientSetState(self, exposed, stateIdx):
        LOG_DBG('Avataring::clientSetState', stateIdx)
        if stateIdx == AvataringStateRef.Fall:
            self.removeAvataringState(AvataringStateRef.Jump)
            self.removeAvataringState(AvataringStateRef.DoubleJump)

        self.setAvataringState(stateIdx)

    @utils.isMyself
    def clientRemoveState(self, exposed, stateIdx):
        LOG_DBG('Avataring::clientRemoveState', stateIdx)
        self.removeAvataringState(stateIdx)

    @utils.isMyself
    def offline(self, exposed, reason):
        LOG_INFO('Avataring::offline~', reason)
        self.base.startOffline(reason)
        self.destroy()

    @utils.isMyself
    def jump(self, exposed, jumpType, spaceNo):
        LOG_DBG('Avataring::jump~', jumpType, spaceNo)
        if jumpType == 1:
            self.setAvataringState(AvataringStateRef.Jump)
        elif jumpType == 2:
            self.removeAvataringState(AvataringStateRef.Jump)
            self.setAvataringState(AvataringStateRef.DoubleJump)
        else:
            LOG_ERR('Avataring::jump invalid jumpType:', jumpType)

    @utils.isMyself
    def breakAwayStuck(self, exposed):
        LOG_DBG('Avataring::breakAwayStuck~')
        _pos, _dir = utils.getPlayerBreakAwayStuckPos(self.spaceNo, self.position)
        self.position = _pos
        self.direction = (0.0, 0.0, _dir * math.pi / 180)
        self.client.onBreakAwayStuckSuccess()

    def _cancelPlayEmoteTimer(self):
        if self.playTimerId:
            self.cancelTimerCB(self.playTimerId, gametimer.TIMER_TAG_STOP_PLAY_EMOTE)
            self.playTimerId = 0

    @utils.isMyself
    def reqPlayEmote(self, exposed, emoteId):
        LOG_DBG('Avataring::reqPlayEmote~', emoteId)
        self._cancelPlayEmoteTimer()
        emoteCfg = PP.datas.get(emoteId)
        emoteTime = emoteCfg['time'] if emoteCfg else 3
        self.playTimerId = self.addTimerCB(emoteTime + 1, 'stopPlayEmote', (gameconst.StopPlayEmoteReason.TimeOut,), gametimer.TIMER_TAG_STOP_PLAY_EMOTE, 'playTimerId')
        self.emoteId = emoteId
        self.setAvataringState(AvataringStateRef.Posture)
        self.allClients.onStartPlayEmote(emoteId)

    @utils.isMyself
    def reqStopPlayEmote(self, exposed):
        LOG_DBG('Avataring::reqStopPlayEmote~', self.emoteId)
        self.stopPlayEmote(gameconst.StopPlayEmoteReason.Client)

    def stopPlayEmote(self, reason):
        LOG_DBG('Avataring::stopPlayEmote~', self.emoteId, reason)
        if not self.hasAvataringState(AvataringStateRef.Posture):
            return
        self._cancelPlayEmoteTimer()
        self.emoteId = 0
        self.removeAvataringState(AvataringStateRef.Posture)
        self.allClients.onStopPlayEmote()

    @utils.isMyself
    def setShowCompleteNum(self, exposed, showCompleteNum):
        LOG_INFO('Avataring::setShowCompleteNum', exposed, showCompleteNum)

        if self.showCompleteNumTimer:
            self.cancelTimerCB(self.showCompleteNumTimer, gametimer.TIMER_TAG_SET_COMPLETE_NUM)
            self.showCompleteNumTimer = 0

        showCompleteNum = min(showCompleteNum, utils.fetchShowCompleteModelNum())
        curTime = utils.curTS()
        _tongpingDelayCD = int(PLSD.datas["tongpingDelayCD"].get("value"))
        if curTime - self.lastSetCompleteNumTime >= _tongpingDelayCD:
            if showCompleteNum != self.showCompleteNum:
                self.showCompleteNum = showCompleteNum
                self.lastSetCompleteNumTime = curTime
                self.isNeedResortView = True
        else:
            _delayTime = (_tongpingDelayCD + 1) - (curTime - self.lastSetCompleteNumTime)
            self.showCompleteNumTimer = self.addTimerCB(
                _delayTime, "setShowCompleteNum",
                (exposed, showCompleteNum),
                gametimer.TIMER_TAG_SET_COMPLETE_NUM, 'showCompleteNumTimer')

    # ----------------------------
    # AOI 优化（参考 Avatar，针对等待服简化）
    # ----------------------------

    # 实体e进入AOI但同步到客户端前调用，可以控制这个实体是否同步到客户端
    def beforeWitnessed(self, e):
        # 等待服不存在跨服、采集物等复杂情况，直接按类型处理
        if not e.IsAvatar:
            e.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)
            return

        if gameconfig.enableViewMgr():
            self.viewMgr.addViewRelation(e.id)
        else:
            self.addViewRelation(e.id)

    def onEnteredView(self, e):
        # 等待服无战斗、组队、团本等系统，无需额外缓存
        pass

    def onLeaveView(self, e):
        if gameconfig.enableViewMgr():
            self.viewMgr.removeViewRelation(e.id)
        else:
            self.removeViewRelation(e.id)

    def onUpdateBegin(self):
        if gameconfig.enableViewMgr():
            _nameNum = utils.fetchShowNameNum()
            _ret = self.viewMgr.reSortRelation(
                self.showCompleteNum,
                _nameNum,
            )
            if _ret is None:
                return

            _complete, _names, _hides, _removes = _ret
            for i in _complete:
                entity = KBEngine.entities.get(i)
                entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

            for i in _names:
                entity = KBEngine.entities.get(i)
                entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

            for i in _hides:
                entity = KBEngine.entities.get(i)
                entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

            if _removes:
                self.client.onRemoveCompleteWitness(_removes)

            return

        self.reSortRelationList()

    def addViewRelation(self, targetId):
        if targetId not in self.viewEntityDict:
            self.viewEntityDict[targetId] = True
            self.isNeedResortView = True

    def removeViewRelation(self, targetId):
        if targetId in self.viewEntityDict:
            self.viewEntityDict.pop(targetId, None)
            self.isNeedResortView = True

    def reSortRelationList(self):
        """
        等待服 AOI 优化：仅对视野内 Avataring 按距离与进视野顺序分层显示。
        viewEntityDict: 所有真实在视野内玩家（dict，key 为 entity id，value 为 near/far 标记）
        viewCompleteSet: 当前全模型set
        viewNameSet: 只显示名字的set
        优先级
        1#20米以内（曼哈顿距离）
        2#进视野早晚
        """
        if not self.isNeedResortView:
            return

        _load = KBEngine.getAverageLoad()
        if _load > 0.8:
            if KBEngine.time() - self.lastResortTimes < gameconfig.highLoadDelay():
                return
        elif _load > 0.7:
            if KBEngine.time() - self.lastResortTimes < 20:
                return

        _listLen = len(self.viewEntityDict)
        if _listLen == 0:
            self.reSortRelationListWithAllList([])
            return

        _targetSurroundArea = CONST.datas['targetSurroundArea']['value']
        _entities = KBEngine.entities

        # 第一遍：计算距离并在 value 中标记 near/far，同时统计 near 数量
        _nearCount = 0
        for _eid in self.viewEntityDict:
            _entity = _entities.get(_eid)
            _isNear = _entity is not None and sMath.manhattanDist(self.position, _entity.position) <= _targetSurroundArea
            self.viewEntityDict[_eid] = _isNear
            if _isNear:
                _nearCount += 1

        # 第二遍：按进入 AOI 顺序填充等长 list，近的在前，远的在后
        _allList = [None] * _listLen
        _nearIdx = 0
        _farIdx = _nearCount
        for _eid, _isNear in self.viewEntityDict.items():
            if _isNear:
                _allList[_nearIdx] = _eid
                _nearIdx += 1
            else:
                _allList[_farIdx] = _eid
                _farIdx += 1

        self.reSortRelationListWithAllList(_allList)

    def reSortRelationListWithAllList(self, allList):
        listLen = len(allList)

        showCompleteModelNum = self.showCompleteNum
        showNameNum = utils.fetchShowNameNum()

        # 新的 complete / name 集合
        curCompleteSet = set(allList[:min(listLen, showCompleteModelNum)])
        curNameSet = set()
        if listLen > showCompleteModelNum:
            curNameSet = set(allList[showCompleteModelNum:min(listLen, showCompleteModelNum + showNameNum)])

        LOG_DBG('Avataring::reSortRelationList curCompleteSet', curCompleteSet)

        # 升级到 complete
        for _eId in curCompleteSet.difference(self.viewCompleteSet):
            entity = KBEngine.entities.get(_eId)
            entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

        # 通知客户端移除不再 complete 的实体
        completeRemove = self.viewCompleteSet.difference(curCompleteSet)
        if completeRemove:
            self.client.onRemoveCompleteWitness(list(completeRemove))

        # 升级到 name（包括从 complete 降级为 name 的实体）
        for _eId in curNameSet.difference(self.viewNameSet):
            entity = KBEngine.entities.get(_eId)
            entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

        # 需要隐藏的：之前在 complete 或 name 中，但现在不在新的 complete 或 name 中
        hideSet = (self.viewCompleteSet | self.viewNameSet).difference(curCompleteSet | curNameSet)
        for _eId in hideSet:
            entity = KBEngine.entities.get(_eId)
            entity and entity.setWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

        self.viewCompleteSet = curCompleteSet
        self.viewNameSet = curNameSet
        self.isNeedResortView = False
        self.lastResortTimes = KBEngine.time()
