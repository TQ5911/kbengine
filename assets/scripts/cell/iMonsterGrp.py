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
        if self.monsterGroupId:
            return self.monsterGroup.sync(self.id, funcName, args, kwargs)

    # -----------------------
    # callback
    # -----------------------
    #
    # MGR Method and callback example:
    #
    # def sayHello(self, synced=False):
    #     WARNING_MSG('Hello my friend!')
    #
    #     if synced:
    #         self.selfSync('sayHelloCB', (self.id, ))
    #
    # def sayHelloCB(self, fromId):
    #     INFO_MSG('Hello my friend, I synced this msg from: {}'.format(
    #             fromId))

    def syncIncreaseHateInGroupCB(self, *args, **kwargs):
        if self.aiController:
            self.aiController.syncIncreaseHateInGroupCB(*args, **kwargs)
