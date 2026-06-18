# -*- coding: utf-8 -*-
from KBEDebug import *
import iBase


class IBaseNoCell(iBase.IBase):

    def doEntireDestroy(self, deleteFromDB, writeToDB):
        if self.isDestroyed:
            return

        self._preEntireDestroy()

        self.destroy(deleteFromDB=deleteFromDB, writeToDB=writeToDB)

        self._postEntireDestroy()

        return

    def _preEntireDestroy(self):
        print('sdfsfsdf')

    def _postEntireDestroy(self):
        pass

    def globalDataSumCallback(self, obj, callbackName, args):
        func = getattr(obj, callbackName, None)
        if not func:
            LOG_ERR('globalDataSumCallback ')
            return
        func(*args)
