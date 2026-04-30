from KBEDebug import *
import gameengine
import gameconst
import experience_fixedWorldLevel
import utils
import gametimer
class IWorldLevel(object):

    def __init__(self):
        LOG_IFO("IWorldLevel init", self.worldLevel)
        gameengine.getGlobalBase('LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)).getDynamicWorldLevel(self)

    def onGetDynamicWorldLevel(self, dynWorldLevel):
        day = utils.getSvrOpenDays()
        day = min(day, experience_fixedWorldLevel.maxKey)
        day = max(day, 1)
        configWorldLevel = experience_fixedWorldLevel.datas[day]['worldLevel']
        worldLevel = max(configWorldLevel, dynWorldLevel)
        self.worldLevel = worldLevel
        LOG_IFO("onGetDynamicWorldLevel", dynWorldLevel, configWorldLevel, worldLevel)

    def onWorldLevelDailyUpdate(self):
        self.addTimerCB(120, '_onWorldLevelDailyUpdate', (), gametimer.TIMER_TAG_WORLD_LEVEL_DAILY_UPDATE)

    def _onWorldLevelDailyUpdate(self):
        gameengine.getGlobalBase('LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)).getDynamicWorldLevel(self)

    