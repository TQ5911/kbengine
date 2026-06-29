
# coding: utf-8
import userType
import PendingAuctionEntry

class PendingAuctionEntryVal(userType.UserSingleType):
    '''PENDING_AUCTION_ENTRIES'''
    def __init__(self, pendingAuctionEntries=()):
        self.pendingAuctionEntries = pendingAuctionEntries

    def toStreamSavedDic(self):
        return {
            'pendingAuctionEntries': self.pendingAuctionEntries,
        }

    def addPendingAuctionEntry(self, auctionItemUUID=0, amount=0, dealTime=0):
        entry = PendingAuctionEntry.PendingAuctionEntry(auctionItemUUID=auctionItemUUID, amount=amount, dealTime=dealTime)
        self.pendingAuctionEntries.append(entry)

class PendingAuctionEntriesMgr(object):
    def createObjFromDict(self, dataDict):
        obj = PendingAuctionEntryVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is PendingAuctionEntryVal


PendingAuctionEntriesInstance = PendingAuctionEntriesMgr()

