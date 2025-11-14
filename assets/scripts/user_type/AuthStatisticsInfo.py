
# coding: utf-8

import userType
import dataUtils
import utils
import gameconst
import itemData_itemData as ID_IDD
import ActTimesInfo


class AuthStatisticsVal(userType.UserSoleType):
    '''AUTH_STATISTICS_DATA_INFO'''
    def __init__(self, oldLevel=0, oldMoney=0, otherGbId=0, authExpire=0,
                 oldScore=0, itemUniqueIds=(), actTimes=(), dailyUseMoney=0,
                 oldExp=0.0, items=(), hostOffline=0, authLogin=0, oldCoin=0,
                 oldDarkIron=0, oldGeniusQi=0):
        self.oldLevel = oldLevel
        self.oldMoney = oldMoney
        self.oldCoin = oldCoin
        self.oldDarkIron = oldDarkIron
        self.oldGeniusQi = oldGeniusQi
        self.otherGbId = otherGbId
        self.authExpire = authExpire
        self.oldScore = oldScore
        # 不可堆叠道具用唯一id确认
        self.itemUniqueIds = list(itemUniqueIds)
        self.actTimesDic = {i.actId: i for i in actTimes}
        self.dailyUseMoney = dailyUseMoney
        self.oldExp = oldExp
        self.hostOffline = hostOffline
        self.authLogin = authLogin

        # 可堆叠道具用这个
        self.itemsDic = {i['itemId']: i['itemNum'] for i in items}

    def addItemByAward(self, awardVal):
        for itemId, num in awardVal.itemDataIter():
            _itemData = ID_IDD.datas.get(itemId)
            if not _itemData:
                continue

            if _itemData['quality'] < gameconst.ItemQuality.ORANGE:
                continue

            self.itemsDic[itemId] = self.itemsDic.get(itemId, 0) + num

        for it in awardVal.itemObjIter():
            _itemData = dataUtils.getCommItemData(it.itemId)
            if not _itemData:
                continue

            if _itemData['quality'] < gameconst.ItemQuality.ORANGE:
                continue

            if it.uniqueId not in self.itemUniqueIds:
                self.itemUniqueIds.append(it.uniqueId)

    def doModifyAuthExpire(self, authExpire):
        self.authExpire = authExpire

    def reset(self):
        if not self.otherGbId:
            return False

        self.authExpire = 0
        self.otherGbId = 0
        return True

    def onAuthLogin(self):
        self.authLogin = utils.getNow()

    def saveOnOffline(self, owner):
        self.oldLevel = owner.getAvatarLevel()
        self.oldMoney = owner.money
        self.oldCoin = owner.coin
        self.oldDarkIron = owner.darkIron
        self.oldGeniusQi = owner.geniusQi
        self.oldScore = owner.getTotalScore()
        self.itemUniqueIds = []
        self.actTimesDic = {}
        self.hostOffline = utils.getNow()

    def addUseMoney(self, delta):
        self.dailyUseMoney += delta

    def addActTimes(self, actId):
        if actId not in self.actTimesDic:
            self.actTimesDic[actId] = ActTimesInfo.ActTimesVal(actId)

        self.actTimesDic[actId].addTimes()

    def toAuthStatisticsSavedDict(self):
        return {
            'oldLevel': self.oldLevel,
            'oldMoney': self.oldMoney,
            'otherGbId': self.otherGbId,
            'authExpire': self.authExpire,
            'oldScore': self.oldScore,
            'itemUniqueIds': self.itemUniqueIds,
            'actTimes': list(self.actTimesDic.values()),
            'dailyUseMoney': self.dailyUseMoney,
            'oldExp': self.oldExp,
            'items': [{'itemId': k, 'itemNum': v} for k, v in self.itemsDic.items()],
            'hostOffline': self.hostOffline,
            'authLogin': self.authLogin,
            'oldCoin': self.oldCoin,
            'oldDarkIron': self.oldDarkIron,
            'oldGeniusQi': self.oldGeniusQi
        }


class AuthStatisticsInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AuthStatisticsVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAuthStatisticsSavedDict()

    def isSameType(self, obj):
        return type(obj) is AuthStatisticsVal


AuthStatisticsInstance = AuthStatisticsInfo()

