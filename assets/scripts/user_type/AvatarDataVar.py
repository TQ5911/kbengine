# -*- encoding:utf-8 -*-

import KBEngine
from KBEDebug import *
import value_value as VLVLD
import gameengine
import dataUtils
import gameconst


def getAvatarBaseAttrVarValue(owner, varId):
    _attrName = VLVLD.datas[varId]['charProp']
    _value = getattr(owner, _attrName, None)
    if _value is None:
        gameengine.panicStack('getAvatarBaseAttrVarValue error, no this attr:', varId, _attrName)
    return _value


def getVarValueFromAvatarDic(owner, varId):
    return owner.avatarVarDict.get(varId, dataUtils.getVariableDefaultVal(varId))


AvatarDataVarFunDic = {
    'vitality': getAvatarBaseAttrVarValue,
}
