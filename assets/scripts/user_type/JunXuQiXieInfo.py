# coding: utf-8
from KBEDebug import *

import userType
import guildWarEquipment_warEquipmentUpgrate as GWE_WEUD


class JunXuQiXieVal(userType.UserSingleType):
    '''JUN_XU_QI_XIE_DATA_INFO'''
    def __init__(self, level=0, exp=0, qixieType=0):
        self.level = level
        self.exp = exp
        self.qixieType = qixieType

    def getCostCoin(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        return GWE_WEUD.datas[_id]['upgradeCoinCost']
    
    def addExp(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        self.exp += GWE_WEUD.datas[_id]['assistExp']
        if self.exp > GWE_WEUD.datas[_id]['upgradeExp']:
            LOG_WARN('JunXuQiXieVal::addExp: exp > upgradeExp', self.exp, GWE_WEUD.datas[_id]['upgradeExp'])
            self.exp = GWE_WEUD.datas[_id]['upgradeExp']

    def needJunxuLevel(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        return GWE_WEUD.datas[_id]['buildingLvReq']
    
    def upgradeFundCost(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        return GWE_WEUD.datas[_id]['upgradeCost']
    
    def isExpSufficient(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        return self.exp >= GWE_WEUD.datas[_id]['upgradeExp']

    def upgrade(self):
        _id = GWE_WEUD.typeLevelDic[self.qixieType][self.level]
        self.exp -= GWE_WEUD.datas[_id]['upgradeExp']
        self.level += 1

    def toJunXuQiXieSavedDict(self):
        return {
            'level': self.level,
            'exp': self.exp,
            'qixieType': self.qixieType,
        }
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, JunXuQiXieVal):
            return False

        return self.level == value.level and \
                self.exp == value.exp


class JunXuQiXieInfo(object):
    def createObjFromDict(self, dataDict):
        obj = JunXuQiXieVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toJunXuQiXieSavedDict()

    def isSameType(self, obj):
        return type(obj) is JunXuQiXieVal


JunXuQiXieInstance = JunXuQiXieInfo()

