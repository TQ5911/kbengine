from KBEDebug import *
import gameengine
import gameconst
import experience_fixedWorldLevel
import utils
import gametimer
class IWorldLevel(object):

    def __init__(self):
        LOG_INFO("IWorldLevel init", self.worldLevel)
        gameengine.getGlobalBase('LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)).getDynamicWorldLevel(self)

    def onGetDynamicWorldLevel(self, dynWorldLevel):
        day = utils.getSvrOpenDays()
        if day in experience_fixedWorldLevel.datas:
            self.worldLevel = experience_fixedWorldLevel.datas[day]['worldLevel']
        else:
            self.worldLevel = max(dynWorldLevel, self.worldLevel)
        LOG_INFO("onGetDynamicWorldLevel", dynWorldLevel, self.worldLevel)
        self.base.updateRoleCache({'worldLevel': self.worldLevel})

    def onWorldLevelDailyUpdate(self):
        self.addTimerCB(120, '_onWorldLevelDailyUpdate', (), gametimer.TIMER_TAG_WORLD_LEVEL_DAILY_UPDATE)

    def _onWorldLevelDailyUpdate(self):
        gameengine.getGlobalBase('LeaderBoardStub' + str(gameconst.LeaderBoardType.AVATAR_LEVEL)).getDynamicWorldLevel(self)