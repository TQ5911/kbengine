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


class IEntityLoader(object):
    def __init__(self):
        self._maxCreateIndex = {}

    def isSpaceLeagal(self, spaceNo):
        _type = formula.whatSpaceType(spaceNo)
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
        DEBUG_MSG("loadEntitiesBatchly-----------", batchNum, interval)
        for i in range(batchNum):
            (entId, _, clsName, needCreateBase, pos, direction, props, rGid) = next(entIter, (
            0, None, None, None, None, None, None, None))
            if not entId:
                INFO_MSG('finish loading all entities', spaceNo)
                if isInit:
                    self.doLoadEntitiesEnd()
                return

            if spaceMgrId:
                props['spaceMgrId'] = spaceMgrId
            if attachedHostId:
                tempMiscProps = props.setdefault('tempMiscProps', {})
                tempMiscProps[gameconst.AvatarProps.beAttachedHostID] = attachedHostId

            self.createCellLocally(clsName, pos, direction, props)

        self._callback(interval, 'loadEntitiesBatchly', (spaceNo, entIter, batchNum, interval, isInit, spaceMgrId, attachedHostId),
                       gametimer.TIMER_TAG_LOAD_ENTITIES_CALL_BACK)

    def loadMonsterGroups(self, spaceNo, spaceMgrId):
        _mapId = formula.getMapId(spaceNo)
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

            self.createCellLocally('MonsterGrp', _pos, _dir, _props)
            yield lambda *args: args

    def doLoadEntities(self, spaceMgrId):
        if not gameconfig.needLoadEntity():
            WARNING_MSG('loadEntities::skip load entities')
            self.doLoadEntitiesEnd()
            return

        entityIDs = self._initEntities(self.spaceNo)
        readyEntitiesList = []
        self.loadLineEntities(self.spaceNo, entityIDs, readyEntitiesList)
        self.loadEntitiesBatchly(self.spaceNo, iter(readyEntitiesList),
                                 gameconfig.entityLoadSpeed(),
                                 gameconst.LoadEntitySetting.BATCH_DELAY, True, spaceMgrId)

        _iter = self.loadMonsterGroups(self.spaceNo, spaceMgrId)
        self.batchlyCall(_iter, 1, 0.1)
        self.doLoadTimerEntities(spaceMgrId)

    def _initEntities(self, spaceNo):
        _mapId = formula.getMapId(spaceNo)
        def _iterGameEntityId():
            if self.isSpaceLeagal(spaceNo):
                spaceConfig = utils.getDunStructureModuleData(_mapId)
                datas = spaceConfig.get('InitEntities', {})
                for entType, ents in datas.items():
                    for id_, data in ents.items():
                        id_ = int(id_)
                        _d = data.get('Props', {})
                        if _d.get('MonsterGroupID', 0):
                            continue

                        if not _d.get('IsOpen', True):
                            WARNING_MSG('_initEntities::Skip not isOpen Monster', id_)
                            continue
                        count_ = int(_d.get('RefreshNum', 1))

                        if not count_:
                            continue

                        if count_ > 999:
                            ERROR_MSG('_initEntities::RefreshNum too large', count_)
                            count_ = 999

                        self._maxCreateIndex.setdefault(id_, 0)
                        self._maxCreateIndex[id_] += count_
                        for i in utils.generateGameEntityId(id_, count_):
                            yield i

        _retList = BalancedObjectGenerator.BalancedObjectGenerator(_iterGameEntityId())
        random.shuffle(_retList)
        return _retList

    def doLoadEntitiesEnd(self):
        DEBUG_MSG("iEntityLoader doLoadEntitiesEnd ", self.spaceNo)
        if formula.isWonderLandSpace(self.spaceNo):
            gameengine.getWonderLandStubBySpaceNo(self.spaceNo).onLoadEntitiesEnd(self.spaceNo)

        elif formula.spaceInWorldLine(self.spaceNo):
            lineType = formula.getMapId(self.spaceNo)
            gameengine.getLineStub(lineType).onLoadEntitiesEnd(self.spaceNo)

        elif formula.isCubeSpace(self.spaceNo):
            gameengine.getCubeStubBySpaceNo(self.spaceNo).onLoadEntitiesEnd(self.spaceNo)

        elif formula.isSiegeWarSpace(self.spaceNo):
            gameengine.getGlobalBase('SiegeWarSpaceStub').onLoadEntitiesEnd(self.spaceNo)

        else:
            INFO_MSG('iEntityLoader::doLoadEntitiesEnd::unknown space type', self.spaceNo)

    def doEntityRefresh(self, gameEntityId, spaceMgrId):
        _entityProps = []
        utils.loadLineReadyEntities(self.spaceNo, [gameEntityId], _entityProps, True)
        for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
            if spaceMgrId:
                _params['spaceMgrId'] = spaceMgrId

            self.createCellLocally(_className, _pos, _dir, _params)

    def _initSpecifiedEntities(self, spaceNo, gidList):
        _mapId = formula.getMapId(spaceNo)
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
                    if className not in ('AirWall', 'Monster',):
                        continue

                    id_ = int(gid)
                    _d = data.get('Props', {})
                    if not _d.get('IsOpen', True):
                        WARNING_MSG('_initSpecifiedEntities::Skip not isOpen Monster', id_)
                        continue
                    count_ = int(_d.get('RefreshNum', 1))
                    if not count_:
                        continue

                    if count_ > 999:
                        ERROR_MSG('_initSpecifiedEntities::RefreshNum too large', count_)
                        count_ = 999

                    self._maxCreateIndex.setdefault(id_, 0)
                    self._maxCreateIndex[id_] += count_
                    for i in utils.generateGameEntityId(id_, count_):
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

        _mapId = formula.getMapId(spaceNo)
        spaceConfig = utils.getDunStructureModuleData(_mapId)
        datas = spaceConfig.get('TimerEntities', {})
        for id_, data in datas.items():
            className = data.get('ClassName', '')
            entityID = data.get('EntityID', 0)
            if className not in ('Monster',):
                WARNING_MSG('loadTimerEntities::className error, ', className)
                continue

            id_ = int(id_)
            _d = data.get('Props', {})
            refreshTimedID = _d.get('RefreshTimedID', 0)
            if not refreshTimedID:
                WARNING_MSG('loadTimerEntities::refreshTimedID error, ', refreshTimedID)
                continue

            if not _d.get('IsOpen', True):
                WARNING_MSG('loadTimerEntities::Skip not isOpen Monster', id_)
                continue
            count_ = int(_d.get('RefreshNum', 1))

            if not count_:
                WARNING_MSG("loadTimerEntities::RefreshNum not exist",spaceNo)
                continue

            if count_ > 999:
                WARNING_MSG('loadTimerEntities::RefreshNum too large', count_)
                count_ = 999

            refreshData = (id_, gameconst.EntityType.MONSTER, entityID, count_)
            readyTimerEntitiesMap.setdefault(refreshTimedID, []).append(refreshData)
            DEBUG_MSG("loadTimerEntities", spaceNo, id_, refreshTimedID, refreshData)
