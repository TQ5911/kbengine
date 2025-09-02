# -*- coding: utf-8 -*-
import formula
from KBEDebug import *
import gametimer
import random
import gameconst
import utils
import const_const
import gameengine
import math
import gameconfig


import Monster as _Monster
import MonsterGrp as _MonsterGrp
import Teleporter as _Teleporter
import CityBattleTeleporter as _CityBattleTeleporter
import Creation as _Creation
import Npc as _Npc
# import CNpc as _CNpc
import Collection as _Collection

import NPC_NPC as NPC_D
import creep_base as CB
import NPC_Pick as NPD
import BalancedObjectGenerator


class IEntityLoaderInBase(object):
    def __init__(self):
        self._maxCreateIndex = {}

    def loadGroupEntities(self, spaceNo, entityIDs, readyEntitiesList, info):
        if not entityIDs:
            return

        loopNum = len(entityIDs)
        tmp_list, _ = entityIDs.popitems(loopNum)

        if not tmp_list:
            return

        info["geIds"] = tmp_list
        for gameEntityId in tmp_list:
            gid, gct = utils.splitGameEntityId(gameEntityId)

            spaceConfig = utils.getDunStructureModuleData(formula.getMapId(spaceNo))
            datas = spaceConfig.get('EntityRefreshPoint', {})
            if str(gid) not in datas:
                continue

            _mPrm = datas[str(gid)]
            className = info['className']
            bornPosition = (_mPrm['PosX'], _mPrm['PosY'], _mPrm['PosZ'])

            if 'Dir' in _mPrm:
                bornDirection = (0.0, 0.0, _mPrm['Dir'] * math.pi / 180)
            else:
                bornDirection = gameconst.DEFAULT_DIRECTION

            tmpProps = {'createIndex': gct}

            params = {
                'spaceNo': spaceNo,
                'spaceno': spaceNo,
                'gameEntityId': gameEntityId,
                'direction': bornDirection,
                'position': bornPosition,
                'isGroupRefresh': 1,
                'tmpProps': tmpProps,
                'refreshTime': info['refreshTime'],
            }

            if 'Props' in _mPrm:
                _pP = _mPrm['Props']

                if 'Radius' in _pP:
                    radius = params['bornRadius'] = float(_pP['Radius'])
                    tmpProps['createRadius'] = radius

            if className == _Collection.__name__:
                collectionId = info['eId']
                collectionType = NPD.datas.get(collectionId, {}).get('type', gameconst.CollectionType.NORMAL)
                dName = NPD.datas.get(collectionId, {}).get('name', "")
                params.update({
                    'name': dName,
                    'collectionId': collectionId,
                    'type': collectionType,
                })

            needCreateBase = 1
            data = (gameEntityId, spaceNo, className, needCreateBase, bornPosition, bornDirection, params, 0)
            DEBUG_MSG("IEntityLoader::loadGroupEntities for single ", spaceNo, className, gameEntityId)
            readyEntitiesList.append(data)

    def loadGroupEntitiesBatchly(self, spaceNo, entIter, batchNum, interval, isInit=False):
        DEBUG_MSG("IEntityLoader::loadGroupEntitiesBatchly-----------")
        for i in range(batchNum):
            (entId, _, clsName, needCreateBase, pos, direction, props, rGid) = next(entIter, (
            0, None, None, None, None, None, None, None))
            if not entId:
                INFO_MSG('IEntityLoader::loadGroupEntitiesBatchly finish loading all entities', spaceNo)
                if isInit:
                    self.onLoadGroupEntitiesEnd(spaceNo)
                return

            self.loadSingleEntity(spaceNo, clsName, needCreateBase, pos, direction, props)

        self._callback(interval, 'loadGroupEntitiesBatchly', (spaceNo, entIter, batchNum, interval, isInit),
                       gametimer.TIMER_TAG_LOAD_GROUP_ENTITIES_CALL_BACK)

    def onLoadGroupEntities(self, info):
        DEBUG_MSG("IEntityLoader::onLoadGroupEntities", info)
        self._onLoadGroupEntities(info)

    def _onLoadGroupEntities(self, info):
        spaceNo = info['spaceNo']
        id = info['id']
        count = info['cnt']

        entityIDs = self._initGroupEntities(spaceNo, id, count)
        readyEntitiesList = []
        self.loadGroupEntities(spaceNo, entityIDs, readyEntitiesList, info)
        self.loadGroupEntitiesBatchly(spaceNo, iter(readyEntitiesList),
                                    gameconst.LoadEntitySetting.BATCH_NUM,
                                    gameconst.LoadEntitySetting.BATCH_DELAY, True)

        DEBUG_MSG("IEntityLoader::_onLoadGroupEntities", info)
        gameengine.getGlobalBase('WorldRefreshEntityStub').onLoadGroupEntitiesAck(info)

    def _initGroupEntities(self, spaceNo, id, count):
        _mapId = formula.getMapId(spaceNo)
        self._maxCreateIndex.setdefault(id, 0)
        fromIdx = self._maxCreateIndex.get(id)
        DEBUG_MSG('IEntityLoader::_initGroupEntities spaceNo, id, count, fromIdx', spaceNo, id, count, fromIdx)
        def _iterGameGroupEntityId():
            spaceConfig = utils.getDunStructureModuleData(_mapId)
            ents = spaceConfig.get('EntityRefreshPoint', {})
            data = ents.get(str(id), None)
            if not data:
                WARNING_MSG('IEntityLoader::_initGroupEntities no data', id)
                return

            self._maxCreateIndex[id] += count
            for i in utils.generateGameEntityIdFrom(id, count, fromIdx):
                yield i

        _retList = BalancedObjectGenerator.BalancedObjectGenerator(_iterGameGroupEntityId())
        random.shuffle(_retList)
        DEBUG_MSG('IEntityLoader::_initGroupEntities _retList', _retList)
        return _retList

    def onLoadGroupEntitiesEnd(self, spaceNo):
        DEBUG_MSG("IEntityLoader::onLoadGroupEntitiesEnd ", spaceNo)

    def onRefreshGroupEntities(self, info):
        DEBUG_MSG("IEntityLoader::onRefreshGroupEntities", info)
        refreshTime = info.get('refreshTime', 1)
        entityIDs = info.get('geIds', None)
        if entityIDs and len(entityIDs) > 0:
            self._callback(refreshTime, '_onRefreshGroupEntities', (info,),
                       gametimer.TIMER_TAG_LOAD_GROUP_ENTITIES_CALL_BACK)
        else:
            self._callback(refreshTime, '_onLoadGroupEntities', (info,),
                       gametimer.TIMER_TAG_LOAD_GROUP_ENTITIES_CALL_BACK)

    def _onRefreshGroupEntities(self, info):
        DEBUG_MSG("IEntityLoader::_onRefreshGroupEntities", info, KBEngine.isShuttingDown())
        if KBEngine.isShuttingDown():
            return

        spaceNo = info['spaceNo']

        entityIDs = BalancedObjectGenerator.BalancedObjectGenerator(info["geIds"])
        readyEntitiesList = []
        self.loadGroupEntities(spaceNo, entityIDs, readyEntitiesList, info)
        self.loadGroupEntitiesBatchly(spaceNo, iter(readyEntitiesList),
                                    gameconst.LoadEntitySetting.BATCH_NUM,
                                    gameconst.LoadEntitySetting.BATCH_DELAY, True)

        DEBUG_MSG("IEntityLoader::_onRefreshGroupEntities", info)
        gameengine.getGlobalBase('WorldRefreshEntityStub').onLoadGroupEntitiesAck(info)
