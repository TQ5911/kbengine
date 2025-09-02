import KBEngine, utils, sMath
from KBEDebug import *
import iCell, iTimer, iGameEntity, iFubenSpace
import gametimer
import formula
import cityBattle_config as CBC
import random
import Math, math

class CoreAreaFlag(iCell.ICell, iTimer.ITimer, iGameEntity.IGameEntity, iFubenSpace.IFubenSpace):

    def __init__(self):
        super(CoreAreaFlag, self).__init__()
        self.coreAreaCenterX = CBC.datas['cityBattle_coreArea']['value'][0][0]
        self.coreAreaCenterZ = CBC.datas['cityBattle_coreArea']['value'][0][1]
        self.coreAreaRadius = CBC.datas['cityBattle_coreArea']['value'][1]
        self.inAreaPlayerDict = {1: {}, 2: {}}
        self.deadPlayerDict = {1: {}, 2: {}}
        self.siegeWarCamp = 0
        self.trapId = 0
        DEBUG_MSG("CoreAreaFlag init", self.coreAreaCenterX, self.coreAreaCenterZ, self.coreAreaRadius)
        
        self._callback(0.1, '_addTrap', (), gametimer.TIMER_TAG_ADD_TRAP)

    def onTimer(self, tid, userData):
        self._onTimer(tid, userData)
        if utils.isBelongTimerTag(userData):
            self._onTimerCallback(tid)
        else:
            super(CoreAreaFlag, self).onTimer(tid, userData)

    def onEnterTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if entity.IsAvatar:
            self.inAreaPlayerDict[entity.siegeWarCamp][entity.id] = entity
            DEBUG_MSG("CoreAreaFlag onEnterTrap", entity.id, entity.siegeWarCamp)
            self.recalculatecoreAreaNum()

    def onLeaveTrap(self, entity, rangeXZ, rangeY, controllerId, userArg):
        if entity.IsAvatar:
            self.inAreaPlayerDict[entity.siegeWarCamp].pop(entity.id)
            if entity.id in self.deadPlayerDict[entity.siegeWarCamp]:
                self.deadPlayerDict[entity.siegeWarCamp].pop(entity.id)
            DEBUG_MSG("CoreAreaFlag onLeaveTrap", entity.id, entity.siegeWarCamp)
            self.recalculatecoreAreaNum()

    #在圈内死亡
    def onPlayerDead(self, entity):
        if entity.id in self.inAreaPlayerDict[entity.siegeWarCamp]:
            self.deadPlayerDict[entity.siegeWarCamp][entity.id] = entity
            DEBUG_MSG("CoreAreaFlag onPlayerDead", entity.id, entity.siegeWarCamp)
            self.recalculatecoreAreaNum()

    def onPlayerRelive(self, entity):
        if entity.id in self.deadPlayerDict[entity.siegeWarCamp]:
            self.deadPlayerDict[entity.siegeWarCamp].pop(entity.id)
            DEBUG_MSG("CoreAreaFlag onPlayerRelive", entity.id, entity.siegeWarCamp)
            self.recalculatecoreAreaNum()

    def recalculatecoreAreaNum(self):
        self.offenseNum = len(self.inAreaPlayerDict[1]) - len(self.deadPlayerDict[1])
        self.defenseNum = len(self.inAreaPlayerDict[2]) - len(self.deadPlayerDict[2])
        DEBUG_MSG("CoreAreaFlag recalculatecoreAreaNum", self.offenseNum, self.defenseNum)

    def _addTrap(self):
        DEBUG_MSG("CoreAreaFlag _addTrap")
        self.trapId = self.addProximity(self.coreAreaRadius, 0, 0)
        DEBUG_MSG("CoreAreaFlag trapId", self.trapId)

    def destroySelf(self):
        DEBUG_MSG("CoreAreaFlag destroySelf")
        if self.trapId > 0:
            self.cancelController(self.trapId)
            self.trapId = 0
        self.safeDestroy()