# coding: utf-8
import gameconst
import actionContext


class IActivityBase(object):
    def activityComplete(self, activityId):
        self.achievementInfo.triggerAchieveByType(
            self, 
            gameconst.AchieveType.ACTIVITY, 
            actionContext.AchievementCtx(activityId=activityId))

