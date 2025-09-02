
# coding: utf-8

import userType


class LeaderBoardAvatarListVal(userType.UserListType):
    '''LEADER_BOARD_AVATAR_LIST_DATA_INFO'''
    def __init__(self, listData=()):
        self.extend(listData)

    def toLeaderBoardAvatarListSavedDict(self):
        return {
            'listData': self,
        }


class LeaderBoardAvatarListInfo(object):
    def createObjFromDict(self, dataDict):
        obj = LeaderBoardAvatarListVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toLeaderBoardAvatarListSavedDict()

    def isSameType(self, obj):
        return type(obj) is LeaderBoardAvatarListVal


LeaderBoardAvatarListInstance = LeaderBoardAvatarListInfo()

