#coding=utf-8

import KBEngine


class ICollectionBossForMgr(object):
    def __init__(self):
        self.collToBoss = {}

    def checkHasBoss(self, bossId):
        if self.tagEntities.get(str(bossId)):
            return True
        return False

    def setCollToBoss(self, collectionId, bossId):
        self.collToBoss[collectionId] = bossId
        self.notifyPlayerCurBossInfo()

    def notifyPlayerCurBossInfo(self):
        _bossList = list(self.collToBoss.values())
        self.syncPlayer(lambda playerEnt: playerEnt.client.onWonderLandBossInfo(_bossList))

    def onPlayerRelogin(self, box, playerGbId):
        super().onPlayerRelogin(box, playerGbId)
        _bossList = list(self.collToBoss.values())
        box.client.onWonderLandBossInfo(_bossList)

    def removeCollToBoss(self, bossId):
        for collectionId, _bossId in self.collToBoss.items():
            if _bossId == bossId:
                self.collToBoss.pop(collectionId)
                self.notifyPlayerCurBossInfo()
                break

    def removeEntById(self, entId):
        super().removeEntById(entId)
        ent = KBEngine.entities.get(entId)
        if ent and ent.IsMonster:
            self.removeCollToBoss(ent.monsterId)

