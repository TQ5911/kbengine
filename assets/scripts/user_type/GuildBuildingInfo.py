
# coding: utf-8

import userType


class GuildBuildingVal(userType.UserSingleType):
    '''GUILD_BUILDING_DATA_INFO'''
    def __init__(self, juYing=None, wuHua=None, xiangFang=None, yanWu=None, cangKu=None, junXu=None):
        self.juYing = juYing
        self.wuHua = wuHua
        self.xiangFang = xiangFang
        self.yanWu = yanWu
        self.cangKu = cangKu
        self.junXu = junXu

    def toGuildBuildingSavedDict(self):
        return {
            'juYing': self.juYing,
            'wuHua': self.wuHua,
            'xiangFang': self.xiangFang,
            'yanWu': self.yanWu,
            'cangKu': self.cangKu,
            'junXu': self.junXu,
        }

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, GuildBuildingVal):
            return False

        return self.juYing == value.juYing and \
                self.wuHua == value.wuHua and \
                self.xiangFang == value.xiangFang and \
                self.yanWu == value.yanWu and \
                self.cangKu == value.cangKu and \
                self.junXu == value.junXu


class GuildBuildingInfo(object):
    def createObjFromDict(self, dataDict):
        obj = GuildBuildingVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toGuildBuildingSavedDict()

    def isSameType(self, obj):
        return type(obj) is GuildBuildingVal


GuildBuildingInstance = GuildBuildingInfo()

