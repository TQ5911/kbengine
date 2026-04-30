#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 weooh qinzezzhen@outlook.com 
#
# Distributed under terms of the MIT license.
from __future__ import unicode_literals, division


class BaseContext(object):
    def __init__(self, tid=0, **kwargs):
        self.tid = tid      # tid is event triggerd chain id
        self._custom_args = {}
        self._init_others(kwargs)

    def _init_others(self, kwargs):
        if not kwargs:
            return 
        self._custom_args.update(kwargs)
    
    def __getattr__(self, item):
        if item == '_custom_args':
            raise AttributeError
        try:
            return self._custom_args[item]
        except KeyError:
            raise AttributeError("'{}' object has no attribute '{}'".format(
                self.__class__.__name__, item))
    
    def __setattr__(self, item, data):
        if item in ('tid', '_custom_args'):
            super().__setattr__(item, data)
        else:
            self.__dict__['_custom_args'][item] = data


class WaitingEventContext(BaseContext):
    def __init__(self, tid=0, waitingE=None, waitingArgs=None,
                 waitingKwargs=None, **kwargs):
        super().__init__(tid, **kwargs)
        self.waitingE = waitingE
        self.waitingArgs = waitingArgs or ()
        self.waitingKwargs = waitingKwargs or {}
