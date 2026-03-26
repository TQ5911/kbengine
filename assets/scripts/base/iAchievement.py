from KBEDebug import *
import KBEngine
import actionContext
import gamedecorator
import gameconst


class IAchievement(object):
    def _sendAchievementInitData(self):
        self.achievementInfo.sendInitDataToClient(self)

    @gamedecorator.checkGameconfigEnable('achievement')
    def takeAchievementRewards(self, exposed, achievementIds):
        INFO_MSG('takeAchievementRewards:', achievementIds)
        self.achievementInfo.takeAllAchievementRewards(achievementIds, self)
    
    def triggerAchievementWithCtx(self, achieveType, ctx):
        self.triggerAchievement(achieveType, ctx)

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


