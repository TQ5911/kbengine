import KBEngine
from KBEDebug import *
from RebornPosBase import RebornPosBase

class RebornPos(RebornPosBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("RebornPos::__init__")

