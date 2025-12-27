# coding: utf-8
import KBEngine
from KBEDebug import *

import MonsterGrp


class IMonsterGrp(object):
    @property
    def monsterGroup(self):
        return KBEngine.entities.get(self.monsterGroupId)

    def isMonsterInGroup(self):
        return True if self.monsterGroupId else False

    def addInMonsterGroup(self, groupId):
        g = KBEngine.entities.get(groupId)

        if g and isinstance(g, MonsterGrp.MonsterGrp):
            self.monsterGroupId = groupId
            g.addId(self.id)

    def rmFromMonsterGroup(self):
        if not self.monsterGroupId:
            return

        monsterGrp = self.monsterGroup

        if not monsterGrp:
            return

        monsterGrp.removeId(self.id)
        #self.monsterGroupId = 0

    def selfSync(self, funcName, args=None, kwargs=None):
        if self.monsterGroup:
            return self.monsterGroup.sync(self.id, funcName, args, kwargs)

    def syncIncreaseHateInGroupCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.syncIncreaseHateInGroupCB(*args, **kwargs)

    def syncTelBackCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.syncTelBackCB(*args, **kwargs)