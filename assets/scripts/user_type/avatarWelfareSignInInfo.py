
# -*- encoding:utf-8 -*-

from KBEDebug import *
import KBEngine
import userType


class welfareSignInInfo(userType.UserSTSoleType):
    def __init__(self, welfareSignInDay=0, welfareLastSignInTimestamp=0, welfareSignInData=0):
        self.welfareSignInDay = welfareSignInDay
        self.welfareLastSignInTimestamp = welfareLastSignInTimestamp
        self.welfareSignInData = welfareSignInData

    def initFromDict(self, dataDic):
        self.welfareSignInDay = dataDic['welfareSignInDay']
        self.welfareLastSignInTimestamp = dataDic['welfareLastSignInTimestamp']
        self.welfareSignInData = dataDic['welfareSignInData']
        return self
    
    def toStreamSavedDic(self):
        dic = {'welfareSignInDay': self.welfareSignInDay,
               'welfareLastSignInTimestamp': self.welfareLastSignInTimestamp,
               'welfareSignInData': self.welfareSignInData}
        return dic

    def hasSignIn(self, signInDayNo):
        mask = 1 << signInDayNo
        return (self.welfareSignInData & mask) == mask

    def doSignIn(self, signInDayNo):
        mask = 1 << signInDayNo
        self.welfareSignInData |= mask

class welfareSignInInstance(userType.UserSTSoleInfo):
    @property
    def cls(self):
        return welfareSignInInfo

welfareSignInInfoInstance = welfareSignInInstance()
