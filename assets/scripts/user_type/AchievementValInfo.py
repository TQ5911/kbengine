
# coding: utf-8

import userType
import utils
import gameconfig
import achievement_details as A_DD
import gameconst
import LogTrackingMgr
from KBEDebug import *

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
    _qualityDict = ctx.qualityDict
    
    addNum = 0
    baseQuality = -1 if len(achieveData['targetParam']) == 1 else achieveData['targetParam'][1]
    for quality, num in _qualityDict.items():
        if quality >= baseQuality:
            addNum += num

    achieveVal.step += addNum
    return achieveVal.step >= achieveData['targetParam'][0]

#技能升级
def _checkSkillUpgrade(avatar, achieveData, achieveVal, ctx):
    limitLevel = -1 if len(achieveData['targetParam']) == 1 else achieveData['targetParam'][1]
    if limitLevel == -1:
        achieveVal.step += 1
    elif ctx.oldLevel < limitLevel and ctx.newLevel >= limitLevel:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveUsePotion(avatar, achieveData, achieveVal, ctx):
    if len(achieveData['targetParam']) == 1:
        achieveVal.step += 1
    elif ctx.itemId in achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

# 在默认基础上增加mapId
def _checkAchieveAddStepWithMapId(avatar, achieveData, achieveVal, ctx):
    if len(achieveData['targetParam']) == 1:
        achieveVal.step += 1
    elif ctx.mapId == achieveData['targetParam'][1]:
        achieveVal.step += 1
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
    _num = achieveData['targetParam'][0]
    if len(achieveData['targetParam']) > 1:
        _mapId = achieveData['targetParam'][1]
        if getattr(ctx, 'mapId', 0) == _mapId:
            achieveVal.step += 1
    else:
        achieveVal.step += 1

    return achieveVal.step >= _num

def _checkAchieveMakeEquipment(avatar, achieveData, achieveVal, ctx):
    _num = achieveData['targetParam'][0]
    if len(achieveData['targetParam']) > 1:
        _quality = achieveData['targetParam'][1]
        if getattr(ctx, 'quality', 0) >= _quality:
            achieveVal.step += 1
    else:
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
    
def _checkAchieveKillTarSuffixMonster(avatar, achieveData, achieveVal, ctx):
    _suffixIds = achieveData['targetParam'][1]
    if ctx.get('suffixId', 0) not in _suffixIds:
        return False
    achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveKillTarMonster(avatar, achieveData, achieveVal, ctx):
    _monsterIds = achieveData['targetParam'][1]
    if ctx.get('monsterId', 0) not in _monsterIds:
        return False
    achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveEnemy(avatar, achieveData, achieveVal, ctx):
    achieveVal.step = max(achieveVal.step, ctx.count)
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveDuel(avatar, achieveData, achieveVal, ctx):
    if ctx.isWin == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveBounty(avatar, achieveData, achieveVal, ctx):
    if ctx.bountyType == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveDungeon(avatar, achieveData, achieveVal, ctx):
    if ctx.dungeonNo == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveEquipQuality(avatar, achieveData, achieveVal, ctx):
    qualityData = ctx.qualityData
    achieveVal.step = 0
    for quality, count in qualityData.items():
        if quality >= achieveData['targetParam'][1]:
            achieveVal.step += count
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveMineCollect(avatar, achieveData, achieveVal, ctx):
    if ctx.collectionId == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveSynthesis(avatar, achieveData, achieveVal, ctx):
    for i in range(len(ctx.getNum)):
        if ctx.getQuality[i] >= achieveData['targetParam'][1]:
            achieveVal.step += ctx.getNum[i]
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveMaxMoney(avatar, achieveData, achieveVal, ctx):
    achieveVal.step = max(achieveVal.step, ctx.money)
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveAddNum(avatar, achieveData, achieveVal, ctx):
    achieveVal.step += ctx.num
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveMeridian(avatar, achieveData, achieveVal, ctx):
    if ctx.slotIdx == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

def _checkAchieveGuildActivity(avatar, achieveData, achieveVal, ctx):
    if ctx.activityType == achieveData['targetParam'][1]:
        achieveVal.step += 1
    return achieveVal.step >= achieveData['targetParam'][0]

# 第一个是checkFunc，第二个代表初始化时候是否要校验一次
_CHECK_ACHIEVE_DIC = {
    gameconst.AchieveType.LEVEL: (_checkAchieveLevelFinished, True),
    gameconst.AchieveType.SCORE: (_checkAchieveScoreFinished, True),
    gameconst.AchieveType.KILL_MONSTER: (_checkAchieveAddStep, False),
    gameconst.AchieveType.DRAW_CARD: (_checkAchieveDrawCardFinished, False),
    gameconst.AchieveType.UNLOCK_MOUNT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.JOIN_GUILD: (_checkAchieveAddStep, False),
    gameconst.AchieveType.ADD_FRIEND: (_checkAchieveAddStep, False),
    gameconst.AchieveType.MAKE_EQUIPMENT: (_checkAchieveMakeEquipment, False),
    gameconst.AchieveType.ENHANCE_EQUIPMENT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.EQUIPMENT_WITH_SPIRIT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.LEVEL_UP_SKILL: (_checkSkillUpgrade, False),
    gameconst.AchieveType.ACTIVITY: (_checkAchieveActivityFinished, False),
    gameconst.AchieveType.PET_BATTLE: (_checkAchievePetBattleNum, True),
    gameconst.AchieveType.PET_EQUIP: (_checkAchievePetEquipNum, True),
    gameconst.AchieveType.LOGIN_DAYS: (_checkAchieveAddStep, True),
    gameconst.AchieveType.DEAD_TIMES: (_checkAchieveAddStep, False),
    gameconst.AchieveType.DO_COLLECT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.USE_POTION: (_checkAchieveUsePotion, False),
    gameconst.AchieveType.MAIN_TASK: (_checkAchieveTask, False),
    gameconst.AchieveType.SUB_TASK: (_checkAchieveTask, False),
    gameconst.AchieveType.HOOK_TASK_REWARD: (_checkAchieveHookReward, False),
    gameconst.AchieveType.LEADER_BOARD: (_checkAchieveLeaderBoard, False),
    gameconst.AchieveType.SIEGE_KILL: (_checkAchieveAddStep, False),
    gameconst.AchieveType.PERSONAL_BOX: (_checkAchieveAddStepWithMapId, False),
    gameconst.AchieveType.VIEWPOINT: (_checkAchieveAddStepWithMapId, False),
    gameconst.AchieveType.KILL_TAR_SUFFIX_MONSTER: (_checkAchieveKillTarSuffixMonster, False),
    gameconst.AchieveType.KILL_TAR_MONSTER: (_checkAchieveKillTarMonster, False),
    gameconst.AchieveType.ENEMY: (_checkAchieveEnemy, False),
    gameconst.AchieveType.DUEL: (_checkAchieveDuel, False),
    gameconst.AchieveType.WONDERLAND_KILL: (_checkAchieveAddStep, False),
    gameconst.AchieveType.BOUNTY: (_checkAchieveBounty, False),
    gameconst.AchieveType.CRUSADE: (_checkAchieveDungeon, False),
    gameconst.AchieveType.CHIEF: (_checkAchieveDungeon, False),
    gameconst.AchieveType.COLLECT: (_checkAchieveAddStep, False),
    gameconst.AchieveType.EQUIP_QUALITY: (_checkAchieveEquipQuality, False),
    gameconst.AchieveType.MINE_COLLECT: (_checkAchieveMineCollect, False),
    gameconst.AchieveType.SYNTHESIS: (_checkAchieveSynthesis, False),
    gameconst.AchieveType.MAX_MONEY: (_checkAchieveMaxMoney, False),
    gameconst.AchieveType.AUCTION_MONEY: (_checkAchieveAddNum, False),
    gameconst.AchieveType.INSCRIPTION: (_checkAchieveAddStep, False),
    gameconst.AchieveType.MERIDIAN: (_checkAchieveMeridian, False),
    gameconst.AchieveType.GUILD_CONTRIB: (_checkAchieveAddNum, False),
    gameconst.AchieveType.GUILD_ACTIVITY: (_checkAchieveGuildActivity, False),
}


class AchievementValVal(userType.UserSingleType):
    '''ACHIEVEMENT_VAL_DATA_INFO'''
    def __init__(self, achieveId=0, flag=0, step=0):
        self.achieveId = achieveId
        self.flag = flag
        self.step = step

    def configData(self):
        return A_DD.datas[self.achieveId]

    def targetType(self):
        return self.configData()['targetType']

    @staticmethod
    def checkSupport(targetType):
        return targetType in _CHECK_ACHIEVE_DIC

    def isFinished(self):
        return utils.bhas(self.flag, gameconst.AchievementFlag.FINISHED)

    def checkCouldChangeFinishedState(self, avatar, achieveData, ctx):
        return _CHECK_ACHIEVE_DIC[achieveData['targetType']][0](avatar, achieveData, self, ctx)

    def updateFromNewAchieveData(self, avatar, achieveData, ctx, src):
        if not achieveData['isOpen']:
            return False

        _oldIsFinished = self.isFinished()
        _oldStep = self.step
        if self.checkCouldChangeFinishedState(avatar, achieveData, ctx):
            self.flag = utils.bset(self.flag, gameconst.AchievementFlag.FINISHED)

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
                avatar.gbID,
                avatar.accountEntity.clientDistinctId,
                avatar.accountEntity.accountName,
                avatar.gbID,
                gameconfig.gameId(),
                self.achieveId,
                avatar.achievementInfo.maxVersion,
                _state,
                self.step,
                avatar.achievementInfo.sumPoint,
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

