# -*- coding: utf-8 -*-
import sys, os
import KBEngine
import functools
import random
import time
import re
import functools
import enum
import MineGlobalData
import itemData_set as IDSD
import const_const as CSTD
import gearBase_gearConst as GBGCD
import gamePlay_gamePlay as GGD
import character_charData as CCDD
import wonderLand_floor as WL_FD
import branchData_branchData as BD_BDD


# baseapp和cellapp上都有的数据key
GLOBALDATA_KEY_SPACE_TO_ITS_BASE = 'kSpaceTobase'
GLOBALDATA_KEY_SPACENO_TO_SPACEID = 'kSpaceNoToSpaceID'
GLOBALDATA_KEY_SPACEID_TO_SPACENO = 'kSpaceIDToSpaceNo'
GLOBALDATA_KEY_BASEAPP = 'kBaseApps'
GLOBALDATA_KEY_BASEAPP_IDX = 'kBaseAppIndex'
GLOBALDATA_KEY_GAME_READY = 'kGameReady'
GLOBALDATA_KEY_APPCALL = 'kAppsCall'
GLOBALDATA_KEY_CELLAPP_CALL = 'kCellAppsCall'
GLOBALDATA_KEY_CREATE_BASEAPP = 'kCreateBaseapp'
GLOBALDATA_KEY_BASEAPP_READY = 'kBaseAppReady'
GLOBALDATA_KEY_ONLINE_NUM = 'kAccountNum'
GLOBALDATA_KEY_REG_NUM = 'kRegAccountNum'
GLOBALDATA_KEY_TODAY_REG_NUM = 'kTodayRegAccountNum'
GLOBALDATA_KEY_TOTAL_ONLINE_NUM = 'kAvatarNum'
GLOBALDATA_KEY_CELLAPP_INITED = 'kCellappInited'
GLOBALDATA_KEY_SVIP_ONLINE_NUM = 'kSVIPOnlineNum'

gameUpdateHertz = 10

# baseapp上的数据key定义
BASEAPP_DATA_KEY_SPACE_MARKER = 'kSpaceMarker'
BASEAPP_DATA_KEY_SPACE_TO_BASE = 'kSpaceToBase'

BASEAPP_STATE_LOCK_WAIT_FULL_PREPARE = 1

GLOBAL_BASE_STUB_ARCHIVE = [
    'GlobalMailStub',
    'SiegeWarStub',
    'CrossSiegeWarStub',
    'WorldBossStub',
    'RedBagStub',
    'MineWarStub',
    'BountyStub',
    'ResourceRecoveryStub',
    ]
GLOBAL_BASE_STUB_UNARCHIVE = [
    'PlayerStub',
    'TeamMatchStub',
    'RaidStub',
    'ItemLinkStub',
    'CrossServerStub',
    'GuildStub',
    'DropStub',
    'ActStub',
    'RaidMatchStub',
    'CrossDataStub',
    'WorldRefreshEntityStub',
    'AntiAddictionStub',
    ]
GLOBAL_BASE_STUB_TEAMSTUB = 'TeamStub'

GLOBAL_BASE_STUB_RAIDSTUB = 'RaidStub'

GLOBAL_BASE_STUB_STATISTICSTUB = 'StatisticStub'

SPACE_NO_DUNGEON_START = 1000
SPACE_NO_DUNGEON_END = 4999

SPACE_NO_HOME_INTERVAL = 10000
COPIED_SPACE_NO_START = 1*SPACE_NO_HOME_INTERVAL  #spaceNo in [1,1000] [1000*SPACE_NO_HOME_INTERVAL, 9999*SPACE_NO_HOME_INTERVAL]

SPACE_NO_HOME_SINGLE_DUNGEON = 6000
SPACE_NO_HOME_TEAM_DUNNGEON  = 4000
assert SPACE_NO_HOME_SINGLE_DUNGEON + SPACE_NO_HOME_TEAM_DUNNGEON == SPACE_NO_HOME_INTERVAL

INT32_MAX = 0x7FFFFFF

# INT32_MAX = int((1 << 31) - 1)
INT32_MIN = int(-(1 << 31))
UINT32_MAX = (1 << 32) - 1
UINT8_MAX = (1 << 8) - 1

INT64_MAX = (1 << 63) - 1
INT64_MIN = -(1 << 63)
UINT64_MAX = (1 << 64) - 1

# 场景类型
SPACE_TYPE_WORLD = 1

MIN_LEVEL = 1

SERVER_ID_BIT_SHIFT = 22
SERVER_TIMESTAMP_BIT_SHIFT = 26
GBID_TIME_BASE = 1517907600
GBID_TIME_INTERVAL = 5 * 60
GBID_TIME_UPDATE_INTERVAL = GBID_TIME_INTERVAL + 10
GBID_BASE = 2 ** (SERVER_ID_BIT_SHIFT + SERVER_TIMESTAMP_BIT_SHIFT)

OFFLINE_REASON_CLIENT_DEATH = 1
OFFLINE_REASON_DESTORY = 2
OFFLINE_REASON_MANNUALLY = 3
OFFLINE_REASON_GMKICK = 4
OFFLINE_REASON_CREATE_CELL_ERROR = 5
OFFLINE_REASON_NO_CLIENT_NEW_CHAR = 6
OFFLINE_REASON_SELECT_CHARACTER = 7
OFFLINE_REASON_LOSE_CELL = 8
OFFLINE_REASON_SPACE_GONE = 9
OFFLINE_REASON_INIT_ERR = 11
OFFLINE_REASON_CELLAPP_DEATH = 12
OFFLINE_REASON_KICK_BY_CENTRAL_SERVER = 14
OFFLINE_REASON_END_CROSS_SERVER = 15
OFFLINE_REASON_IDIP_DELETE_ACCOUNT = 17
OFFLINE_REASON_IDIP_PLAT_AUTHOR_CHANGE = 18
OFFLINE_REASON_SWITCH_SERVER = 19
OFFLINE_REASON_NEWBIE_KICKOUT = 20
OFFLINE_REASON_AUTH_NEED_RECONNECT = 22
OFFLINE_REASON_AUTH_LOW_MORAL = 23 # 善恶值太低，并且是代理状态
OFFLINE_REASON_ANIT_ADDICTION = 24

CENTRAL_SERVER_HEARTBEAT_INTERVAL = 10

ENTITY_POS_POLICY_MAX_NUM = 1000


GAME_CONFIG_TYPE_WONDER_LAND = 1
GAME_CONFIG_TYPE_SQUARE = 2
GAME_CONFIG_TYPE_ROLE_AUTHORIZATION = 3
GAME_CONFIG_TYPE_AUTO_COMBAT = 4

LEGAL_AGE_OF_MAJORITY = 18


# ======================
# 角色基础信息表 a
# 无任何前缀！纯字段名
# ======================
class AvatarFieldsEnum(enum.Enum):
    NAME = "sm_name"
    LEVEL = "sm_level"
    SCHOOL = "sm_school"
    TOTAL_SCORE = "sm_totalScore"
    SEX = "sm_sex"

    # 外观
    APPEARANCE_WEAPON = "sm_appearance_weapon"
    APPEARANCE_BREAST = "sm_appearance_breast"
    APPEARANCE_HAIR_ID = "sm_appearance_outfitData_hairId"
    APPEARANCE_CLOTHES_ID = "sm_appearance_outfitData_clothesId"
    APPEARANCE_PIC_FRAME_ID = "sm_appearance_outfitData_picFrameId"
    APPEARANCE_WING_ID = "sm_appearance_outfitData_wingId"
    APPEARANCE_MOUNT_ID = "sm_appearance_outfitData_mountId"
    APPEARANCE_FACE_SUIT_ID = "sm_appearance_faceData_suitId"
    APPEARANCE_FACE_HAIR_ID = "sm_appearance_faceData_hairIdFaceId"
    APPEARANCE_FACE_COLOR = "sm_appearance_faceData_hairColorIdSkinColorId"

# ======================
# 装备表 eq
# 无任何前缀！纯字段名
# ======================
class EquipFieldsEnum(enum.Enum):
    GRID_ID = "sm_gridId"
    ATTR_JSON = "sm_attrJson"
    ITEM_ID = "sm_itemId"
    CREATE_TIME = "sm_createTime"
    EXPIRE_TIME = "sm_expireTime"
    UNIQUE_ID = "sm_uniqueId"
    BIND_TYPE = "sm_bindType"
    LOCK_STATUS = "sm_lockStatus"


class UniqueIntEnum(type):
    def __new__(cls, name, bases, dct):
        __excluded_fields__ = dct.get('__excluded_fields__', ())
        __include_fields__ = dct.get('__include_fields__', ())
        _unimap = {}
        for _key, _value in dct.items():
            if _key.startswith('__'):
                continue
            if not isinstance(_value, int):
                continue
            if __include_fields__ and _key not in __include_fields__:
                continue
            if __excluded_fields__ and _key in __excluded_fields__:
                continue
            if _value in _unimap:
                _errstr = f"class {name} setattr err, {_key}/{_unimap[_value]}={_value}"
                raise AttributeError(_errstr)
            _unimap[_value] = _key
        return type.__new__(cls, name, bases, dct)

AGGRO_TRIGGER_TRAP = 1
AURA_TRAP = 2
CATCH_TRAP = 3
AOI_EXIT_TRAP = 4
LARGE_ENTITY_VISIBILITY_TRAP = 9
LARGE_ENTITY_HYSTERESIS_TRAP = 10
ESCORT_ROUTE_TRAP = 12


class StateEnum(metaclass=UniqueIntEnum):
    Idle = 0
    Moving = 1
    Shifting = 2
    Fighting = 3
    Death = 4
    Down = 5
    Stunned = 6
    Slow = 7
    Silenced = 8
    Snare = 9
    Frozen = 10
    PImmortal = 11
    MImmortal = 12
    GeneralAttack = 13
    UsingSkill = 14
    Casting = 15
    Channeling = 16
    moveSkill = 17
    moveChannel = 18
    speicalSkill = 19
    Dodging = 20
    Jump = 21
    doubleJump = 22
    Fall = 23
    speedFall = 24
    clientPick = 25
    Sprinting = 26
    Teleporting = 27
    Flying = 28
    bePushed = 31
    riding = 33
    Teleport = 34
    autoFight = 37
    serverControl = 43
    posture = 47

    _stateValMap = {}

    _moveConflictState = []

    breakSkillStates = (Down, Stunned, Frozen)

    @staticmethod
    def _allStates():
        attrs = dir(StateEnum)
        realAttrs = {}
        for attrName in attrs:
            if not attrName.startswith('_'):
                realAttrs[attrName] = getattr(StateEnum, attrName)
        return realAttrs


class RemoveStateReason(metaclass=UniqueIntEnum):
    NORMAL = 0  # 逻辑手动调用的
    OFFLINE = 1
    CONFLICT = 2
    TELEPORT = 3
    EXIT_DUEL = 4
    SKILL_DONE = 5
    CANCEL_GATHER = 6


class LineSubType(metaclass=UniqueIntEnum):
    world = 1
    pressLine = 2


SPACE_NO_INTERVAL = 10000
COPIED_SPACE_NO_START = 1 * SPACE_NO_INTERVAL


class SpaceSubType(metaclass=UniqueIntEnum):
    World = 1
    Yanwu = 2 # 演武场
    Boss = 5 # 大世界boss场景


class SpaceType(metaclass=UniqueIntEnum):
    UnKownSpaceType = 0
    SpaceWorldDungeon = 1
    SpaceNormalDungeon = 2
    SpaceCube = 3
    SpaceLine = 6
    SpaceWonderLand = 7
    SpaceSiegeWar = 8
    SpaceGuild = 9

    @staticmethod
    def getClonedSpaceNoRange(mapId):
        start = mapId * SPACE_NO_INTERVAL
        return (start, start + SPACE_NO_INTERVAL)

    @staticmethod
    def getSingleDungeonSpaceRange(mapId):
        start = mapId * SPACE_NO_HOME_INTERVAL
        return (start, start + SPACE_NO_HOME_SINGLE_DUNGEON)

    @staticmethod
    def getTeamDungeonSpaceRange(mapId):
        start = mapId * SPACE_NO_HOME_INTERVAL + SPACE_NO_HOME_SINGLE_DUNGEON
        return (start, start + SPACE_NO_HOME_TEAM_DUNNGEON)

    @staticmethod
    def getDungeonSpaceRange():
        start = SPACE_NO_DUNGEON_START*SPACE_NO_HOME_INTERVAL
        end = SPACE_NO_DUNGEON_END*SPACE_NO_HOME_INTERVAL
        return (start, end)


class Sex(metaclass=UniqueIntEnum):
    MALE = 1
    FEMALE = 2

    OPPOSITE_WHOLE = MALE + FEMALE


class MapIdDef(object):
    mapUnknown = 0
    mapXinYuanCheng = CSTD.datas['defaultGamePlayID']['value']
    mapDuelGround = 7000
    mapSpecial = 999           #大地图预loading场景

    mapWorldSet = {i for i in GGD.mapWorldSet}

MapIdDef.mapWorldSet.add(MapIdDef.mapDuelGround)

class SpaceLayer(object):
    COMMON = 0
    AIRWALL = 1
    DEFAULT = AIRWALL


INIT_CLIENT_SEND = (
    # 第一个是函数名， 第二个代表OB客户端是否需要下发
        ('sendBagData', True),
        ('sendVariableData', True),
        ('sendServerOpenTime', True),
        ('sendTaskList', True),
        ('sendCliSkillBuildInfo', True),
        ('sendCliConfigData', False),
        ('sendOutfitData', True),
        ('sendLingShouInfo', True),
        ('emitMiniPayload', True),
        ('_sendFriendInfoToClient', True),
        ('sendPlayerPayInfo', True),
        ('sendHolidayPayInfo', True),
        ('_sendGuildInfo', True),
        ('sendDrawCardInfo', True),
        ('sendGuildTrains', True),
        ('_sendAchievementInitData', True),
        ('sendAllEnemyDatas', True),
        ('_sendDropEquipInfo', True),
        ('sendCollectInfo', True),
        ('sendWonderLandLoginData', True),
        ('sendSiegeWarLoginData', True),
        ('sendAllWelfareSignInInfo', False),
        ('avatarLogin', True),
        ('_sendAllGuildRelation', True),
        ('redbagOnLogin', True),
        ('checkOfflineHangup', True),
        ('onMineWarLogin', True),
        ('updateRedisVIPFlag', True),
        ('sendClaimPcLoginRewardInfo', True),
        ('sendAvatarBountyInfo', True),
        ('getAnnouncement', True),
        ('sendMineWarState', True),
)

class ItemType(object):
    Normal = 0
    LingShou = 1
    Resource = 2
    Title = 4


class ItemSubType(object):
    Normal = 0
    LingShouEgg = 0
    HEAL_HP = 1
    HEAL_MP = 2
    Equipment = 4
    EQUIP_CORE = 6
    TASK = 15
    EQUIP_SOUL = 27
    ExtractReward = 52

class LingShouSubType(object):
    Egg = 0
    Equipment = 1

class EntityPropsEnum(metaclass=UniqueIntEnum):
    commonCastCtx = 4
    callbackTmpInfo = 5
    channelSkillTimer = 6
    currentUseSkill = 7
    pendingCheckUseItem = 8

    lastTeleportSpaceNoRecord = 10
    backAccount = 11

    equipDressTempData = 14
    useBagItemData = 15
    RecordLogData = 16
    largeEntTrapId = 17

    # 使用统一的大世界记录
    # - 大世界记录
    # - 进入副本在大世界分线记录(单人/组队/团队)
    # - 进入家园...记录
    # - 进入帮会...记录
    outsideRecords = 18
    logonCreateCellCB = 19
    lastUpdateAreaPos = 20
    gameLengthMarkTime = 21
    updateWorldLineAreaTimer = 22
    taskAreaTarget = 23
    reliveLimitTimeRecord = 24
    spaceEnterT = 25
    aiController = 26
    lastTeleportWorldlinePosRecord = 27
    lastBreakAwayTime = 28
    pendingUseItem = 29
    disableTimerNumErrMsg = 30
    timerNumErrMsgTS = 31
    isCreatingAvatar = 32
    teamInviteRecord = 33
    gatherTarget = 34
    hateRecord = 36
    isResetingSkill = 37
    teamDungeonTeammateConfirmRecord = 38
    teamJoinRecord = 40
    raidJoinRecord = 42     # 团队申请加入记录, 记录在申请者身上
    oldOutfitData = 43
    hpPercent = 46
    mpPercent = 47
    isHpLocked = 51
    avatarScoresInitChecklist = 62
    currentCastingSkill = 65
    currentChannelSkill = 66
    getTeamListRecordData=73
    effectSetProps = 76
    raidDungeonCheckRecord = 81
    chongfengData = 84
    lockMinHp = 96
    mountIllegalTimer = 104
    teamPlayerUploadCacheDict = 112
    lungeSkillData = 130
    dodgeSkillData = 154
    offlineTimeForRestoreBuff = 155
    initAwardFightPropsKey = 156
    isMoralValueChanged = 173
    escortSpeedOverwriteData = 177
    shiftOrDodgeTimer = 182
    CrusadeDunAutoConfirmConfig = 183
    creationEffectEntIds = 187
    crossServerMethodSyncToLocalServerBase = 196
    crossServerMethodSyncToLocalServerCell = 197
    crossServerWaitingClientInitTuple = 198
    crossServerWaitingClientInitTimerId = 199
    crossServerLocalSignInLockBase = 201
    crossServerInitMsgBlockEndTBase = 205
    crossServerInitMsgBlockEndTCell = 206
    AvatarActiveTimestamp = 242  # 玩家活跃时间戳
    cubeAutoRenewSwitch = 244 # 立方房间自动续费开关
    cubeRoomRewardList = 245 # 立方房间奖励列表
    cubeRandRoomCD = 246 # 立方房间随机房间CD
    friendInitStatus = 248
    friendInitEvent = 249
    guildInitEvent = 250
    guildInitStatus = 251
    guildJoinContext = 252
    guildTrainInitCell = 253
    guildTrainInitScore = 254
    firstFly = 256
    equipDropInitStatus = 257
    equipDropInitEvent = 258
    wonderLandSwitch = 260
    wonderLandRewardList = 262

    raidTickTimerId = 300
    raidCreateRaidTeamCheck = 301
    raidBeInvitedRecord = 302
    raidJoinRecord = 303
    raidAvatarPropsCache = 304

    duelRequestId = 305
    currentRecvDuelReqId = 306
    duelReqEndTime = 307
    RecvDuelReqEndTime = 308
    ChiefDunAutoConfirmConfig = 309

    getRaidListRecordData=310
    newbieStepCellCache = 311
    newbieCreateCellCB = 312
    blazeStartTime = 313
    blazeId = 314
    petEquipNumCache = 316
    isLightningArea = 317

    reqSubmitTaskList = 331
    spawnSummonByAI = 332
    spawnSummonList = 333
    fromCubeMapId = 334
    # 自己发送给别人的授权申请信息
    authRoleInfo = 335
    # 自己收到别人发送的授权申请信息
    recvAuthRoleInfo = 336

    teamStatisticDataRecord = 340
    teamStatisticDataDict = 341
    statisticDataRecord = 342
    statisticDataRecordSpaceNo = 343

    deadLaterCallbackInfo = 350

    attachedIDList = 361
    beAttachedHostID = 362
    popRewardItemsDict = 363

    tempBindPhone = 365
    reqBindPhoneCnt = 366
    resetBindPhoneCntTime = 367
    reqBindPhoneTimestamp = 368
    verifyCodeTimestamp = 369
    firstPcLoginTimestamp = 370
    claimPcLoginRewardTimestamp = 371
    autoCombatStartTimestamp = 372
    takeDropInfo = 373

    creationOrder = 390
    lastLoginTime = 391
    cellTotalScore = 392
    cellExperience = 393
    cellMapId = 394

    publishBounty = 400
    acceptBounty = 401
    bountyInfoInited = 402
    waitForBountyInfoInitedTimer = 403
    waitForBountyInfoInitedTimer1 = 404
    idleChangeSpeed = 405
    blazeTimer = 406

    recordPreReport = 410
    preReport = 411
    reportTimestamp = 412
    clientIdleChangeSpeed = 413

class TopSpeedType(object):
    NormalTopSpeed = 100.0
    ShiftingSkillTopSpeed = 5000.0
    TeleportSkillTopSpeed = 10000.0
    FlyingTopSpeed = 1000.0


CELL = 0
BASE = 1
ALL = 2
CLIENT = 3

DEFAULT_AOI = 30.0
DEFAULT_HYST = 5.0
HOME_AOI = 30.0
LARGE_ENTITY_VISIBILITY_TRAP = 9
LARGE_ENTITY_HYSTERESIS_TRAP = 10

DEFAULT_DIRECTION = (0, 0, 0)




STATIC_SPACENOS = (1,)
SPACE_FIX_POS = (0, 0, 0)
CARRIER_FIX_DIS = 2

HOTFIX_PATH = KBEngine.matchPath("scripts/data/hotfix.lua")


class ItemId(object):
    COIN = IDSD.datas['itemID_coin']['value'] # 铜币
    EXP = IDSD.datas['itemID_exp']['value']
    MONEY = IDSD.datas['itemID_money']['value'] # 金币
    DARK_IRON = IDSD.datas['itemID_darkiron']['value']
    COMMON_EQUIPMENT_ID = GBGCD.datas['gearGeneralItemId']['value']
    GUILD_CONTRIB = IDSD.datas['itemID_curGuildContribution']['value']
    GUILD_MONEY = IDSD.datas['itemID_guildMoney']['value']
    GUILD_FUND = IDSD.datas['itemID_guildCoin']['value']
    GUILD_EXP = IDSD.datas['itemID_guildExp']['value']
    COLL_SKIP_MSG_HANDLE = ()
    BIND_MONEY = IDSD.datas['itemID_bind_money']['value']
    APPEARANCE_COIN = IDSD.datas['itemID_appearanceCoin']['value']

class ItemBindType(object):
    BIND = 0
    NORMAL = 1
    BINDTYPE_NOT_SPECIFIED = 2
    VALID_BIND_TYPE = (BIND, NORMAL, BINDTYPE_NOT_SPECIFIED)

class ItemExType(object):
    NORMAL = 1
    SELECTION = 2


class GmModeEnum(object):
    ALL_MODES = []

    _modeIdGen = (i for i in range(20))

    @staticmethod
    def generateModeId(modes, gen):
        m = next(gen)
        modes.append(m)
        return m

    GM_NONE = generateModeId.__func__(ALL_MODES, _modeIdGen)
    GM_NORAML = generateModeId.__func__(ALL_MODES, _modeIdGen)
    GM_NO_SKILLCD = generateModeId.__func__(ALL_MODES, _modeIdGen)


class EnterLineCodeEnum(object):
    ENTER_CHECK_SUCCESS = 0
    ERR_REACH_MAX_MEMBER = 1
    ERR_ONLY_TEAM_MEMBER = 2
    ERR_EXLUDE = 3
    ERR_COMMON = 4
    ERR_NOT_GUILD_MEMBER = 5
    ERR_REACH_MAX_GUILD_MEMBER = 6
    ERR_SPACE_IS_NOT_READY = 7
    ERR_CANNOT_AUTO_ENTER = 9
    ERR_REACH_AREAM_MAX = 10
    ERR_REACH_AREAM_LIMIT = 11
    ERR_REACH_SEC_LIMIT = 12
    ERR_MERGE_LINE = 13
    ERR_REACH_MAX_AVATAR_COUNT = 14

class StreamStringID(object):
    NIL = 0
    GUILD_LOGS_INFO = 4
    WAREHOUSE_INFO = 6
    WAREHOUSE_SORT_INFO = 7
    NORMAL_BAG_INFO = 8
    NORMAL_BAG_SORT_INFO = 9
    LINGSHOU_BAG_INFO = 10
    CLIENT_CONFIG_RECORD = 11
    TASK_LIST_DATA = 12
    COIN_AUCTION_SALE_RECORD = 13
    COIN_AUCTION_BUY_RECORD = 14
    BODY_EQUIP_DATA = 19
    HOTFIX_DATA = 23
    PET_DRAW_CARD_RECORD = 26
    ACHIEVEMENT_DATA = 27
    PLAYER_INFO_DATA = 28
    BOUNTY_RANK_DATA = 29


class UseItem(object):
    TRUE = 1
    FALSE = 2
    PENDING = 3


class ReloginType(object):
    NONE = 0
    FULL_RELOGIN = 1  # 从登陆界面重登
    HALF_RELOGIN = 2  # 游戏内断线重连了


class BagType(object):
    BAG_TYPE_NORMAL = 0
    BAG_TYPE_LINGSHOU_PEN = 1  # 宠物背包
    BAG_TYPE_WAREHOUSE = 2


class BagOPStat(object):
    OPERATE_BAG_STAT_OK = 0
    OPERATE_BAG_DATA_ERR = 1
    OPERATE_BAG_STAT_ERR = 2
    OPERATE_BAG_NO_SPACE = 3
    OPERATE_BAG_BAG_TYPE_ERR = 4
    OPERATE_BAG_ITEMS_NOT_ENOUGH = 5
    OPERATE_BAG_ITEM_EXPIRED = 6
    OPERATE_BAG_LEVEL_ERR = 7
    OPERATE_BAG_CD_ERR = 8
    OPERATE_BAG_ADD_NUM_ERR = 9
    OPERATE_BAG_CANT_BE_DROP = 10
    OPERATE_BAG_BAG_LOCKED = 11
    OPERATE_BAG_DAILY_LIMIT = 14
    OPERATE_BAG_PENDING = 15
    OPERATE_BAG_MAIL_ITEM_REACH_LIMIT = 18
    OPERATE_BAG_REUSE_ITEM_USE_TIMES_FAILED = 19
    OPERATE_BAG_ITEM_DISABLED = 20
    OPERATE_BAG_ITEM_LOCKED = 21
    OPERATE_BAG_ARG_ERR = 22

class BagOpPlan(object):
    OPERATE_BAG_NO_PLAN = 1
    OPERATE_BAG_OK = 2


GAME_REFRESH_OCLOCK = 5

ONE_MINUTE_COST_SECONDS = 60
ONE_DAY_COST_SECONDS = 86400
ONE_HOUR_COST_SECONDES = 3600
HALF_HOUR_COST_SECONDS = 1800
ONE_WEEK_COST_SECONDS = 7 * ONE_DAY_COST_SECONDS
GENERAL_CYCLE_TIME = GAME_REFRESH_OCLOCK * 3600
FIX_TIME = time.localtime(0).tm_hour
FIX_TIME_SECONDS = FIX_TIME * 3600


# 玩家角色状态，
# 0：正常状态
# 1：被删除，标脏
class AvatarFlag(object):
    normal = 1
    delete = 2


class KickAvatar(object):
    none = 0
    kicking = 1
    kicked = 2


class LoginState(object):
    NORMAL = 1
    AVATAR_EXIST = 2


class SignInClientState(object):
    cover = 1
    add = 2
    delete = 3


class WitnessTypeEnum(object):
    WITNESS_ENUM_HIDE = 0
    WITNESS_ENUM_ALL = 1
    WITNESS_ENUM_NAME = 2
    WITNESS_ENUM_IGNORE = 3


class CreateAvatarRes(object):
    OK = 0
    CRS_NAME_DUPLIATED = 1
    CRS_NAME_INVALID = 2
    CRS_ADDICT_JUDGE_FAILED = 3
    CRS_NAME_LENGTH_OVERLIMIT = 4
    CRS_DATABASE_OPR_ERROR = 5
    CRS_GEN_GBID_FAILED = 6
    CRS_CREATE_ENTITY_ERR = 7
    CRS_WRITE_ENTITY_ERR = 8
    CRS_GBID_ERR = 9


class ReourceValType(object):
    UINT32 = 1
    INT32 = 2
    UINT64 = 3
    INT64 = 4
    UINT8 = 5
    DOUBLE = 6


class ReourceMaxValue(object):
    Fraction_MAX = 99


# Match Chinese: \u4e00-\u9fa5
# Match Hiragana: \u3040-\u309F
# Match Katakana: \u30A0-\u30FF
RE_VALIDATE_AVATAR_NAME_COMPILE = re.compile(r'''[\u4e00-\u9fa5]+''')

HTTP_COMMON_HEADER_TUPLE = (
    ('Content-Type', 'application/json'),
    ('cache-control', 'no-cache')
)


class SpaceEnterScene(object):
    DENY = 1
    ALLOW = 2
    ALLOW_CAST = 3


GM_ACCOUNT_LIST = []


class KBEDebugLogLevel(object):
    DEBUG = 1
    INFO = 2
    WARN = WARNING = 3
    ERROR = FATAL = 4


class ClaimTaskSrcEnum(object):
    TASK_SRC_UNKNOWN = 0
    TASK_SRC_NORMAL = 1
    TASK_SRC_GM_FINISH_NEWBIE = 2
    TASK_SRC_GM = 3
    TASK_SRC_JUMP_GAME = 4
    TASK_SRC_MONSTER_NEARBY = 5
    TASK_SRC_ROUND_AUTO_CLAIM = 6
    TASK_SRC_ENTRUST_ACTIVITY = 7
    TASK_SRC_REWARD_TASK = 8
    TASK_SRC_INIT_NEWBIE_TASK = 9
    TASK_SRC_FROM_ACTION = 10
    TASK_SRC_NPC_DIALOG = 11


class EntNumPerPlayerInAOI(object):
    worldLine = 15
    singleDungeon = 5
    teamDungeon = 3


class TeleportLockEnum(metaclass=UniqueIntEnum):
    FREE_TO_TELEPORT = 0
    ENTER_CUBE = 1
    ENTER_WONDERLAND = 2
    ENTER_LINE = 7
    SWITCH_LINE = 8
    ENTER_DUNGEON = 9
    ENTER_SINGLE_DUNGEON = 12

    UNKNOWN = 255


POSITION_ZERO = (0.0, 0.0, 0.0)
DIRECTION_ZERO = (0.0, 0.0, 0.0)

WORLD_LINE_BASE_WEIGHT = 50
WORLD_LINE_UPDATE_WEIGHT_VAL = 10


class TaskCycleType(object):
    CYCLE_TASK_ENUM_NONE = -1
    CYCLE_TASK_ENUM_DAYLY = 0
    CYCLE_TASK_ENUM_WEEKLY = 1
    CYCLE_TASK_ENUM_ONCE = 2


TASK_EVENT_CLAIM = 1
TASK_EVENT_SUBMIT = 2
TASK_EVENT_QUIT = 3


class TaskStatEnum(object):
    TASK_STAT_DEFAULT = TASK_STAT_UNKNOWN = 0
    TASK_STAT_OPEN = 1
    TASK_STAT_CAN_CLAIMED = 2

    TASK_STAT_RUNNING = 3
    TASK_STAT_FINISHED = 4  # 任务目标完成及子任务已提交，非最终状态；
    TASK_STAT_SUBMITTED = 5
    TASK_STAT_FAILED = 6 # 失败
    TASK_STAT_QUIT = 7 #放弃


class TaskType(object):
    TASK_TYPE_NONE = 0
    TASK_TYPE_MAINLINE = 1  # 主线
    TASK_TYPE_SUBLINE = 2  # 支线
    TASK_TYPE_DAYLY = 3  # 日常
    TASK_TYPE_ACTIVITY = 4  # 活动
    TASK_TYPE_HOOK = 5  # 挂机
    TASK_TYPE_HOOK_REWARD = 6  # 悬赏挂机任务
    TASK_TYPE_CRUSADE = 7 # 讨伐任务
    TASK_TYPE_SPIRIT = 8 # 附灵任务

class TaskNotSuccReasonEnum(object):
    UNKNOWN = 0
    MANUAL_QUIT = 1  # 手动放弃任务
    QUIT_ACT = 2  # 主动退出任务关联的活动
    TIMEOUT = 3  # 任务关联的活动超时
    FROM_TEAM_CAPTAIN = 4  # 队长任务失败，队员同步到失败状态
    DROP_TASK_ITEMS = 5  # 丢弃任务物品
    LEAVE_TEAM = 6  # 离开队伍
    AUTO_QUIT = 7  # 任务失败自动放弃
    LEAVE_SPACE = 8  # 离开场景
    VARIABLE = 9  # 变量条件
    CHILD_FAILED = 10  # 子任务失败
    AVATAR_DIE = 11  # 角色死亡
    GUILD_MODIFY = 12  # 帮会信息改变
    FAIL_ACTION = 13  # event-action
    LEAVE_AREA = 14  # 离开区域
    ENTER_AREA = 15  # 进入区域
    DUNGEON_CTRL = 16  # 副本流程
    NPC_GUIDE = 17  # npc引导
    REFRESH = 18  # 刷新任务，旧任务失败
    LEAVE_SPACE_CHECK = 19  # 登陆检测离开副本失败
    LEAVE_SPACE_CLIENT_REPORT = 20  # 登陆检测离开副本失败
    GM = 21  # GM指令
    NPC_DIALOG = 22  # 与npc交谈触发
    LOGIN_AUTO_QUIT = 23  # 登录自动放弃任务
    GROUP_TIMEOUT_QUIT = 24  # 任务组过期放弃


class VarChangeSrcEnum(object):
    VAR_SRC_TASK_CLAIM = 1
    VAR_SRC_TASK_QUIT = 2
    VAR_SRC_TASK_SUBMIT = 3
    VAR_SRC_SPACE = 4
    VAR_SRC_GM = 5
    VAR_SRC_AI = 16
    VAR_SRC_BODY_EQUIP_ADD = 17
    VAR_SRC_BODY_EQUIP_REM = 18
    VAR_SRC_ENTER_MOUNT = 24
    VAR_SRC_EXIT_MOUNT = 25
    VAR_SRC_COMM_ACTION = 26


class TaskOpTypeByTalkToPNC(object):
    CLAIM_TASK = 1
    SUBMIT_TASK = 2
    FAIL_TASK = 3
    NPC_TALK_TARGET = 4


class CommActionSrcType(object):
    TASK = 1
    DIALOG = 2


class TaskTargetType(object):
    # 任务目标
    TARGET_UNKNOWN = 0
    TASK_TARGET_MONSTERS = 1    #杀怪
    TASK_TARGET_ITEMS = 2       #收集道具
    TASK_TARGET_TALK_NPC = 3    #对话npc
    TASK_TARGET_REACH_AREA = 4  #到达区域
    TASK_TARGET_LEVEL = 6       #到达等级
    TASK_TARGET_COUNT = 7       #计数
    TASK_TARGET_COLLECT = 8     #交互采集物
    TASK_TARGET_MONSTER_CARD = 9#激活怪物图鉴
    TASK_TARGET_RELATE_TASK = 10#关联任务
    TASK_TARGET_ACTION = 11     #完成行为（释放技能）
    TASK_TARGET_CINEMA = 12     #播放剧情
    TASK_TARGET_VAR = 13        #变量
    TASK_TARGET_COUNTER = 14    #目标计数


PLAYER_REGISTER_STUB_NUM = 1


class EventActionSrc(object):
    SRC_CLAIM_TASK = 0
    SRC_SUBMIT_TASK = 1
    SRC_QUIT_TASK = 2
    SRC_DIALOG = 3
    SRC_COLLECTION = 4
    SRC_CINEMA = 5
    SRC_ROUND_TASK = 6


class ForceTypeEnum(object):
    UnKownForceType = 0
    Player = 1
    Monster = 2
    Friend = 3
    Guild = 4
    Neutrality = 5
    NPC = 6

    forceEnums = ("UnKownForceType", "Player", "Monster", "Friend", "Guild", "Neutrality", "NPC")
    dunForce = (
        Monster,
        NPC,
        Neutrality,
        Friend
    )

    @staticmethod
    @functools.lru_cache(8, typed=False)
    def getForceType(typeId):
        if ForceTypeEnum.Player <= typeId <= ForceTypeEnum.NPC:
            return ForceTypeEnum.forceEnums[typeId]
        else:
            return ForceTypeEnum.forceEnums[0]


class CollectionType(object):
    NORMAL = 0
    MINERAL = 1
    ZHEN_QI = 2
    PERSONAL_BOX = 3
    VIEWPOINT = 4
    SUMMON_OBJECT = 5 # 召唤物件
    DECAY_BOX = 7 # 衰减宝箱
    MINE_DROP = 8 # 矿战掉落采集物

    VALID_RANGE_ACHIEVEMENT = (MINERAL, ZHEN_QI, PERSONAL_BOX, VIEWPOINT)
    VALID_RANGE_CHECK = (NORMAL, MINERAL, ZHEN_QI, PERSONAL_BOX, VIEWPOINT, SUMMON_OBJECT, DECAY_BOX, MINE_DROP)
    ADD_PICK_AVATAR_CNT = (PERSONAL_BOX, VIEWPOINT, MINE_DROP)

class CollectionPickType(object):
    Countdown_1 = 0  # 读条采集，客户端不屏蔽UI点击
    Countdown_2 = 9  # 读条采集，客户端会屏蔽UI点击
    CountdownAndClientJudge_1 = 1

    CountdownTypes = (Countdown_1, Countdown_2, CountdownAndClientJudge_1)
    ClientJudgeTypes = (CountdownAndClientJudge_1,)


class IDIPBanType(object):
    CHAT = 1


class GMCommandErr(object):
    GM_RET_OK = 0
    GM_RET_TARGET_NOT_EXISTS = 1
    GM_RET_DB_OP_ERR = -3
    GM_RET_ARGS_ERR = -101
    GM_RET_INVALID_CMD = -102
    GM_RET_INVALID_JSON_RESPONSE = -103
    GM_RET_TARGET_OFFLINE = -104
    GM_RET_CMD_SERIAL_EXISTS = -105
    GM_RET_BAN_TYPE_INVALID = -106
    GM_RET_WRITE_TO_DB_ERROR = -107
    GM_RET_MODIFY_TEXT_CHECK_FAILED = -108
    GM_RET_NAME_DUPLICATE = -110
    GM_RET_ACCOUNT_INVALID = -111
    GM_RET_ALREADY_DONE = -112
    GM_RET_INSUFFICIENT = -113
    GM_RET_INTERNAL_ERROR = -114
    GM_RET_NO_COIN = -115
    GM_RET_DB_STATUS_ERR = -118
    GM_RET_REDIS_OP_ERR = -119
    GM_RET_MAX_LIMIT_ERR = -120
    GM_RET_ADD_WEALTH_FAILED = -121
    GM_RET_AFTER_SALE_ERR = -122
    GM_RET_SEND_MAIL_ERR = -123


GM_RAW_PLAYER_FIELDS = 4


class MapRefreshType(object):
    SEC = 0
    HOUR = 1
    DAY = 2
    WEEK = 3

    @staticmethod
    def countSec(params):
        (period, num) = params
        if period == MapRefreshType.SEC:
            return num
        elif period == MapRefreshType.HOUR:
            return num * 3600
        elif period == MapRefreshType.DAY:
            return num * 24 * 3600
        elif period == MapRefreshType.WEEK:
            return num * 7 * 24 * 3600
        else:
            return 0


class STORE_TYPE:
    EXCHANGE_STORE1 = 3
    EXCHANGE_STORE2 = 5


class BaseAppIniting(object):
    LOAD_ENTITY_DBID = 'load-entity-dbid'


class VariableType(object):
    VAR_TYPE_SPACE = 1
    VAR_TYPE_AVATAR = 2


class LoadEntitySetting(object):
    BATCH_DELAY = 0.2


class LogType(object):
    # 不同的type决定不同的格式和写日志方式
    NORMAL = 1
    WLOG = 2
    TLOG = 3


class RedisKey(object):
    IDIPMARQUEE_KEY = "__IDIPMARQUEE_KEY__"
    avatarNameTbl = 'global:avatar_names'
    LOGIN_ACCOUNT_GBID_KEY = "__LOGIN_ACCOUNT_GBID_KEY__"
    WP_WHITE_LSIT_KEY = "__WP_WHITE_LSIT_KEY__"
    GUILD_NAME_TBL = 'global:guild_names'
    GIFT_CODE_TBL = 'global:gift_codes'
    PRIVILEGE_TBL = 'g:vip'
    LEVEL_RUSH_RANK_DATA_KEY = 'g:alrr'
    NORMAL_ONLINE_NUM = 'g:normal_online_num'
    SERVER_OPEN_TIME = 'g:server_open_time'
    SERVER_OPEN_STATE = 'g:server_open_state'
    FULL_PLAYER_INFO_KEY = 'g:full_player_info'

class ForbidType(object):
    SHORT_FORBID = 1  # 临时封禁
    FOREVER_FORBID = 2  # 永久封禁


INVITE_CODE_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class OnLoseCellReason(object):
    DEFAULT = 0
    CELLAPP_DEATH = 1
    ENTIRE_DESTROY = 2
    CELL_SAFE_DESTROY = 3


class ClientUploadDataType(object):
    EMULATOR_INFO = 1
    TYPE_END = 2


READ_MAIL_EXPIRE_TIME = 7 * ONE_DAY_COST_SECONDS
NEW_MAIL_EXPIRE_TIME = 30 * ONE_DAY_COST_SECONDS


class MailDeleteReason(object):
    EXPIRE = 1
    DELETE_READ = 2


class MailAttachState(object):
    NotGet = 0
    HasGET = 1


class MailReadState(object):
    NotRead = 0
    HasRead = 1


class ModifyNameResult(object):
    success = 0
    internalError = 1
    nameExist = 2
    noItem = 3
    nameInvalid = 4


class LuaScriptID:
    GET_USERS_INFO = 2
    FRIEND_INIT = 3
    SEND_FRINED_REQUEST = 4
    SEND_FRIEND_MSG = 5
    GET_FRIEND_MSG = 6
    SET_MAX_NUMBER = 7
    CHECK_AND_SET_SVIP = 8


class AvatarPhotoType(object):
    AvatarPhoto = 1
    AvatarFrame = 2


class ChatSysGMErr:
    OK = 0
    FAIL = 1
    DBERR = 2

CREEP_TAG_LARGE_ENT = 1 # 超大视野的实体
CREEP_TAG_DEATH_MSG = 2 # 死亡会喊话
CREEP_TAG_WARNING_RANGE = 4 # 有预警范围
CREEP_TAG_WONDERLAND_FIXED_BOSS = 5 # 天劫崖固定boss
CREEP_TAG_WONDERLAND_SUMMON_BOSS = 6 # 天劫崖召唤boss
CREEP_TAG_ANTI_TAUNT = 98 # 嘲讽反制
CREEP_TAG_ANTI_MOVE = 99 # 推拉反制

class SkillTag(metaclass=UniqueIntEnum):
    Hot = 13
    Heal = 14
    SingleHeal = 20
    Casting = 24
    Channel = 25
    NeedNoTargetInCasting = 27
    TeleportSkill = 40
    ShiftSkill = 46
    IgnoreImmortal = 54
    MulStageSkill = 58
    Chongfeng = 55
    Lunge = 56
    BlinkToTarget = 57
    AutoCombat = 63
    DoActionTogether = 64  # 技能action就执行一次,在action里结算各个目标
    FightStateSkill = 75
    HealSkill = 76
    LingzhuSkill = 80
    revolveSkill = 97
    randomTarget = 98
    GeneralSkill = 99
    UltraSkill = 100
    talentSkill = 110
    changeCDStatusSkill = 130
    DodgeSkill = 146

class BuffTag(object):
    TagSeeHiddenEnt = 41
    TagGuildLeague = 48
    TagGuildLeagueCollectionBuff = 49
    TagDungeon = 50
    TagBattleFieldSpaceTag = 45
    TagGuildBattleTempPointTag = 46
    TagBTFSLPDungeonRebornTag = 47
    TagDisableSelfHiddenTag = 98


class BuffKind(object):
    KindNegative = -1
    KindControlled = -2
    KindPhysicalDoT = -3
    KindMagicalDoT = -4


class BuffSrcTypeEnum(object):
    Unknow = 0
    Combat = 1


class SkillScopeEnum(metaclass=UniqueIntEnum):
    CIRCLE_CENTER_SELF = 1  # 1=以自身为中心的圆形范围  参数=半径
    CIRCLE_CENTER_TARGET = 2  # 2=以目标为中心的圆形范围  参数=半径
    SELF_TO_TARGET_RECTANGLE = 3  # 3=以目标为方向，以自身为起点的矩形 参数=direction
    USER_DEFINED_SECTOR = 4  # 4=双摇杆扇形,自身为圆心 参数==direction
    USER_DEFINED_RECTANGLE = 5  # 5=双摇杆矩形 参数=direction
    USER_DEFINED_CIRCLE = 6  # 6=双摇杆圆形范围 参数=direction+percent
    MI_CENTER_SELF = 7  # 7=米字型区域
    HALF_MI = 8  # 8=米字前三条
    TARGET_LINKED = 9  # 9=目标周围一定范围内链状目标：闪电链
    TARGET_AUTO = 10  # 10=与不填scope一样，程序内默认选一个
    COLOSSUS_CIRCLE = 11  # 11=巨人发出的circle攻击，主要目标点依据地编位置
    COLOSSUS_RECTANGLE = 12  # 12=等价于5,用于让客户端特殊处理
    CURRENT_DIRECTION_RECTANGLE = 13  # 13=实时朝向的双摇杆矩形
    ANNULAR_CENTER_SELF = 14  # 14=以自身为中心的环形范围 参数=最小半径+最大半径
    MULTI_SECTOR = 15  # 15=以自身为圆心的多个扇形 参数=direction

class EffecType(object):
    ENUM_EFFECT_UNKNOW = 0
    ENUM_EFFECT_BASIC = 1
    ENUM_EFFECT_BY_EVENT = 2
    ENUM_EFFECT_BY_TIMER = 3


class SkillCategory(object):
    CATEGORY_GENERAL_SKILL = 0
    CATEGORY_CAST_SKILL_WITHOUT_ACTION = 1
    CATEGORY_CAST_SKILL_WITH_ACTION = 2

class SkillTempDataKey(object):
    CHANGE_SKILL_CD_STATUS = 1
    NEXT_CAST = 2
    RESTORE_CD_TIMER = 3
    DURATION = 4 # 'duration'
    MUL_ATTACK_ACT_TIMER = 5
    SKILL_DONE_TIMER = 6
    CASTING_CHECK_TIMER = 7
    IS_CHANNELING_EMPTY = 8
    CHANNELING_BULLET_TIMER = 9
    CHANNELING_CALC_TIMER = 10
    T_CHANNELING_START = 11
    CHANNELING_END_TIMER = 12
    CASTING_SKILL_TIMER = 13
    STAGE_CHILD = 14
    STAGE_CD_TIMER = 15
    BEGIN_SKILL_POSITION = 16
    DELAY_CALC_TIMER = 17
    RELEASED_CNT = 18
    TOTAL_RELEASE_CNT = 19
    RELEASE_TIME = 20
    SKILL_ARGS = 21


class SkillCDStatus(object):
    DEFAULT = 0
    # 启用
    ENABLED = 1
    # 禁用
    DISABLED = 2

    VALID = (ENABLED, DISABLED)

SKILL_DMG_DESC = ("", "（水系）", "（雷系）", "（火系）", "（混沌系）")


class SkillAttackType(object):
    ATTACK_NORMAL = 0
    ATTACK_DODGE = 1
    ATTACK_CRIT = 2

class SourceType(metaclass=UniqueIntEnum):
    SrcTpAll=-1
    SrcTpDefault = 0
    SrcTpSkill = 1
    SrcTpAureole = 2
    SrcTpBuff = 3
    SrcTpCreation = 4
    SrcTpItem = 5
    SrcTpPassiveSkill = 6
    SrcTpEquip = 8
    SrcTpTitle = 9
    SrcTpGuildTrain = 10
    SrcTpMonsterManual = 11
    SrcTpScore = 12
    SrcTpHomeBuilding = 13
    SrcTpInit = 14
    SrcTpLevelUp = 15
    SrcTpDungeonAdj = 16
    SrcTpSoulCard = 17
    SrcTpDropWater = 18
    SrcTpWhaleLevel = 19
    SrcTpPlunder = 20
    SrcTpPlunderWhale = 21
    SrcTpPatrol = 22
    SrcTpEscort = 23
    SrcTpPossessed = 24
    SrcTpHonorPK = 26
    SrcTpawardFightProp = 27
    SrcTpFight = 28
    SrcTpEventAction = 29
    SrcTpTeleport = 30
    SrcTpLoseFighting = 31
    SrcTpTowerStage = 32
    SrcTpFlowCtrl = 33
    SrcTpDungeonPlaying = 34
    SrcTpDailyDraw = 35
    SrcTpAvatarChange = 36
    SrcTpSchoolPK = 37
    SrcTpGuildTrainReset = 38
    SrcTpMountProp = 39
    SrcTpPetProp = 40
    SrcTpCollectProp = 41
    SrcTpDuelEnd = 42
    SrcTpDropDeath = 43
    SrcTpMeridianProp = 44
    SrcTpHealWounds = 45
    SrcTpIDLE = 46
    SrcTpAction = 47
    SrcTpCoefficient = 48
    SrcTpAppearance = 49

MAX_BUFF_COUNT = 50

class ChannelingBreak(object):
    BREAK_TP_BE_ATK = 1
    BREAK_TP_LOSE_TARGET = 2
    BREAK_TP_LACK_OF_MP = 3
    BREAK_TP_TARGET_DIE = 4
    BREAK_TP_CONFLICT_STATE = 5
    BREAK_TP_MOVE = 6
    BREAK_TP_CAPTURE = 7
    BREAK_TP_TELEPORT = 8
    BREAK_TP_SELF_DIE = 9
    BREAK_TP_IMMUNE_DEATH = 10
    BREAK_TP_NORMAR_END = 11

class EndCasting(object):
    ECEnumFinished = 1
    ECEnumClientCancel=2
    ECEnumDead = 3
    ECEnumOtherSkill = 4
    ECEnumMissingTarget=5
    ECEnumCaptureMonster=6
    ECEnumBeAttacked = 7
    ECEnumConflictState=8
    ECEnumMove=9
    ECEnumImmuneDeath=10
    ECEnumTeleporting=11
    ECEnumclientPick=12

class ImmuneDeathState(object):
    IMMUNE_VALID = 1
    IMMUNE_DURING = 2
    IMMUNE_FINISHED = 3

class UseSkillCheck(object):
    USC_ENUM_CHEKC_OK = 0
    USC_ENUM_IN_CD = 1
    USC_ENUM_LACK_OF_MP = 1<<1
    USC_ENUM_INVALID_OWNER = 1<<2
    USC_ENUM_STATE_CONFLICT = 1<<3
    USC_ENUM_INVALID_TARGET = 1<<4
    USC_ENUM_INVISIBLE_TARGET = 1<<5
    USC_ENUM_CROSS_SPACE = 1<<6
    USC_ENUM_OUT_OF_RANGE = 1<<7
    USC_ENUM_NEED_CAST = 1<<8
    USC_ENUM_SELF_DIE = 1<<9
    USC_ENUM_SINGLE_HEAL_OUT_OF_RANGE = 1<<10
    USC_ENUM_SHOOTER_SKILL_CANNOT_USE = 1<<11
    USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH = 1<<12
    USC_ENUM_TARGET_NOT_FOUND = 1<<13

    #起手延迟结算时检查需要忽略的条件
    USC_DELAY_CHECK_IGNORES = USC_ENUM_IN_CD | USC_ENUM_LACK_OF_MP | USC_ENUM_OUT_OF_RANGE | USC_ENUM_STATE_CONFLICT | USC_ENUM_INVALID_TARGET | USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH
    #连击技能（例如风入松放一次可以砍出4刀，每刀单独结算）分阶段结算时，每个阶段的检查
    USC_MUL_ATTACK_CHECK_IGNORES = USC_ENUM_IN_CD | USC_ENUM_LACK_OF_MP | USC_ENUM_STATE_CONFLICT | USC_ENUM_ULTRA_SKILL_POWER_NOT_ENOUGH

class ResetSkillReason(object):
    ReasonDefault = 0
    ReasonSkillDone=1
    ReasonStageEnd = 2
    ReasonEndCasting = 3
    ReasonTimeRefreshDone=4
    ReasonTeleport = 5
    ReasonDuelComplete = 6
    ReasonGeneralSkillBreak = 7
    ReasonTransform = 8
    ReasonCleintEnd = 9
    ReasonDodgeSkill = 10
    ReasonUltraSkill = 11
    ReasonSkillStateRemove = 12
    ReasonFreeze = 13
    ReasonBreakByState = 14


class SkillActionType(object):
    StagedAct=1

class ActionProgressEnum(object):
    startActionDoing = 1
    startActionDone = 2
    actionDoing = 3
    actionDone = 4

SCHOOL_PHYSICAL = 1
SCHOOL_MAGIC = 2
SCHOOL_ASSISTANT = 3

class HitType(metaclass=UniqueIntEnum):
    Null = 0
    Hit = 1 # 为0 不下发
    Crit = 2 # 为0 不下发
    #未命中
    Miss = 3
    #闪避
    Dodge = 4 # 为0 不下发
    Heal = 5 # 为0 不下发
    HealCrit = 6 # 为0 不下发
    #物理免疫
    ImmunePhysicalDmg = 7
    #吸收
    Absorb = 8 # 为0 不下发
    #免疫
    Immune = 9
    #抵抗
    Resist = 10
    #状态命中
    HitState = 11
    #吸血
    BloodSuck = 12 # 为0 不下发
    #消除
    Eliminate = 13 # 为0 不下发
    #捕捉
    Catch = 14
    #魔法免疫
    ImmuneMagicDmg = 15
    #辅助免疫
    ImmuneAssistantDmg = 16
    #分摊伤害
    ShareDmg = 17 # 为0 不下发
    #血量回复
    HPRecover = 21 # 为0 不下发
    #伤害免疫
    ImmuneDmg = 22
    #晕眩
    Stun = 24
    #击倒
    Down = 25
    #冰冻
    Frozen = 26
    #定身
    Snare = 27
    #缓速
    Slow = 28
    #控制抵抗or免疫
    AntiControl = 29
    #沉默抵抗or免疫
    AntiSilence = 30
    #combo伤害（如感电炎爆）
    ComboHit = 31 # 为0 不下发
    #combo暴击
    ComboCrit = 32 # 为0 不下发
    #沉默
    Silence = 34
    #位移免疫
    ImmuneDisplacement = 36

    clientIgnoreList = (Absorb, BloodSuck, Dodge, Heal, ImmunePhysicalDmg, ImmuneMagicDmg, ImmuneAssistantDmg, HPRecover)

    zeroFilter = (Hit, Crit, Dodge, Heal, HealCrit, Absorb, BloodSuck, Eliminate, ShareDmg, ComboHit, ComboCrit, HPRecover)

    @staticmethod
    @functools.lru_cache(32)
    def checkInClientIgnoreList(hitType):
        return hitType in HitType.clientIgnoreList

class RemoveType(metaclass=UniqueIntEnum):
    RTEnumDefault = 0
    RTEnumEndByTime = 1
    RTEnumEndByAtt = 2
    RTEnumEndByBeat = 3
    RTEnumEndBySkill = 4
    RTEnumEndByDead = 5
    RTEnumEndByAction = 6
    RTEnumRestoreRemove = 7

class PKModel(object):
    PEACE = 0
    JUSTICE = 1
    ENEMY = 2
    ATTACK = 3
    #GRAY = 3        #灰名模式
    MAX_PK = ATTACK

class IsRelationEnum(object):
    TRUE = 1
    FALSE = 2
    NOT_DEAL = 3

class ForceRelation(object):
    UnKnownForceRelation = 0
    Friend = 1
    Enemy = 2
    Neutrality = 3
    NPC = 4

class RaceTypeEnum(object):
    none = 0
    avatar = 1
    monster = 2
    guildBattleBoss = 3
    pet = 4
    bot = 5
    summon = 6


class CampType(object):
    All = 0
    Enemy = 1
    Self = 2
    Friend = 3
    CreationMaster = 4
    EnemyExTarget = 5
    Team = 6    # 已弃用

class TeamCampType(object):
    All = 0
    Self = 1
    Team = 2
    Raid = 3

class UnsetAllHateReason(object):
    destory = 1
    teleport = 2
    dead = 3
    leaveFightingState = 4

class BattleType(object):
    physics = 1
    magic = 2

class CommonFlagCellType(object):
    IsHealHPLow = 0

class StartActionResult(object):
    Fail = 0
    Success = 1
    Skip = 2

LIFE_ALIVE = 1
LIFE_DEAD = 2
RELIVE_TYPE_NOT_RELIVE = 0      #不复活
RELIVE_TYPE_DIRECTLY = 1        #原地复活
RELIVE_TYPE_TO_NEAR = 2
RELIVE_TYPE_TO_BORN = 3
RELIVE_TYPE_LEAVE_IN_DUNGEON = 3    # 副本中3为直接离开
RELIVE_TYPE_LEAVE_IN_GUILD = 3    # 帮派中3为直接离开

class CastingSkillCDType(object):
    IgnoreMove = 0
    EnterCD = 1
    NotEnterCD = 2

class BornStateType(object):
    '''
    0:引擎默认值，未初始化后
    1:怪物隐身阶段
    2:怪物出生现行静止阶段
    3:普通正常状态
    4:对话后动画
    5:再次正常状态
    6:石化状态
    7:虚影状态
    8:灵魂状态
    9.恢复普通正常状态
    10.born动画
    11.boen后状态
    12.reset动画
    '''
    none = 0
    invisible = 1
    static = 2
    move = 3
    afterDialog = 4
    normal = 5
    stone = 6
    virtual = 7
    soul = 8
    reMove = 9
    bornAnim = 10
    afterBornMove = 11
    resetAnim = 12

    bornDoNothing = (stone, virtual, soul)
    joinCombatTup = (move, normal, afterBornMove)
    speialAIInvalidCombatTup = (move,)
    flowConvTup = (move, stone, virtual)

    # 其他类型后面扩展

class ScriptNone(object):
    pass

scriptNone = ScriptNone()

class AIDefine(object):
    AIEnumPatrolTick      = 3  # 巡逻间隔
    AIEnumPatrolProb      = 75 # 巡逻概率
    AIEnumSummonDis       = 5  # 召唤物跟随最大距离
    AIEnumSummonDisEx     = 30 # 召唤物战斗最大距离
    AIEnumSummonDisAd     = 3  # 召唤物调整最佳距离
    AIEnumSummonDisYL     = 8  # 特殊召唤物（应龙）距离
    AIEnumGoHomeSpeed     = 5  # 脱战回家移速调整

AI_EVENT_ENENY_ENTER_TRAP = 'enemyEnter'
AI_EVENT_ENENY_LEAVE_TRAP = 'enemyLeave'
AI_EVENT_DEAD = 'dead'
AI_EVENT_ON_BE_ATTACKED = 'onBeAttacked'
AI_EVENT_ENTITY_BORN = 'entityBorn'
AI_EVENT_ENTITIES_LOADED = 'spaceEntitiesLoaded'
AI_EVENT_BEFORE_LOADING_ENTITIES = 'beforeLoadingEntities'

class BigWorldSpawnSpanRefreshType(object):
    DEFAULT = 0
    TIMER = 1

class SpeedState(object):
    Normal = 1.0
    Patrol = 1.0

class RouteState(object):
    ROUTE_STATE_IDLE = 0
    ROUTE_STATE_WAIT = 1
    ROUTE_STATE_MOVING = 2
    ROUTE_STATE_SUSPEND = 3
    ROUTE_STATE_COMPLETE = 4
    ROUTE_STATE_STOP = 5

class MailConstID(object):
    REWARD_MAIL_ID = CSTD.datas['getRewardAndBagFull_mailID']['value']
    MAX_GLOBAL_MAIL_SAVE_COUNT = 100
    MAX_GLOBAL_MAIL_OVER_RATE = 90

class JumpType(object):
    FIRST_JUMP = 1
    DOUBLE_JUMP = 2
    FLYING = 3
    SPEED_FALL = 4

class DungeonSrcEnum(object):
    DEFAULT = 0                                   # 默认
    FROM_CLIENT = 1                               # 客户端
    FROM_CLIENT_GM = 2                            # GM命令
    FROM_TASK = 4                                 # 任务流程触发传送
    FROM_KICKOUT_DUNGEON = 5                      # 踢出副本
    FROM_TIME_OUT = 6                             # 副本超时
    FROM_FLOW_CONTROLLER = 7                      # 副本流程控制节点
    FROM_CONFIG = 8                               # custom config变更导致的传送

    COLL_FROM_TASK = (FROM_TASK, )

class CompleteTeleportLeaveFailReason(object):
    ARGS_DEFINED = 1
    UNDEFINED_FUNC = 2
    UNDEFINED_SPACE = 3

    PLAYER_IN_WORLDGUIDE = 10000
    PLAYER_IN_NEWBIEDUN = 10001

    COLL_USEROPRERRNO = (PLAYER_IN_WORLDGUIDE, PLAYER_IN_NEWBIEDUN)

class CastType(object):
    teleport = 1
    teleportClientDelay = 2
    ride = 3
    teleportByUseItem = 4
    teleportAnchor = 5

class ComplexTeleportEnum(object):
    UNKNOWN = 0
    ENTER = 1
    LEAVE = 2

class ComplexTeleportMethodTypeEnum(object):
    beforeEnter = 1
    afterEnter = 2
    beforeLeave = 3
    afterLeave = 4
    postAfterEnter = 5
    postAfterLeave = 6

class GameSpaceRecoverEnum(object):
    RCV_NO_ACTION = 0
    RCV_FULL_HP_IO = 1
    RCV_FULL_HP_IN = 2
    RCV_FULL_HP_OUT = 3

    COLL_ENTER_RCV = (RCV_FULL_HP_IO, RCV_FULL_HP_IN)
    COLL_LEAVE_RCV = (RCV_FULL_HP_IO, RCV_FULL_HP_OUT)

# TeamStub个数
TEAMSTUB_CONF_NUM = 5
TEAM_MEMBER_MAX_NUM = 5
TEAM_APPLY_JOIN_MAX_NUM = 20
TEAM_MAX_LIST_NUM = 15

RAIDSTUB_CONFIG_NUM = 5
RAID_TEAM_MEMBER_MAX_NUM = 5
RAID_LSIT_MAX_NUM = 15
RAID_MEMBER_MAX_NUM = 15
RAID_APPLY_JOIN_MAX_NUM = 20
STATISTICSTUB_CONFIG_NUM = 5

class TeamMicsModeEnum(object):
    OFF = 0
    FREE = 1

    COLL_ALL = (OFF, FREE)

class RaidMicsModeEnum(object):

    OFF = 0
    FREE = 1
    LEADER = 2

    COLL_ALL = (OFF, FREE, LEADER)

class TeamMountState(object):
    none = 0
    ride = 1
    fly = 2

class RaidJoinTypeEnum(object):
    SINGLE = 1
    TEAM = 2

class TeamType(object):
    TEAM = 1
    RAID = 2

TEAM_MARK_MAX_SLOT = 8
class TeamMarkType(object):
    MARK_NONE = 0
    MARK_TEAMMATE = 1
    MARK_ENEMY = 2
    MARK_SCENE = 3

class TeamMarkChangeType(object):
    NONE = 0
    ADD = 1
    MODIFY = 2
    DELETE = 3
    CAPTAIN = 4

class TeamStatisticType(object):
    NONE = 0
    DAMAGE = 1
    HEAL = 2
    HURT = 3
    DEAD = 4

class _RaidErrno(object):
    from userType import Error as _errno

    def _lateReload(self):
        for _value in self.__class__.__dict__.values():
            if _value.__class__.__name__ == 'Error':
                _value.reloadScript()

    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()

    ENUM_UNKNOWN                                 = _errno(0)         # 未知错误
    ENUM_RAID_OK                                 = _errno(1)         # 正常
    ENUM_RAID_PARAM_ERR                          = _errno(2)         # 参数错误
    ENUM_RAID_NOT_IN_TEAM                        = _errno(10000)     # 不在小队中
    ENUM_RAID_ALREADY_IN_TEAM                    = _errno(10001)     # 已经在小队中
    ENUM_RAID_RAID_ID_REPEAT                     = _errno(10002)     # 团队ID重复
    ENUM_RAID_TEAM_ID_REPEAT                     = _errno(10003)     # 小队ID重复(teamId)
    ENUM_RAID_PLAYER_GBID_REPEAT                 = _errno(10004)     # 玩家ID重复
    ENUM_RAID_TEAM_NOT_FOUND                     = _errno(10005)     # 小队ID未找到(teamId)
    ENUM_RAID_PLAYER_GBID_NOT_FOUND              = _errno(10006)     # 玩家ID位找到
    ENUM_RAID_NOT_TEAM_CAPTAIN                   = _errno(10007)     # 不是小队队长
    ENUM_RAID_NOT_IN_RAID                        = _errno(10008)     # 不在团队中
    ENUM_RAID_NOT_RAID_LEADER                    = _errno(10009)     # 不是团长
    ENUM_RAID_RAID_ID_NOT_FOUND                  = _errno(10010)     # 团队ID未找到
    ENUM_RAID_TEAM_IDX_REPEAT                    = _errno(10011)     # 小队IDX重复
    ENUM_RAID_TEAM_IDX_NOT_FOUND                 = _errno(10012)     # 小队IDX未找到
    ENUM_RAID_RAID_ID_NOT_MATCH                  = _errno(10013)     # 团队ID不匹配
    ENUM_RAID_ALREADY_IN_RAID                    = _errno(10014)     # 已经在团队中
    ENUM_RAID_RAID_IS_FULL                       = _errno(10015)     # 团队已满
    ENUM_RAID_ALREADY_APPLY_JOIN                 = _errno(10016)     # 已经申请加入该团队
    ENUM_RAID_APPLY_JOIN_NOT_FOUND               = _errno(10017)     # 申请记录没有找到
    ENUM_RAID_APPLY_JOIN_RECORD_NOT_FOUND        = _errno(10018)     # 申请记录(玩家缓存)没有找到
    ENUM_RAID_UNKNOWN_CAPACITY                   = _errno(10019)     # 不支持的团队人数
    ENUM_RAID_CREATE_RAID_OFR                    = _errno(10020)     # 创建团对时超出人数上限
    ENUM_RAID_TEAM_NUM_NOT_MATCH                 = _errno(10021)     # 小队人物数量没有匹配
    ENUM_RAID_TEAM_MEMBER_NOT_MATCH              = _errno(10022)     # 小队人员没有匹配
    ENUM_RAID_RAID_NOT_ENOUGH_SIT                = _errno(10023)     # 团队不足以加入新的小队
    ENUM_RAID_CHECKING_TEAM_JOIN_FAILED          = _errno(10024)     # 团队检查加入失败(申请)
    ENUM_RAID_AVATAR_REJECTED_ACT                = _errno(10025)     # 玩家主动拒绝操作
    ENUM_RAID_PLAYER_GBID_NOT_MATCH              = _errno(10026)     # 玩家ID不匹配
    ENUM_RAID_JOIN_TYPE_NOT_MATCH                = _errno(10027)     # 团队加入(检查)类型不匹配
    ENUM_RAID_RAID_TEAM_IS_FULL                  = _errno(10028)     # 小队已满
    ENUM_RAID_TEAM_IDX_CHANGED                   = _errno(10029)     # 小队ID变化
    ENUM_RAID_TEAM_ID_CHANGED                    = _errno(10030)     # 小队ID变化(teamId)
    ENUM_RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND  = _errno(10031)     # 邀请记录未找到
    ENUM_RAID_CHECKING_TEAM_INVITE_FAILED        = _errno(10032)     # 团队检查加入失败(邀请)
    ENUM_RAID_TEAM_IS_EMPTY                      = _errno(10033)     # 小队为空
    ENUM_RAID_KICKOUT_SELF                       = _errno(10034)     # 尝试移除自己(self.gbId==gbId)
    ENUM_RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN     = _errno(10035)     # 团长所在队伍不能转移队长
    ENUM_RAID_AWARD_SELF                         = _errno(10036)     # 尝试对自己任命(团长不能对自己小队进行一些任命操作)
    ENUM_RAID_AWARD_SELF_TEAM                    = _errno(10037)     # 尝试对自己所在团队任命
    ENUM_RAID_ALREADY_BE_TEAM_CAPTAIN            = _errno(10038)     # 已经是小队队长
    ENUM_RAID_IS_SAME_TEAM                       = _errno(10039)     # 小队相同
    ENUM_RAID_IS_SAME_PLAYER                     = _errno(10040)     # 玩家相同
    ENUM_RAID_RAID_TEAM_IDX_OFR                  = _errno(10041)     # 创建小队IDX超出上限
    ENUM_RAID_SAME_RAID_TARGET_ID                = _errno(10042)     # 相同目标ID
    ENUM_RAID_DURING_STANDBY_CHECK               = _errno(10043)     # 团队正在进行检查
    ENUM_RAID_STANDBY_RECORD_NOT_FOUND           = _errno(10044)     # 团队检查记录未找到
    ENUM_RAID_STANDBY_ALREADY_CHECKED            = _errno(10045)     # 已经check过
    ENUM_RAID_RAID_LEADER_CHANGED                = _errno(10046)     # 团队已经变更
    ENUM_RAID_TEAM_MEMBER_OFFLINE                = _errno(10047)     # 团队成员离线
    ENUM_RAID_APPLY_JOIN_STUB_VAL_NOT_FOUND      = _errno(10048)     # 申请记录没有找到(RaidStub记录)
    ENUM_RAID_APPLY_JOIN_NUMBER_OFR              = _errno(10049)     # 当前团队申请记录超过上限
    ENUM_RAID_INVITE_SELF_TEAM                   = _errno(10050)     # 玩家尝试邀请自己的小队加入团队
    ENUM_RAID_MICS_NUM_OUT_OF_RANGE              = _errno(10051)     # 麦克风人数到达上限
    ENUM_RAID_MICS_BLOCK                         = _errno(10052)     # 麦克风被强制禁用
    ENUM_RAID_MICS_SWITCH_OFF                    = _errno(10053)     # 麦克风总开关关闭
    ENUM_RAID_MISC_FREE_MODE_LIMIT               = _errno(10054)     # Free模式限制麦克风相关功能
    ENUM_RAID_MISC_LEADER_MODE_LIMIT             = _errno(10054)     # leader模式限制麦克风相关功能
    ENUM_RAID_LEADER_CANT_TURN_OFF_MICS          = _errno(10056)     # 团长禁止关闭麦克风
    ENUM_RAID_MICS_MODE_ERR                      = _errno(10057)     # 团队麦克风模式错误
    ENUM_RAID_INVITED_SAME_PLAYER_INCD           = _errno(10058)     # 同一团队邀请CD
    ENUM_RAID_IS_RAID_LEADER                     = _errno(10059)     # 操作对象是团长A
    ENUM_RAID_TEAM_CANT_DISBAND                  = _errno(10061)     # 小队无法被解散
    ENUM_RAID_UI_DENIED                          = _errno(10062)     # 团队接口被UI相关判断阻止
    ENUM_RAID_ALL_MICS_BLOCKED                   = _errno(10063)     # 已经全员禁麦
    ENUM_RAID_TEAM_MEMBER_DUOHUN                 = _errno(10064)     # 被夺魂
    ENUM_RAID_NOT_RAID_DEPUTY                    = _errno(10065)     # 不是副团长
    ENUM_RAID_NOT_RAID_LEADER_OR_DEPUTY          = _errno(10066)     # 不是团长/副团长
    ENUM_RAID_NOT_RAID_CANNOT_KICK_LEADER        = _errno(10067)     # 不能踢团长
    ENUM_RAID_NOT_RAID_CANNOT_KICK_DEPUTY        = _errno(10068)     # 不能踢副团长
    ENUM_RAID_NOT_RAID_CANNOT_MOVE_LEADER        = _errno(10069)     # 不能移动团长
    ENUM_RAID_NOT_RAID_UNKNOWN_TEAM_MEMBER       = _errno(10070)     # 小队人数不支持
    ENUM_RAID_NOT_SAME_SIEGEWAR_CAMP             = _errno(10071)     # 城战不同阵营

    ENUM_RAID_CHECKING_TEAM_JOIN                 = _errno(50000)     # 团队正在检查组队加入(申请通过)
    ENUM_RAID_CHECKING_TEAM_INVITE               = _errno(50001)     # 团队正在检查组队加入(邀请通过)
    ENUM_RAID_CHECKING_STANDBY_CHECK             = _errno(50002)     # 团队正在进行整团检查(团长发起)
    ENUM_RAID_INVITE_TO_JOIN                     = _errno(50100)     # 团队邀请转变为申请
    ENUM_RAID_TARGET_IS_ILLEGAL                  = _errno(50101)     # 团队目标不合法
    ENUM_RAID_PASSWORD_IS_WRONG                  = _errno(50102)     # 密码不对
    ENUM_RAID_LEVEL_IS_LIMITED                   = _errno(50103)     # 等级不足
    ENUM_RAID_SCORE_LIMITED                      = _errno(50104)     # 战力不足
    ENUM_RAID_SOCRE_IS_ILLEGAL                   = _errno(50105)     # 战力不合法
    ENUM_RAID_LEVEL_IS_ILLEGAL                   = _errno(50106)     # 等级不合法
    ENUM_RAID_PASSWORD_IS_ILLEGAL                = _errno(50107)     # 密码不合法
    ENUM_RAID_PASSWORD_IS_EMPTY                  = _errno(50108)     # 密码为空
    ENUM_RAID_RECRUIT_IS_ILLEGAL                 = _errno(50109)     # 招募不合法
    ENUM_RAID_AUTO_EXPEDITION_IS_ILLEGAL         = _errno(50110)     # 自动开启远征不合法
    ENUM_RAID_SET_TARGET_ILLEGAL                 = _errno(50111)     # 设置目标不合法
    ENUM_RAID_IS_IN_DUNGEON                      = _errno(50112)     # 团队已进入副本
    ENUM_RAID_APPLY_LIST_IS_FULL                 = _errno(50113)     # 团队申请列表满了
    ENUM_RAID_ERR_IGNORE                         = _errno(60000)     # 可以忽略的错误


RaidErrno = _RaidErrno()


class RaidPermission(object):
    """Raid permission enum"""

    UNKNOWN = 0
    MEMBER = 1
    CAPTAIN = 2
    DEPUTY = 3
    LEADER = 4

    @classmethod
    def haveRaidPermission(cls, perm, needPermission, onlyMode=False, exluce=()):
        if perm in exluce:
            return False

        if onlyMode:
            return perm == needPermission

        else:
            return perm >= needPermission

class RaidDungeonStandbyCheckSrcEnum(object):
    """全团检查check"""

    UNKNOWN = 0
    DEFAULT = 1
    ENTER_DUNGEON = 2


class ControlledByReason(object):
    Idle = 0
    AutoCombat = 2
    UseSkill = 3
    ControlledState = 4
    Huache = 5

    ReasonStatePrefix = '{}_'.format(ControlledState)

class AutoCombatState(object):
    Idle = 0
    Fighting = 1
    Suspending = 2

class SuspendAutoCombatReason(object):
    Default = 0
    ClientBreak = 1
    ApplyGather = 2
    Teleport = 3
    Riding = 4
    RouteErr = 5
    StateBreak = 6
    RemoveMove = 9
    DoubleBar = 10
    PlayEmote = 11


class ChangeAutoCombatReason(object):
    Default = 0
    ClientChange = 1
    CaptainTrap = 2
    CaptainChange = 3
    CaptainEnterFightingState = 4

class PKProtectType(object):
    TEAM = 0
    GROUP = 1
    GUILD = 2
    UNION = 3 # 同盟保护

class PKMoralLevel(object):
    KINDNESS = 0
    NORMAL = 1
    EVIL_LOW = 2
    EVIL_MID = 3
    EVIL_HIGH = 4

class PKMapType(object):
    DANGER = 0
    SAFE = 1

# 需要与客户端同步
class ChatChannelEnum(object):
    SYSTEM = 1
    WORLD = 2
    GUILD = 3
    TEAM = 4
    NEARBY = 5
    PERSON = 6
    RAID = 7
    RECRUIT = 8
    SIEGE_WAR = 9
    MAX = 10

    initExcludeChannel = ()
    avatarChannel = (WORLD, GUILD, TEAM, NEARBY)
    voiceChannel = (WORLD, GUILD, TEAM, NEARBY)

class SilentSpeakScene(object):
    ENUM_FRIEND_CHAT = 1             #私聊
    ENUM_CHAT = 2                    #公告聊天
    ENUM_ALL = 99                    #全部

class SilentSpeakState(object):
    ENUM_SET_FRIEND_CHAT = 2
    ENUM_REMOVE_FRIEND_CHAT = 13
    ENUM_SET_CHAT = 4
    ENUM_REMOVE_CHAT = 11
    ENUM_SET_ALL = 6
    ENUM_REMOVE_ALL = 9

class DungeonEntityLoadStatus(object):
    UNLOAD = 0
    LOADING = 1
    LOADED = 2

class DungeonPlayModeEnum(object):
    UNKNOWN = 0
    CRUSADE = 1
    CHIEF = 2
    GUILD_BOSS = 3

    COLL_ALL = (CRUSADE, CHIEF, GUILD_BOSS)
    COLL_SYNC_SPACELEVEL = (CRUSADE, CHIEF, GUILD_BOSS)

class DungeonTicketType(metaclass=UniqueIntEnum):
    # 常规使用
    NORMAL = 1
    # 金币使用
    GOLD = 2
    # 道具使用
    ITEM = 3

class DungeonSpaceMgrProps(object):
    DSMPEnumdungeonRewardBossID = 1000
    DSMPEnumsingleDungeonBelongPlayerGBID = 1001
    DSMPEnumteamDungeonBelongTeamUUID = 1002
    DSMPEnumraidDungeonBelongRaidUUID = 1003
    DSMPEnumdungeonWinFlagSpaceMgrCache = 1004
    DSMPEnumtransPetId = 1005
    DSMPEnumtriggerGuideId = 1006
    DSMPEnumdungeonTimeFreezeSpaceMgrFlag = 1007 # linkeed: EntityPropsEnum. dungeonTimeFreezeEntityFlag
    DSMPEnumguildBossDungeonBelongGuildUUID = 1008
    DSMPEnumbreakStuckPos = 1009
    DSMPEnumbreakStuckDir = 1010

class DungeonSpaceTypeEnum(object):
    """
    NOTE: 同时修改 SpaceType 中的类型
    """
    UNKNOWN = 0
    BIG_WORLD = 1
    COMMON = 2
    BATTLE_FIELD = 5
    SIEGE_WAR = 8
    GUILD_BOSS = 9

    COLL_DUNGEON = (BIG_WORLD, COMMON, BATTLE_FIELD, SIEGE_WAR, GUILD_BOSS)

class DungeonEnterTypeEnum(object):
    UNKNOWN = 0
    SINGLE = 1
    TEAM = 2
    BOTH = 3
    RAID = 4
    GUILD = 5

    COLL_TEAM = (TEAM, BOTH)
    COLL_SINGLE = (SINGLE, BOTH)

    COLL_GUILD = (GUILD)
    COLL_BOTH = (TEAM, SINGLE)
    COLL_ALL = (TEAM, SINGLE, RAID, GUILD)


_DUNGEON_TYPE_LRU_CACHE_SIZE = 4 * 4


class DungeonTypeJudge(object):

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_TEAM:
            return True
        return False


    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isNormalTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceTypeEnum.COMMON \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBigWorldTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceTypeEnum.BIG_WORLD \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isNormalSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceTypeEnum.COMMON \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBigWorldSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceTypeEnum.BIG_WORLD \
                and dungeonEnterType in DungeonEnterTypeEnum.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBothDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON \
                and dungeonEnterType == DungeonEnterTypeEnum.BOTH:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isRaidDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON \
                and dungeonEnterType == DungeonEnterTypeEnum.RAID:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isGuildBossDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON \
                and dungeonSpaceType == DungeonSpaceTypeEnum.GUILD_BOSS \
                and dungeonEnterType == DungeonEnterTypeEnum.GUILD:
            return True
        return False

    @classmethod
    def isDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType in DungeonSpaceTypeEnum.COLL_DUNGEON

    @classmethod
    def isBigWorldDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceTypeEnum.BIG_WORLD

class _ACT_ID_CONST_META(UniqueIntEnum):
    pass

class ACT_ID_CONST(metaclass=_ACT_ID_CONST_META):
    ACTIVITY_GUIDE = 32000032  # 导游
    ACTIVITY_CRUSADE_ID = 32000008

class _RaidDungeonErrno(object):
    from userType import Error as _errno

    def _lateReload(self):
        for _v in self.__class__.__dict__.values():
            if _v.__class__.__name__ == 'Error':
                _v.reloadScript()

    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()

    ENUM_UNKNOWN                                 = _errno(0)         # 未知错误
    ENUM_RAIDDUN_OK                              = _errno(1)         # 正常
    ENUM_RAIDDUN_SKIP                            = _errno(2)         # 跳过
    ENUM_RAIDDUN_DUNGEON_ID_NOT_FOUND            = _errno(20000)     # 团队副本ID未找到
    ENUM_RAIDDUN_NOT_IN_RAID                     = _errno(20001)     # 不在团队中
    ENUM_RAIDDUN_DUNGEON_NO_NOT_MATCH            = _errno(20002)     # 团队副本不匹配
    ENUM_RAIDDUN_NOT_RAID_LEADER                 = _errno(20003)     # 不是团队Leader
    ENUM_RAIDDUN_RAID_ID_NOT_MATCH               = _errno(20004)     # 团队ID不匹配
    ENUM_RAIDDUN_DUNGEON_VAL_NOT_FOUND           = _errno(20005)     # 团队副本val没有找到(RaidDungeonStub)
    ENUM_RAIDDUN_DUNGEON_ALREADY_BE_DESTROYED    = _errno(20006)     # 团队副本已经被销毁(包括标记删除)
    ENUM_RAIDDUN_RAID_ID_NOT_FOUND               = _errno(20007)     # 团队ID没有找到
    ENUM_RAIDDUN_RAID_ALREADY_EXIST_DUNGEON      = _errno(20008)     # 团队已经存在副本
    ENUM_RAIDDUN_NOT_IN_AVAILABLE_SPACE          = _errno(20009)     # 不在合法space中
    ENUM_RAIDDUN_FOUNDER_VAL_NOT_FOUND           = _errno(20010)     # 副本成员没有找到(dungeonRaidStub)
    ENUM_RAIDDUN_NOT_IN_RAID_DUNGEON             = _errno(20011)     # 不在团队副本中
    ENUM_RAIDDUN_DUNGEON_IS_NOT_ACTIVE           = _errno(20012)     # 团队副本不活跃(可能是已经完成或者已经标记销毁)
    ENUM_RAIDDUN_SPACE_UUID_NOT_MATCH            = _errno(20013)     # 团队space唯一ID不相同
    ENUM_RAIDDUN_FOUNDER_IN_DUNGEON              = _errno(20014)     # space中存在玩家
    ENUM_RAIDDUN_GUILD_LEVEL_LOWER               = _errno(20015)     # 帮会等级不够
    ENUM_RAIDDUN_PLAYER_NUM_NOT_MATCH            = _errno(20016)     # 团队副本人数不满足要求
    ENUM_RAIDDUN_PLAYER_IN_FIGHT_STATE           = _errno(20017)     # 团队中有成员在战斗状态
    ENUM_RAIDDUN_PLAYER_NOT_IN_GUILD             = _errno(20018)     # 团本玩家不在帮会中
    ENUM_RAIDDUN_LEADER_LEVEL_LOWER              = _errno(20019)     # 团长等级不足
    ENUM_RAIDDUN_REPEAT_ENTER_SAME_DUNGEON        = _errno(20020)     # 副本内尝试进入同一个副本
    ENUM_RAIDDUN_MEMBER_LEVEL_LOWER              = _errno(20021)     # 团员等级不足
    ENUM_RAIDDUN_ENTER_BLOCK_BY_COMBAT           = _errno(20022)     # 副本内正在战斗无法进入
    ENUM_RAIDDUN_TELGLOBAL_LOCKED                = _errno(20023)     # 传送锁
    ENUM_RAIDDUN_REWARD_NUM_CHECK_FAIL           = _errno(20024)     # 副本可挑战次数不足


RaidDungeonErrno = _RaidDungeonErrno()

class TeamDungeonCheckConditionErrno(object):
    UNKNOWN = 0
    SCORE_CHECK_FAIL = 2
    FIGHTING_FAIL = 3
    NEED_ITEM_FAIL = 4
    PRE_TASK_FAIL = 5
    NEARBY_FAIL = 6
    SC_LEVEL_CHECK_FAIL = 8
    TELEPORT_COND_FAIL = 9
    REWARD_NUM_CHECK_FAIL = 10

class DungeonFlowCompSym(object):
    un = 0
    eq = 1
    lt = 2
    gt = 3
    ge = 4
    le = 5

    _COMPARE_MAP = {
        eq: lambda a, b: a == b,
        gt: lambda a, b: a > b,
        lt: lambda a, b: a < b,
        le: lambda a, b: a <= b,
        ge: lambda a, b: a >= b,
    }

    @classmethod
    def compare(cls, symbol, val1, val2):
        # 找不到符号返回 False
        return cls._COMPARE_MAP.get(symbol, lambda a, b: False)(val1, val2)


class DungeonFlowEventType(object):
    EVdunStart = 'dunStart'       # 副本开始
    EVdunEnd = 'dunEnd'           # 副本结束
    EVdunDelayEnd = 'dunDelayEnd' # 副本延迟结束
    EVdunFailed = 'dunFailed'     # 副本失败
    EVcreateMonster = 'createMonster'     # 创建怪物
    EVremoveMonster = 'removeMonster'     # 回收怪物
    EVcreateNPC = 'createNPC'     # 创建NPC
    EVremoveNPC = 'removeNPC'     # 回收NPC
    EVcreateCollection = 'createCollection'       # 创建采集物
    EVcollBeCollected = 'collBeCollected'         # 采集物被采集事件
    EVmultiCollAllBeCollected = 'multiCollAllBeCollected'     # 多个采集物全部被采集触发事件
    EVremoveCollection = 'removeCollection'       # 回收采集物
    EVcreateAirWall = 'createAirWall'             # 创建空气墙
    EVremoveAirWall = 'removeAirWall'             # 回收空气墙
    EVdelayLoop = 'delayLoop'                     # 带延迟的循环
    EVtaskFinished = 'taskFinished'               # 等待任务完成
    EVtaskFailed = 'taskFailed'                   # 等待任务失败
    EVtaskInProgress = 'taskInProgress'           # 等待人物进行中
    EVmonsterHp = 'monsterHp'                     # 等待怪物血量变化值一定条件
    EVkillMonsterNum = 'killMonsterNum'           # 等待杀怪量变化值达到一定条件
    EVmonsterRestNum = 'monsterRestNum'           # 等待怪物数量变化值达到一定条件
    EVcastSkill = 'castSkill'     # 副本内特定怪物释放
    EVcreateCreationInFixedPosition = 'createCreationInFixedPosition' # 特定位置釋放创生物
    EVsummonMonsterInFixedPosition = 'summonMonsterInFixedPosition'   # 特定位置释放召唤物
    EVaddBuffToMonster = 'addBuffToMonster'                   # 副本内怪物加buff
    EVremoveBuffFromMonster = 'removeBuffFromMonster'         # 副本内怪物去buff
    EVaddBuffToAllPlayer = 'addBuffToAllPlayer'               # 副本内所有玩家加buff
    EVremoveBuffFromAllPlayer = 'removeBuffFromAllPlayer'     # 副本内所有玩家去buff
    EVbroadcastMsg = 'broadcastMsg'               # 副本内广播消息给所有玩家
    EVclearDungeon = 'clearDungeon'               # 移除副本内所有实体
    EValivePlayer = 'alivePlayer'                 # 检测副本内活着的玩家数量
    EVmonsterInBattle = 'monsterInBattle'         # 怪物进入战斗
    EVmonsterLeaveBattle = 'monsterLeaveBattle'   # 怪物离开战斗
    EVstopDelayEvent = 'stopDelayEvent'
    EVcreateCreationInPlayerPosition = 'createCreationInPlayerPosition'       # 玩家附近创建创生物
    EVcreateCreationInMonsterPosition = 'createCreationInMonsterPosition'     # 怪物附近创建创生物
    EVaddBuffToPlayer = 'addBuffToPlayer'         # 玩家添加buff
    EVcastSkillToPlayer = 'castSkillToPlayer'     # 向指定类型玩家释放技能
    EVhaveCreationInRange = 'haveCreationInRange'     # 判断指定怪物内是否存在召唤物
    EVremoveCreation = 'removeCreation'               # 回收特定怪物放出的召唤物
    EVremoveNoHostCreation = 'removeNoHostCreation'   # 回收无主召唤物
    EVdunStageSet = 'dunStageSet'                     # 设置副本阶段
    EVshowPopoverMsg = 'showPopoverMsg'           # 实体弹出气泡消息
    EVpopupdialog = 'popupdialog'                 # 实体弹出其他消息
    EVdungeonTaskForceComplete = 'dungeonTaskForceComplete'   # 副本所有玩家任务强制完成
    EVdungeonTaskForceFailed = 'dungeonTaskForceFailed'       # 副本所有玩家任务强制失败
    EVchangeDunNPCToBattle = 'changeDunNPCToBattle'           # 将副本内NPC切换为可攻击状态
    EVchangeDunNPCToNeutral = 'changeDunNPCToNeutral'         # 将副本内NPC置为中立
    EVchangeDunNPCToFriendly = 'changeDunNPCToFriendly'       # 将副本内NPC置为友善
    EVchangeDunNPCDialog = 'changeDunNPCDialog'               # 更改副本内NPC对话ID
    EVdunAnyPlayerHP = 'dunAnyPlayerHP'           # 等待副本内任一玩家血量变化值达到一定条件
    EVaddEntityArrowTracker = 'addEntityArrowTracker'         # 创建一个指示箭头
    EVremoveEntityArrowTracker = 'removeEntityArrowTracker'   # 移除一个指示箭头
    EVmoveEntityToFixedPosition = 'moveEntityToFixedPosition' # 将副本内实体移动到指定位置
    EVcreateAvatarMirrorFromRandomPlayer = 'createAvatarMirrorFromRandomPlayer'   # 副本内随机玩家创建镜像
    EVclearEntityHate = "clearEntityHate"         # 清除副本内指定Entity仇恨
    EVcreateSummonInPlayerPosition = "createSummonInPlayerPosition"   # 玩家附近创建召唤物
    EVforceSelectEntityTarget = "forceSelectEntityTarget"         # 强制选择目标
    EVrandomTrigger = 'randomTrigger'             # 随机节点
    EVteleportToPosition = 'teleportToPosition'   # 副本传送至特定位置
    EVchangeEntityForce = 'changeEntityForce'     # 副本内改变阵营
    EVintegrationEvent = 'integrationEvent'       # 副本整合节点
    EVchangeSpaceVar = 'changeSpaceVar'           # 修改space变量
    EVkillEntities = 'killEntities'               # 副本内强制杀死实体节点
    EVdungeonEntityImmuneDeath = 'dungeonEntityImmuneDeath'           # 副本内Entity进入濒死状态触发
    EVifAllSelectEntityImmuneDeath = 'ifAllSelectEntityImmuneDeath'   # 全部配置ID实体濒死则执行下面节点
    EVcheckValue = 'checkValue'                   # 副本检查变量
    EVcreateDungeonTeleporter = 'createDungeonTeleporter'     # 创建副本传送门
    EVmonsterChangeInitState = 'monsterChangeInitState'
    EVmonsterAddHateValue = 'monsterAddHateValue'
    EVstopAiTick = 'stopAiTick'                   # 停止特定EntityAI
    EVstartAiTick = 'startAiTick'                 # 开始特定EntityAI
    EVentityStartRouting = 'entityStartRouting'                   # 实体开始使用路点寻路
    EVentityRouteFinished = 'entityRouteFinished'                 # 实体路点寻路完成
    EVentityRoutingMissingEscort = 'entityRoutingMissingEscort'   # 实体路点寻路中附近没有护卫（没有玩家在distance内）
    EVanyPlayerCinemaPlayEnded = 'anyPlayerCinemaPlayEnded'       # 副本内任一玩家动画播放结束触发
    EVcastCinemaPlay = 'castCinemaPlay'           # 开始播放指定ID动画
    EVplayerRestNum = 'playerRestNum'             # 剩余玩家数量

    EVstopCurTrans = 'stopCurTrans'  # 结束当前副本内所有玩家的变身效果
    EVtriggerGuide = 'triggerGuide'  # 触发新手引导
    EVnewTransPetStart = 'newTransPetStart'  # 小世界战斗/新手变身开始
    EVnewTransPetEnd = 'newTransPetEnd'  # 小世界战斗/新手变身结束

    EVchangeAllPlayerCameraStatus = 'changeAllPlayerCameraStatus'         # 副本内所有玩家切换镜头状态
    EVchangeAllPlayerCameraLookPos = 'changeAllPlayerCameraLookPos'       # 副本内所有玩家镜头朝向某处
    EVrevertAllPlayerCameraStatus = 'revertAllPlayerCameraStatus'       # 恢复副本内玩家的上一个镜头状态

    EVchangeNPCSelectableStatus = 'changeNPCSelectableStatus'     # 切换NPC的可选择状态
    EVchangeEntityDirection = 'changeEntityDirection'             # 切换Entity朝向

    EVtimeFreezeStart = 'timeFreezeStart'     # 时间定格开始
    EVtimeFreezeEnd = 'timeFreezeEnd'         # 时间定格结束
    EVplayerForceTrans = 'playerForceTrans'   # 状态改变/副本内指定玩家强制变身
    EVtaskUndertake = 'taskUndertake'         # 副本内接任务

    EVcreateRandomAppearanceNPC = 'createRandomAppearanceNPC'     # 幻化探险/创建随机外观NPC

    EVcreateRebornPos = 'createRebornPos'     # 创建出生点
    EVremoveRebornPos = 'removeRebornPos'     # 回收出生点

    EVtransferToTheDesignatedMap = 'transferToTheDesignatedMap'

    EVnotifyStartBattleCD = 'notifyStartBattleCD' # 开始战斗前的倒计时
    EVcreateBreakAwayStuckPos = 'createBreakAwayStuckPos'                     # 脱离卡点


FLOW_REST_MONSTER_TAG_GID = 1
FLOW_REST_MONSTER_TAG_CBID = 2
FLOW_REST_MONSTER_TAG_ALL = 3


class DungeonFlowPlayerChooseEnum(object):
    UNKNOWN = 0
    MONSTER_CURRENT_TARGET = 1
    RAND_IN_MONSTER_HATRED_LIST = 2
    RAND_IN_MONSTER_HATRED_LIST_EXCEPT_HIGHEST = 3
    RAND_IN_ALL_PLAYERS = 4
    MONSTER_HATRED_LIST_MONSTER = 5

class FlowAddHateEnum(object):
    all = 1
    rand = 2


class GamePlayMapCheckEnum(object):
    DENY = 0
    ALLOW_WITH_MSG = 1
    ALLOW = 2

def getBranchLineCnt(mapId):
    subType = BD_BDD.datas[mapId]["subType"]

    import gameconfig
    return gameconfig.branchLineCnt(subType)


def getWorldLineStubCnt():
    import gameconfig
    return gameconfig.baseAppCount()

@functools.lru_cache(maxsize=None)
def lineStubMap():
    _dic = {}

    for mapId in MapIdDef.mapWorldSet:
        _dic.setdefault(mapId, {
            'stubName': 'WorldLineStub',
            'lineCount': getBranchLineCnt(mapId),
        })

# 演武场 单独添加，因为其subType不为1
    _dic[7000] = {
        'stubName': 'WorldLineStub',
        'lineCount': getBranchLineCnt(7000),
    }

    return _dic

worldLineMapCellIdxDict = {}
def getWorldLineCellIdx(mapId):
    if len(worldLineMapCellIdxDict) == 0:
        idx = 0
        for mapId in MapIdDef.mapWorldSet:
            worldLineMapCellIdxDict[mapId] = idx
            idx += 1
        worldLineMapCellIdxDict[7000] = idx
    return worldLineMapCellIdxDict[mapId]

gSpaceDict = {
}

import gamePlay_gamePlay as GGD
import gamePlay_singleSceneData as GPSSD

for mapId, mapConfig in GGD.datas.items():
    gSpaceDict.setdefault(mapId, {})
    gSpaceDict[mapId]['map'] = GPSSD.datas.get(mapConfig['sceneRes'], {}).get('tmxRes') \
                              or gSpaceDict[mapId].get('map') \
                              or 'big_world'

    if mapConfig.get('type') == SpaceType.SpaceLine:
        pass

class DungeonSrcKickReason(object):
    DEFAULT = 0
    TIMEOUT = 1
    FORCE = 2

class RouteSuspendReason(object):
    UNKNOWN = 0
    NORMAL = 1
    ESCORT_NO_PLAYER_IN_DISTANCE = 2

class CheckMemberReason(object):
    CHECK_MEMBER_FOR_TEAM_DUEL = 1
    CHECK_MEMBER_FOR_BATTLE_FIELD_REGISTRY = 2
    CHECK_MEMBER_FOR_RAID_DUNGEON_CREATE = 3

class OutfitType(object):
    wing = 1
    hair = 2
    clothes = 3
    picFrame = 4
    mount = 5

class MountExitType(object):
    none = 0
    all = 1
    ride = 2
    fly = 3

class AddOutfitReason(object):
    MOUNT_ITEM = 1
    MOUNT_EVENT = 2
    BUY = 3
    EXP_CARD = 4
    GM = 5
    SCORE = 6
    TOP_LIST = 7
    REWARD = 8
    WEDDING_PARTY = 9
    CHANGE_SEX = 10

class CommonFlagType(object):
    WingFlag = 0
    FirstSummonPet = 1

DelayCallOffsetSec=30

class AddLingShouReason(object):
    normal = 1
    reward = 3
    gm = 4
    gmBot = 5
    gmAll = 6
    moveFromWarehouse = 7

class CreationHostType(object):
    EnumNoHost = 0
    EnumAvatar = 1
    EnumMonster = 2
    EnumSummon = 3
    EnumCreation = 4
    EnumPet = 5
    EnumAvatarMirror = 6
    EnumNPC = 7
    EnumOther = 8

class EntityType(object):
    OTHER = 0
    AVATAR = 1
    MONSTER = 2
    SUMMON = 3
    CREATION = 4
    PET = 5
    AVATAR_MIRROR = 6
    NPC = 7
    COLLECTION = 8

className2EntityType = {
    "Monster": EntityType.MONSTER,
    "Collection": EntityType.COLLECTION,
}


class DressEquipOpStat(object):
    EQUIP_OP_FAILED = 0
    EQUIP_OP_ONLY_DRESS = 1
    EQUIP_OP_REPLACED = 2

class EquipTypes(object):
    #mainType
    MAIN_TYPE_WEAPON = 1
    MAIN_TYPE_CLOTHES = 2
    MAIN_TYPE_HEAD = 3
    MAIN_TYPE_SHOE = 4
    MAIN_TYPE_NECKLACE = 5
    MAIN_TYPE_RING = 6
    MAIN_TYPE_BRACELET = 7
    MAIN_TYPE_BELT = 8

    #subType
    SUBTYPE_WEAPON_MONK = 11
    SUBTYPE_WEAPON_MAGE = 12
    SUBTYPE_WEAPON_WARRIOR = 13
    SUBTYPE_CLOTHES_MONK = 21
    SUBTYPE_CLOTHES_MAGE = 22
    SUBTYPE_CLOTHES_WARRIOR = 23
    SUBTYPE_HEAD_MONK = 31
    SUBTYPE_HEAD_MAGE = 32
    SUBTYPE_HEAD_WARRIOR = 33
    SUBTYPE_SHOE_MONK = 41
    SUBTYPE_SHOE_MAGE = 42
    SUBTYPE_SHOE_WARRIOR = 43
    SUBTYPE_NECKLACE_PHYSIC = 58
    SUBTYPE_NECKLACE_MAGIC = 59
    SUBTYPE_RING_PHYSIC = 68
    SUBTYPE_RING_MAGIC = 69
    SUBTYPE_RING_MONK = 70

    SUBTYPE_BRACELET_PHYSIC = 78
    SUBTYPE_BRACELET_MAGIC = 79
    SUBTYPE_BRACELET_DEFENCE = 80
    SUBTYPE_BELT_MONK = 81
    SUBTYPE_BELT_MAGE = 82
    SUBTYPE_BELT_WARRIOR = 83

    SUBTYPE_ORNAMENTS_RING = (SUBTYPE_RING_PHYSIC, SUBTYPE_RING_MAGIC, SUBTYPE_RING_MONK)
    SUBTYPE_ORNAMENTS_BRACELET = (SUBTYPE_BRACELET_PHYSIC, SUBTYPE_BRACELET_MAGIC, SUBTYPE_BRACELET_DEFENCE)

    ALL_MAINTYPES = (MAIN_TYPE_WEAPON, MAIN_TYPE_CLOTHES, MAIN_TYPE_HEAD, MAIN_TYPE_SHOE, MAIN_TYPE_NECKLACE,
                     MAIN_TYPE_RING, MAIN_TYPE_BRACELET, MAIN_TYPE_BELT)
    ALL_SUBTYPES = (
        SUBTYPE_WEAPON_MONK, SUBTYPE_WEAPON_MAGE, SUBTYPE_WEAPON_WARRIOR,
        SUBTYPE_CLOTHES_MONK, SUBTYPE_CLOTHES_MAGE, SUBTYPE_CLOTHES_WARRIOR,
        SUBTYPE_HEAD_MONK, SUBTYPE_HEAD_MAGE, SUBTYPE_HEAD_WARRIOR,
        SUBTYPE_SHOE_MONK, SUBTYPE_SHOE_MAGE, SUBTYPE_SHOE_WARRIOR,
        SUBTYPE_NECKLACE_PHYSIC, SUBTYPE_NECKLACE_MAGIC,
        SUBTYPE_BELT_MONK, SUBTYPE_BELT_MAGE, SUBTYPE_BELT_WARRIOR
                   ) + SUBTYPE_ORNAMENTS_RING + SUBTYPE_ORNAMENTS_BRACELET

EQUIP_OPR_DROP = 1 # 用于log， 掉落
EQUIP_OPR_PICK = 2 # 用于log， 拾取

class BodyEquipSlot(object):
    EQUIP_WEAPON_SLOT = 1
    EQUIP_CLOTHES_SLOT = 2
    EQUIP_HEAD_SLOT = 3
    EQUIP_SHOE_SLOT = 4
    EQUIP_NECKLACE_SLOT = 5
    EQUIP_RING_LEFT_SLOT = 6
    EQUIP_RING_RIGHT_SLOT = 7
    EQUIP_BRACELET_LEFT_SLOT = 8
    EQUIP_BRACELET_RIGHT_SLOT = 9
    EQUIP_BELT_SLOT = 10

class EquipAttrConst(object):
    AFFIX_DEFAULT_LEVEL_GAP = 5

    EQUIP_BELONGTO_BAG = 0
    EQUIP_BELONGTO_BODY = 1

    RANDOM_ENH_NUM = 5
    RANDOM_ENH_AFFIX_WASHING_INDEX = 0      # 词缀洗练次数
    RANDOM_ENH_UPGRADE_INDEX = 4            # 强化次数

class ItemQuality(object):
    WHITE = 0
    GREEN = 1
    BLUE = 2
    PURPLE = 3
    ORANGE = 4
    RED = 5

    COLL_QUALITY = (WHITE, GREEN, BLUE, PURPLE, ORANGE, RED)
    GLYPH_NO_RANDOM_FIX_QUALITY = (WHITE, GREEN)
    SPIRIT_NO_RANDOM_FIX_QUALITY = (WHITE, GREEN, RED)
    ALL_QUALITY = 255

    @classmethod
    def getRandomQuality(cls):
        return random.choice(cls.COLL_QUALITY)


ALL_SCHOOL_TYPE = CCDD.allSchoolList

class EQUIP_DRESS_TYPE(object):
    OP_NORMAL = 0       #正常装备
    OP_QUICK_DRESS = 1  #快速装备
    OP_AUTO_DRESS = 2   #自动装备

#需要服务端记录的客户端配置数据, 0-10000为纯客户端使用字段，10000开始是服务端会有功能的key
class CliConfigDef(object):
    EQUIP_AUTO_DISA_KEY = 10000                            #装备进背包是否自动分解，首位为是否可交易，余下没一位代表一个品质

    EQUIP_AUTO_DISA_DEFAULT_VAL = 0                        #装备进背包是否自动分解默认值: 0 不分解

class AUTO_DISA_KEY(object):
    # 白
    WHITE = 0
    # 绿
    GREEN = 1
    # 蓝
    BLUE = 2
    # 紫
    PURPLE = 3
    # 金
    ORANGE = 4
    # 红
    RED = 5
    # 可交易
    TRADE = 7
    # 自动分解开关
    AUTOS_WITCH = 8
    # 狩猎 
    HUNTER = 10
    # 副本
    DUNGEON = 11
    # 宝箱
    BOX = 12
    # 武器
    WEAPON = 20
    # 衣服
    CLOTHES = 21
    # 头盔
    HELMET = 22
    # 腰带 
    BELT = 23
    # 项链
    NECKLACE = 24
    # 鞋子
    SHOES = 25
    # 戒指
    RING = 26
    # 手镯
    BRACELET = 27

class AUTO_DISA_MAP(object):
    datas = {
        EquipTypes.MAIN_TYPE_WEAPON: AUTO_DISA_KEY.WEAPON,
        EquipTypes.MAIN_TYPE_CLOTHES: AUTO_DISA_KEY.CLOTHES,
        EquipTypes.MAIN_TYPE_HEAD: AUTO_DISA_KEY.HELMET,
        EquipTypes.MAIN_TYPE_SHOE: AUTO_DISA_KEY.BELT,
        EquipTypes.MAIN_TYPE_NECKLACE: AUTO_DISA_KEY.NECKLACE,
        EquipTypes.MAIN_TYPE_RING: AUTO_DISA_KEY.SHOES,
        EquipTypes.MAIN_TYPE_BRACELET: AUTO_DISA_KEY.RING,
        EquipTypes.MAIN_TYPE_BELT: AUTO_DISA_KEY.BRACELET,
    }

class MessageType(object):
    MSG_TYPE_1 = 1
    MSG_TYPE_8 = 8
    MSG_TYPE_9 = 9
    MSG_TYPE_13 = 13
    MSG_TYPE_14 = 14
    MSG_TYPE_16 = 16
    MSG_TYPE_17 = 17
    MSG_TYPE_18 = 18
    MSG_TYPE_19 = 19
    MSG_TYPE_20 = 20
    MSG_TYPE_21 = 21
    MSG_TYPE_22 = 22
    MSG_TYPE_23 = 23

    COLL_BUTTON_MESSAGE = (MSG_TYPE_8, MSG_TYPE_13, MSG_TYPE_16, MSG_TYPE_23)

class TeammateConfirmFailedReason(object):
    REJECT = 1
    TIMEOUT = 2
    TEAM_STATUS_CHANGE = 3

class SkillUpdateSrc(object):
    Unknown=0
    Equip=1

ClassSkillID=0

FRIEND_LOAD_MSG_NUM = 5
SEARCH_FRIEND_PACK_NUM = 10
SEND_MSG_PACK_NUM = 10
SEND_INIT_PACK_NUM = 10
FRIEND_MSG_MAX_LEN = 999


# <!-- 1：发送申请，2：接受申请，3：删除好友，4：拉黑 -->
FRIEND_OPR_SEND_REQ = 1
FRIEND_OPR_ACCEPT_REQ = 2
FRIEND_OPR_DELETE = 3
FRIEND_OPR_BLACKLIST = 4

ADD_FRIEND_ONLINE = 1
ADD_FRIEND_ACCEPT = 2

class PacketSendStatus(object):
    BEGIN = 1
    MID = 2
    END = 3


class FriendRelation(object):
    FRIEND = 1
    STRANGER = 2


class FriendMsgDir(object):
    SEND = 1
    RECV = 2


class FriendRemoveReason(object):
    BE_DEL = 1
    RECENT_FULL = 2
    REMOVE_RECENT = 3
    BLOCK = 4
    CLIENT_REMOVE = 5


class GuildFlags(object):
    DISSOLVE = 0


class LeaderBoardType(object):
    AVATAR_LEVEL = 1
    AVATAR_SCORE = 2
    GUILD = 3
    ACHIEVEMENT = 4
    AVATAR_LEVEL_RUSH_RANK = 100

    ALL_KEYS = (AVATAR_LEVEL, AVATAR_SCORE, GUILD, AVATAR_LEVEL_RUSH_RANK, ACHIEVEMENT)


class DissolveGuildReason(object):
    NO_MEMBER = 1
    IN_ACTIVE = 2


LEADER_BOARD_UPDATE_INTERVAL = 60 * 20
LEADER_BOARD_PAGE_SIZE = 10
LEADER_BOARD_MAX_LOG_SIZE = 100

GUILD_APPLY_CTX_CHECK_TIME_OUT = 60
GUILD_APPLY_TIME_OUT_DUR = 2 * ONE_DAY_COST_SECONDS
GUILD_MEMBER_SEND_MAX = 20
GUILD_BATCH_NUM = 20
GUILD_EVENT_LOG_MAX_NUM = 100
GUILD_MONEY_TO_GUILD_RATE = 1
GUILD_IN_ACTIVE_TIME = 86400

GUILD_ASSIST_DEDUCT_ITEM = ItemId.COIN
GUILD_ASSIST_DEDUCT_NUM = 1000
GUILD_ASSIST_ADD_BUILD_EXP = 1
GUILD_ASSIST_ADD_GUILD_EXP = 1
GUILD_ASSIST_ADD_GUILD_FUND = 1
GUILD_ASSIST_ADD_GUILD_CONTRIBUTION = 1
GUILD_APPLY_EXPIRED_TIME = ONE_DAY_COST_SECONDS

GUILD_DONATE_EXP = 1
GUILD_DONATE_FUND = 1
GUILD_DONATE_CONTRIBUTION = 1
GUILD_DONATE_MONEY = 1

GUILD_INVITE_DURATION = 10

GUILD_OPR_CREATE = 1 # 创建公会
GUILD_OPR_JOIN = 2 # 加入工会
GUILD_OPR_EXIT = 3 # 退出工会
GUILD_OPR_DISSOLVE = 4 # 解散公会

GUILD_UNION_FORGE = 1 # 联盟建立
GUILD_UNION_BREAK = 2 # 联盟破裂
GUILD_HOSTILE_DECLARE = 3 # 敌对宣战
GUILD_HOSTILE_CEASE = 4 # 敌对撤销


class GuildBuilding(object):
    JU_YING = 1
    WU_HUA = 2
    XIANG_FANG = 3
    YAN_WU = 4
    CANG_KU = 5
    JUN_XU = 6


class GuildTmpFlag(object):
    DIRTY = 0
    ONLINE = 1


class CreateGuildResult(object):
    SUCCESS = 0
    NAME_DUPLICATE = 1
    MAYBE_HAS_GUILD = 2
    CREATE_GUILD_FAILED = 3
    UUID_GEN_FAILED = 4


class ExitGuildReason(object):
    DISSOLVE = 1
    KICK = 2
    LEAVE = 3
    MIGRATE = 4
    DB_ERROR = 5

    NEED_NOTIFY_CLIENT = (KICK, LEAVE)


class FriendFlags(object):
    NEED_FIRST_NOTIFY = 0
    IS_ONLINE = 1
    UNREAD = 2
    NEED_PULL_MSG = 3

class FriendOnlineSrc(object):
    MAKE_FRIENDS1 = 1 # 同意好友请求
    MAKE_FRIENDS2 = 2 # 被同意好友请求
    ONLINE = 3


class JoinGuildReason(object):
    CREATE_GUILD = 1
    ONLINE = 2
    APPLY_JOIN = 3
    DEAL_APPLY = 4

    NEED_NOTIFY_ADD_MEMBER = (APPLY_JOIN, DEAL_APPLY)


class ApplyJoinGuildType(object):
    ONE_KEY = 1
    SINGLE = 2
    INVITE = 3


class JoinGuildEvent(object):
    HAS_GUILD = 1
    MAYBE_REMOVE = 2
    JOIN = 3
    RECORD_APPLY = 4
    FULL = 5
    NOT_ELIGIBLE = 6
    HAS_APPLY = 7

class CrossServerState(object):
    ENUM_IN_CURRENT_SERVER = 1
    ENUM_GOTO_CROSS_SERVER = 2
    ENUM_IN_CROSS_SERVER = 3
    ENUM_GOBACK_FROM_CROSS_SERVER = 4

class CrossServerCBComponent(object):
    ENUM_NONE = 0
    ENUM_BASE = 1
    ENUM_CELL = 2
    ENUM_CLIENT = 3

class CrossServerReasonNo(object):
    DEFAULT = 0
    ENTER_CROSS_SIEGE_WAR = 1

class CrossServerWaitingClientInitTuple(object):
    DEFAULT = 0
    BACKSELECTCHARACTER = 1
    OFFLINE = 2

class RemoteServerEntityCallType(object):
    STUB_NAME = 1
    BOX = 2


class AvatarFlagBase(object):
    pass

FIGHT_BACK_DELAY = 2


class AvatarFlagCell(object):
    AUTO_HEAL_HP = 0
    AUTO_HEAL_MP = 1
    # 空闲返回挂机点
    RETURN_IDLE = 2
    # 队伍共享目标
    TEAM_SHARE_TARGET = 3
    # 被攻击时自动反击
    AUTO_FIGHT_BACK = 4
    # 复活时自动返回
    AUTO_RETURN_AFTER_REVIVE = 5
    # 反击状态
    FIGHT_BACK = 6

    QUICK_SETTING_RANGE = (AUTO_HEAL_HP, AUTO_HEAL_MP, AUTO_FIGHT_BACK, AUTO_RETURN_AFTER_REVIVE)


DEATH_PENALTY_INVALID_REC_TIMES = 255
CUBE_MAX_ENTER_NUM = 300 # 混沌回廊分线最大承载量
CUBE_NEW_LINE_THRESHOLD = 200 # 超过这个值之后，混沌回廊的一层会创建新分线
SIEGEWAR_MAX_ENTER_NUM = 500
CUBE_DAILY_TIMES = 1
CUBE_COIN_ITEM_ID = ItemId.MONEY
CUBE_ENTER_TIME_OUT_DUR = 60
WORLDLINE_ENTER_TIME_OUT_DUR = 60
CUBE_ADD_TIMES_TYPE_NULL = 0
CUBE_ADD_TIMES_TYPE_COIN = 1
CUBE_ADD_TIMES_TYPE_ITEM = 2

MONSTER_BE_ATTACK_CLEAR_DUR = 5 * 60

CUBE_EVENT_ENTER = 1
CUBE_EVENT_EXIT = 2
CUBE_EVENT_ADD_TIME = 3

CUBE_PRAY_BUFF = 1
CUBE_PRAY_DEBUFF = 2

CUBE_SIGN_ARENA = 1

CUBE_PRAY_FREE = 1
CUBE_PRAY_ITEM = 2
CUBE_PREY_YUANBAO = 3 #绑定元宝

CUBE_ROOM_KICK_INTERVAL = 10 # 最多每十秒触发一次踢人的tick

# 下面这个是魔方阵timer cb触发时候的回调类型
CUBE_CB_AUTO_RENEW = 1 # 这个回调是自动延时
CUBE_CB_TIME_OUT = 2 # 这个回调是超时踢出副本
CUBE_CB_PROTECT = 3 # 这个回调是保护结束


class CubeRoomEndTimeReason(object):
    ENTER = 1
    ADD_TIME = 2

class RenewDurStatus(object):
    NONE = 0
    # 等待自动续费, 自动续费通常是提前一分钟执行
    WAIT_AUTO = 1
    # 等待结束
    WAIT_END = 2

class CubeAddTimesReason(object):
    RENEW_USE_COIN = 1
    RENEW_USE_ITEM = 2
    FROM_CLIENT = 3
    CHECK_COND = 4

class MailType(object):
    GLOBAL_MAIL_EXCLUDE_NEW_PLAYERS = 1     #全服邮件，只有在发送全服邮件时刻之前已经创建的角色才能收到
    PLAYER_MAIL = 2                         #单人邮件
    GLOBAL_MAIL_INCLUDE_NEW_PLAYERS = 3     #全服邮件，即使在发送之后创建的角色也可以收到
    GLOBAL_MAIL_ACCOUNT = 4                 #发送给account的邮件

TABLE_NAME_GAME_MAIL = 'game_player_mails'


class WriteToDBResult(object):
    # 保存失败
    FAILED                  = 0
    # 保存成功
    SUCCESS                 = 1
    # 找不到数据库
    MISSING_DB_INTERFACE    = -1
    # 正在归档中
    ARCHIVING               = -2

class StoreLimitType(object):
    PERMANENT = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4

class DropShareRewardType(object):
    RANDOM_ONE = 0
    SELF = 1
    ALL_TEAMMATE = 2
    FIRST_BLOOD = 3

# 每轮刷怪的最大数目
INIT_EACH_EN_LOOP_COUNT = 40


class BuyCreditType(object):
    money = 1
    monthCard = 2
    PermanentGift = 7
    FreePermanentPackage = 8
    holidayGift = 10

class AuctionType(object):
    UNKNOWN = 0
    COIN_AUCTION = 1

class UserForbiddenFlag(object):
    FORBIDDEN_AUCTION = 1

class _AuctionErrno(object):
    from userType import Error as _errno

    def _lateReload(self):
        for _v in self.__class__.__dict__.values():
            if _v.__class__.__name__ == 'Error':
                _v.reloadScript()

    def reloadScript(self):
        import utils
        utils.resetClass(self)
        self._lateReload()


    ERR_AUCTION_UNKNOWN                             = _errno(0)
    ERR_AUCTION_OK                              = _errno(1)

    ERR_AUCTION_TYPE_ERR                        = _errno(20000)     # 交易行类型错误
    ERR_AUCTION_ALREADY_IN_AUCTION              = _errno(20001)     # 交易物品已经在交易行
    ERR_AUCTION_ITEM_ATTR_NOT_DEFINED           = _errno(20002)     # 交易物品属性没有定义
    ERR_AUCTION_INDEX_ALREADY_ADDED             = _errno(20003)     # 交易行索引已经存在
    ERR_AUCTION_INDEX_NOT_FOUND                 = _errno(20004)     # 交易行索引没有找到
    ERR_AUCTION_NOT_IN_AUCTION                  = _errno(20005)     # 交易行物品没有找见
    ERR_AUCTION_CACHE_NOT_INIT                  = _errno(20006)     # 玩家交易数据没有初始化完毕
    ERR_AUCTION_AVATAR_GRID_FULL                = _errno(20007)     # 玩家可交易数量已满
    ERR_AUCTION_DEDUCT_ITEM_ERROR               = _errno(20008)     # 玩家(出售时)尝试扣除物品失败
    ERR_AUCTION_DEDUCT_ITEM_NOT_FOUND           = _errno(20009)     # 玩家(出售时候)没有找到物品
    ERR_AUCTION_BUY_ITEM_NOT_ENOUGH             = _errno(20010)     # 玩家购买物品时物品交易行数量不足
    ERR_AUCTION_COIN_NOU_ENOUGH                 = _errno(20011)     # 玩家铜贝不足
    ERR_AUCTION_ITEM_IS_LOCKED                  = _errno(20012)     # 交易行物品被锁住(暂时有其他交易进行)
    ERR_AUCTION_BUY_MUST_NOT_BE_STACKED         = _errno(20013)     # 交易物品必须不可堆叠
    ERR_AUCTION_BUY_MUST_BE_STACKED             = _errno(20014)     # 交易物品必须可堆叠
    ERR_AUCTION_SALE_ITEM_NUM_ERROR             = _errno(20015)     # 交易物品數量错误
    ERR_AUCTION_ITEM_ALREADY_BE_BINDED          = _errno(20016)     # 交易物品被绑定
    ERR_AUCTION_IS_IN_NOTIFY                    = _errno(20017)     # 交易物品在公示期
    ERR_AUCTION_REVIEW_NOT_FOUND                = _errno(20019)     # 审核物品(铜贝/金丝玉贝)未找到
    ERR_AUCTION_REVIEWED_NUMBER_NOT_ENOUGH      = _errno(20020)     # 已审核物品不足
    ERR_AUCTION_ITEM_IN_COOLDOWN                = _errno(20021)     # 交易物品正在冷却
    ERR_AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH      = _errno(20022)     # 玩家背包剩余格子不足
    ERR_AUCTION_CANCEL_SALE_ITEM_NOT_FOUND      = _errno(20023)     # 下架物品没有找到
    ERR_AUCTION_CANCEL_SALE_GBID_NOT_MATCH      = _errno(20024)     # 下架物品PlayerGBID不匹配
    ERR_AUCTION_ITEM_CANNOT_CANCEL_SALE         = _errno(20025)     # 物品无法被下架
    ERR_AUCTION_IS_EXPIRED                      = _errno(20026)     # 物品已经过期
    ERR_AUCTION_PLAYER_BAG_IS_LOCKED            = _errno(20027)     # 玩家背包被锁住, 无法交易
    ERR_AUCTION_BUY_CHECK_NOT_MATCH             = _errno(20028)     # 玩家购买时校验不通过
    ERR_AUCTION_FOLLOWED_ITEM_MAXIMUM           = _errno(20029)     # 玩家关注物品到达上限
    ERR_AUCTION_SALE_RECOMMAND_PRICE_NOT_DEF    = _errno(20030)     # itemId没有对应推荐定价
    ERR_AUCTION_SALE_RECOMMAND_PRICE_OOF        = _errno(20031)     # itemId定价超过推荐百分比
    ERR_AUCTION_UNLOCK_GRID_MAXIMUN             = _errno(20032)     # 交易行解锁格子到达上限
    ERR_AUCTION_UNLOCK_COST_NOT_ENOUGH          = _errno(20033)     # 交易行解锁格子扣除物品不足
    ERR_AUCTION_MONEY_NOU_ENOUGH                = _errno(20034)     # 玩家金币不足
    ERR_AUCTION_PLAYER_NOT_IN_GUILD             = _errno(20035)     # 玩家不在对应帮会中
    ERR_AUCTION_HOMECOMP_ITEM_UN_IDENTIFIED     = _errno(20037)     # 出售家具未鉴定
    ERR_AUCTION_PLAYER_BAG_TYPE_UNKNOWN         = _errno(20038)     # 交易行背包类型未知
    ERR_AUCTION_CANNOT_BUY_SELF_ITEM            = _errno(20039)     # 交易行无法购买自己卖出的商品
    ERR_AUCTION_PLAYER_MAIL_SPACE_FULL          = _errno(20040)     # 玩家邮件剩余空间不足
    ERR_AUCTION_SALED_ITEM_REJECTED             = _errno(20041)     # 交易行对应物品无法出售
    ERR_AUCTION_EQUIP_IN_DROP_REPAIR            = _errno(20042)     # 玩家装备处于掉落修复状态
    ERR_AUCTION_ITEM_IN_BAG_LOCKED_STATUS       = _errno(20043)     # 交易行物品处于背包锁住状态
    ERR_AUCTION_ITEM_IS_FORBIDDEN               = _errno(20044)     # 交易行物品不允许上架
    ERR_AUCTION_SALE_ITEM_ID_ERROR              = _errno(20045)     # 交易物品ID错误

    ERR_AUCTION_IDIP_GM_BAN                     = _errno(20100)     # IDIP禁止

AuctionErrno = _AuctionErrno()

class AuctionItemStatus(object):
    """
    - 状态流转定义:
        INIT --|-------------|--> SELLING --|-------------|--> |--> SELLED
               |--> NOTIFY --|              |--> REVIEW --|    |--> CANCELD
                                                               |============> EXPIRED
    """

    ENUM_INIT = 0
    ENUM_NOTIFY = 1
    ENUM_SELLING = 2
    ENUM_REVIEW = 3
    ENUM_SELLED = 4
    ENUM_CANCELD = 5
    ENUM_EXPIRED = 6

    COLL_INAUCTION = (ENUM_NOTIFY, ENUM_SELLING, ENUM_EXPIRED)
    COLL_CAN_BEFOLLOWED = (ENUM_NOTIFY, ENUM_SELLING)
    COLL_CAN_BE_TYPEDFOLLOWED = (ENUM_SELLING, )

class AuctionSource(object):
    UNKNOWN = 0
    FROM_PLAYER = 1

# 推荐关注商品大类
class AuctionItemCategoryCollection(object):
    START_KEY = 2001
    MAX_COUNT = 20
    CHECK_TIP_INTERVAL = 1

# 公示关注具体商品
class AuctionIdCollection(object):
    START_KEY = 2501
    MAX_COUNT = 20
    CHECK_TIP_INTERVAL = 1

# 公示关注商品大类
class AuctionIdCategoryCollection(object):
    START_KEY = 3001
    MAX_COUNT = 20
    CHECK_TIP_INTERVAL = 1

DROP_REMOTE_CACHE_EXPIRE_TIME = 60
DROP_DROP_EXPIRE_DELAY = 5
DROP_PICK_EXPIRE_DELAY = 10

class DrawCardPoolMacro(object):
    CHECK_TIME_LIMIT_INTERVAL = 3
    CHECK_TIME_LIMIT_TYPE_LOGIN = 1
    CHECK_TIME_LIMIT_TYPE_TIMER = 2

class DropType(object):
    TYPE_DROP                        = 1 #// 掉落
    TYPE_TAKE                        = 2 #// 拾取
    TYPE_TAKE_WAIT_DROP_GET          = 3 #// 捡起来等待领取
    TYPE_REDEEM_WAIT_DROP_GET        = 4 #// 赎回等待领取
    TYPE_GIVEUP_WAIT_DROP_GET        = 5 #// 捡起掉落的人主动放弃, 待失主领取
    TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET = 6 #// 赎回倒计时结束，待拾取者领取
    TYPE_RETURN_WAIT                 = 7 #// 等待返还
    TYPE_RETURN_GET                  = 8 #// 待原主人领取
    TYPE_REWARD                      = 9 #// 领取奖励

class DropNotifyType(object):
    NOTIFY_REMOVE_TAKE                      = -2 #// 移除拾取
    NOTIFY_REMOVE_DROP                      = -1 #// 移除掉落
    NOTIFY_REMOVE_ALL                       = 0  #// 移除所有
    NOTIFY_TYPE_DROP                        = 1  #// 掉落
    NOTIFY_TYPE_TAKE                        = 2  #// 拾取
    NOTIFY_TYPE_TAKE_WAIT_DROP_GET          = 3  #// 捡起来等待领取
    NOTIFY_TYPE_REDEEM_WAIT_DROP_GET        = 4  #// 赎回等待领取
    NOTIFY_TYPE_GIVEUP_WAIT_DROP_GET        = 5  #// 捡起掉落的人主动放弃, 待失主领取
    NOTIFY_TYPE_REDEEM_EXPIRE_WAIT_TAKE_GET = 6  #// 赎回倒计时结束，待拾取者领取
    NOTIFY_TYPE_RETURN_WAIT                 = 7  #// 等待返还
    NOTIFY_TYPE_RETURN_GET                  = 8  #// 待原主人领取
    NOTIFY_TYPE_REWARD                      = 9  #// 领取奖励
    
class DropWayType(object):
    DROP_WAY_TYPE_1 = 1 # 一个库内，不放回，随出若干件道具，不重复
    DROP_WAY_TYPE_2 = 2 # 一个库内，放回，随出若干件道具，可以重复
    DROP_WAY_TYPE_3 = 3 # 库内的道具全部掉落，无视权重
    DROP_WAY_TYPE_4 = 4 # 库内道具依次单独判定是否掉落，每个道具的掉落概率 = 该道具权重 / 10000
    DROP_WAY_TYPE_5 = 5 # 库内道具从上到下挨个判定，每个对象的掉落概率 = 该道具权重 / 10000，当判定成功掉落时，停止随机

class DropConditionType(object):
    DROP_CONDITION_TYPE_1 = 1 # 等级区间
    DROP_CONDITION_TYPE_2 = 2 # 职业
    DROP_CONDITION_TYPE_3 = 3 # 任务
    DROP_CONDITION_TYPE_4 = 4 # 城战灵核


class DropTatgerType(object):
    ITEM = 1 # 物品
    PACKAGE = 2 # 子包
    EQUIPMENT = 3 # 装备
    OTHER = 4 # 其他

class ItemReturnReason(object):
    NOT_RETURN = 0 # 不退回
    DROP_EXPIRE = 1 # 掉落过期
    LEASE_EXPIRE = 2 # 租赁过期

class LeaseRecordType(object):
    LEASE_OUT = 1 # 出租
    LEASE_IN = 2 # 租入

class EnemyRecordType(object):
    KILL_ENEMY = 1 # 击杀敌人
    BE_KILL_BY_ENEMY = 2 # 被敌人击杀


SEND_ENEMY_RECORD_BATCH_NUM = 10


class MoralType(object):
    MORAL_NOT_CHANGE = 0 # 善恶值保持不变
    MORAL_COULD_CHANGE = 1


MORAL_SRC_TYPE_KILL_PLAYER = 1 # 杀人
MORAL_SRC_TYPE_KILL_MONSTER = 2 # 杀怪物


class DungeonFlowMoveAni(object):
    DEFAULT = 0
    RUN01 = 1
    RUN02 = 2

class DungeonCustomAreaType(object):
    RECTANGLE = 0
    CIRCLE = 1
    LINE = 2

    @staticmethod
    def fetchRectVal(data):
        return data['Length'], data['Width']

    @staticmethod
    def fetchCircleRadius(data):
        return data['Radius']

    @staticmethod
    def fetchLineVal(data):
        return data['Length']


class LogOnEnterType(object):
    NONE = 0
    CUBE = 1
    WONDER_LAND = 2


class AchievementFlag(object):
    FINISHED = 0

ACHIEVE_SRC_NEW = 1
ACHIEVE_SRC_UPDATE = 2

# 1:新增 2.完成 3.领取
ACHIEVE_STATE_NEW = 1
ACHIEVE_STATE_FINISH = 2
ACHIEVE_STATE_RECEIVE = 3


class AchieveType(object):
    LEVEL = 1 # 达到等级
    SCORE = 2 # 达到分数
    KILL_MONSTER = 3 # 击杀怪物
    DRAW_CARD = 4 # 精灵契约
    UNLOCK_MOUNT = 5 # 解锁坐骑
    JOIN_GUILD = 6 # 加入帮会
    ADD_FRIEND = 7 # 添加好友
    MAKE_EQUIPMENT = 8 # 制造装备
    ENHANCE_EQUIPMENT = 9 # 强化装备
    EQUIPMENT_WITH_SPIRIT = 10 # 装备附灵
    LEVEL_UP_SKILL = 11 # 技能升级
    ACTIVITY = 12 # 活动
    PET_BATTLE = 13 # 精灵出战
    PET_EQUIP = 14 # 携带精灵秘宝
    LOGIN_DAYS = 15 # 登录天数
    DEAD_TIMES = 16 # 死亡次数
    DO_COLLECT = 17 # 采集次数
    USE_POTION = 19 # 使用药剂
    SUB_TASK = 20 # 支线任务
    MAIN_TASK = 21 # 主线任务
    HOOK_TASK_REWARD = 22 # 悬赏任务
    LEADER_BOARD = 24 # 排行榜
    SIEGE_KILL = 25 # 城战击杀
    PERSONAL_BOX = 26 # 个人宝箱
    VIEWPOINT = 27 # 景观点
    KILL_TAR_SUFFIX_MONSTER = 28 # 击杀特殊词缀怪物
    KILL_TAR_MONSTER = 29 # 击杀特定怪物
    ENEMY = 30 # 仇敌
    DUEL = 31 # 切磋
    WONDERLAND_KILL = 32 # 野外击杀
    BOUNTY = 33 # 悬赏
    CRUSADE = 34 # 普通讨伐
    CHIEF = 35 # 首领讨伐
    COLLECT = 38 # 收集
    EQUIP_QUALITY = 39 # 穿戴装备品质
    MINE_COLLECT = 40 # 矿石采集
    SYNTHESIS = 41 # 合成
    MAX_MONEY = 42 # 携带非绑元宝
    AUCTION_MONEY = 43 # 交易行获得元宝
    INSCRIPTION = 44 # 铭文
    MERIDIAN = 45 # 经脉
    GUILD_CONTRIB = 46 # 帮会贡献
    GUILD_ACTIVITY = 47 # 帮会活动

class AchieveGuildActivityType(object):
    BOSS = 1 #帮会副本boss

class AchieveBountyType(object):
    BE_BOUNTY = 1
    PUBLISH_BOUNTY = 2
    FINISH_BOUNTY = 3

class DuelFlag(object):
    IN_DUEL = 0
    READY = 1
    FIGHT = 2


MAX_DUEL_DISTANCE = 20


class PotionState(object):
    AUTO = 0
    BIND = 1


class DuelFinishReason(object):
    NORMAL = 0
    THIRD_DAMAGE = 1
    SAFE_AREA = 2
    EXCEED_RANGE = 3

DUEL_RECOVER_PERCENT = 0.1

CROSS_ERR_CODE_SUCCESS = 0
CROSS_ERR_CODE_COMMON = 1
CROSS_ERR_CODE_GUILD_NOT_FOUND = 2
CROSS_ERR_CODE_RELATION_MAX_NUM_GUILD1 = 3
CROSS_ERR_CODE_RELATION_MAX_NUM_GUILD2 = 4
CROSS_ERR_CODE_RELATION_EXISTS = 5


class GuildRelationType(object):
    NONE = 0
    UNION = 1
    ENEMY = 2

# WONDERLAND start
MYSTIC_SUMMIT_FLOORS = [1, 2, 3]
WONDERLAND_LINE_NO = 0
WONDERLAND_MAX_ENTER_NUM = 300
WONDERLAND_COIN_ITEM_ID = ItemId.MONEY

WONDER_LAND_DUR_RENEW = 1 # 试炼峰续期
WONDER_LAND_DUR_TIMEOUT = 2 # 试炼峰超时

WONDER_LAND_ENTER_TYPE_TICKET = 1 # 购票进入
WONDER_LAND_ENTER_TYPE_LEFT_TIME = 2 # 还有剩余时间

MORPH_BUILD_STATE = 1 # 变身状态对应技能在build里面对应的状态

BLAZE_CHECK_DIS = 50 # 快速移动监测距离
BLAZE_TIMEOUT = 6

class WonderAddTicketReason(object):
    FROM_CLIENT = 1
    CHECK_COND = 2
    RENEW_USE_COIN = 3
    RENEW_USE_ITEM = 4
# WONDERLAND end

WONDER_LAND_EVENT_ENTER = 1
WONDER_LAND_EVENT_EXIT = 2
WONDER_LAND_EVENT_ADDTIME = 3

# 城战阶段
class SiegeWarState(object):
    NOT_OPEN = 0 #未开启
    SIGN_UP = 1 #报名
    PREPARE_WAR = 2 #宣战期
    WAR_COUNT_DOWN = 3 #已宣战，倒计时期
    WAR = 4 #城战期
    WAR_END = 5 #城战结束，城池管理期

class SiegeWarBiddingResult(object):
    WRONG_STATE = 0
    NOT_ENOUGH_MONEY = 1
    SAME_GUILD = 2
    OUTBID = 3


class SiegeWarSignUpResult(object):
    SUCCESS = 0
    NO_PERMISSION = 1
    ALREADY_SIGN_UP = 2
    NO_MONEY = 3
    IS_CITY_OWNER = 4

class SiegeWarDeclareWarResult(object):
    SUCCESS = 0
    SPECIAL_DAY = 1
    NO_YUXI = 2
    ALREADY_DECLARED = 3
    NO_PERMISSION = 4
    WRONG_TIME = 5
    QUERYING_RESULT = 6

class SiegeWarMonsterCustomId(object):
    SIEGE_BOSS = 'siegeBoss'    #攻城兽
    REINFORCE = 'reinforce'     #援军据点
    MAIN_GATE = 'mainGate'      #主城门
    ORDER_GATE = 'orderGate'    #副城门
    BOW = 'bow'                 #箭塔
    GATE_AIRWALL = 'gateAirwall' #城门空气墙
    ORDER_GATE_AIRWALL = 'orderGateAirwall' #副城门空气墙
    ATTACK_AIRWALL = 'attackAirwall' #进攻方空气墙
    DEFEND_AIRWALL = 'defendAirwall' #防守方空气墙
    GATE_REBORN = 'gateRevive' #城门复活点
    ATTACK_REBORN = 'attackRevive' #进攻方复活点
    DEFEND_REBORN = 'defendRevive' #防守方复活点

class SiegeWarMonsterType(object):
    SIEGE_BOSS = 1              #攻城兽
    REINFORCE = 2               #援军据点
    MAIN_GATE = 3              #主城门
    ORDER_GATE = 4             #副城门
    BOW = 5                    #箭塔
    GATE_AIRWALL = 6           #城门空气墙
    ORDER_GATE_AIRWALL = 7     #副城门空气墙
    ATTACK_AIRWALL = 8         #进攻方空气墙
    DEFEND_AIRWALL = 9         #防守方空气墙
    GATE_REBORN = 10           #城门复活点
    ATTACK_REBORN = 11         #进攻方复活点
    DEFEND_REBORN = 12         #防守方复活点

class SiegeWarMinimapDataType(object):
    TYPE = 0
    HP = 1
    POS = 2
    CAMP = 3
    CONFIG_ID = 4
    INVOKED = 5

siegeWarMonsterEnumDict = {
    SiegeWarMonsterCustomId.SIEGE_BOSS: SiegeWarMonsterType.SIEGE_BOSS,
    SiegeWarMonsterCustomId.REINFORCE: SiegeWarMonsterType.REINFORCE,
    SiegeWarMonsterCustomId.MAIN_GATE: SiegeWarMonsterType.MAIN_GATE,
    SiegeWarMonsterCustomId.ORDER_GATE: SiegeWarMonsterType.ORDER_GATE,
    SiegeWarMonsterCustomId.BOW: SiegeWarMonsterType.BOW,
    SiegeWarMonsterCustomId.GATE_AIRWALL: SiegeWarMonsterType.GATE_AIRWALL,
    SiegeWarMonsterCustomId.ORDER_GATE_AIRWALL: SiegeWarMonsterType.ORDER_GATE_AIRWALL,
    SiegeWarMonsterCustomId.ATTACK_AIRWALL: SiegeWarMonsterType.ATTACK_AIRWALL,
    SiegeWarMonsterCustomId.DEFEND_AIRWALL: SiegeWarMonsterType.DEFEND_AIRWALL,
    SiegeWarMonsterCustomId.GATE_REBORN: SiegeWarMonsterType.GATE_REBORN,
    SiegeWarMonsterCustomId.ATTACK_REBORN: SiegeWarMonsterType.ATTACK_REBORN,
    SiegeWarMonsterCustomId.DEFEND_REBORN: SiegeWarMonsterType.DEFEND_REBORN,
}

siegeWarMonsterPropIdTypeDict = {
    SiegeWarMonsterCustomId.MAIN_GATE: 1,
    SiegeWarMonsterCustomId.REINFORCE: 3,
    SiegeWarMonsterCustomId.SIEGE_BOSS: 4,
    SiegeWarMonsterCustomId.BOW: 5,
}

siegeWarMiniMapNeedSync = {
    SiegeWarMonsterType.SIEGE_BOSS: True,
    SiegeWarMonsterType.REINFORCE: True,
    SiegeWarMonsterType.MAIN_GATE: True,
    SiegeWarMonsterType.ORDER_GATE: True,
    SiegeWarMonsterType.BOW: True,
}

class SiegeWarGameState:
    SIEGE_WAR_STATE_PREPARE = 0
    SIEGE_WAR_STATE_BATTLE = 1
    SIEGE_WAR_STATE_BATTLE_END_AND_HAS_LOSER = 2
    SIEGE_WAR_STATE_BATTLE_END_AND_NO_LOSER = 3
    SIEGE_WAR_STATE_END = 4

class SiegeWarEnterResult:
    SUCCESS = 0
    NOT_START = 1
    NO_ENTRY_QUALIFICATION = 2
    NOT_ENOUGH_NUM = 3

SIEGEWAR_WANTED_BUFF = 64000096
SIEGEWAR_PARE_ACTIVITY_ID = 2
SIEGEWAR_GO_BACK_LINENO = 1002

class ActivityControlType(object):
    # 单人
    SINGLE = 0
    # 组队
    TEAM = 1
    # 组团
    RAID = 2

PARE_ACTIVITY_ID = 100

class GuildTaskType(object):
    COLLECTION = 1  #采集
    DONATION = 2    #帮会捐献
    ENTERMAP = 3    #进入地图
    COMPLETEMAP = 4 #完成地图
    DUEL = 5 # 完成切磋

#雷击区域buff
LIGHTNINGAREABUFF = 64004952

ANCHOR_CAST_DUR = 1

# 铭文效果类型
class InscriptionEffectType(object):
    # 最终伤害提升百分比
    DAMAGE_INCREASE_RATIO = 1
    # 最终伤害提升值
    DAMAGE_INCREASE_VALUE = 2
    # 技能倍率提升
    SKILL_DAMAGE_INCREASE_RATIO = 3
    # 技能命中率
    SKILL_HIT_INCREASE_RATIO = 4
    # 技能暴击提升概率
    SKILL_CRITIAL_HIT_INCREASE_RATIO = 5
    # 技能暴击伤害提升概率
    SKILL_CRITIAL_DAMAGE_INCREASE_RATIO = 6
    # 护盾值提升
    SHIELD_INCREASE_VALUE = 7
    # 护盾值提升百分比
    SHIELD_INCREASE_RATIO = 8
    # 技能等级提升值
    SKILL_LEVEL_INCREASE_VALUE = 9
    # 技能充能提升值
    SKILL_CHARGE_INCREASE_VALUE = 10
    # 蓝耗减少值
    MANA_DECREASE_VALUE = 11
    # 附带效果
    ATTACH_EFFECT= 12
    # 附加buff/debuff
    ADD_EFFECT = 13
    # buff时间延长
    EFFECT_TIME_ADD_VALUE = 14
    # 增加攻击目标数
    ATTACK_TARGET_ADD_VALUE = 15
    # 冷却缩减
    MODIFY_CD = 16
    # 概率刷新CD
    REFRESH_CD = 17
    # 增加伤害次数
    DAMAGE_HIT_ADD_VALUE = 18
    # 创生物次数增加（频率改变）
    CREATION_ADD_PHASE_WITH_FREQUENCY = 19
    # 创生物次数增加（持续时间改变）
    CREATION_ADD_PHASE_WITH_LAST_TIME = 20
    # 提升释放距离
    SKILL_RELEASE_DISTANCE_ADD_VALUE = 21
    # 提升技能范围
    SKILL_RELEASE_RANGE_ADD_VALUE = 22
    # 血量条件触发
    BLOOD_TRIGGER_RATIO = 23
    # 替换技能
    REPLACE_SKILL = 24
    # 技能释放次数提升值
    SKILL_RELEASE_ADD_COUNT= 25
    # 随机单参整数类型
    CHECK_RANDOM_ONE_PARAM_INT_TYPE = (
            DAMAGE_INCREASE_VALUE,
            SKILL_HIT_INCREASE_RATIO,
            SKILL_CRITIAL_HIT_INCREASE_RATIO,
            SHIELD_INCREASE_VALUE,
            SKILL_CHARGE_INCREASE_VALUE,
            MANA_DECREASE_VALUE,
            ATTACK_TARGET_ADD_VALUE,
            MODIFY_CD,
            DAMAGE_HIT_ADD_VALUE,
            CREATION_ADD_PHASE_WITH_FREQUENCY,
            CREATION_ADD_PHASE_WITH_LAST_TIME,
            DAMAGE_INCREASE_RATIO,
            SKILL_DAMAGE_INCREASE_RATIO,
            SKILL_CRITIAL_DAMAGE_INCREASE_RATIO,
            SHIELD_INCREASE_RATIO,
            REFRESH_CD,
            SKILL_RELEASE_RANGE_ADD_VALUE,
            SKILL_RELEASE_DISTANCE_ADD_VALUE,
    )
    # 随机单参浮点类型
    CHECK_RANDOM_ONE_PARAM_FLOAT_TYPE = (
        DAMAGE_INCREASE_RATIO,
        SKILL_DAMAGE_INCREASE_RATIO,
        SKILL_CRITIAL_DAMAGE_INCREASE_RATIO,
        SHIELD_INCREASE_RATIO,
        REFRESH_CD,
        SKILL_RELEASE_RANGE_ADD_VALUE,
        SKILL_RELEASE_DISTANCE_ADD_VALUE,
    )
    # 单参类型
    CHECK_ONE_PARAM_TYPE = (
        SKILL_LEVEL_INCREASE_VALUE,
        REPLACE_SKILL,
        SKILL_RELEASE_ADD_COUNT,
        ADD_EFFECT,
    )
    # 双参类型
    CHECK_TWO_PARAM_TYPE = (
        EFFECT_TIME_ADD_VALUE,
    )
    # 三参类型
    CHECK_THREE_PARAM_TYPE = (
        ATTACH_EFFECT,
    )

BOUNTY_TASK_UI_ID = 'UIRewardTaskPanel'

class CharacterType(object):
    # 道士
    Taoist = 1001
    # 法师
    Mage = 1002
    # 战士
    Warrior = 1003

class SkillSwitchStatus(object):
    # 手动
    MANUAL= 0
    # 自动
    AUTO = 1
    # 有效的取值
    VALID_STATUS = (MANUAL, AUTO)

class EquipmentManufactureType(object):
    # 左侧制造
    MANUFACTURE_LEFT = 1
    # 右侧制造
    MANUFACTURE_RIGHT = 2

SHOW_POPREWARD_DETAIL_KEY=['taskId', 'itemId', 'useNum', 'monsterId', 'collectionId', 'mailGBID', 'achievementId', 'signInDayNo', 'buyCreditId', 'storeId', 'goodsId', 'goodsNum']

class CancelGatherReason(object):
    Client = 0
    Teleport = 1
    BeDamaged = 2
    CrossServer = 3
    GatherCheck = 4
    ApplyGatherCheck = 5
    ApplyGather = 6


class MonsterType(object):
    # 对应creep base表中的type字段
    NORMAL = 1 # 小怪
    ELITE = 2 # 精英
    ADVANCE = 9 # 高规格首领


LARGE_ENTITY_DEFAULT_AOI = 250

class MonsterSuffix(object):
    # 对应creep base表中的nameSuffixID字段
    NORMAL = 1 # 小怪
    ELITE = 4 # 头目
    BOSS = 5 # 首领
    LUCKY = 7 # 幸运怪

    NEED_LOG_SUFFIX = (ELITE, BOSS, LUCKY)

class WorldLineSceneState(object):
    THUNDER = 0 # 落雷
    WIND = 1 # 风场
    LEI_JI = 2 # 雷buff会持续叠加的


class DunCustomId(object):
    THUNDER = '1' # 落雷
    POS_FOR_SKILL = '2' # 用于直接让技能里面设置位置


WORLD_BOSS_MOCK_REFRESH_TIME = 300


# ----------------------------- cube mock start -----------------------------
CUBE_HALL_MAX_NUM = 150
CUBE_COW_DUR_INTERVAL = 5

class TeleporterType(object):
    NONE = 0
    CUBE_RANDOM = 1 # 在混沌回廊随机传送
    CUBE_BACK = 2 # 从奶牛房返回原房间
    TO_CUBE_COW = 3 # 传送到混沌回廊奶牛关
    TO_CUBE_MAP_ID = 4 # 进混沌回廊，customID作为mapId用


class CubeRoomType(object):
    NORMAL = 1 # 普通房
    COW = 2 # 奶牛房
    READY = 3 # 大厅
    TIDE = 4 # 狂潮

    NeedKickTup = (COW, TIDE)


class QuotaDurStatus(object):
    NORMAL = 0
    ENTER = 1
    PROTECT = 2 # 混沌回廊切换房间后前几秒钟不开启倒计时


ENTER_CUBE_HAS_LEFT_TIME = 0
ENTER_CUBE_DEDUCT_TIMES = 1
ENTER_CUBE_SWITCH_LINE = 2


# ----------------------------- cube mock end -----------------------------

HATE_CNT_TYPE_MOVE = 1
HATE_CNT_TYPE_ATTACK = 2

# ----------------------------- auth avatar start ---------------------------
class ClientCallChannel:
    MAIN_CHANNEL = 0
    SUB_CHANNEL = 1
    ALL_CHANNEL = 2
    NONE = 3

AUTH_AVATAR_LOGIN_EXPIRE_TIME = 30 # 30seconds 由于需要跨进程，30秒内跨进程登录
AUTH_ROLE_INFO_EXPIRE_TIME = 30 # 30seconds 这是发出授权申请，到对方接受
AUTH_AVATAR_LEND_EXPIRE_TIME = 30 #角色授权后，对方能登录30天

class AccountHostType(object):
    NONE = 0
    HOST = 1 # 主人的号
    AUTH = 2 # 代理的号

# 授权建立过程中的状态
class AuthState(object):
    NORMAL = 0
    AGREE_AUTH = 1


SELECT_GAME_FAILED_AUTH_EXPIRED = 1
SELECT_GAME_FAILED_MORAL_LOW = 2


class AuthPerFlags(object):
# 1.	商城（默认：关闭）
# 2.	交易行（默认：关闭）
# 3.	仓库提取（默认：开启）
# 4.	装备制造、培养（默认：开启）
# 5.	道具制造、合成（默认：开启）
# 6.	精灵抽卡（默认：开启）
# 7.	帮会（默认：开启）
    MALL = 1 # 商城
    TRADE = 2 # 交易行
    WAREHOUSE = 3 # 仓库提取
    EQUIPMENT = 4 # 装备制造、培养
    PROP = 5 # 道具制造、合成
    POKER = 6 # 精灵抽卡
    GUILD = 7 # 帮会
# ----------------------------- auth avatar end ---------------------------

# bit 位
CELL_FLAGS_IS_HOST_AVATAR = 0
CELL_FLAGS_IS_SPECIAL_AI = 1
CELL_FLAGS_IS_AUTH = 2
CELL_FLAGS_PK_SAFE = 3
CELL_FLAGS_IS_MINE_WAR_SPACE = 4


CALL_LIMIT_SCATTER = 1

class ItemLockStatus(object):
    UNLOCKED = 0 # 未上锁
    LOCKED = 1 # 已上锁
    VALID_STATUS = (UNLOCKED, LOCKED)

class WorkshopResult(object):
    WORKSHOP_UNKNOW                         = 0     # 未知错误
    WORKSHOP_SUCCESS                        = 1     # 成功
    WORKSHOP_FAIL                           = 2     # 失败
    WORKSHOP_LIMIT_FUNC_NOT_OPEN            = 10000 # 功能未开放
    WORKSHOP_LIMIT_MANUFACTURE_NOT_OPEN     = 10001 # 制造未开放
    WORKSHOP_LIMIT_ILLEGAL_CONFIG           = 10002 # 配置非法
    WORKSHOP_LIMIT_BAG_SPACE                = 10003 # 背包满了
    WORKSHOP_LIMIT_BAG_LOCK                 = 10004 # 背包锁了
    WORKSHOP_LIMIT_BATCH_COUNT              = 10005 # 批量制造次数限制
    WORKSHOP_LIMIT_CURRENCY_IS_NOT_ENOUGH   = 10006 # 货币不足
    WORKSHOP_LIMIT_ITEM_IS_NOT_ENOUGH       = 10007 # 道具不足
    WORKSHOP_LIMIT_OVER_MONTHLY_LIMIT       = 10008 # 超出每月限制

class WorkshopOpenStatus(object):
    CLOSE = 0 # 关闭
    OPEN = 1  # 开放

class ItemBelongToType(object):
    BELONGTO_BAG = 1
    BELONGTO_BODY = 2

#
class RedBagType(object):
    NORMAL = 1 # 平均红包
    LUCKLY = 2 # 拼手气红包
class RedBagChannel(object):
    WORLD = 2 # 世界红包
    GUILD = 3 # 公会红包
RED_BAG_CHANNELS = (RedBagChannel.WORLD, RedBagChannel.GUILD)

#特殊药品类增加总携带数量上限
BAG_LIMIT_ITEM_TYPE_DATA = (0, 19)

class AvatarDailyProps(metaclass=UniqueIntEnum):
    dailyTest = 0
    releaseRbNum = 1  # 今日已发红包数量
    fetchRbNum = 2   # 今日已领红包数量

class AvatarWeeklyProps(metaclass=UniqueIntEnum):
    weeklyTest = 0

class EquipConstVale(object):
    # 装备强化破碎标记
    ENHANCEMENT_BROKEN_FLAG = -99

class UIUIVisibleType(object):
    NONE = 0
    TASK = 1
    LEVEL = 2
    DAY = 3

class AuctionConst(object):
    # 我的关注
    ATTENTION_MY = 1
    # 商品关注
    ATTENTION_GOODS = 100

TEAM_STATISTIC_TYPE_TO_LIST = {
    TeamStatisticType.DAMAGE: 'dmgList',
    TeamStatisticType.HEAL: 'healList',
    TeamStatisticType.HURT: 'hurtList',
    TeamStatisticType.DEAD: 'deadList',
}

TEAM_STATISTIC_TYPE_TO_KEY = {
    TeamStatisticType.DAMAGE: 'dmg',
    TeamStatisticType.HEAL: 'heal',
    TeamStatisticType.HURT: 'hurt',
    TeamStatisticType.DEAD: 'dead',
}

class StatisticEnum(object):
    STA_TYPE_DAMAGE = 1
    STA_TYPE_HEAL = 2
    STA_TYPE_HURT = 3
    STA_TYPE_DEAD = 4
    STA_TYPE_DAMAGE_WITH_PET = 5
    STA_TYPE_HURT_WITH_PET = 6
    STA_TYPE_HEAL_WITH_PET = 7
    STA_TYPE_DAMAGE_PER_SECOND = 8
    STA_TYPE_DAMAGE_WITH_PET_PER_SECOND = 9
    STA_TYPE_HURT_PER_SECOND = 10
    STA_TYPE_HURT_WITH_PET_PER_SECOND = 11
    STA_TYPE_HEAL_PER_SECOND = 12
    STA_TYPE_HEAL_WITH_PET_PER_SECOND = 13
    STA_TYPE_WITH_PET = 14

    DUNGEON_VALID_TYPES = (STA_TYPE_DAMAGE, STA_TYPE_HEAL, STA_TYPE_HURT, STA_TYPE_DEAD)

class TeamApplyResult(object):
    # 成功
    TEAM_APPLY_OK = 0
    # 申请失败
    TEAM_APPLY_FAIL = 1
    # 等级不足
    TEAM_APPLY_LEVEL_IS_NOT_ENOUGH = 10001
    # 战力不足
    TEAM_APPLY_SCORE_IS_NOT_ENOUGH = 10002
    # 需要密码
    TEAM_APPLY_NEED_PASSWORD = 10003
    # 密码不对
    TEAM_APPLY_WRONG_PASSWORD = 10004
    # 在副本中
    TEAM_APPLY_IS_IN_DUNGEON = 10005
    # 队伍不存在
    TEAM_IS_NOT_EXIST = 10006
    # 团队不存在
    RAID_IS_NOT_EXIST = 10007
    # 团队满了
    RAID_IS_FULL = 10008
    # 团队申请列表满了
    RAID_APPLY_LIST_IS_FULL = 10009
    # 已经在团队中了
    RAID_APPLY_IS_IN_RAID = 10010
    # 已经在队伍中了
    RAID_APPLY_IS_IN_TEAM = 10011
    # 团队已申请
    RAID_APPLY_IS_APPLIED = 10013
    # 团队UI不可见
    RAID_APPLY_RAID_UI_IS_NOT_VISIBLE = 10014
    # 队伍UI不可见
    TEAM_APPLY_RAID_UI_IS_NOT_VISIBLE = 10015


MINE_HUB_BROKEN_HP = 1

class MINE_WAR_STATE(object):
    PREPARE = MineGlobalData.MineGlobalData.MINE_STATE_PREPARE
    RUNNING = MineGlobalData.MineGlobalData.MINE_STATE_START
    END = MineGlobalData.MineGlobalData.MINE_STATE_END

class MineWarMonsterCustomId(object):
    MINE_CORE = 'mineCore'      #矿战核心
    MINE_FLAG = 'mineFlag'      #矿战旗帜
    MINE_BROKEN_FLAG = 'mineBrokenFlag' #矿战被毁旗帜
    MINE_HUB = 'mineHub'       #矿战枢纽

class MineWarMonsterType(object):
    MINE_NONE = 0
    MINE_CORE = 1      #矿战核心
    MINE_FLAG = 2      #矿战旗帜
    MINE_BROKEN_FLAG = 3 #矿战被毁旗帜
    MINE_HUB = 4       #矿战枢纽

class MINE_WAR_CAMP(object):
    CAMP_DEFEND = 1
    CAMP_ATTACK = 2

mineWarMonsterEnumDict = {
    MineWarMonsterCustomId.MINE_CORE: MineWarMonsterType.MINE_CORE,
    MineWarMonsterCustomId.MINE_FLAG: MineWarMonsterType.MINE_FLAG,
    MineWarMonsterCustomId.MINE_BROKEN_FLAG: MineWarMonsterType.MINE_BROKEN_FLAG,
    MineWarMonsterCustomId.MINE_HUB: MineWarMonsterType.MINE_HUB,
}

class GiftKeyType(object):
    NORMAL = 1              #不限次数兑换
    ONLY_ONE = 2            #全服只能一次

class GiftCodeRedisKey(object):
    KEY = RedisKey.GIFT_CODE_TBL + ":key"
    GROUP = RedisKey.GIFT_CODE_TBL + ":group"
    USED = RedisKey.GIFT_CODE_TBL + ":used"

class DungeonSpaceValType(object):
    NONE = 0
    SINGLE = 1
    TEAM = 2
    RAID = 3
    GUILD_BOSS = 4

class GuildChallengeDungeonOpenType(metaclass=UniqueIntEnum):
    # 直接开启
    DIRECT = 1
    # 预约开启
    APPOINT = 2

    VALID_TYPE=(DIRECT, APPOINT)

class GuildChallengeDungeonOpenFundType(metaclass=UniqueIntEnum):
    # 公会资金
    FUND = 1
    # 公会金币
    MONEY = 2

class GuildChallengeOpenDungeonResult(metaclass=UniqueIntEnum):
    # 成功
    OK = 0
    # 失败
    FAIL = 1
    # 不在正常开启的时间
    NOT_VALID_TIME = 2
    # 战力不足
    NO_ENOUGH_SCORE = 3
    # 不在帮会
    NO_IN_GUILD= 4
    # 权限不足
    NO_ENOUGH_PERMISSION= 5
    # 副本未解锁
    OPEN_DUNGEON_LOCKED= 6
    # 重复开启
    OPEN_DUNGEON_REPEAT = 7
    # 本周开启副本已达上限
    OPEN_DUNGEON_IS_LIMIT = 8
    # 帮会资金不足
    NO_ENOUGH_FUND = 9
    # 帮会金币不足
    NO_ENOUGH_MONEY = 10
    # 在帮会副本中
    IN_GUILD_DUNGEON = 11
    # 没有预约
    NO_GUILD_DUNGEON_ORDER = 12

class SpecialMonsterAIAPType(object):
    NONE = 0
    BUFF_ID = 1

class GuildBossChallengeStatus(object):
    # 初始化
    INIT = 0
    # 预约中
    APPOINT = 1
    # 预约倒计时
    APPOINT_CD = 2
    # 创建中
    CREATING = 3
    # 已创建
    CREATED = 4
    # 开始战斗CD
    START_BATTLE_CD = 5
    # 开始战斗
    START_BATTLE= 6
    # 结算中
    SETTLEMENT = 7

    VALID_STATUS = (INIT, APPOINT, APPOINT_CD, CREATING, CREATED, START_BATTLE_CD, START_BATTLE, SETTLEMENT)

class WorldBossRefreshType(object):
    NONE = 0
    DEAD_TIMER = 1
    TIMED_INTERVALS_TIMER = 2

class TimeLimitedStageType(object):
    START = 1
    END = 2

class TimerEntityRefreshType(object):
    NONE = 0
    TIMED_INTERVALS = 1
    TIME_LIMITED = 2

    SIZE = 3    # 类型数量

#特权用户
class PrivilegeRedisKey(object):
    VIP = RedisKey.PRIVILEGE_TBL + ":v:"         #特权用户    (排队优先)
    SVIP = RedisKey.PRIVILEGE_TBL + ":sv:"       #超级特权    (排队直达)

INVINCIBLE_BUFF_ID = 64000070  # 无敌buffId

class DungeonAddRewardNumCountType(metaclass=UniqueIntEnum):
    # 默认次数
    DEFAULT_COUNT = 1
    # 道具次数
    ITEM_COUNT= 2
    # 金币次数
    COIN_COUNT= 3
    # 有效的类型
    VALID_TYPE = (DEFAULT_COUNT, ITEM_COUNT, COIN_COUNT)

class AntiAddictionDateType(object):
    WEEKEND = 0
    HOLIDAY = 1
    WORKDAY = 2

class AntiAddictionTimeType(object):
    PERMIT = 0
    PROHIBIT = 1

GiftCodeResultMsg = {
    40001: 54000343,
    40002: 54000346,
    40003: 54000352,
    40004: 54000353,
    40005: 54000354,
}

class ShieldType(metaclass=UniqueIntEnum):
    # 生命盾
    LIFE = 1
    # 减伤盾
    REDUCE_DMG = 2

class DevicePlatId(object):
    IOS = 0             # iOS
    ANDROID = 1         # Android
    RESERVE = 2         # reserved
    PC_CLIENT = 3       # PC client
    MICRO_WEB = 4       # Micro web
    MICRO_CLIENT = 5    # Micro client
    SWITCH = 6          # Switch client
    PS_CLIENT = 7       # PS client
    XBOX_CLIENT = 8     # XBOX client
    UNKNOWN = 9         # unkonwn
    OSX = 10            # OSX

class CollectibleDetailStatus(object):
    COLLECTING = 1
    COLLECTED = 2

class DrawCardGuaranteedType(object):
    NONE = 0
    GUARANTEED_RESET = 1
    PITY_RESET = 2
    GET_RESET = 3
    TIME_LIMIT_RESET = 4

class CapacityExpansionType(metaclass=UniqueIntEnum):
    # 背包金币
    BAG_GOLD = 1
    # 背包道具
    BAG_ITEM = 2
    # 仓库金币
    WAREHOUSE_GOLD = 3
    # 仓库道具
    WAREHOUSE_ITEM = 4

class ItemDisassemblyType(metaclass=UniqueIntEnum):
    # 道具
    ITEM = 1
    # 装备
    EQUIP = 2

class TeamJoinType(metaclass=UniqueIntEnum):
    # 默认
    DEFAULT = 0
    # 创建
    CREATE = 1
    # 申请
    APPLY = 2
    # 匹配
    MATCH = 3
    # 招募
    RECRUIT = 4

class ApplySource(metaclass=UniqueIntEnum):
    # 招募
    RECRUIT = 1
    # 队伍申请
    APPLY = 2

    VALID_APPLY_SOURCE = (RECRUIT, APPLY)

class DunegonCompleteReasonType(metaclass=UniqueIntEnum):
    # 默认
    DEFAULT = 0
    # 超时
    TIMEOUT = 1
    # 离开
    LEAVE = 2
    # 完成
    FINISHED = 3
    
SKILL_TIMER_LOG_QUEUE_MAX_CNT = 20


TIMER_CANCEL_RET_SUCCESS = 0
TIMER_CANCEL_RET_ZERO_TIMER = 1
TIMER_CANCEL_RET_NOT_DATA = 2
TIMER_CANCEL_RET_DESTROY = 3
TIMER_CANCEL_RET_MISMATCH = 4
TIMER_CANCEL_ARG_INVALID = 5


SKILL_LOG_OPR_SET_TIMER = 1
SKILL_LOG_OPR_REMOVE_TIMER = 2
SKILL_LOG_OPR_ON_TIMER = 3

class UserEventTag(object):
    EVENT_ON_TEST = 'onTest'
    EVENT_ON_GUILD_UNION_CHANGE = 'onGuildUnionChange'

class ItemMovementType(object):
    BagToWarehouse = 1
    WarehouseToBag = 2

class PetMakeTeamType(object):
    # 出战
    JOIN = 1
    # 离开
    LEAVE = 2

class PetFollowType(object):
    # 取消
    CANCEL = 1
    # 跟随
    FOLLOW = 2

class AuctionCollectDataType(object):
    # 推荐大类关注
    RECOMMEND_CATEGORY = 1
    # 公示大类关注
    PUBLICITY_CATEGORY = 2
    # 公示物品关注
    PUBLICITY_ITEM = 3


class AuctionCollectOpType(object):
    # 加入
    ADD = 1
    # 物品
    REMOVE = 2

class ForbiddenTaskIdOpType(object):
    # 查询
    QUERY = 1
    # 加入
    ADD = 2
    # 移除
    REMOVE = 3

GAME_SERVER_ERR_BAN_FOREVER         = 2001 # 账户被永久封禁
GAME_SERVER_ERR_BAN_WITH_TIME       = 2002 # 账户被临时封禁
GAME_SERVER_ERR_ANTI_ADDICT         = 2003 # 账户被防沉迷
GAME_SERVER_ERR_VERIFY_FAIL         = 2004 # 中心服校验失败
GAME_SERVER_ERR_VERIFY_TIMEOUT      = 2005 # 中心服校验超时
GAME_SERVER_ERR_MEET_REG_MAX        = 2006 # 达到注册上限
GAME_SERVER_ERR_SERVER_OPEN_TIME    = 2007 # 服务器没到开服时间
GAME_SERVER_ERR_PERMIT              = 2008 # 白名单未关
GAME_SERVER_ERR_NO_LOGIN_MGR        = 2009 # 登录管理器不存在
GAME_SERVER_ERR_REG_SWITCH          = 2010 # 注册开关关闭
GAME_SERVER_ERR_REJECT_LOGIN        = 2011 # 拒绝登录
GAME_SERVER_ERR_NO_LOGIN_MGR2       = 2012 # 登录管理器不存在
GAME_SERVER_ERR_APP_VERSION         = 2013 # 登录时整包强更
GAME_SERVER_ERR_PATCH_VERSION       = 2014 # 登录时PATCH强更

class EquipMultiEnhanceResult(object):
    # 成功
    OK = 1
    # 失败
    FAIL = 2
    # 参数错误
    ARG_ERR = 3
    # 穿戴的装备锁住了
    BODY_EQUIP_LOCKED = 4
    # 背包的装备锁住了
    BAG_EQUIP_LOCKED = 5
    # 物品不足
    ITEM_NOT_ENOUGH = 6

class EquipUpgradeType(object):
    # 单级升阶
    SINGLE = 1
    # 多级升阶
    MULTIPLE = 2

    VALID_UPGRADE_TYPE = (SINGLE, MULTIPLE)


SERVER_LOG_TYPE_LOGIN = 1
SERVER_LOG_TYPE_DAILY = 2

class UserTagType(object):
    WHITE_LIST = 0
    NORMAL = 1
    ACTIVATION_CODE = 2
    GREEN_CODE = 3
    
class MailLoadType(object):
    DEFAULT = 0
    GLOBAL_MAIL = 1
    PLAYER_MAIL = 2
    GLOBAL_AND_PLAYER_MAIL = 3

class BountyType(object):
    PUBLIC = 0
    ASSIGN = 1

    VALID_BOUNTY_TYPE = (PUBLIC, ASSIGN)

class PublishBountyResType(object):
    SUCCESS = 0
    PUBLISH_CNT_LIMIT = 1
    ALERADY_PREY = 2
    ALERADY_HUNTER = 3
    PUBLISHER_NOT_ENOUGH_MONEY = 4
    HUNTER_NOT_ONLINE = 5
    PUBLISHER_CHECK_TIME_OUT = 6
    HUNTER_CHECK_TIME_OUT = 7
    HUNTER_REFUSE = 8

class AcceptBountyResType(object):
    SUCCESS = 0
    ALERADY_HUNTER = 1
    NOT_EXIST = 2
    NOT_PUBLIC_TYPE = 3
    NOT_PUBLISHED_STATE = 4
    HUNTER_NOT_ENOUGH_MONEY = 5
    NOT_ASSIGN_HUNTER = 6
    NOT_PRE_PUBLISH_STATE = 7
    PUBLISHER_CHECK_TIME_OUT = 8
    HUNTER_CHECK_TIME_OUT = 9
    HUNTER_REFUSE = 10
    PUBLISHER_NOT_ENOUGH_MONEY = 11
    PUBLISHER_IS_SELF = 12
    PREY_IS_SELF = 13
    NOT_ENOUGH_ACCEPT_LEFT_TIME = 14

PUBLISH_BOUNTY_RES_2_ACCEPT_BOUNTY_RES = {
    PublishBountyResType.PUBLISHER_CHECK_TIME_OUT: AcceptBountyResType.PUBLISHER_CHECK_TIME_OUT,
    PublishBountyResType.PUBLISHER_NOT_ENOUGH_MONEY: AcceptBountyResType.PUBLISHER_NOT_ENOUGH_MONEY,
}

ACCEPT_BOUNTY_RES_RES_2_PUBLISH_BOUNTY_RES = {
    AcceptBountyResType.HUNTER_CHECK_TIME_OUT: PublishBountyResType.HUNTER_CHECK_TIME_OUT,
    AcceptBountyResType.HUNTER_REFUSE: PublishBountyResType.HUNTER_REFUSE,
}

class BountyFlag(object):
    NULL = 0
    PREY = 1
    PREY_HUNTER = 2

class BountyState(object):
    NULL = 0
    PRE_PUBLISH = 1
    PUBLISHED = 2
    PRE_ACCEPT = 3
    ACCEPTED = 4
    PRE_COMPLATE = 5
    COMPLATED = 6

    PUBLISHED_SET = (PUBLISHED, PRE_ACCEPT, ACCEPTED)
    INVALID_CELL_SET_PREY_TYPE = (NULL, COMPLATED)
    INVALID_CELL_SET_HUNTER_TYPE = (NULL, COMPLATED, PUBLISHED)
    VALID_CELL_CLEAR_SET_HUNTER_TYPE = (NULL, ACCEPTED, COMPLATED, PUBLISHED)
    PUBLIC_BOUNTY_NEED_CHECK_EXPIRED_TYPE = (PUBLISHED, ACCEPTED)

class UpdatePreyBuffFlag(object):
    NONE = 0
    ADD = 1
    REMOVE = 2

class UpdateHunterBuffFlag(object):
    NONE = 0
    ADD = 1
    REMOVE = 2

class AvatarBountyInfoType(object):
    PUBLISH = 0
    PREY = 1
    HUNTER = 2

    VALID_AVATAR_BOUNTY_TYPE = (PUBLISH, PREY, HUNTER)

class DeathPenaltyType(object):
    SAFE = 1
    DUNGEON = 2
    NORMAL = 3
    SPECIAL = 4
    DANGEROUS = 5
    INTENSE_BATTLE = 6
    VALID_HUNTER_KILL_PREY_TYPE = (NORMAL, SPECIAL, DANGEROUS)

class BountyAvatarType(object):
    PUBLISHER = 0
    PREY = 1
    HUNTER = 2

class BountyExpiredType(object):
    PUBLIC_PUBLISHED_DOWN = 0
    PUBLIC_ACCEPTED_TO_PUBLISHED = 1
    ASSIGN_ACCEPTED_DOWN = 2

class BountyRankType(object):
    PUBLISHER = 0
    PREY = 1
    HUNTER = 2
    MAX = HUNTER + 1
    ALL_VALID_RANK_TYPE=(HUNTER,)

class BountyRankSubType(object):
    TOTAL = 0
    WEEK = 1
    MAX = WEEK + 1
    ALL_VALID_RANK_TYPE=(TOTAL, WEEK,)

class AvatarBountyInfoUpdateType(object):
    LOGIN = 0
    CLIENT = 1
    ACCEPTED_UPDATE = 2
    COMPLATED_DELETE = 3
    EXPIRED_DELETE = 4
    ACCEPT_EXPIRE_UPDATE = 5
    ACCEPT_EXPIRE_DELETE = 6
    PUBLISHED = 7
    ACCEPTED = 8

class UpdateBountyAvatarKey(object):
    ONLINE = "online"
    NAME = "name"

    PERSISTENT_KEYS = (NAME,)

class UpdateBountyInfoProp(object):
    PUBLISHER_NAME = "name"
    PREY_ONLINE = "preyOnline"
    PREY_NAME = "preyName"
    HUNTER_NAME = "hunterName"

BOUNTY_AVATAR_KEY_2_BOUNTY_PUBLISHER_PROP = {
    UpdateBountyAvatarKey.NAME : UpdateBountyInfoProp.PUBLISHER_NAME,
}

BOUNTY_AVATAR_KEY_2_BOUNTY_PREY_PROP = {
    UpdateBountyAvatarKey.ONLINE : UpdateBountyInfoProp.PREY_ONLINE,
    UpdateBountyAvatarKey.NAME : UpdateBountyInfoProp.PREY_NAME,
}

BOUNTY_AVATAR_KEY_2_BOUNTY_HUNTER_PROP = {
    UpdateBountyAvatarKey.NAME : UpdateBountyInfoProp.HUNTER_NAME,
}
BOUNTY_AVATAR_TYPE_2_CONVERSION_DICT = {
    BountyAvatarType.PUBLISHER : BOUNTY_AVATAR_KEY_2_BOUNTY_PUBLISHER_PROP,
    BountyAvatarType.PREY : BOUNTY_AVATAR_KEY_2_BOUNTY_PREY_PROP,
    BountyAvatarType.HUNTER : BOUNTY_AVATAR_KEY_2_BOUNTY_HUNTER_PROP,
}
########################################
class UpdateHunterRankProp(object):
    HUNTER_ONLINE = "online"
    HUNTER_NAME = "hunterName"

BOUNTY_AVATAR_KEY_2_HUNTER_RANK_PROP = {
    UpdateBountyAvatarKey.ONLINE : UpdateHunterRankProp.HUNTER_ONLINE,
    UpdateBountyAvatarKey.NAME : UpdateHunterRankProp.HUNTER_NAME,
}

BOUNTY_RANK_TYPE_2_CONVERSION_DICT = {
    BountyRankType.PUBLISHER : {},
    BountyRankType.PREY : {},
    BountyRankType.HUNTER : BOUNTY_AVATAR_KEY_2_HUNTER_RANK_PROP,
}

BOUNTY_PAGE_SIZE = 20

class EmoteTimeType(object):
    ONE_SHOT = 0
    LOOP = 1

class StopPlayEmoteReason(object):
    Client = 0
    Teleport = 1
    BeDamaged = 2
    CrossServer = 3
    TimeOut = 4
    LOGIN = 5

class FlyTimerArgs(object):
    Delay = 2.5
    Interval = 2.5

class RemodelingArgs(object):
    INCLUDE = 0
    EXCLUDE = 1

class RemodelingPetResult(object):
    SUCCESS = 0
    FAIL = 1
    WRONG_ARGS = 2
    ITEM_NOT_ENOUGH = 3
    BAG_IS_FULL = 4

class AnnouncementType(object):
    WORLD_BOSS1= 1
    MINE_WAR = 2
    SIEGE_WAR = 3
    WORLD_BOSS2= 4

class UpdateAnnouncementType(object):
    NULL = 0
    MINE_WAR_UPCOMING = 1
    MINE_WAR_ONGOING = 2
    WORLD_BOSS1_UPCOMING = 3
    WORLD_BOSS1_ONGOING = 4
    WORLD_BOSS2_UPCOMING = 5
    WORLD_BOSS2_ONGOING = 6
    SIEGE_WAR_BIDDING = 7
    SIEGE_WAR_UPCOMING = 8
    SIEGE_WAR_ONGOING = 9

ANNOUNCEMENT_TYPE_2_UPDATE_ANNOUNCEMENT_TYPE = {
    AnnouncementType.WORLD_BOSS1: [UpdateAnnouncementType.WORLD_BOSS1_UPCOMING, UpdateAnnouncementType.WORLD_BOSS1_ONGOING],
    AnnouncementType.MINE_WAR: [UpdateAnnouncementType.MINE_WAR_UPCOMING, UpdateAnnouncementType.MINE_WAR_ONGOING],
    AnnouncementType.SIEGE_WAR: [UpdateAnnouncementType.SIEGE_WAR_BIDDING, UpdateAnnouncementType.SIEGE_WAR_UPCOMING, UpdateAnnouncementType.SIEGE_WAR_ONGOING],
    AnnouncementType.WORLD_BOSS2: [UpdateAnnouncementType.WORLD_BOSS2_UPCOMING, UpdateAnnouncementType.WORLD_BOSS2_ONGOING],
}

SIEGE_WAR_STATE_2_UPDATE_ANNOUNCEMENT_TYPE = {
    SiegeWarState.SIGN_UP: UpdateAnnouncementType.SIEGE_WAR_BIDDING,
    SiegeWarState.WAR_COUNT_DOWN: UpdateAnnouncementType.SIEGE_WAR_UPCOMING,
    SiegeWarState.WAR: UpdateAnnouncementType.SIEGE_WAR_ONGOING,
}

class FullPlayerInfoUnlockType:
    Ach = 1
    Collect = 1 << 2
    Pet = 1 << 3
    Mount = 1 << 4
    Meridian = 1 << 5
    Rank = 1 << 6
    Guild = 1 << 7

class ResourceRecoveryType(object):
    NULL = 0
    FREE_TICKET = 1

class FreeTicketSubType(object):
    WONDER_LAND = 0
    CUBE = 1

    VALID_SUB_TYPE = (WONDER_LAND, CUBE,)
    MAX_CNT = CUBE + 1

class FreeTicketUpdateType(object):
    LOGIN = 0
    OFFLINE = 1
    RESET = 2
    UPDATE = 3

class CycleEventTriggerType(object):
    NULL = 0
    LOGIN = 1
    TIMED = 2

RESOURCE_RECOVER_TIME_POINT_STR = '050000'
