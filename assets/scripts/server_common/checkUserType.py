# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import time
import userType
from collections.abc import Iterable
import BaseItem
import math


def checkProperty(owner):
    if KBEngine.publish():
        return

    tempCostTime = time.time()
    propList = KBEngine.getPersistentProperties('Avatar')
    propDic = KBEngine.getUserTypeProperties('Avatar')
    for pName in propDic:
        if hasattr(owner, pName):
            DEBUG_MSG("checkProperty            pName ", pName)
            pObj = getattr(owner, pName)
            dict = propDic[pName].getDictFromObj(pObj)
            checkObj = propDic[pName].createObjFromDict(dict)
            checkObjProperty([pName], pObj, checkObj)

    DEBUG_MSG("const time is ", time.time() - tempCostTime)


def getCheckObj(typeClass, pObj):
    exec("import %s" % (typeClass.split('.')[0],))
    dict = eval('%s.getDictFromObj(pObj)' % (typeClass,))
    checkObj = eval('%s.createObjFromDict(dict)' % (typeClass,))
    return checkObj


def checkObjProperty(pNameList, propObj, checkObj):
    if not isinstance(propObj, BaseItem.PureItem) and isinstance(checkObj, BaseItem.PureItem):
        checkObj.changeToSpecificItem()

    propDict = propObj.__dict__
    checkDict = checkObj.__dict__
    igoreProps = propObj._checkIgnores_()
    if igoreProps:
        propDict = dict(propDict)
        checkDict = dict(checkDict)
        for propName in igoreProps:
            propDict.pop(propName, None)
            checkDict.pop(propName, None)

    pNameList.append(propObj.__class__)
    checkValueProperty(pNameList, propDict, checkDict)
    pNameList.pop()


def checkIterProperty(pNameList, value, checkValue):
    # DEBUG_MSG("checkIterProperty value ", type(value), value)
    # DEBUG_MSG("checkIterProperty checkValue ",  type(checkValue), checkValue)
    if type(value) != type(checkValue):
        valueModuleClass = value.__module__ + "." + value.__class__.__name__
        checkValueModuleClass = checkValue.__module__ + "." + value.__class__.__name__
        if valueModuleClass != checkValueModuleClass:
            sendCheckError(pNameList, value, checkValue)
            return

    if isinstance(value, set):
        if value != checkValue:
            sendCheckError(pNameList, value, checkValue)
            return

    elif isinstance(value, str):
        if value != checkValue:
            sendCheckError(pNameList, value, checkValue)

    elif isinstance(value, dict):
        for k, v in value.items():
            if k not in checkValue:
                sendCheckError(pNameList, value, checkValue)
            else:
                pNameList.append(str(k))
                checkValueProperty(pNameList, v, checkValue[k])
                pNameList.pop()

    else:
        iteValue = iter(value)
        iteCheck = iter(checkValue)
        while True:
            nextValue = next(iteValue, None)
            nextCheckValue = next(iteCheck, None)
            if not nextValue and not nextCheckValue:
                break
            if not nextValue or not nextCheckValue:
                sendCheckError(pNameList, value, checkValue)
                break

            checkValueProperty(pNameList, nextValue, nextCheckValue)


def checkValueProperty(pNameList, value, checkValue):
    # DEBUG_MSG("checkValueProperty value ", type(value), value)
    # DEBUG_MSG("checkValueProperty checkValue ",  type(checkValue), checkValue)
    if isinstance(value, Iterable):
        checkIterProperty(pNameList, value, checkValue)
    elif isinstance(value, userType.UserType):
        checkObjProperty(pNameList, value, checkValue)
    elif value.__class__.__base__.__name__ == 'UserSoleType':
        checkObjProperty(pNameList, value, checkValue)
    elif callable(value):
        return
    else:
        isError = False
        if type(value) == float or type(checkValue) == float:
            if abs(value - checkValue) > 1e-2:
                isError = True
        else:
            if value != checkValue:
                isError = True
        if isError:
            sendCheckError(pNameList, value, checkValue)
            return


def sendCheckError(pNameList, value, checkValue):
    errMsg = "Avatar property"
    for pName in pNameList:
        errMsg = "{} => {}".format(errMsg, pName)
    errMsg = "{} not same value ".format(errMsg)
    ERROR_MSG(errMsg)
    errMsg = "value : {}".format(value)
    ERROR_MSG(errMsg)
    errMsg = "checkValue : {}".format(checkValue)
    ERROR_MSG(errMsg)
