
# coding: utf-8

import userType
import utils
import gameconst
import const_const as C_CD


class HateCounterVal(userType.UserSingleType):
    '''HATE_COUNTER_DATA_INFO'''
    def __init__(self, cntList):
        # cntList = [ [time, delta], [time, delta],... ]
        if cntList is None:
            self.cntList = []
        else:
            self.cntList = cntList

    def addHateCnt(self, _hateType):
        _now = utils.curTS()
        if _hateType == gameconst.HATE_CNT_TYPE_MOVE:
            _delta = C_CD.datas['monsterPathingWeight']['value']
        else:
            _delta = C_CD.datas['monsterCombatingWeight']['value']

        if not self.cntList:
            self.cntList.append([_now, _delta])
            return

        if self.cntList[-1][0] == _now:
            self.cntList[-1][1] += _delta
        else:
            self.cntList.append([_now, _delta])

        _minTime = _now - C_CD.datas['monsterCombatPathingTime']['value']
        while self.cntList and self.cntList[0][0] <= _minTime:
            self.cntList.pop(0)

    def getHateCntVal(self):
        _now = utils.curTS()
        _minTime = _now - C_CD.datas['monsterCombatPathingTime']['value']
        _ret = 0
        for _t, _d in reversed(self.cntList):
            if _t < _minTime:
                break

            _ret += _d

        return _ret

    def toHateCounterSavedDict(self):
        return {
            'cntList': self.cntList
        }


class HateCounterInfo(object):
    def createObjFromDict(self, dataDict):
        obj = HateCounterVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toHateCounterSavedDict()

    def isSameType(self, obj):
        return type(obj) is HateCounterVal


HateCounterInstance = HateCounterInfo()

