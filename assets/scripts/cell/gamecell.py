# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import gameconst

def loadAirWalls():
    # add barrier tmx info
    try:
        KBEngine.loadAirWalls(gameconst.BARRIER_PATH)
    except AttributeError:
        LOG_ERR('Space:: load air walls failed')
        import traceback
        traceback.print_exc()