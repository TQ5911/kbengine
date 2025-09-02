import KBEngine
from KBEDebug import *
from CityBattleTeleporterBase import CityBattleTeleporterBase


class CityBattleTeleporter(CityBattleTeleporterBase):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        DEBUG_MSG("CityBattleTeleporter::__init__")
