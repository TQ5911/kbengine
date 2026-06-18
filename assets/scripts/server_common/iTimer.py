# -*- coding: utf-8 -*-
import random

from KBEDebug import *
import KBEngine

import math
import collections

import gametimer
import gameconst
import traceback
import gameconfig
import gameengine

import utils

if KBEngine.component == 'cellapp':
    TIMER_DATA_PROP = 'timerDataCell'
    DATETIME_TIMER_DATA_PROP = 'datetimeTimerDataCell'
    DATETIME_TIMER_ID = 'datetimeTimerIdCell'
    DATETIME_TIMER_IDCNT = 'datetimeTimerIdCellCount'
    DATETIME_TIMER_TIMECACHE = 'datetimeTimerDataTimeCacheCell'
    DATETIME_TIMER_NEXTT = 'datetimeTimerDataNextTCell'
    isCell = True
else:
    TIMER_DATA_PROP = 'timerDataBase'
    DATETIME_TIMER_DATA_PROP = 'datetimeTimerDataBase'
    DATETIME_TIMER_ID = 'datetimeTimerIdBase'
    DATETIME_TIMER_IDCNT = 'datetimeTimerIdBaseCount'
    DATETIME_TIMER_TIMECACHE = 'datetimeTimerDataTimeCacheBase'
    DATETIME_TIMER_NEXTT = 'datetimeTimerDataNextTBase'
    isCell = False

DatetimeTimerCallbackDataTup = collections.namedtuple(
    "DatetimeTimerCallbackDataTup",
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
    def datetimePropTimerId(self):
        return getattr(self, DATETIME_TIMER_ID, 0)

    @datetimePropTimerId.setter
    def datetimePropTimerId(self, newTimerIdCnt: int):
        setattr(self, DATETIME_TIMER_ID, int(newTimerIdCnt))

    @property
    def datetimePropTimerIdCnt(self):
        return getattr(self, DATETIME_TIMER_IDCNT, 0)

    @datetimePropTimerIdCnt.setter
    def datetimePropTimerIdCnt(self, newTimerId: int):
        setattr(self, DATETIME_TIMER_IDCNT, int(newTimerId))

    @property
    def datetimePropTimerDataNextT(self):
        return getattr(self, DATETIME_TIMER_NEXTT, 0)

    @datetimePropTimerDataNextT.setter
    def datetimePropTimerDataNextT(self, nextT: int):
        setattr(self, DATETIME_TIMER_NEXTT, int(nextT))

    def fetchDatetimeTimerProp(self):
        return getattr(self, DATETIME_TIMER_DATA_PROP)

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
        _crtDatetimeTimerIdCnt = self.datetimePropTimerIdCnt
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        for _i in range(_crtDatetimeTimerIdCnt, gameconst.UINT32_MAX + 1):
            if _i not in datetimeTimerProp:
                return _i
            self.datetimePropTimerIdCnt += 1
        for j in range(1, _crtDatetimeTimerIdCnt):
            if j not in datetimeTimerProp:
                return j
            self.datetimePropTimerIdCnt += 1

        gameengine.panicStack(f"{self.__class__.__name__}::_getNextDatetimeTimerId:: timerId full!!!",
                                  len(datetimeTimerProp), _crtDatetimeTimerIdCnt)
        return 0

    # endregion

    # region Timer Cache
    def _setDateTimerTimeCache(self, endT: int, timerId):
        _datetimeTimerTimeCache = self.getDatetimeTimerDataTimeCache()
        _datetimeTimerTimeCache.setdefault(endT, []).append(timerId)
        _datetimePropTimerDataNextT = self.datetimePropTimerDataNextT
        self.datetimePropTimerDataNextT = min(_datetimePropTimerDataNextT,
                                          endT) if _datetimePropTimerDataNextT > 0 else _datetimePropTimerDataNextT

    def _popDateTimerTimeCache(self, endT, default=()):
        return self.getDatetimeTimerDataTimeCache().pop(endT, default)

    def _getDateTimerTimeCache(self, endT, default=()):
        return self.getDatetimeTimerDataTimeCache().get(endT, default)

    # endregion

    # region Timer Methods
    def _setDatetimeTimerData(self, timerId, data):
        _datetimeTimerProp = self.fetchDatetimeTimerProp()
        if timerId in _datetimeTimerProp:
            gameengine.panicStack(f"{self.__class__.__name__}::_setDatetimeTimerData:: timerId already exists!!!",
                                      timerId, data, _datetimeTimerProp[timerId])

        if not (hasattr(self, 'getTempMiscProp') and self.getTempMiscProp(gameconst.EntityPropsEnum.disableTimerNumErrMsg)) \
                and len(_datetimeTimerProp) >= self.getCallbackNumThreshold():
            gameengine.panicStack(f"{self.__class__.__name__}::_setDatetimeTimerData:: too many callbacks!!!",
                                      timerId, data, len(_datetimeTimerProp), self.IsAvatar, _datetimeTimerProp)

        _datetimeTimerProp[timerId] = data

    def _getDatetimeTimerData(self, timerId, default=None):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        return datetimeTimerProp.get(timerId, default)

    def _hasDatetimeTimerData(self, timerId):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        return timerId in datetimeTimerProp

    def _popDatetimeTimerData(self, timerId, default=None):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        return datetimeTimerProp.pop(timerId, default)

    def _reloadDatetimeTimerData(self):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        for _data in datetimeTimerProp.values():
            _t = _data[1]
            if hasattr(_t, 'reloadScript'):
                _t.reloadScript()
            elif hasattr(_t, '__iter__'):
                for v in _t:
                    if hasattr(v, 'reloadScript'):
                        v.reloadScript()

    def _hasDatetimeTimer(self, timerId):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        return timerId in datetimeTimerProp

    def _datetimeCallback(self, tFire: int, func, args, tag, varTimerID='', **kwargs):
        if not self.datetimePropTimerId:
            gameengine.panicStack(f"{self.__class__.__name__}::_datetimeCallback:: tick timer unregr. !!!",
                                      tFire, func, args, tag, varTimerID, kwargs)
            return 0

        if not func:
            return 0

        if isCell and not self.isReal():
            return 0

        if self.isDestroyed:
            return 0

        if args is None:
            args = ()

        if tFire < utils.curTS():
            getattr(self, func)(*args)
            return 0

        timerId = self._getNextDatetimeTimerId()
        data = DatetimeTimerCallbackDataTup(func, args, varTimerID, tag, math.ceil(tFire))
        self._setDatetimeTimerData(timerId, data)
        self._setDateTimerTimeCache(data.endT, timerId)
        return timerId

    def _cancelDatetimeCallback(self, timerId, tag):
        if not timerId:
            return

        data = self._getDatetimeTimerData(timerId)
        if not data:
            LOG_ERR(f'{self.__class__.__name__}::_cancelDatetimeCallback:: cancel timer timerID not in timerData',
                      timerId, '|', tag, '|', data, self.fetchDatetimeTimerProp())
            for line in traceback.format_stack():
                LOG_ERR(line)
            return

        _, _, _varTimerId, timerTag, _, *_ = data
        if tag not in (gametimer.TIMER_TAG_NONE, timerTag):
            LOG_ERR(f'{self.__class__.__name__}::_cancelDatetimeCallback:: cancel timer mismatch',
                      timerId, '|', tag, '|', data, self.fetchDatetimeTimerProp())
            for line in traceback.format_stack():
                LOG_ERR(line)
            return

        if _varTimerId:
            setattr(self, _varTimerId, 0)

        self._popDatetimeTimerData(timerId)

    def _cancelAllDatetimeCallback(self):
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        for _timerId in list(datetimeTimerProp.keys()):
            self._cancelDatetimeCallback(_timerId, gametimer.TIMER_TAG_NONE)

    def _onTimerDatetimeCallback(self, timerId):
        _data = self._popDatetimeTimerData(timerId)
        if not _data:
            return

        funcName, funcArgs, _varTimerId, _, _, *_ = _data
        if _varTimerId:
            setattr(self, _varTimerId, 0)

        getattr(self, funcName)(*funcArgs)

    def initDatetimeTimerTick(self, start=1):
        tick = self.getDatetimeTimerTickInterval()
        start = random.random() * tick
        if self.datetimePropTimerId:
            gameengine.panicStack(f"{self.__class__.__name__}::initDatetimeTimerTick:: already get timerId!!!",
                                      self.datetimePropTimerId)
            self.pyDelTimer(self.datetimePropTimerId, gametimer.TIMER_DATETIME_ITIMER_CALLBACK)
        self.datetimePropTimerId = self.pyAddTimer(start, tick, gametimer.TIMER_DATETIME_ITIMER_CALLBACK)

    def _onDatetimeTimerTick(self):
        # LOG_ERR("DEBUG:_onDatetimeTimerTick:START:", self.datetimePropTimerDataNextT)
        now = utils.curTS()
        datetimeTimerProp = self.fetchDatetimeTimerProp()
        datetimeTimerTimeCache = self.getDatetimeTimerDataTimeCache()

        if self.datetimePropTimerDataNextT <= 0 and datetimeTimerTimeCache:
            self.datetimePropTimerDataNextT = min(datetimeTimerTimeCache)

        _depth, _depthAlert = 0, 60 * 10
        while 0 < self.datetimePropTimerDataNextT < now and _depth < _depthAlert:
            _thisEndT = self.datetimePropTimerDataNextT
            _timerIdList = self._getDateTimerTimeCache(_thisEndT)
            for _timerId in _timerIdList:
                if not self._hasDatetimeTimerData(_timerId):
                    continue
                _data = self._getDatetimeTimerData(_timerId)
                if not _data:
                    self._popDatetimeTimerData(_timerId)
                    continue
                if _data.endT != _thisEndT:
                    continue
                self._onTimerDatetimeCallback(_timerId)
                _depth += 1

            self._popDateTimerTimeCache(_thisEndT)
            self.datetimePropTimerDataNextT = min(datetimeTimerTimeCache) if datetimeTimerTimeCache else 0

        if _depth >= _depthAlert:
            gameengine.panicStack(f"{self.__class__.__name__}::_onDatetimeTimerTick:: timerId depth alert!!!",
                                      _depth, _depthAlert, self.datetimePropTimerDataNextT, now,
                                      now - self.datetimePropTimerDataNextT, len(datetimeTimerProp))
    # endregion


class ITimer(DatetimeTimerMixin):
    def _setTimerData(self, timerID, data):
        _timerProp = getattr(self, TIMER_DATA_PROP)
        if timerID in _timerProp:
            gameengine.panicStack('timer id already exists!!!', timerID, data, _timerProp[timerID])

        if len(_timerProp) >= gameconfig.callbackNumThreshold():
            if not hasattr(self, 'getTempMiscProp') or not hasattr(self, 'setTempMiscProp'):
                gameengine.panicStack('too many callbacks!!!', self.id, self.__class__.__name__, timerID, data,
                                          len(_timerProp))
            elif not self.getTempMiscProp(gameconst.EntityPropsEnum.disableTimerNumErrMsg) and self.getTempMiscProp(
                    gameconst.EntityPropsEnum.timerNumErrMsgTS, 0) < utils.curTS():
                self.setTempMiscProp(gameconst.EntityPropsEnum.timerNumErrMsgTS, utils.curTS() + 1800)

                _num = 0
                funcDic = {}
                for k, v in _timerProp.items():
                    _num += 1
                    funcDic[v[0]] = funcDic.get(v[0], 0) + 1
                    if _num > 200:
                        break

                _funcList = sorted([(v, k) for k, v in funcDic.items()], reverse=True)
                gameengine.panicStack('too many callbacks!!!', self.id, self.__class__.__name__, timerID, data,
                                          len(_timerProp), _funcList[:5])

        _timerProp[timerID] = data

    def __getTimerData(self, timerID):
        timerProp = getattr(self, TIMER_DATA_PROP)
        return timerProp.get(timerID, None)

    def __popTimerData(self, timerID):
        timerProp = getattr(self, TIMER_DATA_PROP)
        return timerProp.pop(timerID, None)

    def _reloadTimerData(self):
        timerProp = getattr(self, TIMER_DATA_PROP)
        for data in timerProp.values():
            _t = data[1]
            if hasattr(_t, 'reloadScript'):
                _t.reloadScript()
            elif hasattr(_t, '__iter__'):
                for _v in _t:
                    if hasattr(_v, 'reloadScript'):
                        _v.reloadScript()

    def postReloadScript(self):
        self._reloadTimerData()
        self._reloadDatetimeTimerData()
        if hasattr(super(ITimer, self), 'postReloadScript'):
            super(ITimer, self).postReloadScript()

    def _hasTimer(self, timerID):
        timerProp = getattr(self, TIMER_DATA_PROP)
        return timerID in timerProp

    def addTimerCB(self, t, func, args, tag, varTimerID='', clearTimerIdFunc='', clearTimerIdArgs=()):
        if not utils.isBelongTimerTag(tag):
            gameengine.panicStack('callback tag error', tag)
            return 0

        if not func:
            return 0

        if isCell and not self.isReal():
            return 0

        if self.isDestroyed:
            return 0

        if args == None:
            args = ()

        if t < 0:
            traceback.print_stack()

        timerId = self.addTimer(t, 0, tag)

        self._setTimerData(timerId, (func, args, varTimerID, tag, clearTimerIdFunc, clearTimerIdArgs))

        return timerId

    def flowControllerDelayExecEventCallback(self, delayEvent, context):
        delayEvent.handleBeTriggeredAfterDelay(context)

    def asyncCallbackAfter(self, delay, tag=gametimer.TIMER_TAG_NONE, fnName='', varTimeID=''):
        """Usage: tid = self.callbackFun(t, tid).yourOwnFunction(args1, args2, ...)"""
        return _CallbackCalled(delay, varTimeID, fnName, tag, self)

    def flowControllerDelayCallback(self, delayEvent, cbFuncName, cbArgs, cbKwArgs):
        getattr(delayEvent, cbFuncName)(*cbArgs, **cbKwArgs)

    def cancelTimerCB(self, timerID, tag):
        if not timerID:
            return gameconst.TIMER_CANCEL_RET_ZERO_TIMER

        data = self.__getTimerData(timerID)
        if not data:
            return gameconst.TIMER_CANCEL_RET_NOT_DATA

        if self.isDestroyed:
            return gameconst.TIMER_CANCEL_RET_DESTROY

        if len(data) < 6:
            return gameconst.TIMER_CANCEL_ARG_INVALID

        funcName, funcArgs, varTimerId, timerTag, _clearTimerIdFunc, clearTimerIdArgs = data
        if tag != gametimer.TIMER_TAG_NONE and tag != timerTag:
            LOG_ERR('cancel timer mismatch', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                LOG_ERR(line)
            return gameconst.TIMER_CANCEL_RET_MISMATCH
        else:
            self.__popTimerData(timerID)

        # varTimerId = data[2]
        if varTimerId:
            setattr(self, varTimerId, 0)

        if _clearTimerIdFunc:
            getattr(self, _clearTimerIdFunc)(*clearTimerIdArgs)

        if self.delTimer(timerID) < 0:
            LOG_ERR('invalid timerId', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                LOG_ERR(line)

        return gameconst.TIMER_CANCEL_RET_SUCCESS

    def _cancelAllCallbacks(self):
        timerProp = getattr(self, TIMER_DATA_PROP)
        for timerId in list(timerProp.keys()):
            self.cancelTimerCB(timerId, gametimer.TIMER_TAG_NONE)

    def _onTimerCallback(self, timerID):
        _data = self.__popTimerData(timerID)
        if _data == None:
            return

        funcName, funcArgs, _varTimerId, tag, _clearTimerIdFunc, clearTimerIdArgs = _data
        if _varTimerId:
            setattr(self, _varTimerId, 0)

        if _clearTimerIdFunc:
            getattr(self, _clearTimerIdFunc)(*clearTimerIdArgs)

        getattr(self, funcName)(*funcArgs)

    def _onTimerTrigger(self, timerID, userData):
        if not utils.isBelongTimerTag(userData):
            data = self.__getTimerData(timerID)
            if data:
                _, interval, _, _ = data
                if interval == 0:
                    self.__popTimerData(timerID)

    def pyAddTimer(self, start, interval, userData):
        if not utils.isBelongTimerIdTag(userData):
            gameengine.panicStack('pyAddTimer wrong userData range', userData)

        _timerId = self.addTimer(start, interval, userData)
        self._setTimerData(_timerId, ('', interval, '', userData))
        return _timerId

    def pyDelTimer(self, timerID, tag):
        if not timerID:
            return

        data = self.__popTimerData(timerID)
        if not data:
            LOG_ERR('pyDelTimer timerID not exist', timerID, '|', tag)
            return

        if self.isDestroyed:
            return

        if tag != data[3]:
            LOG_ERR('pyDelTimer mismatch', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                LOG_ERR(line)
            return

        if self.delTimer(timerID) < 0:
            LOG_ERR('pyDelTimer invalid timerID', timerID, '|', tag, '|', data, self.getControllers())
            for line in traceback.format_stack():
                LOG_ERR(line)

    def clearTimerId(self, obj, funcName, funcArgs):
        if obj:
            getattr(obj, funcName)(*funcArgs)


class _CallbackCalled(object):
    def __init__(self, t, tid, fnName, tag, owner: ITimer):
        self.varTimeID = tid
        self.delayTime = t
        self.fnName = fnName
        self.owner = owner
        self.tag = tag

    def __call__(self, *args):
        if not self.fnName:
            raise TypeError("special function name '{}' {} not define".format(self.fnName, self.tag))
        return self.owner.addTimerCB(self.delayTime, self.fnName, args, self.tag, self.varTimeID)

    def __getattr__(self, funcName):
        if self.fnName and funcName != self.fnName:
            raise TypeError("'{}' {} must be called as special".format(self.fnName, self.tag))
        if not hasattr(self.owner, funcName):
            raise AttributeError("'{0}' object has no attribute '{1}'".format(self.owner.__class__.__name__, funcName))
        _fn = getattr(self.owner, funcName)
        if not callable(_fn):
            raise TypeError("'{}' object is not callable".format(type(_fn).__name__))
        return lambda *args: self.owner.addTimerCB(self.delayTime, funcName, args, self.tag,
                                                  varTimerID=self.varTimeID)
