
# coding: utf-8
import utils
import userType
import TitleValInfo


class TitleMgrVal(userType.UserSingleType):
    '''TITLE_MGR_DATA_INFO'''
    def __init__(self, titleValList=(), curTitleId=0):
        self.titleValList = self.clearExpireTitle(titleValList)
        if self.hasTitle(curTitleId):
            self.curTitleId = curTitleId
        else:
            self.curTitleId = self.firstTitleId()

    def firstExpireTime(self):
        _firstTime = 0
        for _val in self.titleValList:
            if not _val.expireTime:
                continue

            if not _firstTime:
                _firstTime = _val.expireTime

            elif _firstTime > _val.expireTime:
                _firstTime = _val.expireTime

        return _firstTime

    def doAddTitle(self, owner, titleId):
        if self.hasTitle(titleId):
            return

        _val = TitleValInfo.TitleValVal(titleId)
        self.titleValList.append(_val)
        if not self.curTitleId:
            self.setCurTitle(owner, _val.titleId)

        return _val

    def doClearExpireTitle(self):
        self.titleValList = self.clearExpireTitle(self.titleValList)

    def clearAndResetTitle(self, owner):
        self.titleValList = self.clearExpireTitle(self.titleValList)
        if self.hasTitle(self.curTitleId):
            return

        _firstTitle = self.firstTitleId()
        if _firstTitle:
            self.setCurTitle(owner, _firstTitle)
        else:
            self.setCurTitle(owner, 0)

    def setCurTitle(self, owner, titleId):
        self.curTitleId = titleId
        owner.cell.setTitleCell(self.curTitleId)

    def clearExpireTitle(self, titleValList):
        _ret = []
        _now = utils.curTS()
        for _val in titleValList:
            if not _val.expireTime:
                _ret.append(_val)
                continue

            if _val.expireTime <= _now:
                continue

            _ret.append(_val)

        return _ret

    def firstTitleId(self):
        if not self.titleValList:
            return 0

        return self.titleValList[0].titleId

    def hasTitle(self, titleId):
        for _val in self.titleValList:
            if _val.titleId == titleId:
                return True

        return False

    def toTitleMgrSavedDict(self):
        return {
            'titleValList': self.titleValList,
            'curTitleId': self.curTitleId,
        }


class TitleMgrInfo(object):
    def createObjFromDict(self, dataDict):
        obj = TitleMgrVal(**dataDict)
        return obj

    def getDictFromObj(self, obj):
        return obj.toTitleMgrSavedDict()

    def isSameType(self, obj):
        return type(obj) is TitleMgrVal


TitleMgrInstance = TitleMgrInfo()

