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

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        self.trigger_all(self.EVENT_BIND_IDX, obj)


class RandomEvent(BaseEvent):

    def __init__(self, event_id, controller, event_handler=None,
                 probability=None, prec=2, **kwargs):
        """Random Choosen Event

        :param event_id: element id
        :type event_id: int
        :param controller: element controller
        :type controller: Controller
        :param event_handler: event handler function, defaults to None
        :type event_handler: object, optional
        :param probability: random probability define, defaults to None
        :type probability: dict[element_id:int,probability:float], optional
        """
        super().__init__(event_id, controller, event_handler=event_handler,
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

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        eid = self._choose_random_element()
        self.trigger_all(eid, obj)


class BaseDelayedEvent(BaseEvent, OverOneTickMixin):

    def __init__(self, event_id, controller, event_handler=None,
                 delay_time=0, **kwargs):
        super().__init__(event_id, controller, event_handler=event_handler,
                         **kwargs)
        self._delay_time = delay_time

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        self.next(obj, **ref_params)

    def handle_be_triggered_after_delay(self, obj):
        self.trigger_all(self.EVENT_BIND_IDX, obj)


class BaseWaitingEvent(BaseEvent):

    def get_waiting_key(self, ctx):
        return self.__class__.__name__

    def handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = WaitingEventContext(obj.tid, waiting_e=self,
                                  waiting_args=_w_args,
                                  waiting_kwargs=_w_kwargs)
        key = self.get_waiting_key(obj)
        self._controller.waiting_for_trigger(key, self, ctx)

    def re_handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        _w_args = (src_e, src_idx, idx, obj)
        _w_kwargs = ref_params
        ctx = WaitingEventContext(obj.tid, waiting_e=self,
                                  waiting_args=_w_args,
                                  waiting_kwargs=_w_kwargs)
        key = self.get_waiting_key(obj)
        self._controller.waiting_for_retrigger(key, self, ctx)

    def continue_handle_be_triggered(self, ctx):
        self._con_handle_be_triggered(*ctx.waiting_args, **ctx.waiting_kwargs)

    def _con_handle_be_triggered(self, src_e, src_idx, idx, obj, **ref_params):
        super().handle_be_triggered(src_e, src_idx, idx, obj, **ref_params)
        self.trigger_all(self.EVENT_BIND_IDX, obj)
