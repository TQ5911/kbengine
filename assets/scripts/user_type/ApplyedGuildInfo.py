
# coding: utf-8

import userType
import ApplyedGuildValInfo


class ApplyedGuildVal(userType.UserDictType):
    '''APPLYED_GUILD_DATA_INFO'''
    def __init__(self, applyedData):
        for _data in applyedData:
            self[_data['guildUUID']] = ApplyedGuildValInfo.ApplyedGuildValVal(**_data)

    def toApplyedGuildSavedDict(self):
        return {
            'applyedData': [i.toApplyedGuildValSavedDict() for i in self.values()]
        }


class ApplyedGuildInfo(object):
    def createObjFromDict(self, dataDict):
        obj = ApplyedGuildVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toApplyedGuildSavedDict()

    def isSameType(self, obj):
        return type(obj) is ApplyedGuildVal


ApplyedGuildInstance = ApplyedGuildInfo()

