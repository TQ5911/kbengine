# -*- coding: utf-8 -*-
import sys

from KBEDebug import *

import random
import functools

import utils
import gameconst
import gameengine

import itemData_itemData as ITEMDATA
import gearBase_gearBase as GBGBD
import const_const as CONSTD
import conflict_status as CSD
import value_value as VVD
import formula_generalFormula as FMLGD
import antiAddictCategory_antiAddictCategory as AACADCD
import taskdata as TSKD
import taskEditorConfig_taskEditorInfo as TECTEID
import taskClass_taskMsg as TCTMD
import appearance_dressUpData as ADUD
import appearance_wingData as AWD
import appearance_hairData as AHD
import appearance_avatarFrame as AAF
import taskDesc_taskDesc as TDTD
import taskDesc_taskGroup as TTG
import taskRandTargetPoint as TRTPD
import mounts_mounts as MOUNTS
import antiAddictCategory_antiAddictCategory as AAC_AAC
import rewardData_rewardData as RWDRWDD
import creep_base as CBD
import gearBase_typeExplanation as GBTED
import fightProp_define as FDD
import petData_petData as PDPD
import petData_rank as PDRK
import passiveSkill_passiveSkill as PSPSD
import gearBase_typeTab as GBTBD
import cube_room
import monsterStandardProp_propCurve as MSPPCD
import monsterStandardProp_prop as MSPPD
import skill_skill as SSD
import raid_raidConst as RAID_CONST
import gearBase_gearConst as GBGCD
import skill_specialMonsterAI as S_SMAD
import character_charData as CCD
import teamMatch_matchConfig as TMMCD
import fightProp_atkBlessScore as FASD

def getRaidConstDataValue(key):
    raidConstData = RAID_CONST.datas.get(key, None)
    if not raidConstData:
        return None

    return raidConstData.get('value')

def isRaidCapacityValidate(capacity):
    value = getRaidConstDataValue('raidMemberLimit')
    return capacity and value and capacity >= 1 and capacity <= value

def isEquipItemByItemId(itemId):
    return itemId in GBGBD.datas or itemId == gameconst.ItemId.COMMON_EQUIPMENT_ID

def isReUseItem(itemId):
    itemData = getCommItemData(itemId)
    if not itemData:
        return False
    itemType = itemData.get('type')
    subType = itemData.get('subType')
    return itemType == gameconst.ItemType.Normal and subType == gameconst.ItemSubType.ReUseItem


def getVariableData(varId):
    return VVD.datas[varId]


def getVariableDefaultVal(varId):
    return getVariableData(varId)['defaultValue']


def checkVariableCond(owner, fmlId, paramsStr):
    paramsStr = paramsStr.strip(' ')
    params = [owner.getVariable(int(varId)) for varId in paramsStr.split('|')] if paramsStr else ()
    DEBUG_MSG('in checkVariableCond:', fmlId, paramsStr, params)
    return FMLGD.datas[int(fmlId)]['serverFormula'](*params)


def isSpaceVar(varId):
    return getVariableData(varId)['type'] == gameconst.VariableType.VAR_TYPE_SPACE


def isAvatarVar(varId):
    return getVariableData(varId)['type'] == gameconst.VariableType.VAR_TYPE_AVATAR


def isRelateCharPropVar(varId):
    return varId in VVD.AvatarDataVarIdDic


def isValidItemId(itemId):
    return bool(getItemSpecialDetailData(itemId))


def getCommItemData(itemId):
    # 读取itemData_itemData表里的通用物品配置；装备物品会读取通用装备配置；魂卡目前没定义通用配置；
    itemId = int(itemId)
    itemData = ITEMDATA.datas.get(itemId, None)
    if itemData:
        return itemData
    if isEquipItemByItemId(itemId):
        return ITEMDATA.datas.get(gameconst.ItemId.COMMON_EQUIPMENT_ID, {})


def getItemSpecialDetailData(itemId):
    """根据itemID读取相应特殊表中的字段"""
    itemId = int(itemId)

    return getCommItemData(itemId)


def getItemDefaultBindType():
    #  物品默认全绑定
    # 【【功能点】绑定配置机制优化】
    return gameconst.ItemBindType.BIND


def getConstVal(keyName, default=None):
    'tutorialMissionEnd'
    data = CONSTD.datas.get(keyName, {})
    return data.get('value', default)


def getStateEventId(state):
    return CSD.datas.get(state, {}).get('event')


def getAddItemExtraDesp(srcType):
    return AACADCD.datas.get(srcType, {}).get('rewardDescribe', '')


def isInCrontabDatetimeRange(t, startList, endedList):
    nextStart, _ = utils.nextByTimeTupleList(startList, now=t)
    nextEnded, _ = utils.nextByTimeTupleList(endedList, now=t)
    if not nextStart and not nextEnded:
        return True
    if nextStart == sys.maxsize and nextEnded == sys.maxsize:
        return False
    if nextStart >= nextEnded:
        return True
    return False


def getRealRewardId(rewardId, context, timeStamp=0):
    times = 1
    now = timeStamp or utils.getNow()

    def untilGetValidRewardId(tmpId, tmpTimes):
        return tmpId

    realRewardId = untilGetValidRewardId(rewardId, times)
    if realRewardId != rewardId:
        context.addContextVar('awardId', realRewardId)
    return realRewardId


@functools.lru_cache(128)
def getTaskData(taskId):
    taskData = TSKD.datas.get(str(taskId))
    if not taskData:
        gameengine.reportCritical('getTaskData, no taskdata:', taskId)
    return taskData


def getRootTaskData(taskId):
    taskData = getTaskData(taskId)
    fatherTaskId = taskData.get('FatherTaskId', 0)
    loopCnt = 0
    while fatherTaskId != 0 and loopCnt < 10:
        loopCnt += 1
        taskData = getTaskData(fatherTaskId)
        fatherTaskId = taskFieldVal(taskData, 'FatherTaskId')
    return taskData


def getRootTaskId(taskId):
    return getRootTaskData(taskId).get('TaskId')


def taskFieldVal(taskData, key):
    return taskData.get(key, TECTEID.datas[key]['value'])


def isRootTask(taskId):
    return 0 == taskFieldVal(getTaskData(taskId), 'FatherTaskId')


def isSingleSupportTeamTask(taskId):
    # 支持单人的组队任务
    rootTaskData = getRootTaskData(taskId)
    if taskFieldVal(rootTaskData, 'ClaimCondCheckTeam').get('IsTaskSharing', False):
        return rootTaskData.get('ClaimCondCheckTeam', {}).get('SupportSingle', False)
    else:
        return False


def isTaskInOpenTime(taskId):
    tdtd = TDTD.datas.get(taskId, {})
    taskGroupId = tdtd.get('TaskGroup', 0)
    if not taskGroupId:
        return True
    taskGroupData = TTG.datas.get(taskGroupId, {})
    startTime = taskGroupData.get("startTime", "")
    endTime = taskGroupData.get("endTime", "")
    now = utils.getNow()
    if startTime and utils.parseTimeStr(startTime) > now:
        return False
    if endTime and now > utils.parseTimeStr(endTime):
        return False
    return True


def taskMsgId(msgName):
    return TCTMD.datas[msgName]['value']


def getRandTargetPointTaskIds(rootTaskId):
    return TRTPD.datas.get(str(rootTaskId), [])


def isTeamTask(taskId):
    rootTaskData = getRootTaskData(taskId)
    return taskFieldVal(rootTaskData, 'ClaimCondCheckTeam').get('IsTaskSharing', False)


def isLeafTask(taskId, taskData=None):
    taskData = taskData or getTaskData(taskId)
    return len(taskData['ChildTaskIds']) == 0


def getTaskRoundInfo(taskData):
    roundVal = 0
    roundRwdList = []
    roundActList = []
    roundParamList = []
    # openCondTaskRound finRoundRewardID等导出的默认值可能是 None
    openCondTaskRound = taskFieldVal(taskData, 'OpenCondTaskRound')
    finRoundRewardID = taskFieldVal(taskData, 'FinRoundRewardID')
    roundActionNames = taskFieldVal(taskData, 'FinRoundEventName')
    roundActionParams = taskFieldVal(taskData, 'FinRoundEventParam')

    openCondTaskRound = openCondTaskRound if openCondTaskRound else ''
    openCondTaskRound = openCondTaskRound.strip(' []')
    if openCondTaskRound:
        roundVal = int(openCondTaskRound)

    finRoundRewardID = finRoundRewardID.strip(' []')
    if finRoundRewardID:
        roundRwdList = [int(i) for i in finRoundRewardID.split(",")]

    roundActionNames = roundActionNames.strip(' []')
    if roundActionNames:
        roundActList = [actNames for actNames in roundActionNames.split(";")]

    roundActionParams = roundActionParams.strip(' []')
    if roundActionParams:
        roundParamList = [params for params in roundActionParams.split(";")]

    return roundVal, roundRwdList, roundActList, roundParamList


def filterChildTaskIds(childTaskIds, level, excludedChildTaskIds=None):
    realChildTaskIds = []
    excludedChildTaskIds = excludedChildTaskIds or []
    for childTaskId in childTaskIds:
        if childTaskId in excludedChildTaskIds:
            continue

        childTaskData = getTaskData(childTaskId)
        minLevel = taskFieldVal(childTaskData, 'ClaimCondLevelMin')
        maxLevel = taskFieldVal(childTaskData, 'ClaimCondLevelMax')
        if 0 == maxLevel:
            maxLevel = utils.getPlayerMaxLevel()
        if minLevel <= level <= maxLevel:
            realChildTaskIds.append(childTaskId)

    return realChildTaskIds


def shuffleChildTaskIds(seed, childIds):
    seed and random.seed(seed)
    random.shuffle(childIds)


def calcChildTaskIds(taskData, cfgChildTaskIds, checkLevel, seed=0, excludedChildTaskIds=None):
    # 按照玩家等级和例外条件，筛选子任务
    childTaskIds = filterChildTaskIds(cfgChildTaskIds, checkLevel, excludedChildTaskIds=excludedChildTaskIds)
    if len(childTaskIds) > 0:
        # 随机取任务且不是按照权重取的，那就是随机打乱子任务列表
        if taskFieldVal(taskData, 'ChildDoInRandom') and not taskFieldVal(taskData, 'RandomWithWeight'):
            shuffleChildTaskIds(seed, childTaskIds)
            DEBUG_MSG('     in Task::calcChildTaskIds, ChildDoInRandom, childTaskIds:', childTaskIds)
    return childTaskIds



def getItemActionFunc(itemId):
    return ITEMDATA.datas.get(itemId, {}).get('action', None)


# intVal :: 整数部分
# fraVal :: 小数部分 :: 最多保留两位小数，因此不会大于 100
# needSign :: 是否显示符号
def getCoinBillStr(intVal, fraVal, needSign):
    if needSign:
        return ('%+.02f' % (intVal + fraVal / 100)).rstrip('0').rstrip('.')
    return ('%.02f' % (intVal + fraVal / 100)).rstrip('0').rstrip('.')


def getMailId(srcType, ctxMailId):
    abandonWhenBagFull = AAC_AAC.datas.get(srcType).get('abandonWhenBagFull')
    if not abandonWhenBagFull and not ctxMailId:
        return gameconst.MailConstID.REWARD_MAIL_ID, abandonWhenBagFull
    return ctxMailId, abandonWhenBagFull
def getOutfitConfigData(outfitType, outfitId):
    if outfitType == gameconst.OutfitType.wing:
        return AWD.datas.get(outfitId, None)
    if outfitType == gameconst.OutfitType.hair:
        return AHD.datas.get(outfitId, None)
    if outfitType == gameconst.OutfitType.clothes:
        return ADUD.datas.get(outfitId, None)
    if outfitType == gameconst.OutfitType.picFrame:
        return AAF.datas.get(outfitId, None)
    if outfitType == gameconst.OutfitType.mount:
        return MOUNTS.datas.get(outfitId)
    return

def checkOutfitOpen(outfitType, outfitId):
    configData = getOutfitConfigData(outfitType, outfitId)
    if not configData:
        return False
    isOpen = configData.get('isOpen', None)
    if isOpen == None:
        return True
    if not isOpen:
        return False
    return True

def hasNormalBagRwdItems(rewardId, rwdData=None):
    rwdData = rwdData or RWDRWDD.datas[rewardId]
    if rwdData.get('fixReward') or rwdData.get('singleReward') or rwdData.get('exReward'):
        return True
    nestFixReward = rwdData.get('nestFixReward')
    if nestFixReward:
        for oneRwdData in nestFixReward:
            if hasNormalBagRwdItems(oneRwdData[0]):
                return True
    nestExReward = rwdData.get('nestExReward')
    if nestExReward:
        for oneRwdData in nestFixReward:
            if hasNormalBagRwdItems(oneRwdData[0]):
                return True
    return False

def hasPetItemBagRwdItems(rewardId, rwdData=None):
    rwdData = rwdData or RWDRWDD.datas[rewardId]
    fixPetReward = rwdData.get('fixPetReward')
    singlePetReward = rwdData.get('singlePetReward')
    exPetReward = rwdData.get('exPetReward')
    return bool(fixPetReward) or bool(singlePetReward) or bool(exPetReward)

def isLingShouItem(itemId):
    itemData = getCommItemData(itemId)
    return itemData and itemData['type'] == gameconst.ItemType.LingShou

def getCommItemBagType(itemId):
    itemData = getCommItemData(itemId)
    if itemData['type'] == gameconst.ItemType.Normal:
        return gameconst.BagType.BAG_TYPE_NORMAL
    elif itemData['type'] == gameconst.ItemType.LingShou:
        return gameconst.BagType.BAG_TYPE_LINGSHOU_PEN
    return

def getPetEquipDefaultStatus():
    return 0

def createPetInfo(petId):
    petEquipStatus = getPetEquipDefaultStatus()
    gearNum = getPetGearNum(petId)
    lingShouDict = {
        'petId': petId,
        'equipList': [petEquipStatus] * gearNum,
    }
    return lingShouDict

def getPetGearNum(petId):
    cfgData = PDPD.datas.get(petId)
    grade = cfgData.get('petRank', 0)
    gearNum = PDRK.datas.get(grade, {}).get('gearNum', 0)
    return gearNum

def getPetLevelUpExp(petId):
    cfgData = PDPD.datas.get(petId)
    grade = cfgData.get('petRank', 0)
    levelUpExp = PDRK.datas.get(grade, {}).get('levelExp', None)
    return levelUpExp

def getPetLevelUpConsumeItem(petId):
    cfgData = PDPD.datas.get(petId)
    grade = cfgData.get('petRank', 0)
    consumeItem = PDRK.datas.get(grade, {}).get('consumeItem', None)
    return consumeItem

def getPetLevelProp(petId):
    cfgData = PDPD.datas.get(petId)
    levelProp = cfgData.get('levelProp')
    return levelProp

def isRing(mType, sType):
    return mType == gameconst.EquipTypes.MAIN_TYPE_RING and sType in gameconst.EquipTypes.SUBTYPE_ORNAMENTS_RING

def isBracelet(mType, sType):
    return mType == gameconst.EquipTypes.MAIN_TYPE_BRACELET and sType in gameconst.EquipTypes.SUBTYPE_ORNAMENTS_BRACELET

def equipSlot(mType, subType):
    cfgData = GBTED.datas[subType]
    if not cfgData:
        ERROR_MSG('equipSlot gearBase_typeExplanation not found:', subType)
        return []

    if mType != cfgData['type']:
        ERROR_MSG('equipSlot mType not match:', mType, cfgData['type'])
        return []

    if subType != cfgData['SubType']:
        ERROR_MSG('equipSlot subType not match:', subType, cfgData['subType'])
        return []

    slot = cfgData['slot']
    if type(slot) == int:
        return [slot]
    return slot

def equipRecommendClass(mType, subType):
    cfgData = GBTED.datas[subType]
    if not cfgData:
        ERROR_MSG('equipRecommendClass gearBase_typeExplanation not found:', subType)
        return []

    if mType != cfgData['type']:
        ERROR_MSG('equipRecommendClass mType not match:', mType, cfgData['type'])
        return []

    if subType != cfgData['SubType']:
        ERROR_MSG('equipRecommendClass subType not match:', subType, cfgData['subType'])
        return []

    recommendClass = cfgData['recommendClass']
    if type(recommendClass) == int:
        return [recommendClass]
    return recommendClass

def getEquipItemData(itemId):
    return GBGBD.datas.get(itemId)

def iterGetGearIdsByBaseInfo(quality, gearTypes, gearSubTypes, school):
    DEBUG_MSG('in iterGetGearIdsByBaseInfo:', quality, gearTypes, gearSubTypes, school)
    if not (quality == gameconst.ItemQuality.ALL_QUALITY or gearTypes or gearSubTypes):
        yield from GBGBD.datas.keys()
        return

    _qualities = (quality, ) if quality != gameconst.ItemQuality.ALL_QUALITY else gameconst.ItemQuality.COLL_QUALITY
    _gearTypes = gearTypes or gameconst.EquipTypes.ALL_MAINTYPES
    _gearSubTypes = gearSubTypes or gameconst.EquipTypes.ALL_SUBTYPES
    for _q in _qualities:
        for _t in _gearTypes:
            for _st in _gearSubTypes:
                for _celldata in _getGearIdsByBaseInfo(_q, _t, _st, school):
                    yield _celldata

def getGearIdsByBaseInfo(quality, gearTypes, gearSubTypes, school):
    DEBUG_MSG('in getGearIdsByBaseInfo:', quality, gearTypes, gearSubTypes, school)
    return list(iterGetGearIdsByBaseInfo(quality, gearTypes, gearSubTypes, school))

def _getGearIdsByBaseInfo(quality, gearType, gearSubType, school):
    allSchoolKey = quality*10000 + gearType*1000 + gearSubType*10
    school = school % 1000
    key = quality*10000 + gearType*1000 + gearSubType*10 + school
    return GBGBD.gearsMap.get(key, []) + GBGBD.gearsMap.get(allSchoolKey, [])

def getCreepMD(creepId):
    return CBD.datas.get(creepId, {}).get('magicDrop', 0)

def getPropBaseScore(propName, school = 0):
    cfgData = FDD.datas.get(propName, None)
    if not cfgData:
        ERROR_MSG("getPropScore cfgData not found:", propName)
        return 0
    return cfgData['perPropertyScore']

def getPassiveSkillScore(school, passiveSkillId):
    score = PSPSD.datas[passiveSkillId]['score']
    petPropList = PSPSD.datas[passiveSkillId]['propList']
    if petPropList:
        for propName, val in petPropList:
            score += calcFightPropScore(school, propName, val)
    return score

def getBlessAffixIdByGearType(mainType):
    cfgData = GBTBD.datas.get(mainType)
    if not cfgData:
        ERROR_MSG('getBlessAffixIdByGearType not in cfg', mainType)
        return

    return cfgData['blessAffixID']


def getAllCubeFloors():
    _ret = []
    for _cubeData in cube_room.datas.values():
        if _cubeData['floor'] not in _ret:
            _ret.append(_cubeData['floor'])

    return _ret


def getCubeFloor(mapId):
    return cube_room.datas.get(mapId, {}).get('floor', 0)


def getAllCubeRooms(cubeNo):
    _ret = []
    for _, _cubeData in cube_room.datas.items():
        if _cubeData['floor'] == cubeNo:
            _ret.append(_cubeData)

    return _ret

def getMonsterExp(monsterId, monsterLv):
    expRatio = CBD.datas.get(monsterId).get('expRatio')
    propCurveID = CBD.datas.get(monsterId).get('propCurveID')
    expCurve = MSPPCD.datas[propCurveID].get('expCurve')
    return int(MSPPD.datas[monsterLv].get(expCurve)*expRatio)

def getExpByLevel(avatarLevel,monsterLv, monsterExp):
    if avatarLevel > monsterLv:
        levelDiff = min(avatarLevel - monsterLv, 5)
        return int(monsterExp * (1 - levelDiff * CONSTD.datas['killMonsterLowerExpBonus'].get("value", 0)))
    else:
        levelDiff = min(monsterLv - avatarLevel, 5)
        return int(monsterExp * (1 + levelDiff * CONSTD.datas['killMonsterHighExpBonus'].get("value", 0)))


def getSkillIdByMorphState(skillId, morphState):
    _modId = SSD.skillToModDic.get(skillId)
    if not _modId:
        return skillId

    return SSD.modDic[_modId][morphState]

def checkEquipmentEnhancementType(equipType):
    return equipType in (gameconst.EquipTypes.MAIN_TYPE_WEAPON,
                        gameconst.EquipTypes.MAIN_TYPE_CLOTHES,
                        gameconst.EquipTypes.MAIN_TYPE_HEAD,
                        gameconst.EquipTypes.MAIN_TYPE_SHOE,
                        gameconst.EquipTypes.MAIN_TYPE_NECKLACE,
                        gameconst.EquipTypes.MAIN_TYPE_RING,
                        gameconst.EquipTypes.MAIN_TYPE_BRACELET,
                        gameconst.EquipTypes.MAIN_TYPE_BELT)

def checkEquipmentGlyphType(equipType):
    return equipType in (gameconst.EquipTypes.MAIN_TYPE_WEAPON,)

def checkEquipmentBlessType(equipType, quality):
    # 绿色品质不可祝福
    if quality == gameconst.ItemQuality.GREEN:
        return False
    return equipType in (gameconst.EquipTypes.MAIN_TYPE_WEAPON,)

def checkEquipmentSpiritType(equipType):
    return equipType in (gameconst.EquipTypes.MAIN_TYPE_CLOTHES,
                        gameconst.EquipTypes.MAIN_TYPE_HEAD,
                        gameconst.EquipTypes.MAIN_TYPE_SHOE,
                        gameconst.EquipTypes.MAIN_TYPE_NECKLACE,
                        gameconst.EquipTypes.MAIN_TYPE_RING,
                        gameconst.EquipTypes.MAIN_TYPE_BRACELET,
                        gameconst.EquipTypes.MAIN_TYPE_BELT)

def checkEquipmentUpgradeType(equipType):
    return True

def checkEquipGrowingForbidden(equipItem):
    if not equipItem.isGood():
        return True
    data = GBGCD.datas['equipGrowingForbidden']['value']
    if data and equipItem.itemId in data:
        return True
    return False

def checkAuctionAllowListing(itemID):
    itemData = GBGBD.datas.get(itemID, None)
    if itemData:
        return itemData['auctionAllowListing'] == 1
    itemData = ITEMDATA.datas.get(itemID, None)
    if itemData:
        return itemData['auctionAllowListing'] == 1
    return False

def checkLockAvailableStatus(itemID):
    itemData = GBGBD.datas.get(itemID, None)
    if itemData:
        return itemData['lockAvailable'] == 1
    itemData = ITEMDATA.datas.get(itemID, None)
    if itemData:
        return itemData['lockAvailable'] == 1
    return None

def gellItemSellPrice(itemID):
    itemData = GBGBD.datas.get(itemID, None)
    if itemData:
        return itemData['sellPrice']
    itemData = ITEMDATA.datas.get(itemID, None)
    if itemData:
        return itemData['sellPrice']
    return None

def getItemQuality(itemID):
    itemData = ITEMDATA.datas.get(itemID, None)
    if itemData:
        return itemData['quality']
    itemData = GBGBD.datas.get(itemID, None)
    if itemData:
        return itemData['quality']
    return None

def getAIParameters(creepId):
    _aiParamId = CBD.datas[creepId]['AIParameters']
    if not _aiParamId:
        _aiId = CBD.datas[creepId]['AI']
        if not _aiId:
            return {}
        else:
            _aiParamId = _aiId * 100 + 1

    return S_SMAD.datas.get(_aiParamId, {})


def isCubeCow(mapId):
    _cubeData = cube_room.datas.get(mapId, None)
    if not _cubeData:
        return False

    return _cubeData['type'] == gameconst.CubeRoomType.COW

def filterFightPropScore(school, propName):
    cfgData = FDD.datas.get(propName, None)
    if not cfgData:
        WARNING_MSG("filterFightPropScore fight cfg not found:", propName)
        return 0

    characterData = CCD.datas.get(school, None)
    if characterData:
        # 角色表里需要排除的属性类型
        if characterData['excludePropType'] == cfgData['propType']:
            return 0

    return cfgData['perPropertyScore']

# 计算属性评分之前，需要先加属性（addProp)
def calcFightPropScore(school, propName, val):
    scoreResult = filterFightPropScore(school, propName) * val
    return int(scoreResult)

def calcAvatarBlessScore(playerBox):
    val = playerBox.getProp('adjAtkBless')
    val = min(int(val), FASD.maxKey)
    return FASD.atkBlessScoreDic.get(val, 0)

def getAuctionPublicityKey(equipType, equipQuality):
    return equipType * 100 + equipQuality

def getGuildBossRankRewardKey(dungenNo, rankId):
    return dungenNo * 1000 + rankId

def checkTeamPassword(password):
    if len(password) == 0:
        return True
    return password.isdigit() and len(password) == TMMCD.datas['teamMatch_pwLen']['value']
