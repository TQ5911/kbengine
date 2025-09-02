import KBEngine
from KBEDebug import *
from CoreAreaFlagBase import CoreAreaFlagBase


class CoreAreaFlag(CoreAreaFlagBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("CoreAreaFlag::__init__")
