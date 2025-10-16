from KBEDebug import *
import KBEngine
import actionContext
import gameconst


class IAchievement(object):
    def _sendAchievementInitData(self):
        self.achievementInfo.sendInitDataToClient(self)

    def takeAchievementRewards(self, exposed, achievementIds):
        INFO_MSG('takeAchievementRewards:', achievementIds)
        self.achievementInfo.takeAllAchievementRewards(achievementIds, self)

    def triggerAchievement(self, achieveType, ctx=None):
        ctx = ctx or actionContext.AchievementCtx()
        self.achievementInfo.triggerAchieveByType(
            self,
            achieveType,
            ctx)

    def _checkAchieveDailyRefresh(self, *args):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.LOGIN_DAYS,
            actionContext.AchievementCtx())


