# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gameconst
import gametimer
import utils
import formula
import dataUtils
import gamelog

class BoxGroupTag(object):
    MONSTERS = 'monsterIds'
    COLLECTIONS = 'collectIds'
    INITED = 'inited'
    MAX_COLLECT_NUM = 'maxCollectNum'

class IBoxGroupRefresh(object):
    def __init__(self):
        pass

    def addBoxGroupEntity(self, ent):
        if not (ent.IsMonster or ent.IsCollection):
            return
        chestGroupID = utils.getEntityBoxGroupId(ent.gameEntityId, self.spaceNo)
        if chestGroupID == 0:
            return
        
        entities = self.boxGroupEntities.get(chestGroupID, {})
        if ent.IsMonster:
            if entities.get(BoxGroupTag.MONSTERS) is None:
                entities[BoxGroupTag.MONSTERS] = set()
            entities[BoxGroupTag.MONSTERS].add(ent.id)
        elif ent.IsCollection:
            if entities.get(BoxGroupTag.COLLECTIONS) is None:
                entities[BoxGroupTag.COLLECTIONS] = set()
            entities[BoxGroupTag.COLLECTIONS].add(ent.id)
            ent.groupLock = True

            if not entities.get(BoxGroupTag.INITED, False):
                if entities.get(BoxGroupTag.MAX_COLLECT_NUM) is None:
                    entities[BoxGroupTag.MAX_COLLECT_NUM] = 0
                entities[BoxGroupTag.MAX_COLLECT_NUM] += 1
            elif len(entities[BoxGroupTag.COLLECTIONS]) == entities[BoxGroupTag.MAX_COLLECT_NUM]:
                # 刷新怪物
                self.doRefreshMonster(chestGroupID)

        self.boxGroupEntities[chestGroupID] = entities
        LOG_DBG('addBoxGroupEntity: spaceNo={}, chestGroupID={}, entityId={}, isMonster={}, isCollection={}'.format(self.spaceNo, chestGroupID, ent.id, ent.IsMonster, ent.IsCollection))

    def removeBoxGroupEntity(self, ent):
        chestGroupID = utils.getEntityBoxGroupId(ent.gameEntityId, self.spaceNo)
        if chestGroupID == 0:
            return

        entities = self.boxGroupEntities[chestGroupID]
        if not entities:
            return
        entities[BoxGroupTag.INITED] = True
        if ent.IsMonster and ent.id in entities.get(BoxGroupTag.MONSTERS, set()):
            entities[BoxGroupTag.MONSTERS].remove(ent.id)
            if len(entities[BoxGroupTag.MONSTERS]) == 0:
                # 解锁所有组宝箱
                for collectId in entities[BoxGroupTag.COLLECTIONS]:
                    collectEnt = self.getEntityById(collectId)
                    if collectEnt:
                        collectEnt.groupLock = False
        elif ent.IsCollection:
            entities[BoxGroupTag.COLLECTIONS].remove(ent.id)

    def boxGroupHasUnlock(self, chestGroupID):
        entities = self.boxGroupEntities.get(chestGroupID, {})
        if not entities:
            return False
        collectIds = entities.get(BoxGroupTag.COLLECTIONS, set())
        for collectId in collectIds:
            collectEnt = self.getEntityById(collectId)
            if collectEnt and collectEnt.groupLock:
                return False

        return True

    def addBoxGroupMonster(self, chestGroupID, entityId, monsterGroupId):
        monsters = self.boxGroupMonsters.get(chestGroupID, [])
        monsters.append((entityId, monsterGroupId))
        self.boxGroupMonsters[chestGroupID] = monsters
        LOG_DBG('addBoxGroupMonster: chestGroupID={}, entityId={}, monsterGroupId={}'.format(chestGroupID, entityId, monsterGroupId))

    def doRefreshMonster(self, chestGroupID):
        LOG_DBG('doRefreshMonster: chestGroupID={}'.format(chestGroupID))
        if KBEngine.isShuttingDown():
            return
        monsterInfo = self.boxGroupMonsters.get(chestGroupID, [])
        if not monsterInfo:
            return
        for (entityId, groupId) in monsterInfo:
            _entityProps = []
            utils.loadLineReadyEntities(self.spaceNo, [entityId], _entityProps, True)
            for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
                _params['spaceMgrId'] = self.id
                _params['monsterGroupId'] = groupId
                KBEngine.createEntity(_className, self.spaceID, _pos, _dir, _params)

        self.boxGroupMonsters.pop(chestGroupID, None)

    def addBoxGroupCollect(self, className, pos, dir, params):
        chestGroupID = utils.getEntityBoxGroupId(params['gameEntityId'], self.spaceNo)
        if chestGroupID == 0:
            return
        collects = self.boxGroupCollects.get(chestGroupID, [])
        collects.append((className, pos, dir, params))
        self.boxGroupCollects[chestGroupID] = collects
        LOG_DBG('addBoxGroupCollect: chestGroupID={}, className={}, pos={}, dir={}, params={}'.format(chestGroupID, className, pos, dir, params))

        entities = self.boxGroupEntities.get(chestGroupID, {})
        maxCollectNum = entities.get(BoxGroupTag.MAX_COLLECT_NUM, 0)
        if maxCollectNum > 0 and len(collects) == maxCollectNum:
            # 刷新宝箱
            self.doRefreshCollect(chestGroupID)

    def doRefreshCollect(self, chestGroupID):
        LOG_DBG('doRefreshCollect: chestGroupID={}'.format(chestGroupID))
        if KBEngine.isShuttingDown():
            return
        collectInfo = self.boxGroupCollects.get(chestGroupID, [])
        if not collectInfo:
            return
        for (className, pos, dir, params) in collectInfo:
            KBEngine.createEntity(className, self.spaceID, pos, dir, params)

        self.boxGroupCollects.pop(chestGroupID, None)

