import userType
import utils
import gameconst
import gamePlay_set as GP_SD


class DeathPenaltyVal(userType.UserSingleType):
    def __init__(self, exp=0, expireTime=0):
        self.exp = exp
        self.expireTime = expireTime

    def toStreamSavedDic(self):
        return {"exp": self.exp, "expireTime": self.expireTime}


class DeathPenalty(userType.UserSingleType):
    def __init__(self, deathPenaltyList=()):
        self.deathPenaltyList = []
        for _data in deathPenaltyList:
            self.deathPenaltyList.append(DeathPenaltyVal(**_data))

    def _clear(self, now):
        _retList = []
        while len(self.deathPenaltyList):
            _dpVal = self.deathPenaltyList[-1]
            if _dpVal.expireTime < now or len(self.deathPenaltyList) > GP_SD.datas['maxExpRecSlots']['value']:
                self.deathPenaltyList.pop()
                _retList.append({"expireTime": _dpVal.expireTime, "exp": 0})
            else:
                break

        return _retList

    def getDeathPenaltyExp(self, expireTime):
        for _dpVal in self.deathPenaltyList:
            if _dpVal.expireTime == expireTime:
                return _dpVal.exp

        return 0

    def removeDeathPenaltyVal(self, expireTime):
        for _idx, _dpVal in enumerate(self.deathPenaltyList):
            if _dpVal.expireTime == expireTime:
                self.deathPenaltyList.pop(_idx)
                return True

        return False

    def _isInExpire(self, expireTime):
        for _dpVal in self.deathPenaltyList:
            if _dpVal.expireTime == expireTime:
                return True

        return False

    def toClientDataAll(self):
        now = utils.curTS()
        self._clear(now)
        return [x.toStreamSavedDic() for x in self.deathPenaltyList]

    def addDeathPenaltyExp(self, exp):
        _now = utils.curTS()
        _expireTime = _now + GP_SD.datas['maxExpRecTime']['value']
        while self._isInExpire(_expireTime):
            _expireTime += 1

        _newVal = DeathPenaltyVal(exp, _expireTime)
        self.deathPenaltyList.insert(0, _newVal)

        _retList = []
        _retList.append(_newVal.toStreamSavedDic())

        _retList.extend(self._clear(_now))

        return _retList

    def toStreamSaveDict(self):
        deathPenaltyList = []
        for _data in self.deathPenaltyList:
            deathPenaltyList.append(_data.toStreamSavedDic())
        return {"deathPenaltyList": deathPenaltyList}


class DeathPenaltyInfo(object):
    def createObjFromDict(self, dataDict):
        obj = DeathPenalty(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSaveDict()

    def isSameType(self, obj):
        return type(obj) is DeathPenalty


deathPenaltyInstance = DeathPenaltyInfo()

