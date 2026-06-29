# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

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
    """Avataring 状态位参考定义（0~127），实际语义由客户端控制。"""
    Idle        = 0
    Moving      = 1
    Jump        = 21
    DoubleJump  = 22
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
        self.setAvataringState(stateIdx)

    @utils.isMyself
    def clientRemoveState(self, exposed, stateIdx):
        LOG_DBG('Avataring::clientRemoveState', stateIdx)
        self.removeAvataringState(stateIdx)

    @utils.isMyself
    def offline(self, exposed, reason):
        LOG_DBG('Avataring::offline~')
        self.base.startOffline(reason)
        self.destroy()

    @utils.isMyself
    def jump(self, exposed, jumpType, spaceNo):
        LOG_DBG('Avataring::jump~', jumpType, spaceNo)
        if jumpType == AvataringStateRef.Jump or jumpType == AvataringStateRef.DoubleJump:
            self.setAvataringState(jumpType)

    @utils.isMyself
    def breakAwayStuck(self, exposed):
        LOG_DBG('Avataring::breakAwayStuck~')
        self.position = (350, 100, 350)
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
        self.client.onStartPlayEmote(emoteId)

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
        self.client.onStopPlayEmote()

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
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)

            for i in _names:
                entity = KBEngine.entities.get(i)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

            for i in _hides:
                entity = KBEngine.entities.get(i)
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

            if _removes:
                self.client.onRemoveCompleteWitness(_removes)

            return

        self.reSortRelationList()

    def addViewRelation(self, targetId):
        if targetId not in self.enterViewList:
            self.enterViewList.append(targetId)
            self.viewEnterViewSet.add(targetId)
            self.isNeedResortView = True

    def removeViewRelation(self, targetId):
        if targetId in self.enterViewList:
            self.enterViewList.remove(targetId)
            self.viewLeaveViewSet.add(targetId)
            self.viewEnterViewSet.discard(targetId)
            self.isNeedResortView = True

    def pySetWitnessType(self, eId, witnessType):
        self.setWitnessType(eId, witnessType)

    def reSortRelationList(self):
        """
        等待服 AOI 优化：仅对视野内 Avataring 按距离与进视野顺序分层显示。
        enterViewList: 所有真实在视野内玩家
        viewEnterViewSet: 上次sort之后进AOI的玩家
        viewLeaveViewSet: 上次sort之后离开AOI的玩家
        viewCompleteSet: 当前全模型set
        viewNameSet: 只显示名字的set
        优先级
        1#20米以内（曼哈顿距离）
        2#进视野早晚
        """
        if not self.isNeedResortView:
            return

        _nearList = []
        _farList = []
        for _eid in self.enterViewList:
            _entity = KBEngine.entities.get(_eid)
            if _entity and sMath.manhattanDist(self.position, _entity.position) <= CONST.datas['targetSurroundArea']['value']:
                _nearList.append(_eid)
            else:
                _farList.append(_eid)

        _allList = _nearList + _farList
        self.reSortRelationListWithAllList(_allList)

    def reSortRelationListWithAllList(self, allList):
        _removeCurLevelSet = self.viewEnterViewSet.copy()
        listLen = len(allList)

        showCompleteModelNum = self.showCompleteNum
        showNameNum = utils.fetchShowNameNum()
        curCompleteSet = set(allList[:min(listLen, showCompleteModelNum)])
        LOG_DBG('Avataring::reSortRelationList curCompleteSet', curCompleteSet)
        _addList = curCompleteSet.difference(self.viewCompleteSet)
        for _eId in _addList:
            entity = KBEngine.entities.get(_eId)
            entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)
            _removeCurLevelSet.discard(_eId)
        _rmCompleteSet = self.viewCompleteSet.difference(curCompleteSet)
        _removeCurLevelSet.update(_rmCompleteSet)
        if len(_rmCompleteSet) > 0:
            self.client.onRemoveCompleteWitness(list(_rmCompleteSet))
        self.viewCompleteSet = curCompleteSet

        _ignoreNum = showCompleteModelNum + showNameNum
        if listLen >= showCompleteModelNum:
            _curNameSet = set(allList[showCompleteModelNum:min(listLen, _ignoreNum)])
            _addNameList = _curNameSet.difference(self.viewNameSet)
            for _eId in _addNameList:
                _removeCurLevelSet.discard(_eId)
                _entity = KBEngine.entities.get(_eId)
                _entity and _entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)

            _rmNameSet = self.viewNameSet.difference(_curNameSet)
            _rmNameSet = _rmNameSet.difference(self.viewCompleteSet)
            _removeCurLevelSet.update(_rmNameSet)
            self.viewNameSet = _curNameSet
        else:
            self.viewNameSet.clear()

        # 处理同一帧内出去又进来的情况
        for _eId in (self.viewEnterViewSet & self.viewLeaveViewSet):
            _removeCurLevelSet.discard(_eId)
            entity = KBEngine.entities.get(_eId)
            if _eId in self.viewCompleteSet:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_ALL)
            elif _eId in self.viewNameSet:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_NAME)
            else:
                entity and entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

        for _eId in _removeCurLevelSet:
            if _eId in self.enterViewList:
                _entity = KBEngine.entities.get(_eId)
                _entity and _entity.pySetWitnessType(self.id, gameconst.WitnessTypeEnum.WITNESS_ENUM_HIDE)

        self.isNeedResortView = False
        self.viewEnterViewSet.clear()
        self.viewLeaveViewSet.clear()
