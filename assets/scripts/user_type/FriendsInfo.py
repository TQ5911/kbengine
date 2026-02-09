import Friendship



class FriendshipInfo(object):
    def createObjFromDict(self, dataDict):
        friendship = Friendship.Friendship(**dataDict)
        return friendship

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is Friendship.Friendship


FriendshipInstance = FriendshipInfo()
