import KBEngine
from KBEDebug import *
from BarrierBase import BarrierBase

class Barrier(BarrierBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("Barrier::__init__")

