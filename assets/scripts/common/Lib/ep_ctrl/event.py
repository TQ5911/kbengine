#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division
import random

from ._model import BaseEvent, OverOneTickMixin
from .context import WaitingEventContext


class Event(BaseEvent):

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super().handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        self.trigger_all(self.EVENT_BIND_IDX, obj)


class RandomEvent(BaseEvent):

    def __init__(self, eventId, controller, eventHandler=None,
                 probability=None, prec=2, **kwargs):
        """Random Choosen Event

        :param eventId: element id
        :type eventId: int
        :param controller: element controller
        :type controller: Controller
        :param eventHandler: event handler function, defaults to None
        :type eventHandler: object, optional
        :param probability: random probability define, defaults to None
        :type probability: dict[element_id:int,probability:float], optional
        """
        super().__init__(eventId, controller, eventHandler=eventHandler,
                         **kwargs)
        self._prec = int(prec)
        self._probabilities = self._build_probabilities(probability)

    def _build_probabilities(self, probability):
        if not probability:
            return {}
        _probability = dict(probability)
        if round(sum(_probability.values()), self._prec) > 1:
            raise TypeError('probability sum exceed 1')
        return _probability

    def _gen_real_probabilities(self):
        _rp = {}
        _except_eid = []
        _avg_eid = []
        _tmp_p = 0.00
        _total_p = 0.00
        for _eid, _p in self._probabilities.items():
            _ntmp_p = round(min(_tmp_p + _p, 1.00), self._prec)
            _rp[_eid] = (_tmp_p, _ntmp_p)
            _tmp_p = _ntmp_p
            _total_p = round(min(_total_p + _p, 1.00), self._prec)
            _except_eid.append(_eid)

        for _idx, _binded_d in self._binded_dic.items():
            if _idx in _except_eid:
                continue
            _avg_eid.append(_idx)

        if not _avg_eid:
            return _rp

        _lostp = round(
            max((1.00 - _total_p), 0.00), self._prec) / len(_avg_eid)
        if _lostp:
            for _eid in _avg_eid:
                _ntmp_p = round(min(_tmp_p + _lostp, 1.00), self._prec)
                _rp[_eid] = (_tmp_p, _ntmp_p)
                _tmp_p = _ntmp_p

        return _rp

    def _choose_random_element(self):
        _p = random.random()
        for _eid, (_ps, _pe) in self._gen_real_probabilities().items():
            if _ps <= _p <= _pe:
                return _eid
        return random.choice(list(self._binded_dic))

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super().handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        eid = self._choose_random_element()
        self.trigger_all(eid, obj)


class BaseDelayedEvent(BaseEvent, OverOneTickMixin):

    def __init__(self, eventId, controller, eventHandler=None,
                 delay_time=0, **kwargs):
        super().__init__(eventId, controller, eventHandler=eventHandler,
                         **kwargs)
        self._delay_time = delay_time

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        super().handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        self.next(obj, **refParams)

    def handleBeTriggeredAfterDelay(self, obj):
        self.trigger_all(self.EVENT_BIND_IDX, obj)


class BaseAwaitEvent(BaseEvent):

    def fetchWaitingKey(self, ctx):
        return self.__class__.__name__

    def handleProcessActivated(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = WaitingEventContext(obj.tid, waitingE=self,
                                  waitingArgs=_w_args,
                                  waitingKwargs=_w_kwargs)
        key = self.fetchWaitingKey(obj)
        self._controller.waitingForTrigger(key, self, ctx)

    def reHandleBeTriggered(self, srcE, srcIdx, idx, obj, **refParams):
        _w_args = (srcE, srcIdx, idx, obj)
        _w_kwargs = refParams
        ctx = WaitingEventContext(obj.tid, waitingE=self,
                                  waitingArgs=_w_args,
                                  waitingKwargs=_w_kwargs)
        key = self.fetchWaitingKey(obj)
        self._controller.waiting_for_retrigger(key, self, ctx)

    def continueHandleBeTriggered(self, ctx):
        self._con_handle_be_triggered(*ctx.waitingArgs, **ctx.waitingKwargs)

    def _con_handle_be_triggered(self, srcE, srcIdx, idx, obj, **refParams):
        super().handleProcessActivated(srcE, srcIdx, idx, obj, **refParams)
        self.trigger_all(self.EVENT_BIND_IDX, obj)
