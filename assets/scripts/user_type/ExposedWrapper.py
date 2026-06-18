# -*- coding: utf-8 -*-
from KBEDebug import *

import ResMgr
import gameglobal

def wrapFunc(f):

    @functools.wraps(f)
    def _wrapper(self, *args, **kwargs):
        msgId = gameglobal.globalBlockExposedFuncName.get(f.__name__, None)
        if msgId is not None:
            if KBEngine.component == 'cellapp':
                self.showMsg(msgId, [])
            else:
                self.onMessagePre(msgId, [])
            return

        if self.isCrossServer and not f.crossServerCallable:
            ERROR_MSG("call func not crossServerCallable in crossServer", f.__name__)
            return

        if not self.isCrossServer and not f.localServerCallable:
            ERROR_MSG("call func not localServerCallable in localServer", f.__name__)
            return

        return f(self, *args, **kwargs)

    return _wrapper

class ExposedWrapperMetaClass(type):
    def __new__(cls, name, bases, attrs):
        exposedMethods = KBEngine.getExposedMethods(name)
        whole = len(exposedMethods)
        count = 0
        for methodName in exposedMethods:
            if methodName in attrs:
                method = attrs[methodName]
                setattr(method, 'crossServerCallable', getattr(method, 'crossServerCallable', False))
                setattr(method, 'localServerCallable', getattr(method, 'localServerCallable', True))
                attrs[methodName] = wrapFunc(method)
                count += 1
            else:
                for baseCls in bases:
                    if hasattr(baseCls, methodName):
                        func = getattr(baseCls, methodName)
                        setattr(func, 'crossServerCallable', getattr(func, 'crossServerCallable', False))
                        setattr(func, 'localServerCallable', getattr(func, 'localServerCallable', True))
                        setattr(baseCls, methodName, wrapFunc(func))
                        count += 1

        WARNING_MSG('meta exposed methods:', name, whole, count)
        return super().__new__(cls, name, bases, attrs)

def getPersistBaseProp(attr):
    def f(self):
        return self.BASE_PROPS[0][attr]

    return f


def setPersistBaseProp(attr):
    def f(self, v):
        self.BASE_PROPS[0][attr] = v

    return f


def getPersistBaseClientProp(attr):
    def f(self):
        return self.BASE_CLIENT_PROPS[0][attr]

    return f


def setPersistBaseClientProp(attr):
    def f(self, v):
        oldVal = self.BASE_CLIENT_PROPS[0][attr]
        self.BASE_CLIENT_PROPS[0][attr] = v

    return f


class AvatarBaseMeta(type):
    def __init__(cls, name, bases, attrs):
        super(AvatarBaseMeta, cls).__init__(name, bases, attrs)
        basePropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'BASE_PROPS_VAL/Properties')
        baseClientPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CLI_BASE_PROPS_VAL/Properties')

        for attr in basePropsDef:
            setattr(cls, attr, property(getPersistBaseProp(attr), setPersistBaseProp(attr)))

        for attr in baseClientPropsDef:
            setattr(cls, attr, property(getPersistBaseClientProp(attr), setPersistBaseClientProp(attr)))


def getPersistCellProp(attr):
    def f(self):
        return self.CELL_PROPS[0][attr]

    return f


def setPersistCellProp(attr):
    def f(self, v):
        self.CELL_PROPS[0][attr] = v

    return f


def getPersistCellClientProp(attr):
    def f(self):
        return self.CELL_CLIENT_PROPS[0][attr]

    return f


def setPersistCellClientProp(attr):
    def f(self, v):
        oldVal = self.CELL_CLIENT_PROPS[0][attr]
        self.CELL_CLIENT_PROPS[0][attr] = v

    return f


class AvatarCellMeta(type):
    def __init__(cls, name, bases, attrs):
        super(AvatarCellMeta, cls).__init__(name, bases, attrs)
        cellPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CELL_PROPS_VAL/Properties')
        cellClientPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CLI_CELL_PROPS_VAL/Properties')

        for attr in cellPropsDef:
            setattr(cls, attr, property(getPersistCellProp(attr), setPersistCellProp(attr)))

        for attr in cellClientPropsDef:
            setattr(cls, attr, property(getPersistCellClientProp(attr), setPersistCellClientProp(attr)))
