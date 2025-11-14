# coding: utf-8
import KBEngine
from KBEDebug import *
import functools
import formula
import utils
import creep_countRefresh as CCR

class IMapMonsterRefresh(object):

    @classmethod
    def clearAllCache(cls):
        cls.countLimit.cache_clear()
        cls.refreshMonsterIDs.cache_clear()
        cls.countMonsterIDs.cache_clear()
        cls.countResetTime.cache_clear()

    @staticmethod
    @functools.lru_cache(128)
    def getRefreshDataKey(mapID, monsterIntanceID):
        dataKey = mapID*100000000+monsterIntanceID
        return CCR.refreshMonsterIDIndex.get(dataKey, 0)
    
    @staticmethod
    @functools.lru_cache(128)
    def getRefreshDataKeys(mapID):
        return CCR.mapIDIndex.get(mapID, None)
        
    @staticmethod
    @functools.lru_cache(64)
    def countLimit(dataKey):
        countRefreshData = CCR.datas.get(dataKey, None)
        if countRefreshData:
            return countRefreshData['countLimit']
        return None

    @staticmethod
    @functools.lru_cache(64)
    def refreshMonsterIDs(spaceNo, dataKey):
        mapId = formula.getMapId(spaceNo)
        countRefreshData = CCR.datas.get(dataKey, None)
        if countRefreshData:
            dunData = utils.getDunModuleData(mapId)
            refreshMonsterIDs = countRefreshData['refreshMonsterID']
            if len(refreshMonsterIDs) > 0:
                datas = {}
                for refreshMonsterID in refreshMonsterIDs:
                    datas[refreshMonsterID] = dunData[str(refreshMonsterID)]["Props"]["RefreshNum"]
                return datas
        return None

    @staticmethod
    @functools.lru_cache(64)
    def countMonsterIDs(dataKey):
        countRefreshData = CCR.datas.get(dataKey, None)
        if countRefreshData:
            return countRefreshData['countMonsterID']
        return None

    @staticmethod
    @functools.lru_cache(64)
    def countResetTime(dataKey):
        countRefreshData = CCR.datas.get(dataKey, None)
        if countRefreshData:
            return countRefreshData['countResetTime']
        return None
    
    def __init__(self):
        # 刷新计数
        self.refreshCount = 0
        # 当下死亡或者销毁的刷新怪物记录
        self.killOrDestroyMonsterIDs = {}
        # 等待下一次计数
        self.waitForNextRefresh = False
        # 上一次记录的时间
        self.lastRecordTime = 0

    def onMonsterDestroy(self, monsterId, monsterInstId, spaceMgrId, monsterMgrId, refreshDataKey):
        DEBUG_MSG("onMonsterDestroy ", monsterId, monsterInstId, self.spaceNo, self.spaceID, refreshDataKey)
        if self.lastRecordTime == 0:
            self.lastRecordTime = utils.getNow()
        else:
            lastRecordTime = self.lastRecordTime
            self.lastRecordTime = utils.getNow()
            countResetTime = self.countResetTime(refreshDataKey)
            if countResetTime and countResetTime > 0:
                if self.lastRecordTime - lastRecordTime >= countResetTime:
                    self.refreshCount = 0

        if not self.waitForNextRefresh:
            countMonsterIDs = self.countMonsterIDs(refreshDataKey)
            if countMonsterIDs is None:
                return
            if monsterId in countMonsterIDs:
                self.refreshCount += 1
                if self.refreshCount >= self.countLimit(refreshDataKey):
                    self.refreshCount = 0
                    self.waitForNextRefresh = True
                    self.doMapMonsterRefresh(spaceMgrId, monsterMgrId, monsterInstId, refreshDataKey)
            return

        refreshMonsterIDs = self.refreshMonsterIDs(self.spaceNo, refreshDataKey)
        if refreshMonsterIDs is None:
            return

        if monsterInstId in refreshMonsterIDs.keys():
            self.killOrDestroyMonsterIDs[monsterInstId] = self.killOrDestroyMonsterIDs.get(monsterInstId, 0) + 1
            if self.killOrDestroyMonsterIDs == refreshMonsterIDs:
                self.killOrDestroyMonsterIDs.clear()
                self.refreshCount = 0
                self.waitForNextRefresh = False
                self.lastRecordTime = 0

    def doMapMonsterRefresh(self, spaceMgrId, monsterMgrId, monsterInstId, refreshDataKey):
        DEBUG_MSG("doMapMonsterRefresh ", self.spaceNo, self.spaceID, spaceMgrId, monsterMgrId, refreshDataKey)
        refreshMonsterIDs = self.refreshMonsterIDs(self.spaceNo, refreshDataKey)
        if refreshMonsterIDs is None:
            ERROR_MSG("doMapMonsterRefresh 1, missing refreshMonsterIDs ", self.spaceNo, self.spaceID)
            return

        mapID = formula.getMapId(self.spaceNo)
        dunData = utils.getDunModuleData(mapID)
        instanceIDs = []
        for refreshMonsterID in refreshMonsterIDs.keys():
            monsterData = dunData[str(refreshMonsterID)]
            refreshNum = int(monsterData['Props']['RefreshNum'])
            for i in utils.generateGameEntityId(refreshMonsterID, refreshNum):
                instanceIDs.append(i)

        entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, instanceIDs, entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in entityProps:
            _params['spaceMgrId'] = spaceMgrId
            _params['monsterGroupId'] = monsterMgrId
            KBEngine.createEntity(_className, self.spaceID, _pos, _dir, _params)

