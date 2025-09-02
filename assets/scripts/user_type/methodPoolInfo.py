# -*- coding: utf-8 -*-
import utils
import methodPool


class MethodPoolInfo(object):

    def createObjFromDict(self, dict):
        mp = methodPool.MethodPool()

        for i, methodName in enumerate(dict['methodName']):
            mp[methodName] = dict['callTime'][i]

        return mp

    def getDictFromObj(self, obj):
        mVals = {'methodName': [], 'callTime': [], }

        now = utils.getNow()
        for methodName, callTime in obj.items():
            if callTime <= now:
                continue

            mVals['methodName'].append(methodName)
            mVals['callTime'].append(callTime)

        return mVals

    def isSameType(self, obj):
        return type(obj) is methodPool.MethodPool


instance = MethodPoolInfo()
