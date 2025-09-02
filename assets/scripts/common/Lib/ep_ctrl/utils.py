#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division
from functools import wraps
from uuid import uuid1


def __empty_fun(*args, **kwargs):
    """empty function deosn't return anything"""


def __base_event_trigger_fun(self, src_e, obj, **kwargs):
    self.trigger_all(1, obj)


EMPTY_FUNC = __empty_fun
BASE_EVENT_TRIGGER_FUNC = __base_event_trigger_fun


def api_need_implement(fn):
    @wraps(fn)
    def _wrapper(*args, **kwargs):
        raise NotImplementedError('{} must be implement'.format(fn.__name__))
    return _wrapper


def gen_uuid():
    return int(uuid1())