# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

import gameconst
import gametimer
import utils
import formula
import dataUtils
import gamelog

class IBoxGroupRefresh(object):
    def __init__(self):
        pass

    def addBoxGroupEntity(self, ent):
        if not (ent.IsMonster or ent.IsCollection):
            return
        chestGroupID = utils.getEntityBoxGroupId(ent, self.spaceNo)
        if chestGroupID == 0:
            return
        
        entities = self.boxGroupEntities.get(chestGroupID, {})
        if ent.IsMonster:
            if entities.get('monsterIds') is None:
                entities['monsterIds'] = set()
            entities['monsterIds'].add(ent.id)
        elif ent.IsCollection:
            init = False
            if entities.get('collectIds') is None:
                entities['collectIds'] = set()
                init = True
            entities['collectIds'].add(ent.id)
            ent.groupLock = True
            
            if len(entities['collectIds']) == 1 and not init:
                # 刷新怪物
                self.addTimerCB(2, 'doRefreshMonster', (chestGroupID,), gametimer.TIMER_TAG_BOX_GROUP_REFRESH_MONSTER)

        self.boxGroupEntities[chestGroupID] = entities
        DEBUG_MSG('addBoxGroupEntity: spaceNo={}, chestGroupID={}, entityId={}, isMonster={}, isCollection={}'.format(self.spaceNo, chestGroupID, ent.id, ent.IsMonster, ent.IsCollection))

    def removeBoxGroupEntity(self, ent):
        chestGroupID = utils.getEntityBoxGroupId(ent, self.spaceNo)
        if chestGroupID == 0:
            return

        entities = self.boxGroupEntities[chestGroupID]
        if not entities:
            return
        if ent.IsMonster and ent.id in entities.get('monsterIds', set()):
            entities['monsterIds'].remove(ent.id)
            if len(entities['monsterIds']) == 0:
                # 解锁所有组宝箱
                for collectId in entities['collectIds']:
                    collectEnt = self.getEntityById(collectId)
                    if collectEnt:
                        collectEnt.groupLock = False
        elif ent.IsCollection:
            entities['collectIds'].remove(ent.id)

    def boxGroupHasUnlock(self, chestGroupID):
        entities = self.boxGroupEntities.get(chestGroupID, {})
        if not entities:
            return False
        collectIds = entities.get('collectIds', set())
        for collectId in collectIds:
            collectEnt = self.getEntityById(collectId)
            if collectEnt and collectEnt.groupLock:
                return False

        return True

    def addBoxGroupMonster(self, chestGroupID, entityId, monsterGroupId):
        monsters = self.boxGroupMonsters.get(chestGroupID, [])
        monsters.append((entityId, monsterGroupId))
        self.boxGroupMonsters[chestGroupID] = monsters
        DEBUG_MSG('addBoxGroupMonster: chestGroupID={}, entityId={}, monsterGroupId={}'.format(chestGroupID, entityId, monsterGroupId))

    def doRefreshMonster(self, chestGroupID):
        DEBUG_MSG('doRefreshMonster: chestGroupID={}'.format(chestGroupID))
        if KBEngine.isShuttingDown():
            return
        monsterInfo = self.boxGroupMonsters.get(chestGroupID, [])
        for (entityId, groupId) in monsterInfo:
            _entityProps = []
            utils.loadLineReadyEntities(self.spaceNo, [entityId], _entityProps, True)
            for _, _, _className, _, _pos, _dir, _params, _ in _entityProps:
                _params['spaceMgrId'] = self.id
                _params['monsterGroupId'] = groupId
                KBEngine.createEntity(_className, self.spaceID, _pos, _dir, _params)

        self.boxGroupMonsters.pop(chestGroupID, None)

