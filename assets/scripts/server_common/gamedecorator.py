# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import decorator
import functools
import types
import time
import utils
import gameconfig

SERVER_LOAD_LV_NORMAL = 0


def _limitcall(interval, intervalOnHighLoad, bMsg, msgId, keyFunc=None, msgArgs=()):
    if KBEngine.component == 'baseapp':
        def fwrap(f, self, *args, **kwargs):
            if getattr(KBEngine, 'timeProxy', False):
                return f(self, *args, **kwargs)

            now = time.time()

            if not hasattr(self, 'methodPoolBase'):
                self.methodPoolBase = {}

            if intervalOnHighLoad and hasattr(self, 'loadLv') and self.loadLv > SERVER_LOAD_LV_NORMAL:
                _interval = intervalOnHighLoad
            else:
                _interval = interval

            keyName = keyFunc and '%s_%s' % (f.__name__, keyFunc(args)) or f.__name__

            if now > self.methodPoolBase.get(keyName, 0):
                self.methodPoolBase[keyName] = now + _interval
                return f(self, *args, **kwargs)

            if bMsg and msgId and (utils.instanceof(self, 'Avatar') or utils.instanceof(self, 'Account')):
                self.onMessagePre(msgId, list(msgArgs))

            return None

        return fwrap

    elif KBEngine.component == 'cellapp':
        def fwrap(f, self, *args, **kwargs):
            if getattr(KBEngine, 'timeProxy', False):
                return f(self, *args, **kwargs)

            now = time.time()

            if intervalOnHighLoad and hasattr(self, 'loadLv') and self.loadLv > SERVER_LOAD_LV_NORMAL:
                _interval = intervalOnHighLoad
            else:
                _interval = interval

            keyName = keyFunc and '%s_%s' % (f.__name__, keyFunc(args)) or f.__name__

            if now > self.methodPool.get(keyName, 0):
                self.methodPool[keyName] = now + _interval
                return f(self, *args, **kwargs)

            isAvatar = utils.instanceof(self, 'Avatar')
            if not isAvatar:
                caller = KBEngine.entities.get(args[0])
                isCallerAvatar = utils.instanceof(caller, 'Avatar')

            if bMsg and msgId and (isAvatar or isCallerAvatar):
                self.showMsg(msgId, list(msgArgs))

            return None

        return fwrap

    else:
        raise NotImplementedError


def limitcall(interval, bMsg=True, msgId=0, keyFunc=None, msgArgs=()):
    return decorator.decorator(_limitcall(interval, 0, bMsg, msgId, keyFunc=keyFunc, msgArgs=msgArgs))


def _checkTeleportLock(lockReason):
    def fwrap(f, self, *args, **kwargs):
        _now = utils.getNow()
        if self.isTeleportLocked(lockReason, _now):
            WARNING_MSG(
                f"_checkTeleportLock::teleport locked, {lockReason} -> org:{self.teleportLock}, {self.teleportLockRlsT}",
                _now)
            return None
        return f(self, *args, **kwargs)

    return fwrap


def checkTeleportLock(lockReason):
    return decorator.decorator(_checkTeleportLock(lockReason))


def crossServerOnly(fn):
    fn.crossServerCallable = True
    fn.localServerCallable = False

    @functools.wraps(fn)
    def __(self, *args, **kwargs):
        return fn(self, *args, **kwargs)

    return __


def crossServer(fn):
    fn.crossServerCallable = True
    fn.localServerCallable = True

    @functools.wraps(fn)
    def __(self, *args, **kwargs):
        return fn(self, *args, **kwargs)

    return __


def forwardToLocal(fn):
    @functools.wraps(fn)
    def f(self, *args, **kwargs):
        if self.isCrossServer and self.isCrossServerInOtherServer:
            if KBEngine.component == 'cellapp':
                box = self.otherServerAvatarBox.cell
            else:
                box = self.otherServerAvatarBox
            func = getattr(box, fn.__name__)
            return func(*args, **kwargs)
        else:
            return fn(self, *args, **kwargs)

    return f


def forwardToCross(fn):
    @functools.wraps(fn)
    def f(self, *args, **kwargs):
        if self.isCrossServer and self.isCrossServerInLocalServer:
            if KBEngine.component == 'cellapp':
                box = self.otherServerAvatarBox.cell
            else:
                box = self.otherServerAvatarBox
            func = getattr(box, fn.__name__)
            return func(*args, **kwargs)
        else:
            fn(self, *args, **kwargs)

    return f


def offlineCallback(fn):
    fn.offlineCall = True

    @functools.wraps(fn)
    def __(self, *args, **kwargs):
        return fn(self, *args, **kwargs)

    return __


def checkGameconfigEnable(name):
    def f(func):
        @functools.wraps(func)
        def wrapper(*args):
            enableCall = getattr(gameconfig, name)
            if not enableCall or not enableCall():
                WARNING_MSG('gameconfig not enable:', name)
                return
            return func(*args)

        return wrapper

    return f
