# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine

import utils
import userType
import gametimer


class GloalDataCounter(userType.UserSoleType):
    def __init__(self, cd=1):
        self.changeCD = cd
        self.tLastChanged = utils.getNow()
        self.counter = 0
        self.changeTimer = 0

    def _lateReload(self):
        super(GloalDataCounter, self)._lateReload()

        return

    def _setGlobalData(self, owner, globalKey, forceSet=False):
        now = utils.getNow()

        if forceSet or now - self.tLastChanged >= self.changeCD:
            KBEngine.globalData[globalKey] = self.counter
            self.tLastChanged = now
        elif not self.changeTimer:
            self.changeTimer = owner._callback(self.changeCD, 'globalDataCounterCallback',
                                               (self, 'onTimerSetGlobalCounter', (globalKey,)),
                                               gametimer.TIMER_TAG_GLOBALDATA_COUNTER)

    def incCounter(self, owner, globalKey, inc=1):
        self.counter += inc
        self._setGlobalData(owner, globalKey)

    def decCounter(self, owner, globalKey, dec=1):
        self.counter = max(0, self.counter - dec)

        self._setGlobalData(owner, globalKey)

    def setCounter(self, owner, globalKey, num, forceSet=False):
        self.counter = num

        self._setGlobalData(owner, globalKey, forceSet)

    def onTimerSetGlobalCounter(self, globalKey):
        self.changeTimer = 0
        now = utils.getNow()
        if now - self.tLastChanged >= self.changeCD:
            KBEngine.globalData[globalKey] = self.counter
            self.tLastChanged = now
