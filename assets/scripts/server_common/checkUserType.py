# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import time
import userType
from collections.abc import Iterable
import BaseItem


def checkProperty(owner):
    if KBEngine.publish():
        return

    tempCostTime = time.time()
    propDic = KBEngine.getUserTypeProperties('Avatar')
    for pName in propDic:
        if hasattr(owner, pName):
            _pObj = getattr(owner, pName)
            dict = propDic[pName].getDictFromObj(_pObj)
            checkObj = propDic[pName].createObjFromDict(dict)
            checkObjProperty([pName], _pObj, checkObj)

    LOG_DBG("const time is ", time.time() - tempCostTime)


def checkObjProperty(pNameList, propObj, checkObj, **kwargs):
    if not isinstance(propObj, BaseItem.PureItem) and isinstance(checkObj, BaseItem.PureItem):
        checkObj.changeToSpecificItem()

    _propDict = propObj.__dict__
    checkDict = checkObj.__dict__
    igoreProps = propObj._checkIgnores_()
    if igoreProps:
        _propDict = dict(_propDict)
        checkDict = dict(checkDict)
        for propName in igoreProps:
            _propDict.pop(propName, None)
            checkDict.pop(propName, None)

    pNameList.append(propObj.__class__)
    checkValueProperty(pNameList, _propDict, checkDict)
    pNameList.pop()


def checkIterProperty(pNameList, val, checkValue):
    if type(val) != type(checkValue):
        _valueModuleClass = val.__module__ + "." + val.__class__.__name__
        _checkValueModuleClass = checkValue.__module__ + "." + val.__class__.__name__
        if _valueModuleClass != _checkValueModuleClass:
            sendCheckError(pNameList, val, checkValue)
            return

    if isinstance(val, set):
        if val != checkValue:
            sendCheckError(pNameList, val, checkValue)
            return

    elif isinstance(val, str):
        if val != checkValue:
            sendCheckError(pNameList, val, checkValue)

    elif isinstance(val, dict):
        for _k, _v in val.items():
            if _k not in checkValue:
                sendCheckError(pNameList, val, checkValue)
            else:
                pNameList.append(str(_k))
                checkValueProperty(pNameList, _v, checkValue[_k])
                pNameList.pop()

    else:
        _iteValue = iter(val)
        _iteCheck = iter(checkValue)
        while True:
            nextValue = next(_iteValue, None)
            nextCheckValue = next(_iteCheck, None)
            if not nextValue and not nextCheckValue:
                break
            if not nextValue or not nextCheckValue:
                sendCheckError(pNameList, val, checkValue)
                break

            checkValueProperty(pNameList, nextValue, nextCheckValue)


def checkValueProperty(pNameList, val, checkValue):
    if isinstance(val, Iterable):
        checkIterProperty(pNameList, val, checkValue)
    elif isinstance(val, userType.UserTypeBase):
        checkObjProperty(pNameList, val, checkValue)
    elif val.__class__.__base__.__name__ == 'UserSingleType':
        checkObjProperty(pNameList, val, checkValue)
    elif callable(val):
        return
    else:
        isError = False
        if type(val) == float or type(checkValue) == float:
            if abs(val - checkValue) > 1e-2:
                isError = True
        else:
            if val != checkValue:
                isError = True
        if isError:
            sendCheckError(pNameList, val, checkValue)


def sendCheckError(pNameList, value, checkValue):
    _errMsg = "Avatar property"
    for pName in pNameList:
        _errMsg = "{} => {}".format(_errMsg, pName)
    _errMsg = "{} not same value ".format(_errMsg)
    LOG_ERR(_errMsg)
    _errMsg = "value : {}".format(value)
    LOG_ERR(_errMsg)
    _errMsg = "checkValue : {}".format(checkValue)
    LOG_ERR(_errMsg)
