# -*- encoding:utf-8 -*-
import gameengine
import gameglobal
from KBEDebug import *
import KBEngine

import utils
import userType
import gametimer

DATA_GLOBAL = 1
DATA_BASEAPP = 2


# TOOD x: sync dataSum after baseapp crash&recover
class GloalDataSum(userType.UserSingleType):
    def __init__(self, globalKey, registerFunc, dataType, cd=1):
        self.changeCD = cd
        self.tLastChanged = utils.curTS()
        self.dataSum = 0
        self.delta = 0
        self.changeTimer = 0
        self.dataType = dataType
        self.globalKey = globalKey

        self.registerGlobalDataCB(registerFunc)

    def _lateReload(self):
        super(GloalDataSum, self)._lateReload()

        return

    def registerGlobalDataCB(self, registerFunc):
        registerFunc(self.globalKey, self.onGetDataIncrement)

    def _setGlobalData(self, owner, forceSet=False):
        now = utils.curTS()

        if forceSet or now - self.tLastChanged >= self.changeCD:
            self._doSetData(self.globalKey, self.delta)
            self.delta = 0
            self.tLastChanged = now
        elif not self.changeTimer:
            self.changeTimer = owner.addTimerCB(self.changeCD, 'globalDataSumCallback',
                                               (self, 'onTimerSetGlobalSum', ()), gametimer.TIMER_TAG_GLOBALDATA_SUM)

    def onGetDataIncrement(self, delta):
        self.dataSum = max(self.dataSum + delta, 0)

    def incSum(self, owner, inc=1):
        self.delta += inc
        self._setGlobalData(owner)

    def decSum(self, owner, dec=1):
        self.delta -= dec

        self._setGlobalData(owner)

    def setSum(self, owner, num, forceSet=False):
        self.dataSum = num

    def _doSetData(self, key, val):
        if self.dataType == DATA_GLOBAL:
            LOG_ERR('GloalDataSum: global sum. todo...')
        elif self.dataType == DATA_BASEAPP:
            gameengine.broadcastBaseapp('onBaseappSumIncrement', (key, val))
        else:
            LOG_ERR('GloalDataSum: unsupported data type', self.dataType, self.globalKey)

    def onTimerSetGlobalSum(self):
        self.changeTimer = 0
        now = utils.curTS()
        if now - self.tLastChanged >= self.changeCD:
            self._doSetData(self.globalKey, self.delta)
            self.delta = 0
            self.tLastChanged = now
