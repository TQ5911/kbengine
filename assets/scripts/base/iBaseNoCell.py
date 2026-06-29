# -*- coding: utf-8 -*-
from KBEDebug import *
import iBase


class IBaseNoCell(iBase.IBase):

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return

        self._onPreEntireDestroy()
        self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)
        self._onPostEntireDestroy()

    def _onPreEntireDestroy(self):
        print('sdfsfsdf')

    def _onPostEntireDestroy(self):
        pass

    def globalDataSumCallback(self, obj, callbackName, args):
        func = getattr(obj, callbackName, None)
        if not func:
            LOG_ERR('globalDataSumCallback ')
            return
        func(*args)
