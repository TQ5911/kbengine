# -*- coding: utf-8 -*-
from KBEDebug import *
import KBEngine


import iBaseWithCell
import iSpaceMgr


class DungeonSpaceMgr(iBaseWithCell.IBaseWithCell, iSpaceMgr.ISpaceMgr):
    
    def __init__(self, **kwargs):
        super(DungeonSpaceMgr, self).__init__()

