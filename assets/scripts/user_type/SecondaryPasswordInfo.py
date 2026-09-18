
# -*- encoding:utf-8 -*-

import functools

from KBEDebug import *
import KBEngine
import userType
import gameconst
import utils


def _onLoadSecondaryPasswordInfoFromDB(accountDbId, callback, ret, num, insertId, err):
    if err:
        ERROR_MSG('loadSecondaryPasswordInfoFromDB error:', err, accountDbId)
        callback(None)
        return

    info = secondaryPasswordInfo()
    if ret:
        versionId, secondaryPassword, verityFailedCnt, lockedStep, lockedTimestamp, beEnable = ret[0]
        info.versionId = int(versionId.decode('ascii')) if isinstance(versionId, bytes) else int(versionId)
        info.secondaryPassword = secondaryPassword.decode('utf-8') if isinstance(secondaryPassword, bytes) else str(secondaryPassword)
        info.verityFailedCnt = int(verityFailedCnt.decode('ascii')) if isinstance(verityFailedCnt, bytes) else int(verityFailedCnt)
        info.lockedStep = int(lockedStep.decode('ascii')) if isinstance(lockedStep, bytes) else int(lockedStep)
        info.lockedTimestamp = int(lockedTimestamp.decode('ascii')) if isinstance(lockedTimestamp, bytes) else int(lockedTimestamp)
        info.beEnable = bool(int(beEnable.decode('ascii')) if isinstance(beEnable, bytes) else int(beEnable))

    callback(info)

def loadSecondaryPasswordInfoFromDB(accountDbId, callback):
    # 策划需求变了，要求代理玩家上线不再受二级密码影响了
    info = secondaryPasswordInfo()
    callback(info)

def loadSecondaryPasswordInfoFromDB_deprecated(accountDbId, callback):
    """
    从数据库读取二级密码信息，并返回 secondaryPasswordInfo 实例
    @param accountName: 账号名
    @param callback: 回调函数，签名为 callback(info)，
                     info 为 secondaryPasswordInfo 实例；查询失败时 info 为 None，
                     无记录时 info 为默认初始化的 secondaryPasswordInfo 实例
    """
    _sql = (
        f'SELECT sm_secondaryPwdInfo_versionId, sm_secondaryPwdInfo_secondaryPassword, '
        f'sm_secondaryPwdInfo_verityFailedCnt, sm_secondaryPwdInfo_lockedStep, '
        f'sm_secondaryPwdInfo_lockedTimestamp, sm_secondaryPwdInfo_beEnable '
        f'FROM tbl_Account WHERE id={accountDbId}'
    )

    KBEngine.executeRawDatabaseCommand(
        _sql,
        functools.partial(_onLoadSecondaryPasswordInfoFromDB, accountDbId, callback)
    )


class secondaryPasswordInfo(userType.UserSingleType):
    def __init__(self, versionId=0, secondaryPassword='', verityFailedCnt=0, lockedStep=0, lockedTimestamp=0, beEnable=False, checkLockedExpiredTimerId=0):
        self.versionId = versionId
        self.secondaryPassword = secondaryPassword
        self.verityFailedCnt = verityFailedCnt
        self.lockedStep = lockedStep
        self.lockedTimestamp = lockedTimestamp
        self.beEnable = beEnable
        self.checkLockedExpiredTimerId = checkLockedExpiredTimerId

    def initFromDict(self, dataDic):
        self.versionId = dataDic['versionId']
        self.secondaryPassword = dataDic['secondaryPassword']
        self.verityFailedCnt = dataDic['verityFailedCnt']
        self.lockedStep = dataDic['lockedStep']
        self.lockedTimestamp = dataDic['lockedTimestamp']
        self.beEnable = dataDic['beEnable']
        return self
    
    def toStreamSavedDic(self):
        dic = {
            'versionId': self.versionId,
            'secondaryPassword': self.secondaryPassword,
            'verityFailedCnt': self.verityFailedCnt,
            'lockedStep': self.lockedStep,
            'lockedTimestamp': self.lockedTimestamp,
            'beEnable': self.beEnable
        }
        return dic

    def toStreamClientDic(self):
        dic = {
            'hasSecondaryPassword': self.hasSecondaryPassword(),
            'verityFailedCnt': self.verityFailedCnt,
            'lockedTimestamp': self.lockedTimestamp,
            'beEnable': self.beEnable
        }
        return dic

    @staticmethod
    def latestVersion():
        return 1

    def setDefault(self, beEnable=True):
        if self.versionId == self.latestVersion():
            return
        
        self.versionId += 1
        if self.versionId == 1:
            self.beEnable = beEnable

    def hasSecondaryPassword(self):
        return len(self.secondaryPassword) > 0
    
    def updateSecondaryPassword(self, pwd):
        self.clearPunishmentInfo()
        self.secondaryPassword = pwd

    def delSecondaryPassword(self):
        self.clearPunishmentInfo()
        self.secondaryPassword = ''

    def enableSecondaryPassword(self):
        self.clearPunishmentInfo()
        self.beEnable = not self.beEnable

    def veritySecondaryPassword(self):
        self.clearPunishmentInfo()

    def clearPunishmentInfo(self):
        self.verityFailedCnt = 0
        self.lockedStep = 0
        self.lockedTimestamp = 0

    def incrVerityFailedCnt(self, now, cfgList):
        self.verityFailedCnt += 1
        lockedStep = self.lockedStep
        lockedTimestamp = 0
        msgId = 0
        for idx, cfg in enumerate(reversed(cfgList)):
            if self.verityFailedCnt < cfg[0]:
                continue
            self.lockedStep = len(cfgList) - idx
            lockedTimestamp = now + cfg[1] * 60
            msgId = cfg[2]
            break

        if lockedStep != self.lockedStep:
            self.lockedTimestamp = lockedTimestamp
            return True, msgId
        return False, msgId

    def checkBeVerityLocked(self, now):
        return self.lockedTimestamp > now

    def beVerityLockedExpired(self):
        self.clearPunishmentInfo()

    def dailyResetPunishmentInfo(self):
        self.clearPunishmentInfo()

    def setCheckLockedExpiredTimerId(self, timerId):
        self.checkLockedExpiredTimerId = timerId

    def getCheckLockedExpiredTimerId(self):
        return self.checkLockedExpiredTimerId

    def getSecondaryPassword(self):
        return self.secondaryPassword

    def getLockedStep(self):
        return self.lockedStep

    def getLockedTimestamp(self):
        return self.lockedTimestamp

    def getBeEnable(self):
        return self.beEnable
    
class secondaryPasswordInstance(object):
    def createObjFromDict(self, dataDict):
        secondaryPasswordInst = secondaryPasswordInfo()
        secondaryPasswordInst.initFromDict(dataDict)
        return secondaryPasswordInst
    
    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()
    
    def isSameType(self, obj):
        return type(obj) is secondaryPasswordInfo
    
secondaryPasswordInstance = secondaryPasswordInstance()
##############################################################
class secondaryPasswordVerityInfo(userType.UserSingleType):
    def __init__(self, beEnable=False, versionId=0, useMoney=False, money=0, useBindMoney=False, bindMoney=0, 
                 itemWash=False, itemDisassemble=False, saleItem=False, rentalItem=False, beVerity=False, 
                 beAccess=False, accessIdx=0, accessTimestamp=0):
        self.beEnable = beEnable

        self.versionId = versionId
        self.beAccess = beAccess
        self.accessIdx = accessIdx

        self.useMoney = useMoney
        self.money = money
        self.useBindMoney = useBindMoney
        self.bindMoney = bindMoney
        self.itemWash = itemWash
        self.itemDisassemble = itemDisassemble
        self.saleItem = saleItem
        self.rentalItem = rentalItem

        self.beVerity = beVerity
        self.accessTimestamp = accessTimestamp

    @classmethod
    def _checkIgnores_(cls):
        return 'beVerity', 'accessTimestamp'

    def initFromDict(self, dataDic):
        self.beEnable = dataDic['beEnable']

        self.versionId = dataDic['versionId']
        self.beAccess = dataDic['beAccess']
        self.accessIdx = dataDic['accessIdx']

        self.useMoney = dataDic['useMoney']
        self.money = dataDic['money']
        self.useBindMoney = dataDic['useBindMoney']
        self.bindMoney = dataDic['bindMoney']
        self.itemWash = dataDic['itemWash']
        self.itemDisassemble = dataDic['itemDisassemble']
        self.saleItem = dataDic['saleItem']
        self.rentalItem = dataDic['rentalItem']

        return self
    
    def toStreamSavedDic(self):
        dic = {
            'beEnable': self.beEnable,

            'versionId': self.versionId,
            'beAccess': self.beAccess,
            'accessIdx': self.accessIdx,

            'useMoney': self.useMoney,
            'money': self.money,
            'useBindMoney': self.useBindMoney,
            'bindMoney': self.bindMoney,
            'itemWash': self.itemWash,
            'itemDisassemble': self.itemDisassemble,
            'saleItem': self.saleItem,
            'rentalItem': self.rentalItem,
        }
        return dic

    def toStreamClientDic(self):
        dic = {
            'beEnable': self.beEnable,

            'accessIdx': self.accessIdx,

            'money': self.money,
            'bindMoney': self.bindMoney,
            'itemWash': self.itemWash,
            'itemDisassemble': self.itemDisassemble,
            'saleItem': self.saleItem,
            'rentalItem': self.rentalItem,
        }
        return dic
    
    def updateBeVerity(self, now, beVerity, cfgList):
        self.beVerity = beVerity
        if self.beAccess:
            self.accessTimestamp = now + cfgList[self.accessIdx] if beVerity else 0
        else:
            self.accessTimestamp = 0

    def checkBeVerity(self, now):
        if not self.beVerity:
            return False

        if self.beAccess:
            if self.accessTimestamp >= now:
                return True
            else:
                self.beVerity = False
                self.accessTimestamp = 0
                return False

        return True

    def checkNeedVerity(self, checkInfo, itemDisassemblyLimit):
        if checkInfo[0] == gameconst.SecondaryPasswordCheckType.USE_MONEY:
            if not self.useMoney:
                return False
            if len(checkInfo) <= 1:
                return True
            return checkInfo[1] >= self.money
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.USE_BIND_MONEY:
            if not self.useBindMoney:
                return False
            if len(checkInfo) <= 1:
                return True
            return checkInfo[1] >= self.bindMoney
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.SALE_ITEM:
            return self.saleItem
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.RENTAL_ITEM:
            return self.rentalItem
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.ITEM_WASH:
            return self.itemWash
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.ITEM_DISASSEMBLE:
            if not self.itemDisassemble:
                return False
            if len(checkInfo) <= 1:
                return True
            return checkInfo[1] >= itemDisassemblyLimit
        elif checkInfo[0] == gameconst.SecondaryPasswordCheckType.AUTH:
            return True

        return False

    def getBeEnable(self):
        return self.beEnable

    @staticmethod
    def latestVersion():
        return 3

    def setDefault(self, beEnable=True, beAccess=True, accessIdx=0, useMoney=True, money=100, useBindMoney=True, bindMoney=100, 
                   itemWash=True, itemDisassemble=True, saleItem=True, rentalItem=True):
        if self.versionId == self.latestVersion():
            return
        
        self.versionId += 1
        if self.versionId == 1:
            self.beAccess = True
            self.accessIdx = accessIdx
            self.useMoney = useMoney
            self.money = money
            self.useBindMoney = useBindMoney
            self.bindMoney = bindMoney
            self.itemWash = itemWash
            self.itemDisassemble = itemDisassemble
            self.saleItem = saleItem
        elif self.versionId == 2:
            self.rentalItem = rentalItem
        elif self.versionId == 3:
            self.beEnable = beEnable

        self.setDefault(beEnable, beAccess, accessIdx, useMoney, money, useBindMoney, bindMoney, 
                   itemWash, itemDisassemble, saleItem, rentalItem)

    @staticmethod
    def getModifyPropList():
        return (('beEnable', bool), ('accessIdx', int), ('money', int), ('bindMoney', int), ('itemWash', bool), ('itemDisassemble', bool), ('saleItem', bool), ('rentalItem', bool))

    def modifyProp(self, clientCfg):
        updatePropList = []
        modifyPropList = self.getModifyPropList()
        for modifyProp in modifyPropList:
            if not hasattr(self, modifyProp[0]):
                continue
            if modifyProp[0] not in clientCfg:
                continue
            oldVal = modifyProp[1](getattr(self, modifyProp[0]))
            newVal = modifyProp[1](clientCfg[modifyProp[0]])
            if oldVal == newVal:
                continue

            updatePropList.append(modifyProp[0])
            setattr(self, modifyProp[0], newVal)

        return updatePropList

class secondaryPasswordVerityInstance(object):
    def createObjFromDict(self, dataDict):
        secondaryPasswordInst = secondaryPasswordVerityInfo()
        secondaryPasswordInst.initFromDict(dataDict)
        return secondaryPasswordInst
    
    def getDictFromObj(self, obj):
        return obj.toStreamSavedDic()
    
    def isSameType(self, obj):
        return type(obj) is secondaryPasswordVerityInfo
    
secondaryPasswordVerityInstance = secondaryPasswordVerityInstance()
