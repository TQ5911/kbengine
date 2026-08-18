
# coding: utf-8
import userType
import AuctionSnatchRecord
import gameconst

class AuctionSnatchRecords(userType.UserSingleType):
    '''AUCTION_SNATCH_RECORDS'''
    def __init__(self, auctionUUID=0, itemId = 0, price=0, number=0, publicityEndTime=0, records=None, status=gameconst.AuctionSnatchStatus.DEFAULT):
        self.auctionUUID = auctionUUID
        self.itemId = itemId
        self.price = price
        self.number = number
        self.publicityEndTime = publicityEndTime
        self.records = records if records is not None else []
        self.status = status

    def toStreamSavedDic(self):
        return {
            'auctionUUID': self.auctionUUID,
            'itemId': self.itemId,
            'price': self.price,
            'number': self.number,
            'publicityEndTime': self.publicityEndTime,
            'records': self.records,
            'status': self.status,
        }
    
    def addAuctionSnatchRecords(self, gbId, name, opUUID):
        record = AuctionSnatchRecord.AuctionSnatchRecord(gbId, name, opUUID)
        self.records.append(record)

    def isFinished(self):
        return self.status == gameconst.AuctionSnatchStatus.DONE
    
    def setFinished(self):
        self.status = gameconst.AuctionSnatchStatus.DONE

    def clearRecords(self):
        self.records.clear()

class AuctionSnatchRecordsMgr(object):
    def createObjFromDict(self, dataDict):
        obj = AuctionSnatchRecords(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()

    def isSameType(self, obj):
        return type(obj) is AuctionSnatchRecords


AuctionSnatchRecordsInstance = AuctionSnatchRecordsMgr()

