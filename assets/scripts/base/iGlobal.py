# -*- coding: utf-8 -*-
from KBEDebug import *
import gameengine
import gameglobal
import gamesql

class IGlobal(object):

    def onGlobalBase(self, ok, globalName='', recordDbid=False):
        if ok == False:
            LOG_WARN('fail to create base:', self.classname())
            self.doEntireDestroy(False, False)
            return

        LOG_INFO('onGlobalBase', globalName, self.classname())
        if globalName:
            gameengine.setGlobalData(globalName, self)
        else:
            gameengine.setGlobalData(self.classname(), self)

        self.canBeDestroyed = False

        if recordDbid:
            self.writeToDB(self._onWriteToDB)

    @classmethod
    def classname(cls):
        return cls.__name__

    def _onWriteToDB(self, ok, entity):
        LOG_DBG('in _onWriteToDB:', entity, entity.databaseID)
        if not ok:
            LOG_ERR('zt: fail to write DB:', self.id, self.classname())
        else:
            gamesql.recordEntityDBID(self.classname(), self.databaseID)

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        if hasattr(super(), 'doNext'):
            super().doNext()

    def doLast(self):
        pass


