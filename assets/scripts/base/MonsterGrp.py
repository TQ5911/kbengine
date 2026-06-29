# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gametimer
import gameconst

import iBaseWithCell
import iFubenSpace
import iTimer
import utils

import creep_group as CRG


class MonsterGrp(iBaseWithCell.IBaseWithCell, iFubenSpace.IFubenSpace,
                 iTimer.ITimer):
    """deprecated"""
    def __init__(self, **args):
        super(MonsterGrp, self).__init__()

    def onLoseCell(self, reason=gameconst.OnLoseCellReasonEnum.DEFAULT):
        pass

    def onTimer(self, tid, userArg):
        pass
