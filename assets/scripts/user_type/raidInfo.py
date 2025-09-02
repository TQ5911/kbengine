# coding: utf-8
from KBEDebug import *
import KBEngine

import userType
import raid


class RaidValInfo(userType.UserSTDSoleInfo):

    @property
    def cls(self):
        return raid.RaidVal


class PlayerRaidCacheValInfo(userType.UserSTDSoleInfo):

    @property
    def cls(self):
        return raid.PlayerRaidCacheVal


# raid info in raidStub
raidValInstance = RaidValInfo()
# raid cache info in player
playerRaidCacheValInstance = PlayerRaidCacheValInfo()