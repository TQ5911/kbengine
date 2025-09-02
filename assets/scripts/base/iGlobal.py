# -*- coding: utf-8 -*-
from KBEDebug import *
import gameengine
import gameglobal
import gamebase
import gameconst
import gamesql
import _pickle as cPickle

class IGlobal(object):

    @classmethod
    def classname(cls):
        return cls.__name__

    def onGlobalBase(self, ok, globalName='', recordDbid=False):
        if ok == False:
            print('fail to create base:', self.classname())
            self.entireDestroy(False, False)
            return

        INFO_MSG('onGlobalBase', self.classname(), globalName)
        if globalName:
            gameengine.setGlobalData(globalName, self)
        else:
            gameengine.setGlobalData(self.classname(), self)
        #sgameengine.getGlobalBase('BaseStub').halfPrepare(self.classname())

        self._doRegGlobalBase()

        self.canBeDestroyed = False

        if recordDbid:
            self.writeToDB(self._onWriteToDB)
        return

    #global对象base注册完成后的回调函数
    def _doRegGlobalBase(self):
        pass

    def _onWriteToDB(self, ok, entity):
        DEBUG_MSG('in _onWriteToDB:', entity, entity.databaseID)
        if not ok:
            ERROR_MSG('zt: fail to write DB:',self.classname(), self.id)
        else:
            gamesql.recordEntityDBID(self.classname(), self.databaseID)

    def doNext(self):
        gameglobal.localBaseApp.fullPrepare(self.classname())
        if hasattr(super(), 'doNext'):
            super().doNext()

    def doLast(self):
        pass


