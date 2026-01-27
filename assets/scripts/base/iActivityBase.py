# coding: utf-8
import gameconst
import cube_config
import actionContext


class IActivityBase(object):
    def activityComplete(self, activityId):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.ACTIVITY,
            actionContext.AchievementCtx(activityId=activityId))

        self.authStatistics.addActTimes(activityId)

        if activityId == cube_config.datas['cubeActID']['value']:
            self.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, cube_config.datas['cubeActID']['value'])



