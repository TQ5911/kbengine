# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine

import utils
import gametimer


class IBase(KBEngine.Entity):
    IsAvatar = False

    @classmethod
    def classname(cls):
        return cls.__name__

    def __init__(self):
        super(IBase, self).__init__()

        self.birthInMem = utils.getNow()

        self.shouldAutoBackup = False

        return

    def preReloadScript(self):
        return

    def reloadScript(self):
        for pName, pVal in self.__dict__.items():
            if pName.startswith('__'):
                continue

            if hasattr(pVal, 'reloadScript'):
                pVal.reloadScript()

        if hasattr(self, 'cellData'):
            for pName, pVal in self.cellData.items():
                if hasattr(pVal, 'reloadScript'):
                    pVal.reloadScript()

        return

    def postReloadScript(self):
        if hasattr(super(IBase, self), 'postReloadScript'):
            super(IBase, self).postReloadScript()

    def isPersistent(self):
        return False

    def entireDestroy(self, deleteFromDB, writeToDB):
        pass

    def renewalBase(self, attr):
        for k, v, in attr.items():
            setattr(self, k, v)

        return

    def callMethod(self, methodName, methodArgs):
        if not hasattr(self, methodName):
            return

        getattr(self, methodName)(*methodArgs)
        return

    def createCellNearSelf(self, baseMailbox):
        baseMailbox.createCellNearHere(self.cell)
        return

    def createCellNearHere(self, cellMailbox):
        try:
            self.createCellEntity(cellMailbox)
        except Exception as e:
            ERROR_MSG('createCellNearHere: fail to create cellEntity', cellMailbox, e)
            self.entireDestroy(False, False)
        return

    def hasArchive(self):
        return self.databaseID != 0

    def _postEntireDestroy(self):
        pass

    def resetLimitcall(self):
        self.methodPoolBase.clear()

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

        self._callback(interval, 'batchlyCall', (it, batchNum, interval, callback), gametimer.TIMER_TAG_BATCHLY_CALL)

    def getCellData(self, key, defaultValue):
        return self.cellData.get(key, defaultValue)

    def setTempMiscProp(self, propId, value):
        if type(propId) is not int:
            return

        self.tempMiscPropsBase[propId] = value

    def getTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.get(propId, default)

    def popTempMiscProp(self, propId, default=None):
        return self.tempMiscPropsBase.pop(propId, default)

    def hasTempMiscProp(self, propId):
        return propId in self.tempMiscPropsBase
