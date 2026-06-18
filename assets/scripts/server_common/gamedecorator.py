# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import decorator
import functools
import types
import time
import utils
import gameconfig

import visible_visible as UVVD
import const_const as C_CD

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

            if bMsg and msgId and (utils.isinstanceof(self, 'Avatar') or utils.isinstanceof(self, 'Account')):
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

            isAvatar = utils.isinstanceof(self, 'Avatar')
            if not isAvatar:
                caller = KBEngine.entities.get(args[0])
                isCallerAvatar = utils.isinstanceof(caller, 'Avatar')

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
        _now = utils.curTS()
        if self.isTeleportLocked(lockReason, _now):
            LOG_WARN(
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

def doCheckGameConfig(avatar, name, needMsg = True):
    info = gameconfig.CONFIG.get(name)
    if not info:
        LOG_ERR('gameconfig not found: 1', name)
        return False
    configName, convFunc, default, defaultV, desc, cid, flags = info
    v = KBEngine.globalData['CONFIG'][configName]
    if not v:
        if KBEngine.component == 'cellapp':
            avatar.showMsg(C_CD.datas['systemSwitch']['value'], [])
        else:
            avatar.onMessagePre(C_CD.datas['systemSwitch']['value'], [])
        #LOG_WARN('gameconfig not enable: 2', name)
        return False
    
    # 检查是否存在主从系统开关
    mainSwitch = UVVD.typeToMain.get(name)
    if mainSwitch:
        if name != mainSwitch:
            info = gameconfig.CONFIG.get(mainSwitch)
            if not info:
                LOG_ERR('gameconfig not found: 3', mainSwitch)
                return False
            configName, convFunc, default, defaultV, desc, cid, flags = info
            v = KBEngine.globalData['CONFIG'][configName]
            if not v:
                LOG_WARN('gameconfig not enable: 4', name)
                return False
    return True

def checkGameconfigEnable(name):
    def f(func):
        @functools.wraps(func)
        def wrapper(*args):
            if doCheckGameConfig(args[0], name):
                return func(*args)

        return wrapper

    return f


def prevent_instance_reentry(method):
    """
    实例级方法防重入装饰器（无锁，轻量）
    本函数慎用，因为会影响返回值结果
    主要是防止一些递归调用中的重入情况
    如果你的函数希望递归就不要用了
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        attr = f"_reentry_flag_{method.__name__}"
        if getattr(self, attr, False):
            LOG_DBG(f"[重入拦截] {method.__name__} 正在执行，跳过")
            return None
        setattr(self, attr, True)
        try:
            return method(self, *args, **kwargs)
        finally:
            setattr(self, attr, False)
    return wrapper


def teleportInQueue(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.teleportInfoDict:
            LOG_WARN(f"{f.__name__}::teleportInQueue::teleporting, skip")
            self.teleportQueue.append((
                f.__name__,
                args,
                kwargs
            ))
            return

        return f(self, *args, **kwargs)

    return wrapper


_doubleTeleportEnable = False
_doubleTeleportSet = set()
_doubleTeleportQueue = []
def testDoubleTeleport(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if not _doubleTeleportEnable:
            return f(self, *args, **kwargs)

        if f.__name__ in _doubleTeleportSet:
            return f(self, *args, **kwargs)

        _doubleTeleportSet.add(f.__name__)

        if _doubleTeleportQueue:
            while _doubleTeleportQueue:
                _func, _args, _kwargs = _doubleTeleportQueue.pop(0)
                getattr(self, _func)(*_args, **_kwargs)

            return f(self, *args, **kwargs)

        else:
            _doubleTeleportQueue.append((
                f.__name__,
                args,
                kwargs
            ))
            return

    return wrapper
