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
    value = getattr(owner, attrName, None)
    if value is None:
        gameengine.panicStack('getAvatarBaseAttrVarValue error, no this attr:', varId, attrName)
    return value


def getVarValueFromAvatarDic(owner, varId):
    return owner.avatarVarDic.get(varId, dataUtils.getVariableDefaultVal(varId))


AvatarDataVarFunDic = {
    'vitality': getAvatarBaseAttrVarValue,
}
