# -*- coding: utf-8 -*-
import KBEngine
import formula
from KBEDebug import *
import gametimer
import random
import gameconst
import utils
import gameengine
import gameconfig
import BalancedObjectGenerator
import creep_base as CBD
import branchData_set as BDS



class IEntityLoader(object):
    def __init__(self):
        self._maxCreateIndex = {}

    def isSpaceLeagal(self, spaceNo):
        _type = formula.getSpaceType(spaceNo)
        return _type == gameconst.SpaceType.SpaceLine\
            or _type == gameconst.SpaceType.SpaceCube\
            or _type == gameconst.SpaceType.SpaceWonderLand\
            or _type == gameconst.SpaceType.SpaceSiegeWar

    def loadLineEntities(self, spaceNo, entityIDs, readyEntitiesList, isRefresh=False):
        if not entityIDs:
            return

        loopNum = len(entityIDs)
        tmp_list, _ = entityIDs.popitems(loopNum)
        if not tmp_list:
            return

        utils.loadLineReadyEntities(spaceNo, tmp_list, readyEntitiesList, isRefresh)

    def loadEntitiesBatchly(self, spaceNo, entIter, batchNum, interval, isInit=False, spaceMgrId=0, attachedHostId=0):
        LOG_DBG("loadEntitiesBatchly-----------", batchNum, interval)
        _iter = self.loadEntitiesAsync(entIter, isInit, spaceMgrId, attachedHostId)
        self.batchlyCall(_iter, batchNum, interval)

    def loadEntitiesAsync(self, entIter, isInit, spaceMgrId=0, attachedHostId=0):
        while True:
            _ret = next(entIter, None)
            if _ret is None:
                break

            (_, _, clsName, _, pos, direction, props, _) = _ret

            if spaceMgrId:
                props['spaceMgrId'] = spaceMgrId

            if attachedHostId:
                tempMiscProps = props.setdefault('tempMiscProps', {})
                tempMiscProps[gameconst.EntityPropsEnum.beAttachedHostID] = attachedHostId

            while True:
                try:
                    self.createCellLocally(clsName, pos, direction, props)
                    yield utils.emptyFunc
                    break
                except SystemError as e:
                    LOG_WARN('loadEntitiesAsync::SystemError', e)
                    yield utils.emptyFunc

        if isInit:
            self.doLoadEntitiesEnd()

        yield utils.emptyFunc

    def _loadMonsterGroups(self, spaceNo, spaceMgrId):
        _mapId = formula.fetchMapId(spaceNo)
        if not utils.isDunGroupModuleDataExist(_mapId):
            return

        _groupData = utils.getDunGroupModuleData(_mapId)
        if not _groupData:
            return

        for _groupId, _gids in _groupData.items():
            _groupId = int(_groupId)
            _props = {
                'groupId': _groupId,
                'spaceNo': spaceNo,
                'spaceMgrId': spaceMgrId
            }

            _pos = (0.0, 0.0, 0.0)
            _dir = (0.0, 0.0, 0.0)

            while True:
                try:
                    self.createCellLocally('MonsterGrp', _pos, _dir, _props)
                    yield utils.emptyFunc
                    break
                except SystemError as e:
                    LOG_WARN('_loadMonsterGroups::SystemError', e)
                    yield utils.emptyFunc


    def doLoadEntities(self, spaceMgrId):
        if not gameconfig.needLoadEntity():
            LOG_WARN('loadEntities::skip load entities')
            self.doLoadEntitiesEnd()
            return

        self.loadCommonEntities(spaceMgrId)
        self.loadMonsterGroups(spaceMgrId)

    def loadMonsterGroups(self, spaceMgrId):
        _iter = self._loadMonsterGroups(self.spaceNo, spaceMgrId)
        self.batchlyCall(_iter, 1, 0.1)
        self.doLoadTimerEntities(spaceMgrId)

    def loadCommonEntities(self, spaceMgrId):
        entityIDs = self._initEntities(self.spaceNo)
        readyEntitiesList = []
        self.loadLineEntities(self.spaceNo, entityIDs, readyEntitiesList)
        self.loadEntitiesBatchly(self.spaceNo, iter(readyEntitiesList),
                                 gameconfig.entityLoadSpeed(),
                                 gameconst.LoadEntitySetting.BATCH_DELAY, True, spaceMgrId)

    def _initEntities(self, spaceNo):
        _mapId = formula.fetchMapId(spaceNo)
        def _iterGameEntityId():
            if self.isSpaceLeagal(spaceNo):
                spaceConfig = utils.getDunStructModData(_mapId)
                datas = spaceConfig.get('InitEntities', {})
                for entType, ents in datas.items():
                    for id_, data in ents.items():
                        id_ = int(id_)
                        _d = data.get('Props', {})
                        if _d.get('MonsterGroupID', 0):
                            continue

                        if not _d.get('IsOpen', True):
                            LOG_WARN('_initEntities::Skip not isOpen Monster', id_)
                            continue
                        count_ = int(_d.get('RefreshNum', 1))

                        if not count_:
                            continue

                        if count_ > 999:
                            LOG_ERR('_initEntities::RefreshNum too large', count_)
                            count_ = 999

                        self._maxCreateIndex.setdefault(id_, 0)
                        self._maxCreateIndex[id_] += count_
                        for i in utils.genGameEntityId(id_, count_):
                            yield i

        _retList = BalancedObjectGenerator.BalancedObjectGenerator(_iterGameEntityId())
        random.shuffle(_retList)
        return _retList

    def doLoadEntitiesEnd(self):
        LOG_DBG("iEntityLoader doLoadEntitiesEnd ", self.spaceNo)
        if formula.inWonderLandScene(self.spaceNo):
            gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onLoadEntitiesEnd(self.spaceNo)

        elif formula.inWorldLineScene(self.spaceNo):
            lineType = formula.fetchMapId(self.spaceNo)
            gameengine.getLineStub(lineType).onLoadEntitiesEnd(self.spaceNo)

        elif formula.inCubeScene(self.spaceNo):
            gameengine.getCubeStubBySpaceNo(self.spaceNo).onLoadEntitiesEnd(self.spaceNo)

        elif formula.inSiegeWarScene(self.spaceNo):
            gameengine.getGlobalBase('SiegeWarSpaceStub').onLoadEntitiesEnd(self.spaceNo)

        else:
            LOG_INFO('iEntityLoader::doLoadEntitiesEnd::unknown space type', self.spaceNo)

    def doEntityRefresh(self, gameEntityId, spaceMgrId, pointData):
        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [gameEntityId], _entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            spaceMgr = None
            if spaceMgrId:
                _params['spaceMgrId'] = spaceMgrId
                spaceMgr = KBEngine.entities.get(spaceMgrId)

            boxGroupId = utils.getEntityBoxGroupId(gameEntityId, self.spaceNo)
            if boxGroupId > 0 and spaceMgr:
                spaceMgr.addBoxGroupCollect(_className, _pos, _dir, _params)
            else:
                self.createCellLocally(_className, _pos, _dir, _params)

        self.removeEntityRefreshTimer(gameEntityId, spaceMgrId, pointData)

    def removeEntityRefreshTimer(self, gameEntityId, spaceMgrId, pointData):
        LOG_DBG("removeEntityRefreshTimer", gameEntityId, spaceMgrId, pointData)
        if not spaceMgrId:
            return
        spaceMgr = KBEngine.entities.get(spaceMgrId)
        if not spaceMgr:
            return
        gid = utils.parseGidFromGameEntityId(gameEntityId)
        spaceMgr.onCancelEntityRefreshTimer(gid, pointData["refreshTimerId"])

    def _initSpecifiedEntities(self, spaceNo, gidList):
        _mapId = formula.fetchMapId(spaceNo)
        def _iterGameEntityId():
            if self.isSpaceLeagal(spaceNo):
                dunData = utils.getDunModuleData(_mapId)
                for gid in gidList:
                    if not dunData:
                        continue
                    data = dunData.get(gid, None)
                    if not data:
                        continue

                    className = data.get('ClassName', '')
                    if className not in ('AirWall', 'Monster', 'Collection'):
                        continue

                    id_ = int(gid)
                    _d = data.get('Props', {})
                    if not _d.get('IsOpen', True):
                        LOG_WARN('_initSpecifiedEntities::Skip not isOpen Monster', id_)
                        continue
                    count_ = int(_d.get('RefreshNum', 1))
                    if not count_:
                        continue

                    if count_ > 999:
                        LOG_ERR('_initSpecifiedEntities::RefreshNum too large', count_)
                        count_ = 999

                    self._maxCreateIndex.setdefault(id_, 0)
                    self._maxCreateIndex[id_] += count_
                    for i in utils.genGameEntityId(id_, count_):
                        yield i

        _retList = BalancedObjectGenerator.BalancedObjectGenerator(_iterGameEntityId())
        random.shuffle(_retList)
        return _retList

    def doLoadSpecifiedEntities(self, gids, spaceMgrId, attachedHostId=0):
        entityIDs = self._initSpecifiedEntities(self.spaceNo, gids)
        readyEntitiesList = []
        self.loadLineEntities(self.spaceNo, entityIDs, readyEntitiesList, True)
        self.loadEntitiesBatchly(self.spaceNo, iter(readyEntitiesList),
                                 gameconfig.entityLoadSpeed(),
                                 gameconst.LoadEntitySetting.BATCH_DELAY, False, spaceMgrId, attachedHostId)

    def doLoadTimerEntities(self, spaceMgrId):
        if not spaceMgrId:
            return
        spaceMgr = KBEngine.entities.get(spaceMgrId)
        if not spaceMgr:
            return

        readyTimerEntitiesMap = {}
        self.loadTimerEntities(self.spaceNo, readyTimerEntitiesMap)
        spaceMgr.initTimerEntities(self, readyTimerEntitiesMap)

    def loadTimerEntities(self, spaceNo, readyTimerEntitiesMap):
        if not self.isSpaceLeagal(spaceNo):
            return

        _mapId = formula.fetchMapId(spaceNo)
        spaceConfig = utils.getDunStructModData(_mapId)
        datas = spaceConfig.get('TimerEntities', {})
        for id_, data in datas.items():
            className = data.get('ClassName', '')
            entityID = data.get('EntityID', 0)
            if className not in ('Monster', 'Collection'):
                LOG_WARN('loadTimerEntities::className error, ', className)
                continue
            
            if formula.inWorldLineScene(spaceNo):
                lineNo = formula.parseLineNo(spaceNo)
                nameSuffixID = -1
                if entityID in CBD.datas:
                    nameSuffixID = CBD.datas[entityID]['nameSuffixID']

                if nameSuffixID in BDS.datas["Branch_creepNotRefresh"]["value"] and lineNo != 0 and lineNo != -1:
                    LOG_DBG("skip create monster", spaceNo, entityID, nameSuffixID, lineNo)
                    continue

            id_ = int(id_)
            _d = data.get('Props', {})
            refreshTimedID = _d.get('RefreshTimedID', 0)
            if not refreshTimedID:
                LOG_WARN('loadTimerEntities::refreshTimedID error, ', refreshTimedID)
                continue

            if not _d.get('IsOpen', True):
                LOG_WARN('loadTimerEntities::Skip not isOpen Monster', id_)
                continue
            count_ = int(_d.get('RefreshNum', 1))

            if not count_:
                LOG_WARN("loadTimerEntities::RefreshNum not exist",spaceNo)
                continue

            if count_ > 999:
                LOG_WARN('loadTimerEntities::RefreshNum too large', count_)
                count_ = 999

            refreshData = (id_, gameconst.className2EntityType[className], {"EntityID":entityID, "RefreshNum":count_})
            readyTimerEntitiesMap.setdefault(refreshTimedID, []).append(refreshData)
            LOG_DBG("loadTimerEntities", spaceNo, id_, refreshTimedID, refreshData)
