# -*- coding: utf-8 -*-
import collections
import MineGlobalData

# 记录了全局所有baseapp的地址到其mailbox的映射
baseAppCache = {}
# spaceNo到spaceId的对应的映射,包括了该服务器的所有静态和副本地图
spaceNOIDCache = {}
# spaceId到spaceNo的对应映射,包括了该服务器的所有静态和副本地图
spaceIDNOCache = {}
# 记录entity名字到它数据库中DBID的映射
entityTypeToDBIDDic = None

# 记录accountBox
localAccountCache = {}

roleCache = {}

# 等待服 Avataring 实体缓存，key: entityId, value: roleInfo dict
avataringCache = {}

mallItemPriceCache = {}
mallItemLastUpdateTime = {}
mallItemPriceInfoDict = {}

# 记录role gbId到entityId的映射
roleGBIDToEntId = {}

reloadedModuleDic = {}
reloadedModuleIdDic = {}
reloadedCls = {}
gmCmdData = {}
GM_CMD_FUNC_NAMES = set()
GM_CMDS = {}
GM_CMD_ARG_PERMISSION_CHECKER = {}


def clearCommandsCache():
    GM_CMDS.clear()
    GM_CMD_FUNC_NAMES.clear()
    GM_CMD_ARG_PERMISSION_CHECKER.clear()

newAuctionItemCache = {}
expiredDrawCardPoolCache = {}

def clearDataCache(clearGlobalAttrCacheList):
    for attrCache in clearGlobalAttrCacheList:
        attrCache and attrCache.clear()

staticCell = None


gbIdSeqId = 0
gbIdTSIdx = 0

hotfix = ''

# 地图所有传送门GameEntiyID到传送门实体ID的一一映射
# key: spaceNo
# value: dict
#   key: TeleporterEntity.teleportId
#   value: (TeleporterEntity.id,TeleporterEntity.gameentityId)
teleporterGIDToEntIdMap = {}
complexTeleportTypeFnMap = {}

isBootstrap = False
isBaseAppReady = False
isRelivedBaseapp = False
deadBaseapps = {}

globalBlockExposedFuncName = {}
refreshCount = 0

# uid->methodName,cellapp上为cell方法，baseapp上为base方法
avatarExposedMethods = {}

# interface 注册人数
registerCount = 0

globalObIdTs = 0
globalObIdSeqId = 0

localSpaceNoMap = {}
localSpaceIDMap = {}
readyBaseappOrder = set()

localBaseApp = None
localAdminStub = None
localLoginStub = None
localAuctionStub = None
localLeaseStub = None
localOrderStub = None
cellAvatarCountDict = {}

# cell
cellAvatarCount = 0
lastBroadcastCellAvatarCount = 0
cellSpaceDungeonMap = {}

# 本服世界等级，由 LeaderBoardStub 同步到 globalData，cell/base 均可读取
worldLevel = 0
# 跨服世界等级（跨服算出后广播到各服）
crossWorldLevel = 0

requiredClientVersion = {}

def onLineEntityReady(spaceNo):
    localBaseApp.onLineEntityReady(spaceNo)


globalMailsCacheList = []

switchGlobalVal = None

areaData = None

spaceGeometryTaskData = None

globalActData = {}

freeTicketNumConfig = {}
antiAddictionData = [0, 0]
localMinorAccountCache = {}

globalSiegeWarData = {
    'isBidding': False
}

# 帮会关系记录
guildRelationDic = {}
# 帮会关系记录的版本
guildRelationVersion = 0

# 敌对立关系实体记录（entity-level）：
#   key: (attackType, attackId, targetType, targetId) 稳定的战争行唯一键
#   value: dict { 'attackType':.., 'attackId':.., 'attackServerId':..,
#                 'targetType':.., 'targetId':.., 'targetServerId':.., 'endTime':.. }
# 这是敌对关系的唯一权威来源。单个实体行（帮会↔帮会 / 帮会↔联盟 / 联盟↔联盟）
# 不再展开成 N×M 的帮会↔帮会对；每个帮会当前的敌对集合以该行 + 实时联盟成员身份
# 推导（见 utils.isEntityEnemy / isGuildRelationEnemy）。
enemyRelationDic = {}
# 敌对立关系记录的版本
enemyRelationVersion = 0
# 当前服务器别名
curServerAlias = ''
curServerName = ''
mapleServerInfo = {}

# 账号设置下次登录的base 进程的compId用的
accountCompIdCache = {}

# 同个进程内限制调用次数的字典
callLimitDic = {}

appCallIdx = 0

# 事件注册记录
hookDict = {}

# 全服屏蔽的任务记录
forbiddenTaskIds = {}

mineGlobalData = MineGlobalData.MineGlobalData()
mineCanAttackBits = 0


chatForbiddenSet = set()

dunCreateTS = 0
dunCreateNum = 0

