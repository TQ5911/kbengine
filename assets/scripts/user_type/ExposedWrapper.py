# -*- coding: utf-8 -*-
from KBEDebug import *

import ResMgr


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
        if self.client and oldVal != v:
            self.client.onBasePersistPropChanged(attr, str(v))

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
        if self.client and oldVal != v:
            self.client.onCellPersistPropChanged(attr, str(v))

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
