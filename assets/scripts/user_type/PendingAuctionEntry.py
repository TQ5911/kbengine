
# coding: utf-8
import userType

class PendingAuctionEntry(userType.UserSingleType):
    '''PENDING_AUCTION_ENTRY'''
    def __init__(self, auctionItemUUID=0, bindMoney=0, money=0, dealTime=0, isSettled=False):
        self.auctionItemUUID = auctionItemUUID
        self.bindMoney = bindMoney
        self.money = money
        self.dealTime = dealTime
        self.isSettled = isSettled

    def toStreamSavedDic(self):
        return {
            'auctionItemUUID': self.auctionItemUUID,
            'bindMoney': self.bindMoney,
            'money': self.money,
            'dealTime': self.dealTime,
            'isSettled': self.isSettled
        }


class PendingAuctionEntryMgr(object):
    def createObjFromDict(self, dataDict):
        obj = PendingAuctionEntry(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is PendingAuctionEntry


PendingAuctionEntryInstance = PendingAuctionEntryMgr()