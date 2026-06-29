# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import gametimer
import utils


class IBase(KBEngine.Entity):
    IsAvatar = False

    def __init__(self):
        super(IBase, self).__init__()
        self.birthInMem = utils.curTS()
        self.shouldAutoBackup = False

    @classmethod
    def classname(cls):
        return cls.__name__

    def preReloadScript(self):
        pass

    def reloadScript(self):
        for pName, _pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(_pVal, 'reloadScript'):
                _pVal.reloadScript()

        if hasattr(self, 'cellData'):
            for pName, _pVal in self.cellData.items():
                if hasattr(_pVal, 'reloadScript'):
                    _pVal.reloadScript()

    def postReloadScript(self):
        if not hasattr(super(IBase, self), 'postReloadScript'):
            return

        super(IBase, self).postReloadScript()

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        pass

    def isPersistent(self):
        return False

    def renewalBase(self, attr):
        for k, v, in attr.items():
            setattr(self, k, v)

    def callMethod(self, methodName, args):
        if not hasattr(self, methodName):
            return

        getattr(self, methodName)(*args)

    def createCellNearSelf(self, baseMailbox):
        baseMailbox.createCellNearHere(self.cell)

    def createCellNearHere(self, cellMailbox):
        try:
            self.createCellEntity(cellMailbox)
        except Exception as e:
            LOG_ERR('createCellNearHere: fail to create cellEntity', cellMailbox, e)
            self.doEntireDestroy(False, False)

    def hasArchive(self):
        return self.databaseID != 0

    def resetLimitcall(self):
        self.methodPoolBase.clear()

    def _onPostEntireDestroy(self):
        pass

    # 分批次调用，必须继承iTimer
    # 只在base支持，因为cell中_callback参数里不能包含callable
    def batchlyCall(self, iterableCall, batchNum, interval=0.5, callback=None):
        it = iter(iterableCall)
        for i in range(batchNum):
            callObj = next(it, None)
            if callObj is None:
                callback and callback()
                return

            callObj()

        self.addTimerCB(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)

    def setTempMiscProp(self, propId, val):
        if type(propId) is not int:
            return

        self.baseTempMiscProps[propId] = val

    def getCellData(self, key, defaultValue):
        return self.cellData.get(key, defaultValue)

    def popTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.pop(propId, default)

    def getTempMiscProp(self, propId, default=None):
        return self.baseTempMiscProps.get(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.baseTempMiscProps
