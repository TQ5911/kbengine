# -*- coding: utf-8 -*-
import utils
import methodPool


class MethodPoolInfo(object):

    def createObjFromDict(self, dict):
        _mp = methodPool.MethodPool()

        for i, methodName in enumerate(dict['methodName']):
            _mp[methodName] = dict['callTime'][i]

        return _mp

    def isSameType(self, obj):
        return type(obj) is methodPool.MethodPool

    def getDictFromObj(self, obj):
        _mVals = {'methodName': [], 'callTime': [], }

        now = utils.curTS()
        for methodName, callTime in obj.items():
            if callTime <= now:
                continue

            _mVals['methodName'].append(methodName)
            _mVals['callTime'].append(callTime)

        return _mVals


instance = MethodPoolInfo()
