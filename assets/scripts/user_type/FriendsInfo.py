# import Friends
import Friendship


# class FriendsInfo(object):
#     def createObjFromDict(self, dataDict):
#         friends = Friends.Friends()
#         friends.initFromDict(dataDict)
#         return friends
#
#     def getDictFromObj(self, obj):
#         return obj.toSavedDict()
#
#     def isSameType(self, obj):
#         return type(obj) is Friends.Friends


class FriendshipInfo(object):
    def createObjFromDict(self, dataDict):
        friendship = Friendship.Friendship(**dataDict)
        return friendship

    def getDictFromObj(self, obj):
        return obj.toSavedDict()

    def isSameType(self, obj):
        return type(obj) is Friendship.Friendship


# FriendsInstance = FriendsInfo()
FriendshipInstance = FriendshipInfo()
