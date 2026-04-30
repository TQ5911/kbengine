#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division

import copy

from .gragh import BaseElementGraghBuilder
from .exceptions import EP_ControllerError
from .utils import gen_uuid
from .context import BaseContext


class Controller(object):
    """For relationship with Other Event/Variables/Flow, Controller manage
       their action, include trigger/etc. """

    TRIGGER_NODE_START_IDX = 1

    def __init__(self, start_node=None):
        self._variables = {}
        self.elementsDic = {}
        self.waitingsDict = {}
        self._reAwaitCache = {}
        self._start_node = None     # start node must be an event
        start_node and self.add_start_node(start_node)
        self._stopped = False

    @property
    def stopped(self):
        return self._stopped

    def buildElement(self, element_cls, element_id=None, **kwargs):
        element_id = element_id if element_id is not None else gen_uuid()
        return element_cls(element_id, self, **kwargs)

    def add_start_node(self, start_node):
        if self._start_node is not None:
            raise TypeError('Repeated add start node')
        self._start_node = start_node
        start_node._controller = self

    def replace_start_node(self, start_node):
        self._start_node = start_node

    def add_variable(self, var_name, var_value):
        if var_name in self._variables:
            raise EP_ControllerError('Repeated add variable, {}'.format(var_name),
                                     self)
        self._variables[var_name] = var_value

    def set_variable(self, var_name, new_var_value):
        if var_name not in self._variables:
            raise AttributeError('Can\'t find variable, {}'.format(var_name))
        self._variables[var_name] = new_var_value

    def get_variable(self, var_name, default=None):
        return self._variables.get(var_name, default)

    def has_variable(self, var_name):
        return var_name in self._variables

    def trigger_now(self, ctx=None):
        if not self._start_node:
            raise EP_ControllerError(
                'Controller cannot trigger, not start node', self)
        ctx = ctx or BaseContext(tid=gen_uuid())
        self._start_node.trigger_all(self.TRIGGER_NODE_START_IDX, ctx)

    def waitingForTrigger(self, key, e, eCtx):
        self.waitingsDict.setdefault(key, [])
        self.waitingsDict[key].append((e, eCtx))

    def waiting_for_retrigger(self, key, e, eCtx):
        self._reAwaitCache.setdefault(key, [])
        self._reAwaitCache[key].append((e, eCtx))

    def toBeTrigger(self, key):
        if key not in self.waitingsDict:
            return
        events = self.waitingsDict[key]
        copy_events = copy.copy(events)
        events.clear()
        try:
            for e, eCtx in copy_events:
                e.continueHandleBeTriggered(eCtx)
        finally:
            del self.waitingsDict[key]
            if key in self._reAwaitCache:
                for e, eCtx in self._reAwaitCache[key]:
                    self.waitingForTrigger(key, e, eCtx)
                del self._reAwaitCache[key]

    def cancel_trigger_events(self, key, ids=None):
        if key not in self.waitingsDict:
            return
        if not ids:
            del self.waitingsDict[key]
        else:
            _events = self.waitingsDict[key]
            _rm_events = []
            for _idx, (e, _) in enumerate(_events):
                if ids and e.id in ids:
                    _rm_events.append(_idx)

            for _rm_idx in reversed(_rm_events):
                _events.pop(_rm_idx)

    def get_trigger_events(self, key, default=None):
        return self.waitingsDict.get(key, default)

    def check_all(self):
        for _ in self.iter_check_all():
            pass

    def iter_check_all(self):
        for e in self.elementsDic.values():
            yield e.self_check()

    def regr_element(self, e):
        self.elementsDic[e.id] = e

    def unregr_element(self, eid):
        e = self.elementsDic.pop(eid, None)
        if e:
            # remove controller afrer un regr element
            e._controller = None

    def stop_all(self):
        self._stopped = True

    def export_gragh_view(self, fd=None, builder=None):
        builder = builder or BaseElementGraghBuilder()
        results = {}
        for eid, e in self.elementsDic.items():
            name, data, r_binds, r_refs = builder.build(e)
            results[eid] = dict(name=name, data=data,
                                bind_relations=r_binds,
                                ref_relations=r_refs)
        if fd:
            import json
            json.dump(results, fd)
        return results

