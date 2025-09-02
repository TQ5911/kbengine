import KBEngine
from KBEDebug import *
from DuelFlagBase import DuelFlagBase


class DuelFlag(DuelFlagBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("DuelFlag::__init__")
