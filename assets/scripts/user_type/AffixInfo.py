# -*- coding: utf-8 -*-

import KBEngine

import dataUtils
from KBEDebug import *
import userType
import gameconst
import affix_affix as AFAFD
import math
import random
import gameengine


class Affix(userType.UserSoleType):
    def __init__(self, affixId, affixLv=1):
        self.afxId = affixId
        self.lv = max(affixLv, 1)
        self.affixVal = 0

    def toAffixValList(self):
        val = [self.afxId, self.lv, self.affixVal]
        return val

    def fromAffixValList(self, val):
        self.lv = val[1]
        self.affixVal = val[2]

    def toAfxClientDic(self):
        return {
            'affixId': self.afxId,
            'affixVal': self.affixVal,
        }

    def getAfxScore(self):
        afxData = AFAFD.datas.get(self.afxId)
        if not afxData:
            return 0
        score_data = afxData.get('score')
        prop = afxData.get('prop')
        if prop:
            propScore = int(dataUtils.getPropBaseScore(prop) * self.affixVal)
        else:
            propScore = 0
        return int(propScore + score_data)

class AffixAdjustType(object):
    AFFIX_ADJUST_EQUIP_DROP = 0
    AFFIX_ADJUST_EQUIP_WASH = 1


def genFixedAffix(iLevel, affixId, rate):
    affixData = AFAFD.datas.get(affixId)
    levelGap = affixData.get('levelGap', gameconst.EquipAttrConst.AFFIX_DEFAULT_LEVEL_GAP)
    affixLv = min(max(math.ceil(iLevel/levelGap), 1), affixData['maxLevel'])
    affixObj = Affix(affixId, affixLv=affixLv)

    affixValFloorList = affixData['floor'](affixLv)
    affixValCeilList = affixData['ceiling'](affixLv)
    if not affixValFloorList or not affixValCeilList:
        return

    affixVals = []
    for floorVal, ceilVal in zip(affixValFloorList, affixValCeilList):
        val = floorVal + (ceilVal - floorVal) * rate
        if isinstance(floorVal, int) and isinstance(ceilVal, int):
            val = int(val)
        else:
            val = round(val, 4)
        affixVals.append(val)
        break

    affixObj.affixVal = affixVals[0]

    return affixObj

def genRandomAffix(affixId, iLevel, val):
    affixData = AFAFD.datas.get(affixId)
    levelGap = affixData.get('levelGap', gameconst.EquipAttrConst.AFFIX_DEFAULT_LEVEL_GAP)
    affixLv = min(max(math.ceil(iLevel/levelGap), 1), affixData['maxLevel'])

    affixObj = Affix(affixId, affixLv=affixLv)
    affixObj.affixVal = val
    return affixObj

def genOneAffix(iLevel, affixId):
    affixData = AFAFD.datas.get(affixId)
    levelGap = affixData.get('levelGap', gameconst.EquipAttrConst.AFFIX_DEFAULT_LEVEL_GAP)
    affixLv = min(max(math.ceil(iLevel/levelGap), 1), affixData['maxLevel'])
    affixObj = Affix(affixId, affixLv=affixLv)

    affixValFloorList = affixData['floor'](affixLv)
    affixValCeilList = affixData['ceiling'](affixLv)
    if not affixValFloorList or not affixValCeilList:
        return
    affixVals = []
    for floorVal, ceilVal in zip(affixValFloorList, affixValCeilList):
        if isinstance(floorVal, int) and isinstance(ceilVal, int):
            val = random.randint(floorVal, ceilVal)
        else:
            val = random.uniform(floorVal, ceilVal)
            val = round(val, 4)
        affixVals.append(val)
        break

    affixObj.affixVal = affixVals[0]
    return affixObj

def genBlessAffix(iLevel, affixId):
    affixData = AFAFD.datas.get(affixId)
    levelGap = affixData.get('levelGap', gameconst.EquipAttrConst.AFFIX_DEFAULT_LEVEL_GAP)
    affixLv = min(max(math.ceil(iLevel / levelGap), 1), affixData['maxLevel'])
    affixObj = Affix(affixId, affixLv=affixLv)
    return affixObj

def applyAffixPropEffectToAvatar(owner, affixItem, attrNameList, attrValList, attrSrcType, afxValStartIdx=0, afxValEndIdx=-1):
    #词条对avatar单属性的加成
    DEBUG_MSG('in applyAffixPropEffectToAvatar:',  attrNameList, attrValList)
    valNum = len(attrValList)
    if afxValEndIdx >= valNum:
        gameengine.reportCritical('applyAffixPropEffectToAvatar, afx end idx error:', attrValList, afxValStartIdx, afxValEndIdx)
        return

    for idx, attrName in enumerate(attrNameList):
        valueIdx = afxValStartIdx+idx
        if afxValEndIdx == -1:
            val = attrValList[valueIdx] if valueIdx < valNum else attrValList[afxValEndIdx]
        else:
            val = attrValList[valueIdx] if valueIdx < afxValEndIdx else attrValList[afxValEndIdx]
        affixItem.recordAffixAddSingleProp(attrName, val)
        owner.addProp(attrName, val, attrSrcType)
    return

def removeAffixEffectFromAvatar(owner, affixItem, baseAttrAddValDic, attrSrcType):
    DEBUG_MSG('in removeAffixEffectFromAvatar')
    # 移除单属性加成
    DEBUG_MSG('     in removeAffixEffectFromAvatar, baseAttrsByAfxVal:', baseAttrAddValDic)
    for propName, val in baseAttrAddValDic.items():
        owner.addProp(propName, -1 * val, attrSrcType)
    # # 移除技能加成
    affixItem.removeAddSkillLv(owner)
    return
