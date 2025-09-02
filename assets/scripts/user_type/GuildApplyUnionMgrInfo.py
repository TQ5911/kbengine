
# coding: utf-8

import userType
import GuildApplyUnionInfo
import GuildApplyUnionSenderInfo
import utils
import gameconst

import guildAuthorization_authorizationID_def as GA_AI_DD
import guild_guildConst as G_GCD

class GuildApplyUnionMgrVal(userType.UserSoleType):
    '''GUILD_APPLY_UNION_MGR_DATA_INFO'''
    # type hint
    applyUnionDic: dict
    senderDict: dict

    def __init__(self, applyUnionList=(), senderList=()):
        self.applyUnionDic = {}
        for _auVal in applyUnionList:
            self.applyUnionDic[_auVal.guildUUID] = _auVal

        self.senderDict = {}
        for _senderVal in senderList:
            self.senderDict[_senderVal.guildUUID] = _senderVal

    def addSender(self, guildUUID, guildName, guildIcon, flag, guildScore):
        _now = utils.getNow()
        _expireTime = _now + G_GCD.datas['guild_unionApplicationTimeLimit']['value'] * gameconst.ONE_DAY_SECONDS
        _senderVal = GuildApplyUnionSenderInfo.GuildApplyUnionSenderVal(
            guildUUID, guildName, guildIcon, flag, guildScore, _expireTime)
        self.senderDict[guildUUID] = _senderVal
        return _senderVal
    
    def isApplyUnionFull(self):
        return len(self.applyUnionDic) >= G_GCD.datas['guild_unionApplicationNum']['value']
    
    def isSenderFull(self):
        return len(self.senderDict) >= G_GCD.datas['guild_unionApplicationNum']['value']
    
    def removeApplyUnion(self, guildUUID, guild):
        _auVal = self.applyUnionDic.pop(guildUUID, None)
        if not _auVal:
            return

        guild.broadcastByPermission(
            GA_AI_DD.datas.guildUnion,
            lambda box: box.client.onRemoveApplyGuildUnion(guildUUID))
        
    def removeSender(self, guildUUID):
        self.senderDict.pop(guildUUID, None)

    def addApplyUnion(self, guildUUID, guildName, guildIcon, flag, guildScore, guildLevel):
        _now = utils.getNow()
        _expireTime = _now + G_GCD.datas['guild_unionApplicationTimeLimit']['value'] * gameconst.ONE_DAY_SECONDS
        _auVal = GuildApplyUnionInfo.GuildApplyUnionVal(
            guildUUID, 
            _expireTime, 
            guildName, 
            guildIcon, 
            flag, 
            guildScore, 
            guildLevel)
        self.applyUnionDic[guildUUID] = _auVal
        return _auVal
    
    def isInSender(self, guildUUID):
        _senderVal = self.senderDict.get(guildUUID)
        if not _senderVal:
            return False

        return _senderVal.endTime > utils.getNow()

    def isInApplyUnion(self, guildUUID):
        _auVal = self.applyUnionDic.get(guildUUID)
        if not _auVal:
            return False

        return _auVal.endTime > utils.getNow()

    def toGuildApplyUnionMgrSavedDict(self):
        return {
            'applyUnionList': list(self.applyUnionDic.values()),
            'senderList': list(self.senderDict.values()),
        }


class GuildApplyUnionMgrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildApplyUnionMgrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildApplyUnionMgrSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildApplyUnionMgrVal


GuildApplyUnionMgrInstance = GuildApplyUnionMgrInfo()

