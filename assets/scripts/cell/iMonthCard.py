# coding: utf-8

from KBEDebug import *

import gameconst
import gameconfig
import utils

class IMonthCard(object):
    def __init__(self):
        pass

    def addMonthCardByItem(self, monthCardId, opUUID, ctx):
        self.setPendingUseId(opUUID, ctx)
        self.base.addMonthCardByItem(monthCardId, opUUID, ctx)
        return gameconst.UseItemEnum.PENDING

    def syncMonthCardInfo(self, monthCardExpireTime, bigMonthCardExpireTime):
        self.monthCardExpireTimeCell = monthCardExpireTime
        self.bigMonthCardExpireTimeCell = bigMonthCardExpireTime

    def isMonthCardExpiredCell(self):
        if not gameconfig.visibleConfigEnabled('monthCard'):
            return True
        return self.monthCardExpireTimeCell < utils.curTS() and self.bigMonthCardExpireTimeCell < utils.curTS()
    
    def isBigMonthCardExpiredCell(self):
        return self.bigMonthCardExpireTimeCell < utils.curTS()
