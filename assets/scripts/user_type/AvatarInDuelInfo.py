
# coding: utf-8

import userType


class AvatarInDuelVal(userType.UserSoleType):
    '''AVATAR_IN_DUEL_DATA_INFO'''
    def __init__(self, gbId=0, box=None, eid=0, leaveCnt=0, name=''):
        self.gbId = gbId
        self.box = box
        self.eid = eid
        self.leaveCnt = leaveCnt
        self.name = name

    def toAvatarInDuelSavedDict(self):
        return {
            'gbId': self.gbId,
            'box': self.box,
            'eid': self.eid,
            'leaveCnt': self.leaveCnt,
            'name': self.name,
        }


class AvatarInDuelInfo(object):
    def createObjFromDict(self, dataDict):
        obj = AvatarInDuelVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toAvatarInDuelSavedDict()

    def isSameType(self, obj):
        return type(obj) is AvatarInDuelVal


AvatarInDuelInstance = AvatarInDuelInfo()

