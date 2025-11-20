# coding: utf-8

from KBEDebug import *

import KBEngine
import utils
import buyCredit_buyCreditConst as BCBCCD
import buyCredit_buyCredit as BCBCD
import time
import gameconst
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import gameclass

class IMonthCard(object):
    def __init__(self):
        pass

    def addMonthCardByItem(self, monthCardId, opUUID, ctx):
        self.setPendingUseId(opUUID, ctx)
        self.base.addMonthCardByItem(monthCardId, opUUID, ctx)
        return gameconst.UseItem.PENDING