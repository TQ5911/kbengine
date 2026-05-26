# -*- coding: utf-8 -*-
import collections
import MineGlobalData

# 记录了全局所有baseapp的地址到其mailbox的映射
baseAppCache = {}
# spaceNo到spaceId的对应的映射,包括了该服务器的所有静态和副本地图
spaceNOIDCache = {}
# spaceId到spaceNo的对应映射,包括了该服务器的所有静态和副本地图
spaceIDNOCache = {}
# 记录了全局所有静态地图的spaceno到SpaceMarker的映射
localSpaceMarkers = {}
# 记录entity名字到它数据库中DBID的映射
entityTypeToDBID = None

# 记录accountBox
localAccountCache = {}

roleCache = {}

# 记录role gbId到entityId的映射
roleGBIDToEntId = {}

reloadedModuleMap = {}
reloadedModuleIdMap = {}
reloadedCls = {}

gmCmdData = {}

GM_CMDS = {}
GM_CMD_FUNC_NAMES = set()
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

