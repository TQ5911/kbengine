# coding: utf-8
import gameconst
import cube_config
import actionContext
import wonderLand_config as WL_CD


class IActivityBase(object):
    def activityComplete(self, activityId):
        self.achievementInfo.triggerAchieveByType(
            self,
            gameconst.AchieveType.ACTIVITY,
            actionContext.AchievementCtx(activityId=activityId))

        self.authStatistics.addActTimes(activityId)

        if activityId == cube_config.datas['cubeActID']['value']:
            self.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, cube_config.datas['cubeActID']['value'])

        elif activityId == WL_CD.datas['wonderLandActID']['value']:
            self.completeGuildTask(gameconst.GuildTaskType.ENTERMAP, WL_CD.datas['wonderLandActID']['value'])



