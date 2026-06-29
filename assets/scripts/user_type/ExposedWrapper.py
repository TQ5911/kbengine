# -*- coding: utf-8 -*-
from KBEDebug import *

import functools
import ResMgr
import gameglobal

def wrapFunc(targetFunc):

    @functools.wraps(targetFunc)
    def _wrapper(self, *args, **kwargs):
        _msgId = gameglobal.globalBlockExposedFuncName.get(targetFunc.__name__, None)
        if _msgId is not None:
            if KBEngine.component == 'cellapp':
                self.showMsg(_msgId, [])
            else:
                self.onMessagePre(_msgId, [])
            return

        if self.isCrossServer and not targetFunc.crossServerCallable:
            ERROR_MSG("call func not crossServerCallable in crossServer", targetFunc.__name__)
            return

        if not self.isCrossServer and not targetFunc.localServerCallable:
            ERROR_MSG("call func not localServerCallable in localServer", targetFunc.__name__)
            return

        return targetFunc(self, *args, **kwargs)

    return _wrapper

class ExposedWrapperMetaClass(type):
    def __new__(cls, name, bases, attrs):
        _exposedMethods = KBEngine.getExposedMethods(name)
        _whole = len(_exposedMethods)
        _count = 0
        for methodName in _exposedMethods:
            if methodName in attrs:
                _method = attrs[methodName]
                setattr(_method, 'crossServerCallable', getattr(_method, 'crossServerCallable', False))
                setattr(_method, 'localServerCallable', getattr(_method, 'localServerCallable', True))
                attrs[methodName] = wrapFunc(_method)
                _count += 1
            else:
                for _baseCls in bases:
                    if hasattr(_baseCls, methodName):
                        func = getattr(_baseCls, methodName)
                        setattr(func, 'crossServerCallable', getattr(func, 'crossServerCallable', False))
                        setattr(func, 'localServerCallable', getattr(func, 'localServerCallable', True))
                        setattr(_baseCls, methodName, wrapFunc(func))
                        _count += 1

        WARNING_MSG('meta exposed methods:', name, _whole, _count)
        return super().__new__(cls, name, bases, attrs)

def setPersistBaseProp(attr):
    def innerFunc(self, v):
        self.BASE_PROPS[0][attr] = v

    return innerFunc


def getPersistBaseProp(attr):
    def innerFunc(self):
        return self.BASE_PROPS[0][attr]

    return innerFunc


def setPersistBaseClientProp(attr):
    def innerFunc(self, v):
        self.BASE_CLIENT_PROPS[0][attr] = v

    return innerFunc


def getPersistBaseClientProp(attr):
    def innerFunc(self):
        return self.BASE_CLIENT_PROPS[0][attr]

    return innerFunc


class AvatarBaseMeta(type):
    def __init__(cls, name, bases, attrs):
        super(AvatarBaseMeta, cls).__init__(name, bases, attrs)
        _basePropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'BASE_PROPS_VAL/Properties')
        _baseClientPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CLI_BASE_PROPS_VAL/Properties')

        for attr in _basePropsDef:
            setattr(cls, attr, property(getPersistBaseProp(attr), setPersistBaseProp(attr)))

        for attr in _baseClientPropsDef:
            setattr(cls, attr, property(getPersistBaseClientProp(attr), setPersistBaseClientProp(attr)))


def setPersistCellProp(attr):
    def innerFunc(self, v):
        self.CELL_PROPS[0][attr] = v

    return innerFunc


def getPersistCellProp(attr):
    def innerFunc(self):
        return self.CELL_PROPS[0][attr]

    return innerFunc


def getPersistCellClientProp(attr):
    def innerFunc(self):
        return self.CELL_CLIENT_PROPS[0][attr]

    return innerFunc


def setPersistCellClientProp(attr):
    def innerFunc(self, v):
        self.CELL_CLIENT_PROPS[0][attr] = v

    return innerFunc


class AvatarCellMeta(type):
    def __init__(cls, name, bases, attrs):
        super(AvatarCellMeta, cls).__init__(name, bases, attrs)
        _cellPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CELL_PROPS_VAL/Properties')
        _cellClientPropsDef = ResMgr.getChildrenName(ResMgr.entityDefTypes(), 'CLI_CELL_PROPS_VAL/Properties')

        for attr in _cellPropsDef:
            setattr(cls, attr, property(getPersistCellProp(attr), setPersistCellProp(attr)))

        for attr in _cellClientPropsDef:
            setattr(cls, attr, property(getPersistCellClientProp(attr), setPersistCellClientProp(attr)))
