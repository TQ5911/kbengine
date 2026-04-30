# coding: utf-8
import KBEngine
from KBEDebug import *

import userType


class HolidayPayInfo(userType.UserSingleType):
    def __init__(self):
        # key:creditID value:list[holidayID, gainTimes]
        self.creditDic = {}

    def __repr__(self):
        return self.creditDic.__repr__()

    # pickler
    def fromData(self, dataDic):
        for item in dataDic['holidayPayList']:
            self.creditDic.setdefault(item['creditID'], [0, 0])
            self.creditDic[item['creditID']][0] = item['holidayID']
            self.creditDic[item['creditID']][1] = item['gainTimes']
        return self

    # pickler
    def toData(self):
        _ = []
        for creditID, (holidayID, gainTimes) in self.creditDic.items():
            _.append({
                'holidayID': holidayID,
                'creditID': creditID,
                'gainTimes': gainTimes
            })
        return {'holidayPayList': _}

    def clearConfig(self, holidayID, gifts):
        for creditID in gifts:
            if creditID in self.creditDic and self.creditDic[creditID][0] == holidayID:
                del self.creditDic[creditID]

    def insertConfig(self, holidayID, gifts):
        for creditID in gifts:
            if creditID in self.creditDic: continue
            self.creditDic[creditID] = [holidayID, 0]

    def makeClientData(self, creditID=0):
        if not creditID:
            _ = []
            for creditID, (holidayID, gainTimes) in self.creditDic.items():
                if gainTimes > 0:
                    _.append({
                        'creditID': creditID,
                        'holidayID': holidayID,
                        'gainTimes': gainTimes,
                    })
            return _
        elif creditID in self.creditDic:
            return {
                'creditID': creditID,
                'holidayID': self.creditDic[creditID][0],
                'gainTimes': self.creditDic[creditID][1],
            }

        return None

    def holidayID(self, creditID):
        if creditID in self.creditDic:
            return self.creditDic[creditID][0]
        return 0

    def gainTimes(self, creditID):
        if creditID in self.creditDic:
            return self.creditDic[creditID][1]
        return 0

    def paySuccess(self, creditID):
        if creditID in self.creditDic:
            self.creditDic[creditID][1] += 1

class HolidayPayInfoPickler(object):
    def createObjFromDict(self, dataDic):
        return HolidayPayInfo().fromData(dataDic)

    def getDictFromObj(self, obj:HolidayPayInfo):
        return obj.toData()

    def isSameType(self, obj):
        return isinstance(obj, HolidayPayInfo)

inst = HolidayPayInfoPickler()