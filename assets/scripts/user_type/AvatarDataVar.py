# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import value_value as VLVLD
import gameengine
import dataUtils
import gameconst
import itemData_itemData as IDIDD


def getAvatarBaseAttrVarValue(owner, varId):
    attrName = VLVLD.datas[varId]['charProp']
    # 暂时从avater身上剥离自动属性
    if attrName == "equipWashNum":
        gridID, itemObj = owner.getAnimaItemObj()
        if gridID < 0 or not itemObj:
            return 0
        return itemObj.getAnima()
    
    value = getattr(owner, attrName, None)
    if value is None:
        gameengine.reportCritical('getAvatarBaseAttrVarValue error, no this attr:', varId, attrName)
    return value


def getVarValueFromAvatarDic(owner, varId):
    return owner.avatarVarDic.get(varId, dataUtils.getVariableDefaultVal(varId))


AvatarDataVarFunDic = {
    'vitality': getAvatarBaseAttrVarValue,
    'equipWashNum': getAvatarBaseAttrVarValue,

    # 'level':getAvatarLevelValue,
}
