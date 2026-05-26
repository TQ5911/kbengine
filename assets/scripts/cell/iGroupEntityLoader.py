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


class IGroupEntityLoader(object):
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
            gid, gct = utils.splitFromGameEntityId(gameEntityId)

            spaceConfig = utils.getDunStructModData(formula.fetchMapId(spaceNo))
            datas = spaceConfig.get('EntityRefreshPoint', {})
            if str(gid) not in datas:
                continue

            _mPrm = datas[str(gid)]
            className = info['className']
            _bornPosition = (_mPrm['PosX'], _mPrm['PosY'], _mPrm['PosZ'])

            if 'Dir' in _mPrm:
                _bornDirection = (0.0, 0.0, _mPrm['Dir'] * math.pi / 180)
            else:
                _bornDirection = gameconst.DEFAULT_DIRECTION

            tmpProps = {'createIndex': gct}

            params = {
                'spaceNo': spaceNo,
                'spaceno': spaceNo,
                'gameEntityId': gameEntityId,
                'direction': _bornDirection,
                'position': _bornPosition,
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

            needCreateBase = 0
            data = (gameEntityId, spaceNo, className, needCreateBase, _bornPosition, _bornDirection, params, 0)
            LOG_DBG("IGroupEntityLoader::loadGroupEntities for single ", spaceNo, className, gameEntityId)
            readyEntitiesList.append(data)

    def loadGroupEntitiesBatchly(self, spaceNo, entIter, batchNum, interval, isInit=False, spaceMgrId=0):
        LOG_DBG("loadGroupEntitiesBatchly-----------", batchNum, interval)
        _iter = self.loadGroupEntitiesAsync(entIter, isInit, spaceMgrId)
        self.batchlyCall(_iter, batchNum, interval)

    def loadGroupEntitiesAsync(self, entIter, isInit, spaceMgrId=0):
        while True:
            _ret = next(entIter, None)
            if _ret is None:
                break

            (_, _, clsName, _, pos, direction, props, _) = _ret

            if spaceMgrId:
                props['spaceMgrId'] = spaceMgrId

            while True:
                try:
                    self.createCellLocally(clsName, pos, direction, props)
                    yield utils.emptyFunc
                    break
                except SystemError as e:
                    LOG_WARN('IGroupEntityLoader::loadGroupEntitiesAsync SystemError', e)
                    yield utils.emptyFunc

        if isInit:
            self.onLoadGroupEntitiesEnd()

        yield utils.emptyFunc

    def onLoadGroupEntities(self, info, spaceMgrId):
        LOG_DBG("IGroupEntityLoader::onLoadGroupEntities", info, spaceMgrId)
        self._onLoadGroupEntities(info, spaceMgrId)

    def _onLoadGroupEntities(self, info, spaceMgrId):
        spaceNo = info['spaceNo']
        id = info['id']
        count = info['cnt']

        entityIDs = self._initGroupEntities(spaceNo, id, count)
        readyEntitiesList = []
        self.loadGroupEntities(spaceNo, entityIDs, readyEntitiesList, info)
        self.loadGroupEntitiesBatchly(spaceNo, iter(readyEntitiesList),
                                    gameconfig.entityLoadSpeed(),
                                    gameconst.LoadEntitySetting.BATCH_DELAY, True, spaceMgrId)

        LOG_DBG("IGroupEntityLoader::_onLoadGroupEntities", info, spaceMgrId)
        gameengine.getGlobalBase('WorldRefreshEntityStub').onLoadGroupEntitiesAck(info)

    def _initGroupEntities(self, spaceNo, id, count):
        _mapId = formula.fetchMapId(spaceNo)
        self._maxCreateIndex.setdefault(id, 0)
        fromIdx = self._maxCreateIndex.get(id)
        LOG_DBG('IGroupEntityLoader::_initGroupEntities spaceNo, id, count, fromIdx', spaceNo, id, count, fromIdx)
        def _iterGameGroupEntityId():
            spaceConfig = utils.getDunStructModData(_mapId)
            ents = spaceConfig.get('EntityRefreshPoint', {})
            data = ents.get(str(id), None)
            if not data:
                LOG_WARN('IGroupEntityLoader::_initGroupEntities no data', id)
                return

            self._maxCreateIndex[id] += count
            for i in utils.genGameEntityIdFrom(id, count, fromIdx):
                yield i

        _retList = BalancedObjectGenerator.BalancedObjectGenerator(_iterGameGroupEntityId())
        random.shuffle(_retList)
        LOG_DBG('IGroupEntityLoader::_initGroupEntities _retList', _retList)
        return _retList

    def onLoadGroupEntitiesEnd(self):
        LOG_DBG("IGroupEntityLoader::onLoadGroupEntitiesEnd ")

    def onRefreshGroupEntities(self, info, spaceMgrId):
        LOG_DBG("IGroupEntityLoader::onRefreshGroupEntities", info, spaceMgrId)
        refreshTime = info.get('refreshTime', 1)
        entityIDs = info.get('geIds', None)
        if entityIDs and len(entityIDs) > 0:
            self._onRefreshGroupEntities(info, spaceMgrId)
        else:
            self._onLoadGroupEntities(info, spaceMgrId)

    def _onRefreshGroupEntities(self, info, spaceMgrId):
        LOG_DBG("IGroupEntityLoader::_onRefreshGroupEntities", info, spaceMgrId, KBEngine.isShuttingDown())
        if KBEngine.isShuttingDown():
            return

        spaceNo = info['spaceNo']

        entityIDs = BalancedObjectGenerator.BalancedObjectGenerator(info["geIds"])
        readyEntitiesList = []
        self.loadGroupEntities(spaceNo, entityIDs, readyEntitiesList, info)
        self.loadGroupEntitiesBatchly(spaceNo, iter(readyEntitiesList),
                                    gameconfig.entityLoadSpeed(),
                                    gameconst.LoadEntitySetting.BATCH_DELAY, False, spaceMgrId)

        LOG_DBG("IGroupEntityLoader::_onRefreshGroupEntities", info, spaceMgrId)
        gameengine.getGlobalBase('WorldRefreshEntityStub').onLoadGroupEntitiesAck(info)

    def onDestroyGroupEntities(self, info, spaceMgrId):
        LOG_DBG("IGroupEntityLoader::onDestroyGroupEntities", info, spaceMgrId)
        if not spaceMgrId:
            return
        spaceMgr = KBEngine.entities.get(spaceMgrId)
        if not spaceMgr:
            return

        spaceMgr.onDestroyGroupEntities(info)
