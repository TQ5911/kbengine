# -*- coding: utf-8 -*-
import sys, os
import KBEngine
import functools
import random
import time
import re

import itemData_set as IDSD
import const_const as CSTD
import gearBase_gearConst as GBGCD
import gamePlay_gamePlay as GGD
import character_charData as CCDD
import wonderLand_floor as WL_FD

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

# baseapp上的数据key定义
BASEAPP_DATA_KEY_SPACE_MARKER = 'kSpaceMarker'
BASEAPP_DATA_KEY_SPACE_TO_BASE = 'kSpaceToBase'

GLOBAL_BASE_STUB_ARCHIVE = [
    'GlobalMailStub',
    'SiegeWarStub',
    'CrossSiegeWarStub',
    'WorldBossStub',
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
    'CubeStub',
    ]
GLOBAL_BASE_STUB_TEAMSTUB = 'TeamStub'

GLOBAL_BASE_STUB_RAIDSTUB = 'RaidStub'

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

GLOBAL_SERVER_SHIFT = 22
GLOBAL_TIME_SHIFT = 26
GBID_TIME_BASE = 1517907600
GBID_TIME_INTERVAL = 5 * 60
GBID_TIME_UPDATE_INTERVAL = GBID_TIME_INTERVAL + 10
GBID_BASE = 2 ** (GLOBAL_SERVER_SHIFT + GLOBAL_TIME_SHIFT)

AVATAR_OFFLINE_REASON_CLIENT_DEATH = 1
AVATAR_OFFLINE_REASON_DESTORY = 2
AVATAR_OFFLINE_REASON_MANNUALLY = 3
AVATAR_OFFLINE_REASON_GMKICK = 4
AVATAR_OFFLINE_CREATE_CELL_ERROR = 5
AVATAR_OFFLINE_NO_CLIENT_NEW_CHAR = 6
AVATAR_OFFLINE_REASON_SELECT_CHARACTER = 7
AVATAR_OFFLINE_REASON_LOSE_CELL = 8
AVATAR_OFFLINE_REASON_SPACE_GONE = 9
AVATAR_OFFLINE_REASON_INIT_ERR = 11
AVATAR_OFFLINE_REASON_CELLAPP_DEATH = 12
AVATAR_OFFLINE_REASON_KICK_BY_CENTRAL_SERVER = 14
AVATAR_OFFLINE_REASON_END_CROSS_SERVER = 15
AVATAR_OFFLINE_REASON_IDIP_DELETE_ACCOUNT = 17
AVATAR_OFFLINE_REASON_IDIP_PLAT_AUTHOR_CHANGE = 18
AVATAR_OFFLINE_REASON_SWITCH_SERVER = 19
AVATAR_OFFLINE_REASON_NEWBIE_KICKOUT = 20

CENTRAL_SERVER_HEARTBEAT_INTERVAL = 10

ENTITY_POS_POLICY_MAX_NUM = 1000


class UniqueIntEnum(type):
    def __new__(cls, name, bases, dct):
        __blocklist__ = dct.get('__blocklist__', ())
        __whitelist__ = dct.get('__whitelist__', ())
        _unimap = dict()
        for k, v in dct.items():
            if k.startswith('__'):
                continue
            if not isinstance(v, int):
                continue
            if __whitelist__ and k not in __whitelist__:
                continue
            if __blocklist__ and k in __blocklist__:
                continue
            if v in _unimap:
                _errstr = f"class {name} setattr err, {k}/{_unimap[v]}={v}"
                raise AttributeError(_errstr)
            _unimap[v] = k
        return type.__new__(cls, name, bases, dct)

HATE_TRAP = 1
AUREOLE_TRAP = 2
CAPTURE_TRAP = 3
LEAVE_AOI_TRAP = 4
NPC_GUIDE_START = 5
HOME_CONSTRUCT = 6
BELONG_RAID_TRAP = 7
DUN_TEL_TRAP = 8
LARGE_ENT_WITNESS = 9
LARGE_ENT_HYST = 10
NPC_GUIDE_STOP = 11
ROUTE_ESCORT_TRAP = 12
WHALE_FOLLOW_TRAP = 13


class State(metaclass=UniqueIntEnum):
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
    TeamFollowing = 32
    riding = 33
    Teleport = 34
    autoFight = 37
    serverControl = 43

    _stateValMap = {}

    _moveConflictState = []

    breakSkillStates = (Down, Stunned, Frozen)

    @staticmethod
    def _allStates():
        attrs = dir(State)
        realAttrs = {}
        for attrName in attrs:
            if not attrName.startswith('_'):
                realAttrs[attrName] = getattr(State, attrName)
        return realAttrs

    @staticmethod
    def getStateByVal(stateVal):
        return State._stateValMap[stateVal]

    @staticmethod
    def buildStateValMap():
        for state in range(32):
            State._stateValMap[1 << state] = state

    @staticmethod
    def getMoveConflictState():
        import conflict_conflict as CCD
        moveEvent = CCD.datas[29100004]
        for state, val in moveEvent.items():
            if val == 3 and int(state) not in (State.UsingSkill, State.speicalSkill):
                State._moveConflictState.append(int(state))

    @staticmethod
    @functools.lru_cache(128)
    def isMoveConflictState(state):
        return state in State._moveConflictState


class RemoveStateReason(metaclass=UniqueIntEnum):
    NORMAL = 0  # 逻辑手动调用的
    OFFLINE = 1
    CONFLICT = 2
    TELEPORT = 3
    EXIT_DUEL = 4


class LineSubType(metaclass=UniqueIntEnum):
    world = 1
    pressLine = 2


SPACE_NO_INTERVAL = 10000
COPIED_SPACE_NO_START = 1 * SPACE_NO_INTERVAL


class SpaceSubType(metaclass=UniqueIntEnum):
    World = 1
    Yanwu = 2 # 演武场
    Boss = 3 # 大世界boss场景


class SpaceType(metaclass=UniqueIntEnum):
    UnKownSpaceType = 0
    SpaceWorldDungeon = 1
    SpaceNormalDungeon = 2
    SpaceCube = 3
    SpaceLine = 6
    SpaceWonderLand = 7
    SpaceSiegeWar = 8

    @staticmethod
    def getCopiedSpaceNoRange(mapId):
        start = mapId * SPACE_NO_INTERVAL
        return (start, start + SPACE_NO_INTERVAL)

    @staticmethod
    def getSingleDungeonSpaceNoRange(mapId):
        start = mapId * SPACE_NO_HOME_INTERVAL
        return (start, start + SPACE_NO_HOME_SINGLE_DUNGEON)

    @staticmethod
    def getTeamDungeonSpaceNoRange(mapId):
        start = mapId * SPACE_NO_HOME_INTERVAL + SPACE_NO_HOME_SINGLE_DUNGEON
        return (start, start + SPACE_NO_HOME_TEAM_DUNNGEON)

    @staticmethod
    def getDungeonSpaceNoRange():
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
    DEFAULT = COMMON = 0
    AIRWALL = 1


class ItemType(object):
    Normal = 0
    LingShou = 1
    Resource = 2


class ItemSubType(object):
    Normal = 0
    LingShouEgg = 0
    HEAL_HP = 1
    HEAL_MP = 2
    Equipment = 4
    ExtractReward = 52
    SpiritBoard = 15


class AvatarProps(metaclass=UniqueIntEnum):
    commonCastCtx = 4
    callbackTmpInfo = 5
    channelSkillTimer = 6
    currentUseSkill = 7
    pendingCheckUseItem = 8

    lastTeleportSpaceNoRecord = 10
    backAccount = 11
    immuneDeath = 12
    timebackSkillData = 13

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
    followNotRideFlag = 97
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
    cubeDurStatus = 247 # 立方房间持续状态
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
    wonderLandDurStatus = 261
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
    unlockBountyTaskFlag = 315
    petEquipNumCache = 316
    isLightningArea = 317

    popRewardItemsDict = 330
    reqSubmitTaskList = 331
    spawnSummonByAI = 332
    spawnSummonList = 333
    fromCubeMapId = 334


class TopSpeedType(object):
    NormalTopSpeed = 100.0
    ShiftingSkillTopSpeed = 1000.0
    TeleportSkillTopSpeed = 10000.0
    FlyingTopSpeed = 1000.0


CELL = 0
BASE = 1
ALL = 2
CLIENT = 3

DEFAULT_AOI = 30.0
DEFAULT_HYST = 5.0
HOME_AOI = 30.0
LARGE_ENT_WITNESS = 9
LARGE_ENT_HYST = 10

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
    # 引灵盘
    SPIRIT_BOARD = 30000016
    # 真气
    GENIUS_QI = 30000100

class ItemBindType(object):
    BIND = 0
    NORMAL = 1
    BINDTYPE_NOT_SPECIFIED = 2
    VALID_BIND_TYPE = (BIND, NORMAL, BINDTYPE_NOT_SPECIFIED)


class GmMode(object):
    ALL_MODES = []

    _modeGen = (i for i in range(20))

    @staticmethod
    def generateMode(modes, gen):
        m = next(gen)
        modes.append(m)
        return m

    GM_NONE = generateMode.__func__(ALL_MODES, _modeGen)
    GM_NORAML = generateMode.__func__(ALL_MODES, _modeGen)
    GM_NO_SKILLCD = generateMode.__func__(ALL_MODES, _modeGen)


class EnterLineCode(object):
    CAN_ENTER = 0
    FAIL_REACH_MAX_MEMBER = 1
    FAIL_ONLY_TEAM_MEMBER = 2
    FAIL_EXLUDE = 3
    FAIL_COMMON = 4
    FAIL_NOT_GUILD_MEMBER = 5
    FAIL_REACH_MAX_GUILD_MEMBER = 6
    FAIL_SPACE_IS_NOT_READY = 7
    FAIL_CANNOT_AUTO_ENTER = 9
    FAIL_REACH_AREAM_MAX = 10
    FAIL_REACH_AREAM_LIMIT = 11
    FAIL_REACH_SEC_LIMIT = 12


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
    BAG_OP_STAT_OK = 0
    BAG_OP_DATA_ERR = 1
    BAG_OP_STAT_ERR = 2
    BAG_OP_NO_SPACE = 3
    BAG_OP_BAG_TYPE_ERR = 4
    BAG_OP_ITEMS_NOT_ENOUGH = 5
    BAG_OP_ITEM_EXPIRED = 6
    BAG_OP_LEVEL_ERR = 7
    BAG_OP_CD_ERR = 8
    BAG_OP_ADD_NUM_ERR = 9
    BAG_OP_CANT_BE_DROP = 10
    BAG_OP_BAG_LOCKED = 11
    BAG_OP_DAILY_LIMIT = 14
    BAG_OP_PENDING = 15
    BAG_OP_MAIL_ITEM_REACH_LIMIT = 18
    BAG_OP_REUSE_ITEM_USE_TIMES_FAILED = 19
    BAG_OP_ITEM_DISABLED = 20
    BAG_OP_ITEM_LOCKED = 21

class BagOpPlan(object):
    BAG_OP_NO_PLAN = 1
    BAG_OP_OK = 2


GAME_REFRESH_OCLOCK = 5

ONE_MINUTE_SECONDS = 60
ONE_DAY_SECONDS = 86400
ONE_HOUR_SECONDES = 3600
HALF_HOUR_SECONDS = 1800
ONE_WEEK_SECONDS = 7 * ONE_DAY_SECONDS
WEEK_SENCONDS = ONE_DAY_SECONDS * 7
FIFTEEN_MINUTES = 900
COMMON_CYCLE_TIME = GAME_REFRESH_OCLOCK * 3600
CORRECT_TIME = time.localtime(0).tm_hour
CORRECT_TIME_SECONDS = CORRECT_TIME * 3600


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


class NavCost(object):
    costBlock = 0
    costPass = 1
    costBorder = 2
    costWater = 3
    costEnd = 4

    COST_COLL_AVATAR = (costPass,)
    COST_COLL_ENTITY = (costPass, costBorder)


class WitnessType(object):
    WITNESS_TYPE_HIDE = 0
    WITNESS_TYPE_ALL = 1
    WITNESS_TYPE_NAME = 2
    WITNESS_TYPE_IGNORE = 3


class CreateAvatarRes(object):
    OK = 0
    NAME_DUPLIATED = 1
    NAME_INVALID = 2
    ADDICT_JUDGE_FAILED = 3
    NAME_LENGTH_OVERLIMIT = 4
    DATABASE_OPR_ERROR = 5
    GEN_GBID_FAILED = 6
    CREATE_ENTITY_ERR = 7
    WRITE_ENTITY_ERR = 8
    GBID_ERR = 9
    NEED_DID = 10


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


WeekDayDic = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}


class ClaimTaskSrc(object):
    UNKNOWN = 0
    NORMAL = 1
    GM_FINISH_NEWBIE = 2
    GM = 3
    JUMP_GAME = 4
    MONSTER_NEARBY = 5
    ROUND_AUTO_CLAIM = 6
    ENTRUST_ACTIVITY = 7
    REWARD_TASK = 8
    INIT_NEWBIE_TASK = 9
    FROM_ACTION = 10
    NPC_DIALOG = 11


class EntNumPerPlayerInAOI(object):
    worldLine = 15
    singleDungeon = 5
    teamDungeon = 3


class TeleportLock(metaclass=UniqueIntEnum):
    FREE_TO_TELEPORT = 0
    ENTER_LINE = 7
    SWITCH_LINE = 8
    ENTER_DUNGEON = 9
    ENTER_GUILD = 10
    ENTER_HOME = 11
    ENTER_PLANE = 3

    ENTER_SINGLE_DUNGEON = 12

    UNKNOWN = 255


POSITION_ZERO = (0.0, 0.0, 0.0)
DIRECTION_ZERO = (0.0, 0.0, 0.0)

WORLD_LINE_BASE_WEIGHT = 50
WORLD_LINE_UPDATE_WEIGHT_VAL = 10


class TaskOpStat(object):
    TASK_OP_OK = 0
    TASK_OP_CLAIM_ERR = 1
    TASK_OP_TEAM_PLAYER_ALREADY_HAS = 2


class TaskCycleType(object):
    TASK_CYCLE_NONE = -1
    TASK_CYCLE_DAYLY = 0
    TASK_CYCLE_WEEKLY = 1
    TASK_CYCLE_ONCE = 2


class TaskStat(object):
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

class TaskNotSuccReason(object):
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


class VarChangeSrc(object):
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


class ForceType(object):
    UnKownForceType = 0
    Player = 1
    Monster = 2
    Friend = 3
    Guild = 4
    Neutrality = 5
    NPC = 6

    forceTypes = ("UnKownForceType", "Player", "Monster", "Friend", "Guild", "Neutrality", "NPC")

    @staticmethod
    @functools.lru_cache(8, typed=False)
    def getForceType(typeId):
        if ForceType.Player <= typeId <= ForceType.NPC:
            return ForceType.forceTypes[typeId]
        else:
            return ForceType.forceTypes[0]


class CollectionType(object):
    NORMAL = 0
    MINERAL = 1
    ZHEN_QI = 2
    PERSONAL_BOX = 3
    VIEWPOINT = 4

    VALID_RANGE_ACHIEVEMENT = (MINERAL, ZHEN_QI, PERSONAL_BOX, VIEWPOINT)
    VALID_RANGE_CHECK = (NORMAL, MINERAL, ZHEN_QI, PERSONAL_BOX, VIEWPOINT)


class CollectionPickType(object):
    Countdown_1 = 0  # 读条采集，客户端不屏蔽UI点击
    Countdown_2 = 9  # 读条采集，客户端会屏蔽UI点击
    ClientJudge_1 = 1

    CountdownTypes = (Countdown_1, Countdown_2)
    ClientJudgeTypes = (ClientJudge_1,)


class GMCommandErr(object):
    OK = 0
    TARGET_NOT_EXISTS = 1
    DB_OP_ERR = -3
    ARGS_ERR = -101
    INVALID_CMD = -102
    INVALID_JSON_RESPONSE = -103
    TARGET_OFFLINE = -104
    CMD_SERIAL_EXISTS = -105
    BAN_TYPE_INVALID = -106
    WRITE_TO_DB_ERROR = -107
    MODIFY_TEXT_CHECK_FAILED = -108
    NAME_DUPLICATE = -110
    ACCOUNT_INVALID = -111
    ALREADY_DONE = -112
    INSUFFICIENT = -113
    INTERNAL_ERROR = -114
    NO_COIN = -115
    DB_STATUS_ERR = -118
    REDIS_OP_ERR = -119
    MAX_LIMIT_ERR = -120
    ADD_WEALTH_FAILED = -121
    AFTER_SALE_ERR = -122
    SEND_MAIL_ERR = -123


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


class STORE_TYPE(metaclass=UniqueIntEnum):
    MONEY_STORE_TYPE = 1
    COIN_STORE_TYPE = 10


class BaseAppIniting(object):
    LOAD_ENTITY_DBID = 'load-entity-dbid'


class VariableType(object):
    VAR_TYPE_SPACE = 1
    VAR_TYPE_AVATAR = 2


class LoadEntitySetting(object):
    BATCH_NUM = 20
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


READ_MAIL_EXPIRE_TIME = 7 * ONE_DAY_SECONDS
NEW_MAIL_EXPIRE_TIME = 30 * ONE_DAY_SECONDS


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
    ADD_HOME_STORE_LIMIT = 1
    GET_USERS_INFO = 2
    FRIEND_INIT = 3
    SEND_FRINED_REQUEST = 4
    SEND_FRIEND_MSG = 5
    GET_FRIEND_MSG = 6


class AvatarPhotoType(object):
    AvatarPhoto = 1
    AvatarFrame = 2


class ChatSysGMErr:
    OK = 0
    FAIL = 1
    DBERR = 2


class SkillTag(metaclass=UniqueIntEnum):
    Hot = 13
    Heal = 14
    SingleHeal = 20
    Casting = 24
    Channel = 25
    NeedNoTargetInCasting = 27
    TeleportSkill = 40
    DodgeSkill = 46
    EndTimebackSkill = 47
    IgnoreImmortal = 54
    MulStageSkill = 58
    Chongfeng = 55
    Lunge = 56
    BlinkToTarget = 57
    ZedSkill = 60
    ResetCDZedSkill = 61
    AutoCombat = 63
    DoActionTogether = 64  # 技能action就执行一次,在action里结算各个目标
    FightStateSkill = 75
    HealSkill = 76
    LingzhuSkill = 80
    lzSpecialSkill = 95
    revolveSkill = 97
    randomTarget = 98
    GeneralSkill = 99
    UltraSkill = 100
    talentSkill = 110


class BuffTag(object):
    SeeHiddenEnt = 41
    GuildLeague = 48
    GuildLeagueCollectionBuff = 49
    Home = Dungeon = BTFDungeon = 50
    BattleFieldSpaceTag = 45
    GuildBattleTempPointTag = 46
    BTFSLPDungeonRebornTag = 47
    DisableSelfHiddenTag = 98


class BuffKind(object):
    Negative = -1
    Controlled = -2
    PhysicalDoT = -3
    MagicalDoT = -4

    KIND_COLL = (Negative, Controlled, PhysicalDoT, MagicalDoT)


class BuffSrcType(object):
    Unknow = 0
    Combat = 1
    Crystal = 2


class SkillScope(metaclass=UniqueIntEnum):
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
    EFFECT_UNKNOW = 0
    EFFECT_BASIC = 1
    EFFECT_BY_EVENT = 2
    EFFECT_BY_TIMER = 3


class SkillCategory(object):
    GENERAL_SKILL = 0
    CAST_SKILL_WITHOUT_ACTION = 1
    CAST_SKILL_WITH_ACTION = 2


SKILL_DMG_DESC = ("", "（水系）", "（雷系）", "（火系）", "（混沌系）")


class SkillAttackType(object):
    ATTACK_NORMAL = 0
    ATTACK_DODGE = 1
    ATTACK_CRIT = 2

class SourceType(metaclass=UniqueIntEnum):
    All=-1
    Default = 0
    Skill = 1
    Aureole = 2
    Buff = 3
    Creation = 4
    Item = 5
    PassiveSkill = 6
    BuffPoint = 7
    Equip = 8
    Title = 9
    GuildTrain = 10
    MonsterManual = 11
    Score = 12
    HomeBuilding = 13
    Init = 14
    LevelUp = 15
    DungeonAdj = 16
    SoulCard = 17
    DropWater = 18
    WhaleLevel = 19
    Plunder = 20
    PlunderWhale = 21
    Patrol = 22
    Escort = 23
    Possessed = 24
    HonorPK = 26
    awardFightProp = 27
    Fight = 28
    EventAction = 29
    Teleport = 30
    LoseFighting = 31
    TowerStage = 32
    FlowCtrl = 33
    DungeonPlaying = 34
    DailyDraw = 35
    AvatarChange = 36
    SchoolPK = 37
    GuildTrainReset = 38
    MountProp = 39
    PetProp = 40
    CollectProp = 41
    DuelEnd = 42
    DropDeath = 43

MAX_BUFF_COUNT = 50

class ChannelingBreak(object):
    BE_ATK = 1
    LOSE_TARGET = 2
    LACK_OF_MP = 3
    TARGET_DIE = 4
    CONFLICT_STATE = 5
    MOVE = 6
    CAPTURE = 7
    TELEPORT = 8
    SELF_DIE = 9
    IMMUNE_DEATH = 10
    NORMAR_END = 11

class EndCasting(object):
    Finished = 1
    ClientCancel=2
    Dead = 3
    OtherSkill = 4
    MissingTarget=5
    CaptureMonster=6
    BeAttacked = 7
    ConflictState=8
    Move=9
    ImmuneDeath=10
    Teleporting=11
    clientPick=12

class ImmuneDeathState(object):
    IMMUNE_VALID = 1
    IMMUNE_DURING = 2
    IMMUNE_FINISHED = 3

class UseSkillCheck(object):
    CHEKC_OK = 0
    IN_CD = 1
    LACK_OF_MP = 1<<1
    INVALID_OWNER = 1<<2
    STATE_CONFLICT = 1<<3
    INVALID_TARGET = 1<<4
    INVISIBLE_TARGET = 1<<5
    CROSS_SPACE = 1<<6
    OUT_OF_RANGE = 1<<7
    NEED_CAST = 1<<8
    SELF_DIE = 1<<9
    SINGLE_HEAL_OUT_OF_RANGE = 1<<10
    SHOOTER_SKILL_CANNOT_USE = 1<<11
    ULTRA_SKILL_POWER_NOT_ENOUGH = 1<<12

    #起手延迟结算时检查需要忽略的条件
    DELAY_CHECK_IGNORES = IN_CD | LACK_OF_MP | OUT_OF_RANGE | STATE_CONFLICT | INVALID_TARGET | ULTRA_SKILL_POWER_NOT_ENOUGH
    BIGWORLD_DUEL_DELAY_CHECK_IGNORES = IN_CD | LACK_OF_MP | OUT_OF_RANGE | STATE_CONFLICT | ULTRA_SKILL_POWER_NOT_ENOUGH
    #连击技能（例如风入松放一次可以砍出4刀，每刀单独结算）分阶段结算时，每个阶段的检查
    MUL_ATTACK_CHECK_IGNORES = IN_CD | LACK_OF_MP | STATE_CONFLICT | ULTRA_SKILL_POWER_NOT_ENOUGH

class ResetSkillReason(object):
    Default = 0
    SkillDone=1
    StageEnd = 2
    EndCasting = 3
    TimeRefreshDone=4
    Teleport = 5
    DuelComplete = 6
    GeneralSkillBreak = 7
    Transform = 8
    CleintEnd = 9
    DodgeSkill = 10
    UltraSkill = 11
    SkillStateRemove = 12
    Freeze = 13

class SkillActionType(object):
    StagedAct=1

class ActionProgressType(object):
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

    clientIgnoreList = (Absorb, BloodSuck, Dodge, Heal, ImmunePhysicalDmg, ImmuneMagicDmg, ImmuneAssistantDmg)

    zeroFilter = (Hit, Crit, Dodge, Heal, HealCrit, Absorb, BloodSuck, Eliminate, ShareDmg)

    @staticmethod
    @functools.lru_cache(32)
    def isInClientIgnoreList(hitType):
        return hitType in HitType.clientIgnoreList

class RemoveType(metaclass=UniqueIntEnum):
    Default = 0
    EndByTime = 1
    EndByAtt = 2
    EndByBeat = 3
    EndBySkill = 4
    EndByDead = 5
    EndByAction = 6
    RestoreRemove = 7

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

class RaceType(object):
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

    bornDoNothing = (stone, virtual, soul)
    joinCombatTup = (move, normal)
    flowConvTup = (move, stone, virtual)

    # 其他类型后面扩展

class ScriptNone(object):
    pass

scriptNone = ScriptNone()

class AIDefine(object):
    PatrolTick      = 3  # 巡逻间隔
    PatrolProb      = 75 # 巡逻概率
    SummonDis       = 5  # 召唤物跟随最大距离
    SummonDisEx     = 30 # 召唤物战斗最大距离
    SummonDisAd     = 3  # 召唤物调整最佳距离
    SummonDisYL     = 8  # 特殊召唤物（应龙）距离
    GoHomeSpeed     = 5  # 脱战回家移速调整

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
    DROP_RWD_BAG_FULL_MAIL_ID = CSTD.datas['dropRewardAndBagFull_mailID']['value']
    REWARD_MAIL_ID = CSTD.datas['getRewardAndBagFull_mailID']['value']

class JumpType(object):
    FIRST_JUMP = 1
    DOUBLE_JUMP = 2
    FLYING = 3
    SPEED_FALL = 4

class DungeonSrcEnum(object):
    DEFAULT = 0                                   # 默认
    FROM_CLIENT = 1                               # 客户端
    FROM_CLIENT_GM = 2                            # GM命令
    FROM_FOLLOW_CAPTAIN = 3                       # 跟随队长
    FROM_TASK = 4                                 # 任务流程触发传送
    FROM_KICKOUT_DUNGEON = 5                      # 踢出副本
    FROM_TIME_OUT = 6                             # 副本超时

    COLL_FROM_TASK = (FROM_TASK, )

class CompleteTeleportLeaveFailedReason(object):
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

class ComplexTeleportType(object):
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

class GamePlayRecoverEnum(object):
    RCV_NO_ACTION = 0
    RCV_FULL_HP_IO = 1
    RCV_FULL_HP_IN = 2
    RCV_FULL_HP_OUT = 3

    COLL_ENTER_RCV = (RCV_FULL_HP_IO, RCV_FULL_HP_IN)
    COLL_LEAVE_RCV = (RCV_FULL_HP_IO, RCV_FULL_HP_OUT)

# TeamStub个数
TEAMSTUB_CONFIG_NUM = 5
TEAM_MEMBER_MAX_NUM = 5
TEAM_APPLY_JOIN_MAX_NUM = 20
TEAM_LIST_MAX_NUM = 15

RAIDSTUB_CONFIG_NUM = 5
RAID_TEAM_MEMBER_MAX_NUM = 5
RAID_LSIT_MAX_NUM = 15

class TeamMicsMode(object):
    OFF = 0
    FREE = 1

    COLL_ALL = (OFF, FREE)

class RaidMicsMode(object):

    OFF = 0
    FREE = 1
    LEADER = 2

    COLL_ALL = (OFF, FREE, LEADER)

class TeamMountState(object):
    none = 0
    ride = 1
    fly = 2

class RaidJoinType(object):
    SINGLE = 1
    TEAM = 2

class TeamType(object):
    TEAM = 1
    RAID = 2

MARK_OTHER_MAX_NUM = 15    # 最大标记数量
class TeamMarkType(object):
    MARK_NONE = 0
    MARK_RED = 1
    MARK_BLUE = 2
    MARK_PURPLE = 3
    MARK_ORANGE = 4

class TeamMarkChangeType(object):
    NONE = 0
    ADD = 1
    MODIFY = 2
    DELETE = 3
    CAPTAIN = 4
    
class _RaidErrno(object):
    from userType import Error as _errno

    def reloadScript(self):
        import utils
        utils.resetCls(self)
        self._lateReload()
        return

    def _lateReload(self):
        for k, v in self.__class__.__dict__.items():
            if v.__class__.__name__ == 'Error':
                v.reloadScript()

    UNKNOWN                                 = _errno(0)         # 未知错误
    RAID_OK                                 = _errno(1)         # 正常
    RAID_PARAM_ERR                          = _errno(2)         # 参数错误
    RAID_NOT_IN_TEAM                        = _errno(10000)     # 不在小队中
    RAID_ALREADY_IN_TEAM                    = _errno(10001)     # 已经在小队中
    RAID_RAID_ID_REPEAT                     = _errno(10002)     # 团队ID重复
    RAID_TEAM_ID_REPEAT                     = _errno(10003)     # 小队ID重复(teamId)
    RAID_PLAYER_GBID_REPEAT                 = _errno(10004)     # 玩家ID重复
    RAID_TEAM_NOT_FOUND                     = _errno(10005)     # 小队ID未找到(teamId)
    RAID_PLAYER_GBID_NOT_FOUND              = _errno(10006)     # 玩家ID位找到
    RAID_NOT_TEAM_CAPTAIN                   = _errno(10007)     # 不是小队队长
    RAID_NOT_IN_RAID                        = _errno(10008)     # 不在团队中
    RAID_NOT_RAID_LEADER                    = _errno(10009)     # 不是团长
    RAID_RAID_ID_NOT_FOUND                  = _errno(10010)     # 团队ID未找到
    RAID_TEAM_IDX_REPEAT                    = _errno(10011)     # 小队IDX重复
    RAID_TEAM_IDX_NOT_FOUND                 = _errno(10012)     # 小队IDX未找到
    RAID_RAID_ID_NOT_MATCH                  = _errno(10013)     # 团队ID不匹配
    RAID_ALREADY_IN_RAID                    = _errno(10014)     # 已经在团队中
    RAID_RAID_IS_FULL                       = _errno(10015)     # 团队已满
    RAID_ALREADY_APPLY_JOIN                 = _errno(10016)     # 已经申请加入该团队
    RAID_APPLY_JOIN_NOT_FOUND               = _errno(10017)     # 申请记录没有找到
    RAID_APPLY_JOIN_RECORD_NOT_FOUND        = _errno(10018)     # 申请记录(玩家缓存)没有找到
    RAID_UNKNOWN_CAPACITY                   = _errno(10019)     # 不支持的团队人数
    RAID_CREATE_RAID_OFR                    = _errno(10020)     # 创建团对时超出人数上限
    RAID_TEAM_NUM_NOT_MATCH                 = _errno(10021)     # 小队人物数量没有匹配
    RAID_TEAM_MEMBER_NOT_MATCH              = _errno(10022)     # 小队人员没有匹配
    RAID_RAID_NOT_ENOUGH_SIT                = _errno(10023)     # 团队不足以加入新的小队
    RAID_CHECKING_TEAM_JOIN_FAILED          = _errno(10024)     # 团队检查加入失败(申请)
    RAID_AVATAR_REJECTED_ACT                = _errno(10025)     # 玩家主动拒绝操作
    RAID_PLAYER_GBID_NOT_MATCH              = _errno(10026)     # 玩家ID不匹配
    RAID_JOIN_TYPE_NOT_MATCH                = _errno(10027)     # 团队加入(检查)类型不匹配
    RAID_RAID_TEAM_IS_FULL                  = _errno(10028)     # 小队已满
    RAID_TEAM_IDX_CHANGED                   = _errno(10029)     # 小队ID变化
    RAID_TEAM_ID_CHANGED                    = _errno(10030)     # 小队ID变化(teamId)
    RAID_APPLY_BE_INVITED_RECORD_NOT_FOUND  = _errno(10031)     # 邀请记录未找到
    RAID_CHECKING_TEAM_INVITE_FAILED        = _errno(10032)     # 团队检查加入失败(邀请)
    RAID_TEAM_IS_EMPTY                      = _errno(10033)     # 小队为空
    RAID_KICKOUT_SELF                       = _errno(10034)     # 尝试移除自己(self.gbId==gbId)
    RAID_LEADER_TEAM_CANT_TRANS_CAPTAIN     = _errno(10035)     # 团长所在队伍不能转移队长
    RAID_AWARD_SELF                         = _errno(10036)     # 尝试对自己任命(团长不能对自己小队进行一些任命操作)
    RAID_AWARD_SELF_TEAM                    = _errno(10037)     # 尝试对自己所在团队任命
    RAID_ALREADY_BE_TEAM_CAPTAIN            = _errno(10038)     # 已经是小队队长
    RAID_IS_SAME_TEAM                       = _errno(10039)     # 小队相同
    RAID_IS_SAME_PLAYER                     = _errno(10040)     # 玩家相同
    RAID_RAID_TEAM_IDX_OFR                  = _errno(10041)     # 创建小队IDX超出上限
    RAID_SAME_RAID_TARGET_ID                = _errno(10042)     # 相同目标ID
    RAID_DURING_STANDBY_CHECK               = _errno(10043)     # 团队正在进行检查
    RAID_STANDBY_RECORD_NOT_FOUND           = _errno(10044)     # 团队检查记录未找到
    RAID_STANDBY_ALREADY_CHECKED            = _errno(10045)     # 已经check过
    RAID_RAID_LEADER_CHANGED                = _errno(10046)     # 团队已经变更
    RAID_TEAM_MEMBER_OFFLINE                = _errno(10047)     # 团队成员离线
    RAID_APPLY_JOIN_STUB_VAL_NOT_FOUND      = _errno(10048)     # 申请记录没有找到(RaidStub记录)
    RAID_APPLY_JOIN_NUMBER_OFR              = _errno(10049)     # 当前团队申请记录超过上限
    RAID_INVITE_SELF_TEAM                   = _errno(10050)     # 玩家尝试邀请自己的小队加入团队
    RAID_MICS_NUM_OUT_OF_RANGE              = _errno(10051)     # 麦克风人数到达上限
    RAID_MICS_BLOCK                         = _errno(10052)     # 麦克风被强制禁用
    RAID_MICS_SWITCH_OFF                    = _errno(10053)     # 麦克风总开关关闭
    RAID_MISC_FREE_MODE_LIMIT               = _errno(10054)     # Free模式限制麦克风相关功能
    RAID_MISC_LEADER_MODE_LIMIT             = _errno(10054)     # leader模式限制麦克风相关功能
    RAID_LEADER_CANT_TURN_OFF_MICS          = _errno(10056)     # 团长禁止关闭麦克风
    RAID_MICS_MODE_ERR                      = _errno(10057)     # 团队麦克风模式错误
    RAID_INVITED_SAME_PLAYER_INCD           = _errno(10058)     # 同一团队邀请CD
    RAID_IS_RAID_LEADER                     = _errno(10059)     # 操作对象是团长A
    RAID_FOLLOW_IN_BTF_DUN_FORBID           = _errno(10060)     # 战场内无法跟随
    RAID_TEAM_CANT_DISBAND                  = _errno(10061)     # 小队无法被解散
    RAID_UI_DENIED                          = _errno(10062)     # 团队接口被UI相关判断阻止
    RAID_ALL_MICS_BLOCKED                   = _errno(10063)     # 已经全员禁麦
    RAID_TEAM_MEMBER_DUOHUN                 = _errno(10064)     # 被夺魂
    RAID_NOT_RAID_DEPUTY                    = _errno(10065)     # 不是副团长
    RAID_NOT_RAID_LEADER_OR_DEPUTY          = _errno(10066)     # 不是团长/副团长
    RAID_NOT_RAID_CANNOT_KICK_LEADER        = _errno(10067)     # 不能踢团长
    RAID_NOT_RAID_CANNOT_KICK_DEPUTY        = _errno(10068)     # 不能踢副团长
    RAID_NOT_RAID_CANNOT_MOVE_LEADER        = _errno(10069)     # 不能移动团长
    RAID_NOT_RAID_UNKNOWN_TEAM_MEMBER       = _errno(10070)     # 小队人数不支持
    
    RAID_CHECKING_TEAM_JOIN                 = _errno(50000)     # 团队正在检查组队加入(申请通过)
    RAID_CHECKING_TEAM_INVITE               = _errno(50001)     # 团队正在检查组队加入(邀请通过)
    RAID_CHECKING_STANDBY_CHECK             = _errno(50002)     # 团队正在进行整团检查(团长发起)
    RAID_INVITE_TO_JOIN                     = _errno(50100)     # 团队邀请转变为申请
    RAID_TARGET_IS_ILLEGAL                  = _errno(50101)     # 团队目标不合法

    RAID_ERR_IGNORE                         = _errno(60000)     # 可以忽略的错误


RaidErrno = _RaidErrno()


class RaidPermission(object):
    """Raid permission enum"""

    UNKNOWN = 0
    MEMBER = 1
    CAPTAIN = 2
    DEPUTY = 3
    LEADER = 4

    @classmethod
    def havePermission(cls, permission, needPermission, onlyMode=False, exluce=()):
        if permission in exluce:
            return False
        if onlyMode:
            return permission == needPermission
        return permission >= needPermission

class RaidDungeonStandbyCheckSrcEnum(object):
    """全团检查check"""

    UNKNOWN = 0
    DEFAULT = 1
    ENTER_DUNGEON = 2

class TeamFollowState(object):
    Idle = 0
    Follow = 1
    Suspending = 2

class SuspendFollowReason(object):
    Default = 0
    ClientBreak = 1
    ApplyGather = 2
    Teleport = 3
    Riding = 4
    RouteErr = 5
    StateBreak = 6
    AutoCombat = 7

class ControlledByReason(object):
    Idle = 0
    Follow = 1
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
    Follow = 7
    ForceFollow = 8

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
class ChatChannel(object):
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

    @staticmethod
    def DEFAULT():
        channel = 0
        for i in range(ChatChannel.MAX):
            if i in ChatChannel.initExcludeChannel:
                continue
            channel = channel | (1 << i)

        return channel

    avatarChannel = (WORLD, GUILD, TEAM, NEARBY)

    voiceChannel = (WORLD, GUILD, TEAM, NEARBY)

class SilentSpeakScene(object):
    FRIEND_CHAT = 1             #私聊
    CHAT = 2                    #公告聊天
    ALL = 99                    #全部

class SilentSpeakState(object):
    SET_FRIEND_CHAT = 2
    REMOVE_FRIEND_CHAT = 13
    SET_CHAT = 4
    REMOVE_CHAT = 11
    SET_ALL = 6
    REMOVE_ALL = 9

class DungeonEntityLoadStatus(object):
    UNLOAD = 0
    LOADING = 1
    LOADED = 2

class DungeonPlayModeEnum(object):
    UNKNOWN = 0
    CRUSADE = 1 
    CHIEF = 2

    COLL_ALL = (CRUSADE, CHIEF)
    COLL_SYNC_SPACELEVEL = (CRUSADE, CHIEF)

class DungeonSpaceMgrProps(object):
    dungeonRewardBossID = 1000
    singleDungeonBelongPlayerGBID = 1001
    teamDungeonBelongTeamUUID = 1002
    raidDungeonBelongRaidUUID = 1003
    dungeonWinFlagSpaceMgrCache = 1004
    transPetId = 1005
    triggerGuideId = 1006
    dungeonTimeFreezeSpaceMgrFlag = 1007 # linkeed: AvatarProps. dungeonTimeFreezeEntityFlag

class DungeonSpaceType(object):
    """
    NOTE: 同时修改 SpaceType 中的类型
    """
    UNKNOWN = 0
    BIG_WORLD = 1
    COMMON = 2
    BATTLE_FIELD = 5
    GUILD = 8
    HOME = 9
    WEDDING_PARTY = 11
    HONOR_PK = 12
    SINGLE_TOWER = 13
    SCHOOL_PK = 16

    COLL_DUNGEON = (BIG_WORLD, COMMON, BATTLE_FIELD, GUILD, HOME, WEDDING_PARTY, HONOR_PK, SINGLE_TOWER,SCHOOL_PK)

class DungeonEnterType(object):
    UNKNOWN = 0
    SINGLE = 1
    TEAM = 2
    BOTH = 3
    RAID = 4

    COLL_TEAM = (TEAM, BOTH)
    COLL_SINGLE = (SINGLE, BOTH)

    COLL_BOTH = (TEAM, SINGLE)
    COLL_ALL = (TEAM, SINGLE, RAID)


_DUNGEON_TYPE_LRU_CACHE_SIZE = 4 * 4


class DungeonType(object):

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceType.COLL_DUNGEON \
                and dungeonEnterType in DungeonEnterType.COLL_TEAM:
            return True
        return False


    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isNormalTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.COMMON \
                and dungeonEnterType in DungeonEnterType.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBigWorldTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.BIG_WORLD \
                and dungeonEnterType in DungeonEnterType.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isGuildTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.GUILD \
                and dungeonEnterType in dungeonEnterType.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isHomeTeamDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.HOME \
                and dungeonEnterType in DungeonEnterType.COLL_TEAM:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceType.COLL_DUNGEON \
                and dungeonEnterType in DungeonEnterType.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isNormalSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.COMMON \
                and dungeonEnterType in DungeonEnterType.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBigWorldSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.BIG_WORLD \
                and dungeonEnterType in DungeonEnterType.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isGuildSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.GUILD \
                and dungeonEnterType in DungeonEnterType.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isHomeSingleDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.HOME \
                and dungeonEnterType in DungeonEnterType.COLL_SINGLE:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isBothDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceType.COLL_DUNGEON \
                and dungeonEnterType == DungeonEnterType.BOTH:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isRaidDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType in DungeonSpaceType.COLL_DUNGEON \
                and dungeonEnterType == DungeonEnterType.RAID:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isNormalRaidDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.COMMON \
                and dungeonEnterType == DungeonEnterType.RAID:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isGuildRaidDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.GUILD \
                and dungeonEnterType == DungeonEnterType.RAID:
            return True
        return False

    @classmethod
    @functools.lru_cache(_DUNGEON_TYPE_LRU_CACHE_SIZE)
    def isHomeRaidDungeon(cls, dungeonSpaceType, dungeonEnterType):
        if dungeonSpaceType == DungeonSpaceType.HOME \
                and dungeonEnterType == DungeonEnterType.RAID:
            return True
        return False

    @classmethod
    def isDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType in DungeonSpaceType.COLL_DUNGEON

    @classmethod
    def isBigWorldDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.BIG_WORLD

    @classmethod
    def isGuildDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.GUILD

    @classmethod
    def isHomeDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.HOME

    @classmethod
    def isPVPDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.BATTLE_FIELD

    @classmethod
    def isWeddingParty(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.WEDDING_PARTY

    @classmethod
    def isHonorPKDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.HONOR_PK

    @classmethod
    def isSchoolPKDungeon(cls, dungeonSpaceType: int):
        return dungeonSpaceType == DungeonSpaceType.SCHOOL_PK

class _ACT_ID_CONST_META(UniqueIntEnum):
    pass

class ACT_ID_CONST(metaclass=_ACT_ID_CONST_META):
    ACTIVITY_GUIDE = 32000032  # 导游
    ACTIVITY_CRUSADE_ID = 32000008

class _RaidDungeonErrno(object):
    from userType import Error as _errno

    def reloadScript(self):
        import utils
        utils.resetCls(self)
        self._lateReload()
        return

    def _lateReload(self):
        for k, v in self.__class__.__dict__.items():
            if v.__class__.__name__ == 'Error':
                v.reloadScript()

    UNKNOWN                                 = _errno(0)         # 未知错误
    RAIDDUN_OK                              = _errno(1)         # 正常
    RAIDDUN_SKIP                            = _errno(2)         # 跳过
    RAIDDUN_DUNGEON_ID_NOT_FOUND            = _errno(20000)     # 团队副本ID未找到
    RAIDDUN_NOT_IN_RAID                     = _errno(20001)     # 不在团队中
    RAIDDUN_DUNGEON_NO_NOT_MATCH            = _errno(20002)     # 团队副本不匹配
    RAIDDUN_NOT_RAID_LEADER                 = _errno(20003)     # 不是团队Leader
    RAIDDUN_RAID_ID_NOT_MATCH               = _errno(20004)     # 团队ID不匹配
    RAIDDUN_DUNGEON_VAL_NOT_FOUND           = _errno(20005)     # 团队副本val没有找到(RaidDungeonStub)
    RAIDDUN_DUNGEON_ALREADY_BE_DESTROYED    = _errno(20006)     # 团队副本已经被销毁(包括标记删除)
    RAIDDUN_RAID_ID_NOT_FOUND               = _errno(20007)     # 团队ID没有找到
    RAIDDUN_RAID_ALREADY_EXIST_DUNGEON      = _errno(20008)     # 团队已经存在副本
    RAIDDUN_NOT_IN_AVAILABLE_SPACE          = _errno(20009)     # 不在合法space中
    RAIDDUN_FOUNDER_VAL_NOT_FOUND           = _errno(20010)     # 副本成员没有找到(dungeonRaidStub)
    RAIDDUN_NOT_IN_RAID_DUNGEON             = _errno(20011)     # 不在团队副本中
    RAIDDUN_DUNGEON_IS_NOT_ACTIVE           = _errno(20012)     # 团队副本不活跃(可能是已经完成或者已经标记销毁)
    RAIDDUN_SPACE_UUID_NOT_MATCH            = _errno(20013)     # 团队space唯一ID不相同
    RAIDDUN_FOUNDER_IN_DUNGEON              = _errno(20014)     # space中存在玩家
    RAIDDUN_GUILD_LEVEL_LOWER               = _errno(20015)     # 帮会等级不够
    RAIDDUN_PLAYER_NUM_NOT_MATCH            = _errno(20016)     # 团队副本人数不满足要求
    RAIDDUN_PLAYER_IN_FIGHT_STATE           = _errno(20017)     # 团队中有成员在战斗状态
    RAIDDUN_PLAYER_NOT_IN_GUILD             = _errno(20018)     # 团本玩家不在帮会中
    RAIDDUN_LEADER_LEVEL_LOWER              = _errno(20019)     # 团长等级不足
    RAIDUN_REPEAT_ENTER_SAME_DUNGEON        = _errno(20020)     # 副本内尝试进入同一个副本
    RAIDDUN_MEMBER_LEVEL_LOWER              = _errno(20021)     # 团员等级不足
    RAIDDUN_ENTER_BLOCK_BY_COMBAT           = _errno(20022)     # 副本内正在战斗无法进入
    RAIDDUN_TELGLOBAL_LOCKED                = _errno(20023)     # 传送锁
    RAIDDUN_REWARD_NUM_CHECK_FAIL           = _errno(20024)     # 副本可挑战次数不足


RaidDungeonErrno = _RaidDungeonErrno()

class TeamDungeonCheckConditionErrno(object):
    UNKNOWN = 0
    SCORE_CHECK_FAIL = 2
    FIGHTING_FAIL = 3
    NEED_ITEM_FAIL = 4
    PRE_TASK_FAIL = 5
    NEARBY_FAIL = 6
    FOLLOW_CAP_FAIL = 7
    SC_LEVEL_CHECK_FAIL = 8
    TELEPORT_COND_FAIL = 9
    REWARD_NUM_CHECK_FAIL = 10

class DungeonFlowCompareSymbol(object):
    un = 0     # unknown
    eq = 1      # ==
    lt = 2      # <
    gt = 3      # >
    ge = 4      # >=
    le = 5      # <=

    @classmethod
    def compare(cls, symbol, val1, val2):
        if symbol == cls.eq:
            return val1 == val2
        if symbol == cls.lt:
            return val1 < val2
        if symbol == cls.gt:
            return val1 > val2
        if symbol == cls.ge:
            return val1 >= val2
        if symbol == cls.le:
            return val1 <= val2
        return False

class DungeonFlowEventName(object):
    dunStart = 'dunStart'       # 副本开始
    dunEnd = 'dunEnd'           # 副本结束
    dunDelayEnd = 'dunDelayEnd' # 副本延迟结束
    dunFailed = 'dunFailed'     # 副本失败
    createMonster = 'createMonster'     # 创建怪物
    removeMonster = 'removeMonster'     # 回收怪物
    createNPC = 'createNPC'     # 创建NPC
    removeNPC = 'removeNPC'     # 回收NPC
    createCollection = 'createCollection'       # 创建采集物
    collBeCollected = 'collBeCollected'         # 采集物被采集事件
    multiCollAllBeCollected = 'multiCollAllBeCollected'     # 多个采集物全部被采集触发事件
    removeCollection = 'removeCollection'       # 回收采集物
    createAirWall = 'createAirWall'             # 创建空气墙
    removeAirWall = 'removeAirWall'             # 回收空气墙
    createBuffPoint = 'createBuffPoint'         # 创建buff点
    removeBuffPoint = 'removeBuffPoint'         # 回收buff点
    delayLoop = 'delayLoop'                     # 带延迟的循环
    taskFinished = 'taskFinished'               # 等待任务完成
    taskFailed = 'taskFailed'                   # 等待任务失败
    taskInProgress = 'taskInProgress'           # 等待人物进行中
    monsterHp = 'monsterHp'                     # 等待怪物血量变化值一定条件
    killMonsterNum = 'killMonsterNum'           # 等待杀怪量变化值达到一定条件
    monsterRestNum = 'monsterRestNum'           # 等待怪物数量变化值达到一定条件
    castSkill = 'castSkill'     # 副本内特定怪物释放
    createCreationInFixedPosition = 'createCreationInFixedPosition' # 特定位置釋放创生物
    summonMonsterInFixedPosition = 'summonMonsterInFixedPosition'   # 特定位置释放召唤物
    addBuffToMonster = 'addBuffToMonster'                   # 副本内怪物加buff
    removeBuffFromMonster = 'removeBuffFromMonster'         # 副本内怪物去buff
    addBuffToAllPlayer = 'addBuffToAllPlayer'               # 副本内所有玩家加buff
    removeBuffFromAllPlayer = 'removeBuffFromAllPlayer'     # 副本内所有玩家去buff
    broadcastMsg = 'broadcastMsg'               # 副本内广播消息给所有玩家
    clearDungeon = 'clearDungeon'               # 移除副本内所有实体
    alivePlayer = 'alivePlayer'                 # 检测副本内活着的玩家数量
    monsterInBattle = 'monsterInBattle'         # 怪物进入战斗
    monsterLeaveBattle = 'monsterLeaveBattle'   # 怪物离开战斗
    stopDelayEvent = 'stopDelayEvent'
    createCreationInPlayerPosition = 'createCreationInPlayerPosition'       # 玩家附近创建创生物
    createCreationInMonsterPosition = 'createCreationInMonsterPosition'     # 怪物附近创建创生物
    addBuffToPlayer = 'addBuffToPlayer'         # 玩家添加buff
    castSkillToPlayer = 'castSkillToPlayer'     # 向指定类型玩家释放技能
    haveCreationInRange = 'haveCreationInRange'     # 判断指定怪物内是否存在召唤物
    removeCreation = 'removeCreation'               # 回收特定怪物放出的召唤物
    removeNoHostCreation = 'removeNoHostCreation'   # 回收无主召唤物
    dunStageSet = 'dunStageSet'                     # 设置副本阶段
    showPopoverMsg = 'showPopoverMsg'           # 实体弹出气泡消息
    popupdialog = 'popupdialog'                 # 实体弹出其他消息
    dungeonTaskForceComplete = 'dungeonTaskForceComplete'   # 副本所有玩家任务强制完成
    dungeonTaskForceFailed = 'dungeonTaskForceFailed'       # 副本所有玩家任务强制失败
    changeDunNPCToBattle = 'changeDunNPCToBattle'           # 将副本内NPC切换为可攻击状态
    changeDunNPCToNeutral = 'changeDunNPCToNeutral'         # 将副本内NPC置为中立
    changeDunNPCToFriendly = 'changeDunNPCToFriendly'       # 将副本内NPC置为友善
    changeDunNPCDialog = 'changeDunNPCDialog'               # 更改副本内NPC对话ID
    dunAnyPlayerHP = 'dunAnyPlayerHP'           # 等待副本内任一玩家血量变化值达到一定条件
    addEntityArrowTracker = 'addEntityArrowTracker'         # 创建一个指示箭头
    removeEntityArrowTracker = 'removeEntityArrowTracker'   # 移除一个指示箭头
    moveEntityToFixedPosition = 'moveEntityToFixedPosition' # 将副本内实体移动到指定位置
    createAvatarMirrorFromRandomPlayer = 'createAvatarMirrorFromRandomPlayer'   # 副本内随机玩家创建镜像
    clearEntityHate = "clearEntityHate"         # 清除副本内指定Entity仇恨
    createSummonInPlayerPosition = "createSummonInPlayerPosition"   # 玩家附近创建召唤物
    forceSelectEntityTarget = "forceSelectEntityTarget"         # 强制选择目标
    randomTrigger = 'randomTrigger'             # 随机节点
    trapBeTriggered = 'trapBeTriggered'         # 陷阱被触发
    teleportToPosition = 'teleportToPosition'   # 副本传送至特定位置
    changeEntityForce = 'changeEntityForce'     # 副本内改变阵营
    integrationEvent = 'integrationEvent'       # 副本整合节点
    changeSpaceVar = 'changeSpaceVar'           # 修改space变量
    killEntities = 'killEntities'               # 副本内强制杀死实体节点
    dungeonEntityImmuneDeath = 'dungeonEntityImmuneDeath'           # 副本内Entity进入濒死状态触发
    ifAllSelectEntityImmuneDeath = 'ifAllSelectEntityImmuneDeath'   # 全部配置ID实体濒死则执行下面节点
    checkValue = 'checkValue'                   # 副本检查变量
    createDungeonTeleporter = 'createDungeonTeleporter'     # 创建副本传送门
    monsterChangeInitState = 'monsterChangeInitState'
    monsterAddHateValue = 'monsterAddHateValue'
    stopAiTick = 'stopAiTick'                   # 停止特定EntityAI
    startAiTick = 'startAiTick'                 # 开始特定EntityAI
    entityStartRouting = 'entityStartRouting'                   # 实体开始使用路点寻路
    entityRouteFinished = 'entityRouteFinished'                 # 实体路点寻路完成
    entityRoutingMissingEscort = 'entityRoutingMissingEscort'   # 实体路点寻路中附近没有护卫（没有玩家在distance内）
    anyPlayerCinemaPlayEnded = 'anyPlayerCinemaPlayEnded'       # 副本内任一玩家动画播放结束触发
    castCinemaPlay = 'castCinemaPlay'           # 开始播放指定ID动画
    changeWeather = 'changeWeather'             # 当前场景切换到指定天气
    playerRestNum = 'playerRestNum'             # 剩余玩家数量

    stopCurTrans = 'stopCurTrans'  # 结束当前副本内所有玩家的变身效果
    triggerGuide = 'triggerGuide'  # 触发新手引导
    newTransPetStart = 'newTransPetStart'  # 小世界战斗/新手变身开始
    newTransPetEnd = 'newTransPetEnd'  # 小世界战斗/新手变身结束

    changeAllPlayerCameraStatus = 'changeAllPlayerCameraStatus'         # 副本内所有玩家切换镜头状态
    changeAllPlayerCameraLookPos = 'changeAllPlayerCameraLookPos'       # 副本内所有玩家镜头朝向某处
    revertAllPlayerCameraStatus = 'revertAllPlayerCameraStatus'       # 恢复副本内玩家的上一个镜头状态

    changeNPCSelectableStatus = 'changeNPCSelectableStatus'     # 切换NPC的可选择状态
    changeEntityDirection = 'changeEntityDirection'             # 切换Entity朝向

    timeFreezeStart = 'timeFreezeStart'     # 时间定格开始
    timeFreezeEnd = 'timeFreezeEnd'         # 时间定格结束
    playerForceTrans = 'playerForceTrans'   # 状态改变/副本内指定玩家强制变身
    taskUndertake = 'taskUndertake'         # 副本内接任务

    createRandomAppearanceNPC = 'createRandomAppearanceNPC'     # 幻化探险/创建随机外观NPC

class DungeonFlowPlayerChooseType(object):
    UNKNOWN = 0
    MONSTER_CURRENT_TARGET = 1
    RAND_IN_MONSTER_HATRED_LIST = 2
    RAND_IN_MONSTER_HATRED_LIST_EXCEPT_HIGHEST = 3
    RAND_IN_ALL_PLAYERS = 4
    MONSTER_HATRED_LIST_MONSTER = 5

class FlowAddHateType(object):
    all = 1
    rand = 2

class FriendUnreadState(object):
    mine = 0  # 自己发给别人的信息处于未读状态
    other = 1  # 别人发给自己的信息处于未读状态

    ALL_READ = 0b0000_0000  # 所有状态位皆置位0(mine, other 位都reset 为0),总状态
    OTHER_UNREAD = 0b0000_0010  # 其他人的消息未读


class FriendRequestType(object):
    notDeal = 1
    delete = 2
    accept = 3
    reject = 4

class FriendSendDirection(object):
    send = 0
    recv = 1

class GamePlayMapCheckEnum(object):
    DENY = 0
    ALLOW_WITH_MSG = 1
    ALLOW = 2

def getWorldLineCnt():
    import gameconfig
    return gameconfig.worldLineCnt()


def getWorldLineStubCnt():
    import gameconfig
    return gameconfig.baseAppCount()

lineStubMap = {}

for mapId in MapIdDef.mapWorldSet:
    lineStubMap.setdefault(mapId, {
        'stubName': 'WorldLineStub',
        'lineCount': getWorldLineCnt(),
    })

# 演武场 单独添加，因为其subType不为1
lineStubMap[7000] = {
    'stubName': 'WorldLineStub',
    'lineCount': getWorldLineCnt(),
}

spaceDict = {
}

import gamePlay_gamePlay as GGD
import gamePlay_singleSceneData as GPSSD

for mapId, mapConfig in GGD.datas.items():
    spaceDict.setdefault(mapId, {})
    spaceDict[mapId]['map'] = GPSSD.datas.get(mapConfig['sceneRes'], {}).get('tmxRes') \
                              or spaceDict[mapId].get('map') \
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
    Mount_ITEM = 1
    Mount_EVENT = 2
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
    NoHost = 0
    Avatar = 1
    Monster = 2
    Summon = 3
    Creation = 4
    Pet = 5
    AvatarMirror = 6
    NPC = 7
    Other = 8

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

    SUBTYPE_ORNAMENTS_RING = (SUBTYPE_RING_PHYSIC, SUBTYPE_RING_MAGIC, SUBTYPE_RING_MONK)
    SUBTYPE_ORNAMENTS_BRACELET = (SUBTYPE_BRACELET_PHYSIC, SUBTYPE_BRACELET_MAGIC, SUBTYPE_BRACELET_DEFENCE)

    ALL_MAINTYPES = (MAIN_TYPE_WEAPON, MAIN_TYPE_CLOTHES, MAIN_TYPE_HEAD, MAIN_TYPE_SHOE, MAIN_TYPE_NECKLACE, MAIN_TYPE_RING, MAIN_TYPE_BRACELET)
    ALL_SUBTYPES = (
        SUBTYPE_WEAPON_MONK, SUBTYPE_WEAPON_MAGE, SUBTYPE_WEAPON_WARRIOR,
        SUBTYPE_CLOTHES_MONK, SUBTYPE_CLOTHES_MAGE, SUBTYPE_CLOTHES_WARRIOR,
        SUBTYPE_HEAD_MONK, SUBTYPE_HEAD_MAGE, SUBTYPE_HEAD_WARRIOR,
        SUBTYPE_SHOE_MONK, SUBTYPE_SHOE_MAGE, SUBTYPE_SHOE_WARRIOR,
        SUBTYPE_NECKLACE_PHYSIC, SUBTYPE_NECKLACE_MAGIC,
                   ) + SUBTYPE_ORNAMENTS_RING + SUBTYPE_ORNAMENTS_BRACELET

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
    NO_RANDOM_FIX_QUALITY = (WHITE, GREEN)

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

class AUTO_DISA_QUALITY_KEY(object):
    WHITE = 0
    GREEN = 1
    BLUE = 2
    PURPLE = 3
    ORANGE = 4
    RED = 5
    TRADE = 7

class MessageType(object):
    MESSAGE_TYPE_1 = 1
    MESSAGE_TYPE_8 = 8
    MESSAGE_TYPE_9 = 9
    MESSAGE_TYPE_13 = 13
    MESSAGE_TYPE_14 = 14
    MESSAGE_TYPE_16 = 16
    MESSAGE_TYPE_17 = 17
    MESSAGE_TYPE_18 = 18
    MESSAGE_TYPE_19 = 19
    MESSAGE_TYPE_20 = 20
    MESSAGE_TYPE_21 = 21
    MESSAGE_TYPE_22 = 22
    MESSAGE_TYPE_23 = 23

    COLL_BUTTON_MESSAGE = (MESSAGE_TYPE_8, MESSAGE_TYPE_13, MESSAGE_TYPE_16, MESSAGE_TYPE_23)

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

    ALL_KEYS = (AVATAR_LEVEL, AVATAR_SCORE)


class DissolveGuildReason(object):
    NO_MEMBER = 1
    IN_ACTIVE = 2


LEADER_BOARD_UPDATE_INTERVAL = 60 * 20


GUILD_APPLY_CTX_CHECK_TIME_OUT = 60
GUILD_APPLY_TIME_OUT_DUR = 2 * ONE_DAY_SECONDS
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
GUILD_APPLY_EXPIRED_TIME = ONE_DAY_SECONDS

GUILD_DONATE_EXP = 1
GUILD_DONATE_FUND = 1
GUILD_DONATE_CONTRIBUTION = 1
GUILD_DONATE_MONEY = 1

GUILD_INVITE_DURATION = 10


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
    IN_CURRENT_SERVER = 1
    GOTO_CROSS_SERVER = 2
    IN_CROSS_SERVER = 3
    GOBACK_FROM_CROSS_SERVER = 4

class CrossServerCallbackComponent(object):
    NONE = 0
    BASE = 1
    CELL = 2
    CLIENT = 3

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


DEATH_PENALTY_INVALID_REC_TIMES = 255
CUBE_MAX_NUM = 2
CUBE_MAX_ENTER_NUM = 300
SIEGEWAR_MAX_ENTER_NUM = 500
CUBE_DAILY_TIMES = 1
CUBE_COIN_ITEM_ID = ItemId.MONEY
CUBE_ENTER_TIME_OUT_DUR = 60

MONSTER_BE_ATTACK_CLEAR_DUR = 5 * 60

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
    ARCHIVING = -2

class StoreLimitType(object):
    PERMANENT = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4

class DropShareRewardType(object):
    RANDOM_ONE = 0
    SELF = 1
    ALL_TEAMMATE = 2

# 每轮刷怪的最大数目
INIT_EACH_EN_LOOP_COUNT = 40


class BuyCreditType(object):
    money = 1
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

    def reloadScript(self):
        import utils
        utils.resetCls(self)
        self._lateReload()
        return

    def _lateReload(self):
        for k, v in self.__class__.__dict__.items():
            if v.__class__.__name__ == 'Error':
                v.reloadScript()

    UNKNOWN_ERR                             = _errno(0)
    AUCTION_OK                              = _errno(1)
    PARAM_ERROR                             = _errno(2)         # 参数错误

    AUCTION_TYPE_ERR                        = _errno(20000)     # 交易行类型错误
    AUCTION_ALREADY_IN_AUCTION              = _errno(20001)     # 交易物品已经在交易行
    AUCTION_ITEM_ATTR_NOT_DEFINED           = _errno(20002)     # 交易物品属性没有定义
    AUCTION_INDEX_ALREADY_ADDED             = _errno(20003)     # 交易行索引已经存在
    AUCTION_INDEX_NOT_FOUND                 = _errno(20004)     # 交易行索引没有找到
    AUCTION_NOT_IN_AUCTION                  = _errno(20005)     # 交易行物品没有找见
    AUCTION_CACHE_NOT_INIT                  = _errno(20006)     # 玩家交易数据没有初始化完毕
    AUCTION_AVATAR_GRID_FULL                = _errno(20007)     # 玩家可交易数量已满
    AUCTION_DEDUCT_ITEM_ERROR               = _errno(20008)     # 玩家(出售时)尝试扣除物品失败
    AUCTION_DEDUCT_ITEM_NOT_FOUND           = _errno(20009)     # 玩家(出售时候)没有找到物品
    AUCTION_BUY_ITEM_NOT_ENOUGH             = _errno(20010)     # 玩家购买物品时物品交易行数量不足
    AUCTION_COIN_NOU_ENOUGH                 = _errno(20011)     # 玩家铜贝不足
    AUCTION_ITEM_IS_LOCKED                  = _errno(20012)     # 交易行物品被锁住(暂时有其他交易进行)
    AUCTION_BUY_MUST_NOT_BE_STACKED         = _errno(20013)     # 交易物品必须不可堆叠
    AUCTION_BUY_MUST_BE_STACKED             = _errno(20014)     # 交易物品必须可堆叠
    AUCTION_SALE_ITEM_NUM_ERROR             = _errno(20015)     # 交易物品數量错误
    AUCTION_ITEM_ALREADY_BE_BINDED          = _errno(20016)     # 交易物品被绑定
    AUCTION_IS_IN_NOTIFY                    = _errno(20017)     # 交易物品在公示期
    # AUCTION_CANNOT_CANCEL_SALE              = _errno(20018)     # 交易物品暂时无法下架
    AUCTION_REVIEW_NOT_FOUND                = _errno(20019)     # 审核物品(铜贝/金丝玉贝)未找到
    AUCTION_REVIEWED_NUMBER_NOT_ENOUGH      = _errno(20020)     # 已审核物品不足
    AUCTION_ITEM_IN_COOLDOWN                = _errno(20021)     # 交易物品正在冷却
    AUCTION_PLAYER_BAG_GRID_NOT_ENOUGH      = _errno(20022)     # 玩家背包剩余格子不足
    AUCTION_CANCEL_SALE_ITEM_NOT_FOUND      = _errno(20023)     # 下架物品没有找到
    AUCTION_CANCEL_SALE_GBID_NOT_MATCH      = _errno(20024)     # 下架物品PlayerGBID不匹配
    AUCTION_ITEM_CANNOT_CANCEL_SALE         = _errno(20025)     # 物品无法被下架
    AUCTION_IS_EXPIRED                      = _errno(20026)     # 物品已经过期
    AUCTION_PLAYER_BAG_IS_LOCKED            = _errno(20027)     # 玩家背包被锁住, 无法交易
    AUCTION_BUY_CHECK_NOT_MATCH             = _errno(20028)     # 玩家购买时校验不通过
    AUCTION_FOLLOWED_ITEM_MAXIMUM           = _errno(20029)     # 玩家关注物品到达上限
    AUCTION_SALE_RECOMMAND_PRICE_NOT_DEF    = _errno(20030)     # itemId没有对应推荐定价
    AUCTION_SALE_RECOMMAND_PRICE_OOF        = _errno(20031)     # itemId定价超过推荐百分比
    AUCTION_UNLOCK_GRID_MAXIMUN             = _errno(20032)     # 交易行解锁格子到达上限
    AUCTION_UNLOCK_COST_NOT_ENOUGH          = _errno(20033)     # 交易行解锁格子扣除物品不足
    AUCTION_MONEY_NOU_ENOUGH                = _errno(20034)     # 玩家金币不足
    AUCTION_PLAYER_NOT_IN_GUILD             = _errno(20035)     # 玩家不在对应帮会中
    AUCTION_HOMECOMP_ITEM_UN_IDENTIFIED     = _errno(20037)     # 出售家具未鉴定
    AUCTION_PLAYER_BAG_TYPE_UNKNOWN         = _errno(20038)     # 交易行背包类型未知
    AUCTION_CANNOT_BUY_SELF_ITEM            = _errno(20039)     # 交易行无法购买自己卖出的商品
    AUCTION_PLAYER_MAIL_SPACE_FULL          = _errno(20040)     # 玩家邮件剩余空间不足
    AUCTION_SALED_ITEM_REJECTED             = _errno(20041)     # 交易行对应物品无法出售
    AUCTION_EQUIP_IN_DROP_REPAIR            = _errno(20042)     # 玩家装备处于掉落修复状态

    AUCTION_IDIP_GM_BAN                     = _errno(20100)     # IDIP禁止

AuctionErrno = _AuctionErrno()

class AuctionItemStatus(object):
    """
    - 状态流转定义:
        INIT --|-------------|--> SELLING --|-------------|--> |--> SELLED
               |--> NOTIFY --|              |--> REVIEW --|    |--> CANCELD
                                                               |============> EXPIRED
    """

    INIT = 0
    NOTIFY = 1
    SELLING = 2
    REVIEW = 3
    SELLED = 4
    CANCELD = 5
    EXPIRED = 6

    COLL_INAUCTION = (NOTIFY, SELLING, EXPIRED)
    COLL_CAN_BEFOLLOWED = (NOTIFY, SELLING)
    COLL_CAN_BE_TYPEDFOLLOWED = (SELLING, )

class AuctionSource(object):
    UNKNOWN = 0
    FROM_PLAYER = 1

class AuctionCollection(object):
    START_KEY = 2001
    MAX_COUNT = 20
    CHECK_TIP_INTERVAL = 1

DROP_REMOTE_CACHE_EXPIRE_TIME = 60
DROP_DROP_EXPIRE_DELAY = 5
DROP_PICK_EXPIRE_DELAY = 10

class DropType(object):
    TYPE_DROP   = 1 #// 掉落
    TYPE_TAKE   = 2 #// 有人捡起了这个掉落
    TYPE_REDEEM = 3 #// 主人赎回
    TYPE_GIVEUP = 4 #// 捡起掉落的人主动放弃

class DropNotifyType(object):
    NOTIFY_DROP_EXPIRE = 1 # 你掉落的装备过期了
    NOTIFY_TAKE_EXPIRE = 2 # 你捡起的装备过期了

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

class EnemyRecordType(object):
    KILL_ENEMY = 1 # 击杀敌人
    BE_KILL_BY_ENEMY = 2 # 被敌人击杀


SEND_ENEMY_RECORD_BATCH_NUM = 10


class MoralType(object):
    MORAL_NOT_CHANGE = 0 # 善恶值保持不变
    MORAL_COULD_CHANGE = 1


class DungeonFlowMoveAni(object):
    DEFAULT = 0
    RUN01 = 1
    RUN02 = 2

class DungeonCustomAreaType(object):
    RECTANGLE = 0
    CIRCLE = 1
    LINE = 2

    @staticmethod
    def getRectangleVal(data):
        return data['Length'], data['Width']

    @staticmethod
    def getCircleRadius(data):
        return data['Radius']

    @staticmethod
    def getLineVal(data):
        return data['Length']
    

class LogOnEnterType(object):
    NONE = 0
    CUBE = 1
    WONDER_LAND = 2


class AchievementFlag(object):
    FINISHED = 0


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
    COLLECT = 23 # 收集
    LEADER_BOARD = 24 # 排行榜
    SIEGE_KILL = 25 # 城战击杀
    PERSONAL_BOX = 26 # 个人宝箱
    VIEWPOINT = 27 # 景观点


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

MORPH_BUILD_STATE = 1 # 变身状态对应技能在build里面对应的状态

BLAZE_CHECK_DIS = 5 # 快速移动监测距离
BLAZE_TIMEOUT = 6

class WonderAddTicketReason(object):
    FROM_CLIENT = 1
    CHECK_COND = 2
    RENEW_USE_COIN = 3
    RENEW_USE_ITEM = 4
# WONDERLAND end

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

class ActivityControlType(object):
    # 单人
    SINGLE = 0
    # 组队
    TEAM = 1
    # 组团
    RAID = 2

class GuildTaskType(object):
    COLLECTION = 1  #采集
    DONATION = 2    #帮会捐献
    ENTERMAP = 3    #进入地图
    COMPLETEMAP = 4 #完成地图
#雷击区域buff
LIGHTNINGAREABUFF = 64004952

ANCHOR_CAST_DUR = 1

# 铭文效果类型
class InscriptionEffectType(metaclass=UniqueIntEnum):
    # 替换技能
    REPLACE_SKILL = 15


BOUNTY_TASK_UI_ID = 28

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

class WorldLineSceneState(object):
    THUNDER = 0 # 落雷
    WIND = 1 # 风场
    LEI_JI = 2 # 雷buff会持续叠加的


class CreationCustomType(object):
    THUNDER = '1' # 落雷


WORLD_BOSS_MOCK_REFRESH_TIME = 60


# ----------------------------- cube mock start -----------------------------
MAX_CUBE_LINE = 2
CUBE_HALL_MAX_NUM = 150
CUBE_COW_DUR_INTERVAL = 5

class TeleporterType(object):
    NONE = 0
    CUBE_HALL = 1 # 混沌回廊大厅的传送门
    CUBE_BACK = 2 # 从奶牛房返回原房间
    TO_CUBE_COW = 3 # 传送到混沌回廊奶牛关
    TO_CUBE_MAP_ID = 4 # 进混沌回廊，customID作为mapId用


class CubeRoomType(object):
    NORMAL = 1
    COW = 2


# ----------------------------- cube mock end -----------------------------

# ----------------------------- AI mock start -----------------------------
# ----------------------------- AI mock end -----------------------------

class ItemLockStatus(object):
    UNLOCKED = 0 # 未上锁
    LOCKED = 1 # 已上锁
    VALID_STATUS = (UNLOCKED, LOCKED)

class RaidAttrType(object):
    # 积分
    Score = 1

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

class WorkshopOpenStatus(object):
    CLOSE = 0 # 关闭
    OPEN = 1  # 开放
