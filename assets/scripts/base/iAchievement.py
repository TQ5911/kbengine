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

class IAchievement(object):
    def __init__(self):
        self.mapExploreInfo.checkNewMapExploreData()

    def _sendAchievementInitData(self):
        self.achievementInfo.sendInitDataToClient(self)

    @gamedecorator.checkGameconfigEnable('achievement')
    def takeAchievementRewards(self, exposed, achievementIds):
        LOG_INFO('takeAchievementRewards:', achievementIds)
        self.achievementInfo.takeAllAchievementRewards(achievementIds, self)

    def onCrossServerTriggerAchieveByType(self, achieveType, ctx):
        LOG_INFO("onCrossServerTriggerAchieveByType", achieveType, ctx)
        if isinstance(ctx, dict):
            ctx['fromCrossServer'] = True
        else:
            ctx.fromCrossServer = True
        self.triggerAchievement(achieveType, ctx)
    
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

        LOG_INFO("before triggerMapExplore:", mapId, tp, num, self.mapExploreInfo.mapDatas[mapId])
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
        mapExploreInfo.rewardData[0] += num * GED.mapId2Point[mapId][tp]
    
        LOG_INFO("after triggerMapExplore:", mapId, tp, num, self.mapExploreInfo.mapDatas[mapId])
        self.onMessagePre(M_M_DD.datas.explorationRate, [str(num * GED.mapId2Point[mapId][tp]),])
        self.client.onUpdateMapExplore([mapExploreInfo,])

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