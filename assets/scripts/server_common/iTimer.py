# -*- coding: utf-8 -*-
import random

from KBEDebug import *
import KBEngine

import collections
import math

import gametimer
import gameconst
import traceback
import gameengine
import gameconfig

import utils

if KBEngine.component == 'cellapp':
    TIMER_PROP = 'timerDataCell'
    DATETIME_TIMER_PROP = 'datetimeTimerDataCell'
    DATETIME_TIMER_ID = 'datetimeTimerIdCell'
    DATETIME_TIMER_IDCNT = 'datetimeTimerIdCellCount'
    DATETIME_TIMER_TIMECACHE = 'datetimeTimerDataTimeCacheCell'
    DATETIME_TIMER_NEXTT = 'datetimeTimerDataNextTCell'
    isCell = True
else:
    TIMER_PROP = 'timerDataBase'
    DATETIME_TIMER_PROP = 'datetimeTimerDataBase'
    DATETIME_TIMER_ID = 'datetimeTimerIdBase'
    DATETIME_TIMER_IDCNT = 'datetimeTimerIdBaseCount'
    DATETIME_TIMER_TIMECACHE = 'datetimeTimerDataTimeCacheBase'
    DATETIME_TIMER_NEXTT = 'datetimeTimerDataNextTBase'
    isCell = False

DatetimeTimerCallbackData = collections.namedtuple(
    "DatetimeTimerCallbackData",
    ("funcName", "funcArgs", "varTimerID", "tag", "endT"))


class DatetimeTimerMixin(object):
    """
    NOTE(): 使用DataTime需要
        1. 在适当位置调用addDatetimeTimerTick方法
        2. 在onTimer方法中加入以下代码

        def onTimer(...):
            ....
            elif userArg == gametimer.TIMER_DATETIME_ITIMER_CALLBACK:
                self._onDatetimeTimerTick()
            ...
    """

    # region Properties
    @property
    def datetimeTimerId(self):
        return getattr(self, DATETIME_TIMER_ID, 0)

    @datetimeTimerId.setter
    def datetimeTimerId(self, newTimerIdCnt: int):
        setattr(self, DATETIME_TIMER_ID, int(newTimerIdCnt))

    @property
    def datetimeTimerIdCnt(self):
        return getattr(self, DATETIME_TIMER_IDCNT, 0)

    @datetimeTimerIdCnt.setter
    def datetimeTimerIdCnt(self, newTimerId: int):
        setattr(self, DATETIME_TIMER_IDCNT, int(newTimerId))

    def getDatetimeTimerProp(self):
        return getattr(self, DATETIME_TIMER_PROP)

    @property
    def datetimeTimerDataNextT(self):
        return getattr(self, DATETIME_TIMER_NEXTT, 0)

    @datetimeTimerDataNextT.setter
    def datetimeTimerDataNextT(self, nextT: int):
        setattr(self, DATETIME_TIMER_NEXTT, int(nextT))

    def getDatetimeTimerDataTimeCache(self):
        return getattr(self, DATETIME_TIMER_TIMECACHE, 0)

    def getDatetimeTimerTickInterval(self) -> float:
        return 2

    def getDatetimeTimerRandomTickRange(self, numTick):
        return numTick * self.getDatetimeTimerTickInterval()

    def getCallbackNumThreshold(self):
        return gameconfig.callbackNumThreshold()

    # endregion

    # region cnt methods
    def _getNextDatetimeTimerId(self):
        _crtDatetimeTimerIdCnt = self.datetimeTimerIdCnt
        datetimeTimerProp = self.getDatetimeTimerProp()
        for i in range(_crtDatetimeTimerIdCnt, gameconst.UINT32_MAX + 1):
            if i not in datetimeTimerProp:
                return i
            self.datetimeTimerIdCnt += 1
        for j in range(1, _crtDatetimeTimerIdCnt):
            if j not in datetimeTimerProp:
                return j
            self.datetimeTimerIdCnt += 1

        gameengine.reportCritical(f"{self.__class__.__name__}::_getNextDatetimeTimerId:: timerId full!!!",
                                  _crtDatetimeTimerIdCnt, len(datetimeTimerProp))
        return 0

    # endregion

    # region Timer Cache
    def _setDateTimerTimeCache(self, endT: int, timerId):
        datetimeTimerTimeCache = self.getDatetimeTimerDataTimeCache()
        datetimeTimerTimeCache.setdefault(endT, []).append(timerId)
        datetimeTimerDataNextT = self.datetimeTimerDataNextT
        self.datetimeTimerDataNextT = min(datetimeTimerDataNextT,
                                          endT) if datetimeTimerDataNextT > 0 else datetimeTimerDataNextT

    def _getDateTimerTimeCache(self, endT, default=()):
        return self.getDatetimeTimerDataTimeCache().get(endT, default)

    def _popDateTimerTimeCache(self, endT, default=()):
        return self.getDatetimeTimerDataTimeCache().pop(endT, default)

    # endregion

    # region Timer Methods
    def _setDatetimeTimerData(self, timerId, data):
        datetimeTimerProp = self.getDatetimeTimerProp()
        if timerId in datetimeTimerProp:
            gameengine.reportCritical(f"{self.__class__.__name__}::_setDatetimeTimerData:: timerId already exists!!!",
                                      timerId, data, datetimeTimerProp[timerId])

        if not (hasattr(self, 'getTempMiscProp') and self.getTempMiscProp(gameconst.AvatarProps.disableTimerNumErrMsg)) \
                and len(datetimeTimerProp) >= self.getCallbackNumThreshold():
            gameengine.reportCritical(f"{self.__class__.__name__}::_setDatetimeTimerData:: too many callbacks!!!",
                                      timerId, data, len(datetimeTimerProp), self.IsAvatar, datetimeTimerProp)

        datetimeTimerProp[timerId] = data

    def _getDatetimeTimerData(self, timerId, default=None):
        datetimeTimerProp = self.getDatetimeTimerProp()
        return datetimeTimerProp.get(timerId, default)

    def _hasDatetimeTimerData(self, timerId):
        datetimeTimerProp = self.getDatetimeTimerProp()
        return timerId in datetimeTimerProp

    def _popDatetimeTimerData(self, timerId, default=None):
        datetimeTimerProp = self.getDatetimeTimerProp()
        return datetimeTimerProp.pop(timerId, default)

    def _reloadDatetimeTimerData(self):
        datetimeTimerProp = self.getDatetimeTimerProp()
        for data in datetimeTimerProp.values():
            t = data[1]
            if hasattr(t, 'reloadScript'):
                t.reloadScript()
            elif hasattr(t, '__iter__'):
                for v in t:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def _hasDatetimeTimer(self, timerId):
        datetimeTimerProp = self.getDatetimeTimerProp()
        return timerId in datetimeTimerProp

    def _datetimeCallback(self, tFire: int, funcName, funcArgs, tag, varTimerID='', **kwargs):
        if not self.datetimeTimerId:
            gameengine.reportCritical(f"{self.__class__.__name__}::_datetimeCallback:: tick timer unregr. !!!",
                                      tFire, funcName, funcArgs, tag, varTimerID, kwargs)
            return 0

        if not funcName:
            return 0

        if isCell and not self.isReal():
            return 0

        if self.isDestroyed:
            return 0

        if funcArgs is None:
            funcArgs = ()

        if tFire < utils.getNow():
            getattr(self, funcName)(*funcArgs)
            return 0

        timerId = self._getNextDatetimeTimerId()
        data = DatetimeTimerCallbackData(funcName, funcArgs, varTimerID, tag, math.ceil(tFire))
        self._setDatetimeTimerData(timerId, data)
        self._setDateTimerTimeCache(data.endT, timerId)
        return timerId

    def toCallbackByDatetimeAfter(self, t, tag=gametimer.TIMER_TAG_NONE, fnName='', varTimeID=''):
        return _CallbackByDatetimeCalled(t, varTimeID, fnName, tag, self)

    def _cancelDatetimeCallback(self, timerId, tag):
        if not timerId:
            return

        data = self._getDatetimeTimerData(timerId)
        if not data:
            ERROR_MSG(f'{self.__class__.__name__}::_cancelDatetimeCallback:: cancel timer timerID not in timerData',
                      timerId, '|', tag, '|', data, self.getDatetimeTimerProp())
            for line in traceback.format_stack():
                ERROR_MSG(line)
            return

        funcName, funcArgs, varTimerId, timerTag, endT, *_ = data
        if tag not in (gametimer.TIMER_TAG_NONE, timerTag):
            ERROR_MSG(f'{self.__class__.__name__}::_cancelDatetimeCallback:: cancel timer mismatch',
                      timerId, '|', tag, '|', data, self.getDatetimeTimerProp())
            for line in traceback.format_stack():
                ERROR_MSG(line)
            return

        if varTimerId:
            setattr(self, varTimerId, 0)

        self._popDatetimeTimerData(timerId)

    def _cancelAllDatetimeCallback(self):
        datetimeTimerProp = self.getDatetimeTimerProp()
        for timerId in list(datetimeTimerProp.keys()):
            self._cancelDatetimeCallback(timerId, gametimer.TIMER_TAG_NONE)

    def _onTimerDatetimeCallback(self, timerId):
        data = self._popDatetimeTimerData(timerId)
        if not data:
            return

        funcName, funcArgs, varTimerId, timerTag, endT, *_ = data
        if varTimerId:
            setattr(self, varTimerId, 0)

        getattr(self, funcName)(*funcArgs)

    def addDatetimeTimerTick(self, start=1):
        tick = self.getDatetimeTimerTickInterval()
        start = random.random() * tick
        if self.datetimeTimerId:
            gameengine.reportCritical(f"{self.__class__.__name__}::addDatetimeTimerTick:: already get timerId!!!",
                                      self.datetimeTimerId)
            self.pyDelTimer(self.datetimeTimerId, gametimer.TIMER_DATETIME_ITIMER_CALLBACK)
        self.datetimeTimerId = self.pyAddTimer(start, tick, gametimer.TIMER_DATETIME_ITIMER_CALLBACK)

    # def _onDatetimeTimerTick(self):
    #     datetimeTimerProp = self.getDatetimeTimerProp()
    #     for timerId in datetimeTimerProp:
    #         if not self._hasDatetimeTimerData(timerId):
    #             continue

    #         data = self._getDatetimeTimerData(timerId)
    #         if not data:
    #             self._popDatetimeTimerData(timerId)
    #             continue

    #         if utils.getNow() < data.endT:
    #             continue

    #         self._onTimerDatetimeCallback(timerId)
    def _onDatetimeTimerTick(self):
        # ERROR_MSG("DEBUG:_onDatetimeTimerTick:START:", self.datetimeTimerDataNextT)
        now = utils.getNow()
        datetimeTimerProp = self.getDatetimeTimerProp()
        datetimeTimerTimeCache = self.getDatetimeTimerDataTimeCache()

        if self.datetimeTimerDataNextT <= 0 and datetimeTimerTimeCache:
            self.datetimeTimerDataNextT = min(datetimeTimerTimeCache)

        _depth, _depthAlert = 0, 60 * 10
        while 0 < self.datetimeTimerDataNextT < now and _depth < _depthAlert:
            _thisEndT = self.datetimeTimerDataNextT
            _timerIdList = self._getDateTimerTimeCache(_thisEndT)
            for _timerId in _timerIdList:
                if not self._hasDatetimeTimerData(_timerId):
                    continue
                data = self._getDatetimeTimerData(_timerId)
                if not data:
                    self._popDatetimeTimerData(_timerId)
                    continue
                if data.endT != _thisEndT:
                    continue
                self._onTimerDatetimeCallback(_timerId)
                _depth += 1

            self._popDateTimerTimeCache(_thisEndT)
            self.datetimeTimerDataNextT = min(datetimeTimerTimeCache) if datetimeTimerTimeCache else 0

        if _depth >= _depthAlert:
            gameengine.reportCritical(f"{self.__class__.__name__}::_onDatetimeTimerTick:: timerId depth alert!!!",
                                      _depth, _depthAlert, self.datetimeTimerDataNextT, now,
                                      now - self.datetimeTimerDataNextT, len(datetimeTimerProp))
        # ERROR_MSG("DEBUG:_onDatetimeTimerTick:ENDED:", self.datetimeTimerDataNextT)
    # endregion


class ITimer(DatetimeTimerMixin):
    def _setTimerData(self, timerID, data):
        timerProp = getattr(self, TIMER_PROP)
        if timerID in timerProp:
            gameengine.reportCritical('timer id already exists!!!', timerID, data, timerProp[timerID])

        if len(timerProp) >= gameconfig.callbackNumThreshold():
            if not hasattr(self, 'getTempMiscProp') or not hasattr(self, 'setTempMiscProp'):
                gameengine.reportCritical('too many callbacks!!!', self.id, self.__class__.__name__, timerID, data,
                                          len(timerProp))
            elif not self.getTempMiscProp(gameconst.AvatarProps.disableTimerNumErrMsg) and self.getTempMiscProp(
                    gameconst.AvatarProps.timerNumErrMsgTS, 0) < utils.getNow():
                self.setTempMiscProp(gameconst.AvatarProps.timerNumErrMsgTS, utils.getNow() + 1800)

                num = 0
                funcDic = {}
                for k, v in timerProp.items():
                    num += 1
                    funcDic[v[0]] = funcDic.get(v[0], 0) + 1
                    if num > 200:
                        break

                funcList = sorted([(v, k) for k, v in funcDic.items()], reverse=True)
                gameengine.reportCritical('too many callbacks!!!', self.id, self.__class__.__name__, timerID, data,
                                          len(timerProp), funcList[:5])

        timerProp[timerID] = data

    def __getTimerData(self, timerID):
        timerProp = getattr(self, TIMER_PROP)
        return timerProp.get(timerID, None)

    def __popTimerData(self, timerID):
        timerProp = getattr(self, TIMER_PROP)
        return timerProp.pop(timerID, None)

    def _reloadTimerData(self):
        timerProp = getattr(self, TIMER_PROP)
        for data in timerProp.values():
            t = data[1]
            if hasattr(t, 'reloadScript'):
                t.reloadScript()
            elif hasattr(t, '__iter__'):
                for v in t:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def postReloadScript(self):
        if hasattr(super(ITimer, self), 'postReloadScript'):
            super(ITimer, self).postReloadScript()
        self._reloadTimerData()
        self._reloadDatetimeTimerData()

    def _hasTimer(self, timerID):
        timerProp = getattr(self, TIMER_PROP)
        return timerID in timerProp

    def _callback(self, t, funcName, funcArgs, tag, varTimerID='', clearTimerIdFunc='', clearTimerIdArgs=()):
        if not utils.isBelongTimerTag(tag):
            gameengine.reportCritical('callback tag error', tag)
            return 0

        if not funcName:
            return 0

        if isCell and not self.isReal():
            return 0

        if self.isDestroyed:
            return 0

        if funcArgs == None:
            funcArgs = ()

        if t < 0:
            traceback.print_stack()

        timerId = self.addTimer(t, 0, tag)

        self._setTimerData(timerId, (funcName, funcArgs, varTimerID, tag, clearTimerIdFunc, clearTimerIdArgs))

        return timerId

    def toCallbackAfter(self, t, tag=gametimer.TIMER_TAG_NONE, fnName='', varTimeID=''):
        """Usage: tid = self.callbackFun(t, tid).yourOwnFunction(args1, args2, ...)"""
        return _CallbackCalled(t, varTimeID, fnName, tag, self)

    def flowControllerDelayExecEventCallback(self, delayEvent, context):
        delayEvent.handle_be_triggered_after_delay(context)

    def flowControllerDelayCallback(self, delayEvent, cbFuncName, cbArgs, cbKwArgs):
        getattr(delayEvent, cbFuncName)(*cbArgs, **cbKwArgs)

    def _cancelCallback(self, timerID, tag):
        if not timerID:
            return gameconst.TIMER_CANCEL_RET_ZERO_TIMER

        data = self.__getTimerData(timerID)
        if not data:
            return gameconst.TIMER_CANCEL_RET_NOT_DATA

        if self.isDestroyed:
            return gameconst.TIMER_CANCEL_RET_DESTROY

        funcName, funcArgs, varTimerId, timerTag, clearTimerIdFunc, clearTimerIdArgs = data
        if tag != gametimer.TIMER_TAG_NONE and tag != timerTag:
            ERROR_MSG('cancel timer mismatch', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                ERROR_MSG(line)
            return gameconst.TIMER_CANCEL_RET_MISMATCH
        else:
            self.__popTimerData(timerID)

        # varTimerId = data[2]
        if varTimerId:
            setattr(self, varTimerId, 0)

        if clearTimerIdFunc:
            getattr(self, clearTimerIdFunc)(*clearTimerIdArgs)

        if self.delTimer(timerID) < 0:
            ERROR_MSG('invalid timerId', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                ERROR_MSG(line)

        return gameconst.TIMER_CANCEL_RET_SUCCESS

    def _cancelAllCallbacks(self):
        timerProp = getattr(self, TIMER_PROP)
        for timerId in list(timerProp.keys()):
            self._cancelCallback(timerId, gametimer.TIMER_TAG_NONE)

    def _onTimerCallback(self, timerID):
        data = self.__popTimerData(timerID)
        if data == None:
            return

        funcName, funcArgs, varTimerId, tag, clearTimerIdFunc, clearTimerIdArgs = data
        if varTimerId:
            setattr(self, varTimerId, 0)

        if clearTimerIdFunc:
            getattr(self, clearTimerIdFunc)(*clearTimerIdArgs)

        getattr(self, funcName)(*funcArgs)

    def _onTimer(self, timerID, userData):
        if not utils.isBelongTimerTag(userData):
            data = self.__getTimerData(timerID)
            if data:
                funcName, interval, varTimerId, tag = data
                if interval == 0:
                    self.__popTimerData(timerID)

    def pyAddTimer(self, start, interval, userData):
        if not utils.isBelongTimerIdTag(userData):
            gameengine.reportCritical('pyAddTimer wrong userData range', userData)

        timerId = self.addTimer(start, interval, userData)
        self._setTimerData(timerId, ('', interval, '', userData))
        return timerId

    def pyDelTimer(self, timerID, tag):
        if not timerID:
            return

        data = self.__popTimerData(timerID)
        if not data:
            ERROR_MSG('pyDelTimer timerID not exist', timerID, '|', tag)
            return

        if self.isDestroyed:
            return

        if tag != data[3]:
            ERROR_MSG('pyDelTimer mismatch', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                ERROR_MSG(line)
            return

        if self.delTimer(timerID) < 0:
            ERROR_MSG('pyDelTimer invalid timerID', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                ERROR_MSG(line)

    def clearTimerId(self, obj, funcName, funcArgs):
        if obj:
            getattr(obj, funcName)(*funcArgs)


class _CallbackByDatetimeCalled(object):
    def __init__(self, t, tid, fnName, tag, owner: ITimer):
        self.delayTime = t
        self.varTimeID = tid
        self.fnName = fnName
        self.tag = tag
        self.owner = owner

    def __call__(self, *args):
        if not self.fnName:
            raise TypeError("special function name '{}' not define".format(self.fnName))
        return self.owner._datetimeCallback(self.delayTime, self.fnName, args, self.tag, self.varTimeID)

    def __getattr__(self, fnName):
        if self.fnName and fnName != self.fnName:
            raise TypeError("'{}' must be called as special".format(self.fnName))
        if not hasattr(self.owner, fnName):
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.owner.__class__.__name__, fnName))
        fn = getattr(self.owner, fnName)
        if not callable(fn):
            raise TypeError("'{}' object is not callable".format(type(fn).__name__))
        return lambda *args: self.owner._datetimeCallback(self.delayTime, fnName, args, self.tag,
                                                          varTimerID=self.varTimeID)


class _CallbackCalled(object):
    def __init__(self, t, tid, fnName, tag, owner: ITimer):
        self.delayTime = t
        self.varTimeID = tid
        self.fnName = fnName
        self.tag = tag
        self.owner = owner

    def __call__(self, *args):
        if not self.fnName:
            raise TypeError("special function name '{}' not define".format(self.fnName))
        return self.owner._callback(self.delayTime, self.fnName, args, self.tag, self.varTimeID)

    def __getattr__(self, fnName):
        if self.fnName and fnName != self.fnName:
            raise TypeError("'{}' must be called as special".format(self.fnName))
        if not hasattr(self.owner, fnName):
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.owner.__class__.__name__, fnName))
        fn = getattr(self.owner, fnName)
        if not callable(fn):
            raise TypeError("'{}' object is not callable".format(type(fn).__name__))
        return lambda *args: self.owner._callback(self.delayTime, fnName, args, self.tag,
                                                  varTimerID=self.varTimeID)
