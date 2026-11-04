from KBEDebug import *
import KBEngine
import actionContext
import gamedecorator
import gameconst
import MapExploreInfo
import gamePlay_explorationRate as GED
import gamePlay_explorationReward as GER
import gameclass
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
import dropAward
import message_Message_def as M_M_DD
import LogTrackingMgr
import gameconfig
import antiAddictCategory_antiAddictCategory_def as AAC_AAC_DD

class IAchievement(object):
    def __init__(self):
        self.mapExploreInfo.checkNewMapExploreData()

    def _sendAchievementInitData(self):
        self.achievementInfo.sendInitDataToClient(self)

    @gamedecorator.checkGameconfigEnable('achievement')
    @gamedecorator.crossServer
    def takeAchievementRewards(self, exposed, achievementIds):
        LOG_INFO('takeAchievementRewards:', achievementIds)
        if gameconfig.isCrossServer():
            self.syncMethodCallToLocalServerBase('_takeAchievementRewards', (achievementIds,))
        else:
            self._takeAchievementRewards(achievementIds)

    def _takeAchievementRewards(self, achievementIds):
        self.achievementInfo.takeAllAchievementRewards(achievementIds, self)
        self.syncMethodCallToCrossServerBase('_takeAchievementRewards', (achievementIds,))

    #本服获取完成就奖励，同步给跨服
    def _onLocalServerTakeAllAchievementRewards(self, crossServerPack, popRewardUUID, _takeIds, sumPoint):
        LOG_INFO('onLocalServerTakeAllAchievementRewards:', crossServerPack, popRewardUUID, _takeIds, sumPoint)
        for _awardVal, _opUUID, _detail in crossServerPack:
            self.addWealth(AAC_AAC_DD.datas.BONUS_SRC_ACHIEVEMENT, _awardVal, _opUUID, _detail, directly=False)
        self._showPopReward(AAC_AAC_DD.datas.BONUS_SRC_ACHIEVEMENT, popRewardUUID, gameclass.AwardDetailCls(achievementId=_takeIds))
        self.client.onTakeAchievementRewards(_takeIds, sumPoint)

    def onCrossServerTriggerAchieveByType(self, achieveType, ctx):
        LOG_INFO("onCrossServerTriggerAchieveByType", achieveType, ctx)
        self.triggerAchievement(achieveType, ctx)

    def gmResetAchievement(self, achieveId, resetStep):
        """GM 重置成就项为未完成状态（只回退成就状态，不回收已发奖励）。"""
        ok, errMsg, oldState, oldStep = self.achievementInfo.gmResetAchievement(achieveId, resetStep)
        if not ok:
            return False, errMsg, 0, 0
        LOG_INFO('gmResetAchievement', achieveId, resetStep, oldState, oldStep)
        self.achievementInfo.sendInitDataToClient(self)
        if not gameconfig.isCrossServer():
            self._updateLeaderBoardAvatar()
            LogTrackingMgr.LogTrackingMgr.Achievement_Update(
                self.gbID,
                self.accountEntity.clientDistinctId,
                self.accountEntity.accountName,
                self.gbID,
                gameconfig.gameId(),
                achieveId,
                self.achievementInfo.maxVersion,
                gameconst.ACHIEVE_STATE_GM_RESET,
                oldStep,
                self.achievementInfo.sumPoint
            )
        # 跨服镜像同步（操作回放，镜像不落库；镜像上本方法内的跨服同步为空转）
        self.syncMethodCallToCrossServerBase('gmResetAchievement', (achieveId, resetStep))
        return True, '', oldState, oldStep
    
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

    def triggerMapExplore(self, mapId, tp, num):
        if mapId not in self.mapExploreInfo.mapDatas:
            return

        # 地图探索以策划配置为准：探索表未配置的项目不计入探索度
        pointMap = GED.mapId2Point.get(mapId)
        if not pointMap or tp not in pointMap:
            LOG_INFO("triggerMapExplore skip, not configured:", mapId, tp, num)
            return
        point = pointMap[tp]

        LOG_INFO("before triggerMapExplore:", mapId, tp, num, self.mapExploreInfo.mapDatas[mapId])
        # v5.2 新手历程 3=地图探索次数
        self.beginnerJourney_onTaskEvent(
            gameconst.BjTaskType.BJ_TASK_TYPE_MAP_EXPLORE,
            delta=num * point, mapId=mapId
        )

        mapExploreInfo = self.mapExploreInfo.mapDatas[mapId]
        enum2val = {
            gameconst.AchieveType.PERSONAL_BOX: mapExploreInfo.personalBox,
            gameconst.AchieveType.VIEWPOINT: mapExploreInfo.viewPoint,
            gameconst.AchieveType.HOOK_TASK_REWARD: mapExploreInfo.hookTask,
            gameconst.AchieveType.AREA_TASK: mapExploreInfo.areaTask,
        }
        if enum2val[tp][0] + num > enum2val[tp][1]:
            num = enum2val[tp][1] - enum2val[tp][0]
        if num <= 0:
            LOG_INFO("triggerMapExplore reach max:", mapId, tp, num)
            return
        enum2val[tp][0] += num
        mapExploreInfo.rewardData[0] += num * point

        LOG_INFO("after triggerMapExplore:", mapId, tp, num, self.mapExploreInfo.mapDatas[mapId])
        if tp != gameconst.AchieveType.HOOK_TASK_REWARD:
            self.onMessagePre(M_M_DD.datas.explorationRate, [str(num * point),])
        self.client.onUpdateMapExplore([mapExploreInfo,])

        LogTrackingMgr.LogTrackingMgr.map_exploration(self.gbID, self.accountEntity.clientDistinctId, mapId, tp, mapExploreInfo.rewardData[0], mapExploreInfo.rewardSlot)

    def sendAllMapExploreData(self):
        res = []
        for mapId, mapExploreInfo in self.mapExploreInfo.mapDatas.items():
            res.append(mapExploreInfo)
        LOG_INFO("do sendAllMapExploreData:", len(res))
        self.client.onUpdateMapExplore(res)
        
    def getMapExploreReward(self, exposed, mapId, slot):
        LOG_INFO("getMapExploreReward:", mapId, slot)
        if mapId not in self.mapExploreInfo.mapDatas:
            LOG_ERR("getMapExploreReward: mapId not in mapDatas:", mapId)
            return

        mapExploreInfo = self.mapExploreInfo.mapDatas[mapId]
        if mapExploreInfo.rewardSlot >= slot:
            LOG_ERR("getMapExploreReward: rewardSlot >= slot:", mapId, slot, mapExploreInfo.rewardSlot)
            return

        LOG_INFO("getMapExploreReward: mapExploreInfo:", mapExploreInfo, mapExploreInfo.rewardSlot, slot)
        _detail = gameclass.AwardDetailCls()
        _src = AAC_AACDD.datas.BONUS_SRC_EXPLORATION_REWARD
        _awardVal = dropAward.AwardVal()


        for i in range(mapExploreInfo.rewardSlot+1, min(slot+1, len(GER.mapId2Reward[mapId]))):
            point, reward = GER.mapId2Reward[mapId][i]
            if mapExploreInfo.rewardData[0] < point:
                break
            mapExploreInfo.rewardSlot += 1
            _ctx = self.getAvatarAwardCtx(reward, None)
            _awardVal += dropAward.getAwardOne(
                reward,
                _ctx
            )
        awardCtx = self.getAvatarAwardCtx(0, None)
        opUUID = KBEngine.genUUID64()
        self.addWealth(_src, _awardVal, opUUID, _detail, awardCtx)

        self.client.onUpdateMapExplore([mapExploreInfo,])