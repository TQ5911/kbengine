
# coding: utf-8
import userType

class AuctionSnatchRecord(userType.UserSingleType):
    '''AUCTION_SNATCH_RECORD'''
    def __init__(self, gbId=0, name='', opUUID=0):
        self.gbId = gbId
        self.name = name
        self.opUUID = opUUID

    def toStreamSavedDic(self):
        return {
            'gbId': self.gbId,
            'name': self.name,
            'opUUID': self.opUUID,
        }

class AuctionSnatchRecordMgr(object):
    def createObjFromDict(self, dataDict):
        obj = AuctionSnatchRecord(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is AuctionSnatchRecord


AuctionSnatchRecordInstance = AuctionSnatchRecordMgr()

