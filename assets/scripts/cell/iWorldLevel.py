from KBEDebug import *
import utils
import gametimer

class IWorldLevel(object):

    def __init__(self):
        self._syncWorldLevelFromGlobal()

    def _syncWorldLevelFromGlobal(self):
        worldLevel = utils.getWorldLevel()
        LOG_INFO("syncWorldLevelFromGlobal", self.worldLevel, worldLevel)
        self.worldLevel = worldLevel
        self.base.updateRoleCache({'worldLevel': worldLevel})

    def onGetDynamicWorldLevel(self, dynWorldLevel):
        LOG_INFO("onGetDynamicWorldLevel", dynWorldLevel, self.worldLevel)
        self._syncWorldLevelFromGlobal()

    def onWorldLevelDailyUpdate(self):
        self.addTimerCB(120, '_onWorldLevelDailyUpdate', (), gametimer.TIMER_TAG_WORLD_LEVEL_DAILY_UPDATE)

    def _onWorldLevelDailyUpdate(self):
        self._syncWorldLevelFromGlobal()
