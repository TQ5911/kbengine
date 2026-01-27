
# coding: utf-8

import userType
import utils
import gameconfig
import achievement_details as A_DD
import gameconst
import LogTrackingMgr


# 等级成就
def _checkAchieveLevelFinished(avatar, achieveData, achieveVal, ctx):
    achieveVal.step = max(achieveVal.step, avatar.getRoleCacheAttr('level', 1))
    return achieveVal.step >= achieveData['targetParam'][0]

# 积分成就
def _checkAchieveScoreFinished(avatar, achieveData, achieveVal, ctx):
    achieveVal.step = max(achieveVal.step, avatar.getTotalScore())
    return achieveVal.step >= achieveData['targetParam'][0]

# 精灵契约成就
def _checkAchieveDrawCardFinished(avatar, achieveData, achieveVal, ctx):
    achieveVal.step += ctx.addNum
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveAddStep(avatar, achieveData, achieveVal, ctx):
    achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchievePetBattleNum(avatar, achieveData, achieveVal, ctx):
    achieveVal.step = max(achieveVal.step, avatar.curBattlePetNum())
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchievePetEquipNum(avatar, achieveData, achieveVal, ctx):
    _quality = achieveData['targetParam'][0]
    _num = achieveData['targetParam'][1]
    achieveVal.step = max(achieveVal.step, avatar.getPetEquipNum(_quality))
    return achieveVal.step >= _num

def _checkAchieveHookReward(avatar, achieveData, achieveVal, ctx):
    _mapId = achieveData['targetParam'][0]
    _num = achieveData['targetParam'][1]
    if getattr(ctx, 'mapId', 0) == _mapId:
        achieveVal.step += 1

    return achieveVal.step >= _num

def _checkAchieveTask(avatar, achieveData, achieveVal, ctx):
    _taskId = achieveData['targetParam'][0]
    if _taskId != getattr(ctx, 'taskId', 0):
        return False

    achieveVal.step = 1
    return True

def _checkAchieveActivityFinished(avatar, achieveData, achieveVal, ctx):
    if getattr(ctx, 'activityId', 0) == achieveData['targetParam'][0]:
        achieveVal.step += 1
        return achieveVal.step >= achieveData['targetParam'][1]

    return False

def _checkAchieveLeaderBoard(avatar, achieveData, achieveVal, ctx):
    _type = achieveData['targetParam'][0]
    _num = achieveData['targetParam'][1]
    if _type != getattr(ctx, 'lbType', 0):
        return False

    if getattr(ctx, 'rank', 0) <= _num:
        achieveVal.step = 1
        return True

    else:
        return False

# 第一个是checkFunc，第二个代表初始化时候是否要校验一次
_CHECK_ACHIEVE_DIC = {
    gameconst.AchieveType.LEVEL: (_checkAchieveLevelFinished, True),
    gameconst.AchieveType.SCORE: (_checkAchieveScoreFinished, True),
    gameconst.AchieveType.KILL_MONSTER: (_checkAchieveAddStep, False),
    gameconst.AchieveType.DRAW_CARD: (_checkAchieveDrawCardFinished, False),
    gameconst.AchieveType.UNLOCK_MOUNT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.JOIN_GUILD: (_checkAchieveAddStep, False),
    gameconst.AchieveType.ADD_FRIEND: (_checkAchieveAddStep, False),
    gameconst.AchieveType.MAKE_EQUIPMENT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.ENHANCE_EQUIPMENT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.LEVEL_UP_SKILL: (_checkAchieveAddStep, False),
    gameconst.AchieveType.ACTIVITY: (_checkAchieveActivityFinished, False),
    gameconst.AchieveType.PET_BATTLE: (_checkAchievePetBattleNum, True),
    gameconst.AchieveType.PET_EQUIP: (_checkAchievePetEquipNum, True),
    gameconst.AchieveType.LOGIN_DAYS: (_checkAchieveAddStep, True),
    gameconst.AchieveType.DEAD_TIMES: (_checkAchieveAddStep, False),
    gameconst.AchieveType.DO_COLLECT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.USE_POTION: (_checkAchieveAddStep, False),
    gameconst.AchieveType.MAIN_TASK: (_checkAchieveTask, False),
    gameconst.AchieveType.SUB_TASK: (_checkAchieveTask, False),
    gameconst.AchieveType.HOOK_TASK_REWARD: (_checkAchieveHookReward, False),
    gameconst.AchieveType.LEADER_BOARD: (_checkAchieveLeaderBoard, False),
    gameconst.AchieveType.SIEGE_KILL: (_checkAchieveAddStep, False),
    gameconst.AchieveType.PERSONAL_BOX: (_checkAchieveAddStep, False),
    gameconst.AchieveType.VIEWPOINT: (_checkAchieveAddStep, False),
}


class AchievementValVal(userType.UserSoleType):
    '''ACHIEVEMENT_VAL_DATA_INFO'''
    def __init__(self, achieveId=0, flag=0, step=0):
        self.achieveId = achieveId
        self.flag = flag
        self.step = step

    def configData(self):
        return A_DD.datas[self.achieveId]

    def targetType(self):
        return self.configData()['targetType']

    def isFinished(self):
        return utils.hasBit(self.flag, gameconst.AchievementFlag.FINISHED)

    def checkCouldChangeFinishedState(self, avatar, achieveData, ctx):
        return _CHECK_ACHIEVE_DIC[achieveData['targetType']][0](avatar, achieveData, self, ctx)

    def updateFromNewAchieveData(self, avatar, achieveData, ctx, src):
        if not achieveData['isOpen']:
            return False

        _oldIsFinished = self.isFinished()
        _oldStep = self.step
        if self.checkCouldChangeFinishedState(avatar, achieveData, ctx):
            self.flag = utils.bitSet(self.flag, gameconst.AchievementFlag.FINISHED)

        if _oldIsFinished != self.isFinished():
            _isLog = True
            _state = gameconst.ACHIEVE_STATE_FINISH

        elif src == gameconst.ACHIEVE_SRC_NEW:
            _isLog = True
            _state = gameconst.ACHIEVE_STATE_NEW

        else:
            _isLog = False
            _state = 0

        if _isLog:
            LogTrackingMgr.LogTrackingMgr.Achievement_Update(
                avatar.accountEntity.accountName,
                avatar.gbID,
                gameconfig.gameId(),
                self.achieveId,
                avatar.achievementInfo.maxVersion,
                _state,
                self.step,
            )

        return self.step > _oldStep

    @classmethod
    def fromAchieveData(cls, avatar, achieveData, ctx):
        # 新增的成就会走到这里
        _achieveVal = cls(achieveData['ID'])
        if _CHECK_ACHIEVE_DIC[achieveData['targetType']][1]:
            _achieveVal.updateFromNewAchieveData(avatar, achieveData, ctx, gameconst.ACHIEVE_SRC_NEW)
        return _achieveVal

    def toAchievementValSavedDict(self):
        return {
            'achieveId': self.achieveId,
            'flag': self.flag,
            'step': self.step
        }

    def __str__(self):
        return 'AchievementValVal(achieveId={}, flag={}, step={})'.format(self.achieveId, self.flag, self.step)


class AchievementValInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AchievementValVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAchievementValSavedDict()

    def isSameType(self, obj):
        return type(obj) is AchievementValVal


AchievementValInstance = AchievementValInfo()

