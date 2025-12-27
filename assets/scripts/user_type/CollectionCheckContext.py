class CollectionCheckType(object):
    WONDER_LAND = 1
    SIEGE_WAR = 2

class CollectionCheckWonderLand(object):
    CHECK_TYPE = CollectionCheckType.WONDER_LAND
    def __init__(self, itemId, itemNum, bossId, collectionId):
        self.itemId = itemId
        self.itemNum = itemNum
        self.bossId = bossId
        self.collectionId = collectionId

    def checkCell(self, avatarCell):
        return avatarCell.checkSummonWonderLandBossCell(self.bossId)

    def checkBase(self, avatarBase):
        return avatarBase.checkSummonWonderLandBossBase(self.itemId, self.itemNum)

class CollectionCheckSiegeWar(object):
    CHECK_TYPE = CollectionCheckType.SIEGE_WAR
    def __init__(self, collectionId):
        self.collectionId = collectionId

    def checkCell(self, avatarCell):
        return avatarCell.siegeWarPrecheckCollection(self.collectionId)

    def checkBase(self, avatarBase):
        return True
