# coding: utf-8
import KBEngine
from KBEDebug import *

import MonsterGrp


class IMonsterGrp(object):
    def isMonsterInGroup(self):
        return True if self.monsterGroupId else False

    @property
    def monsterGroup(self):
        return KBEngine.entities.get(self.monsterGroupId)

    def addInMonsterGroup(self, groupId):
        _g = KBEngine.entities.get(groupId)

        if _g and isinstance(_g, MonsterGrp.MonsterGrp):
            self.monsterGroupId = groupId
            _g.addId(self.id)

    def rmFromMonsterGroup(self):
        if not self.monsterGroupId:
            return

        _monsterGrp = self.monsterGroup

        if not _monsterGrp:
            return

        _monsterGrp.removeId(self.id)

    def selfSync(self, funcName, args=None, kwargs=None):
        if self.monsterGroup:
            return self.monsterGroup.sync(self.id, funcName, args, kwargs)

    def syncIncHateInGroupCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.syncIncHateInGroupCB(*args, **kwargs)

    def syncTelBackCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.syncTelBackCB(*args, **kwargs)

    def luckyGroupStandCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.luckyGroupStandCB(*args, **kwargs)

