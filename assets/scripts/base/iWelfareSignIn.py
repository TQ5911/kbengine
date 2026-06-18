# coding: utf-8
from KBEDebug import *
import KBEngine
import gameconst
import gameclass
import dropAward
import gameengine
import gameglobal
import gamedecorator
import utils
import welfare_welfarePages as WWCONFIG
import welfare_serverLogin as WSLCONFIG
import welfare_levelReward as WLRD
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD
from user_type.avatarWelfareSignInInfo import welfareSignInInfo
import LogTrackingMgr

signInIDS = {
    "SevenSign": 1,
    "TenSign": 2,
}

levelWelfareIDS = {
    "LevelReward": 4,
}

tagClassIDS = {
    "phoneBind": 5,
    'PcLoginReward': 6,
}

class levelWelfareType:
    LEVEL_REWARD = 1

class IWelfareSignIn(object):
    def __init__(self):
        for _, v in WWCONFIG.datas.items():
            key = v["unlockID"]
            if key in signInIDS:
                if key not in self.welfareSignInInfos:
                    self.welfareSignInInfos[key] = welfareSignInInfo()
            
            if key in levelWelfareIDS:
                if key not in self.welfareLevelInfos:
                    self.welfareLevelInfos[key] = 0

    @gamedecorator.checkGameconfigEnable('welfare')
    def reqWelfareSignIn(self, exposed, signInDayNo, welfareType):
        if welfareType == "TenSign":
            self.reqWelfareSignInTenDay(welfareType, signInDayNo)
        elif welfareType == "SevenSign":
            self.reqWelfareSignInSevenDay(welfareType, signInDayNo)
        else:
            LOG_ERR('call reqWelfareSignIn: no welfareType', welfareType)
            return

    @gamedecorator.checkGameconfigEnable('welfare_tenSign')
    def reqWelfareSignInTenDay(self, welfareType, signInDayNo):
        self._reqWelfareSignIn(welfareType, signInDayNo)

    @gamedecorator.checkGameconfigEnable('welfare_sevenSign')
    def reqWelfareSignInSevenDay(self, welfareType, signInDayNo):
        self._reqWelfareSignIn(welfareType, signInDayNo)
    
    def _reqWelfareSignIn(self, welfareType, signInDayNo):
        LOG_INFO('call reqWelfareSignIn', welfareType, signInDayNo)
        welfareSignInInfo = self.welfareSignInInfos.get(welfareType, None)
        if not welfareSignInInfo:
            LOG_ERR('call reqWelfareSignIn: no welfareType', welfareType)
            return
        
        if not welfareSignInInfo.welfareSignInDay:
            LOG_ERR('call reqWelfareSignIn: not lock')
            return

        if signInDayNo > welfareSignInInfo.welfareSignInDay or signInDayNo <= 0:
            LOG_ERR('call reqWelfareSignIn: day err', signInDayNo, welfareSignInInfo.welfareSignInDay)
            return

        if welfareSignInInfo.hasSignIn(signInDayNo):
            LOG_WARN('call reqWelfareSignIn: alerady sign in', signInDayNo)
            return

        welfareSignInInfo.doSignIn(signInDayNo)

        self.sendWelfareSignInInfo(welfareType)

        opUUID = self.addSignInAward(signInDayNo, welfareType)
        if not opUUID:
            LOG_ERR('call reqWelfareSignIn: add award err', signInDayNo)
            return
        
        if welfareType == "SevenSign":
            LogTrackingMgr.LogTrackingMgr.Welfare_SignInSevenDay(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                self.gbID,
                WSLCONFIG.kvData.get(welfareType, {}).get(signInDayNo, 0),
                self.getAvatarLevel(),
                welfareSignInInfo.welfareSignInDay,
                signInDayNo,
                opUUID
            )
        elif welfareType == "TenSign":
            LogTrackingMgr.LogTrackingMgr.Welfare_SignInTenDay(
                self.gbID,
                self.accountEntity.clientDistinctId, 
                self.gbID,
                WSLCONFIG.kvData.get(welfareType, {}).get(signInDayNo, 0),
                self.getAvatarLevel(),
                welfareSignInInfo.welfareSignInDay,
                signInDayNo,
                opUUID
            )
    
    @gamedecorator.checkGameconfigEnable('welfare_levelReward')
    def reqLevelWelfare(self, exposed, slotNo, welfareType):
        LOG_INFO('call reqLevelWelfare', slotNo, welfareType)
        if welfareType not in self.welfareLevelInfos:
            LOG_ERR('call reqLevelWelfare: no welfareType', welfareType)
            return

        rid = slotNo
        if rid not in WLRD.datas:
            LOG_ERR('call reqLevelWelfare: no slotNo', slotNo)
            return

        tp = WLRD.datas[rid].get('type', 0)
        if tp != 1:
            LOG_ERR('call reqLevelWelfare: unexpected type', slotNo, tp)
            return

        condition = WLRD.datas[rid]['condition']
        if self.getAvatarLevel() < condition:
            LOG_ERR('call reqLevelWelfare: not meet condition', slotNo, self.getAvatarLevel(), condition)
            return
        
        if not self.checkUnlock(levelWelfareIDS[welfareType]):
            LOG_ERR('call reqLevelWelfare: not unlock', slotNo)
            return
        
        mask = 1 << slotNo
        if (self.welfareLevelInfos[welfareType] & mask) == mask:
            LOG_ERR('call reqLevelWelfare: already claimed', slotNo)
            return
        self.welfareLevelInfos[welfareType] |= mask

        rewardId = WLRD.datas[rid]['rewardID']
        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetailCls()
        opUUID = KBEngine.genUUID64()
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_WELFARE_LEVEL, rewardId, 1, opUUID, detail, awardCtx)

        self.sendLevelWelfareInfo(welfareType)

        LogTrackingMgr.LogTrackingMgr.Level_Reward(
            self.gbID,
            self.accountEntity.clientDistinctId, 
            self.gbID,
            self.getAvatarLevel(),
            rid,
            condition,
            self.getAvatarSchool(),
            opUUID
        )

        return True
        

    def addSignInAward(self, signInDayNo, welfareType):
        LOG_INFO('call addSignInAward')
        key = WSLCONFIG.kvData.get(welfareType, {}).get(signInDayNo, 0)
        if not key:
            LOG_ERR('call addSignInAward: no key', welfareType, signInDayNo)
            return False

        rewardId = WSLCONFIG.datas.get(key, {}).get('rewardID', 0)
        if not rewardId:
            LOG_ERR('call addSignInAward: no reward')
            return False

        awardCtx = self.getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetailCls(signInDayNo=signInDayNo)
        opUUID = KBEngine.genUUID64()
        srcType = AAC_AACDD.datas.BONUS_SRC_WELFARE_SIGN_IN if welfareType == "SevenSign" else AAC_AACDD.datas.BONUS_SRC_WELFARE_TEN_SIGN_IN
        self.addAwards(srcType, rewardId, 1, opUUID, detail, awardCtx)
        return opUUID

    def welfareSignInOnLogin(self):
        LOG_INFO('call welfareSignInOnLogin')
        self.checkAndUnlockWelfareSignIn(updateFlag = True)
        self.checkAndUpdateWelfareSignIn(updateFlag = False)

    def checkAndUnlockWelfareSignIn(self, updateFlag = True, offsetSeconds = gameconst.GENERAL_CYCLE_TIME):
        LOG_INFO('call checkAndUnlockWelfareSignIn')

        for welfareType, welfareSignInInfo in self.welfareSignInInfos.items():
            if welfareSignInInfo.welfareSignInDay:
                LOG_INFO('call checkAndUnlockWelfareSignIn, already lock', welfareSignInInfo.welfareSignInDay)
                continue
            
            if welfareType not in signInIDS:
                continue

            if not self.checkUnlock(signInIDS[welfareType]):
                LOG_INFO('call checkAndUnlockWelfareSignIn: can not lock')
                continue

            self.onWelfareSignInUpdate(updateFlag, offsetSeconds, welfareType)

        for welfareType in self.welfareLevelInfos.keys():
            if not self.checkUnlock(levelWelfareIDS[welfareType]):
                LOG_INFO('call checkAndUnlockWelfareSignIn: can not lock')
                continue

            self.sendLevelWelfareInfo(welfareType)

    def checkAndUpdateWelfareSignIn(self, tType = 0, updateFlag = True, offsetSeconds = gameconst.GENERAL_CYCLE_TIME):
        LOG_INFO('call checkAndUpdateWelfareSignIn')
        for welfareType, welfareSignInInfo in self.welfareSignInInfos.items():
            if not welfareSignInInfo.welfareSignInDay:
                LOG_INFO('call checkAndUpdateWelfareSignIn, not lock')
                continue
            self.onWelfareSignInUpdate(updateFlag, offsetSeconds, welfareType)

    def onWelfareSignInUpdate(self, updateFlag, offsetSeconds, welfareType):
        LOG_INFO('call onWelfareSignInUpdate',updateFlag, offsetSeconds, welfareType)
        welfareSignInInfo = self.welfareSignInInfos.get(welfareType, None)
        if not welfareSignInInfo:
            LOG_ERR('call onWelfareSignInUpdate: no welfareType', welfareType)
            return

        if welfareType not in WSLCONFIG.maxDayData:
            return
        
        maxSignInDay = WSLCONFIG.maxDayData[welfareType]
        if welfareSignInInfo.welfareSignInDay >= maxSignInDay:
            LOG_INFO('call onWelfareSignInUpdate: all signed in', welfareSignInInfo.welfareSignInDay)
            return

        newDaySignIn = updateFlag
        curTimestamp = utils.curTS()
        if not updateFlag:
            newDaySignIn = utils.checkDiffDay(curTimestamp, welfareSignInInfo.welfareLastSignInTimestamp, offsetSeconds)

        if not newDaySignIn:
            LOG_INFO('call onWelfareSignInUpdate: alerady signed in today', welfareSignInInfo.welfareLastSignInTimestamp)
            return

        self.updateWelfareSignIn(curTimestamp, welfareType)

        self.sendWelfareSignInInfo(welfareType)

    def sendAllWelfareSignInInfo(self):
        for welfareType, welfareSignInInfo in self.welfareSignInInfos.items():
            self.sendWelfareSignInInfo(welfareType)

        for welfareType in self.welfareLevelInfos.keys():
            self.sendLevelWelfareInfo(welfareType)

    def sendWelfareSignInInfo(self, welfareType):
        LOG_INFO('call sendWelfareSignInInfo', welfareType)
        welfareSignInInfo = self.welfareSignInInfos.get(welfareType, None)
        if not welfareSignInInfo:
            LOG_ERR('call sendWelfareSignInInfo: no welfareType', welfareType)
            return

        if not welfareSignInInfo.welfareSignInDay:
            LOG_INFO('call sendWelfareSignInInfo: not lock')
            return

        if not self.client:
            LOG_INFO('call sendWelfareSignInInfo: no client')
            return

        self.client.onGetWelfareSignInInfo(welfareSignInInfo, welfareType)
        LOG_INFO('call sendWelfareSignInInfo done', welfareSignInInfo)

    def sendLevelWelfareInfo(self, welfareType):
        LOG_INFO('call sendLevelWelfareInfo', welfareType)
        if welfareType not in self.welfareLevelInfos:
            LOG_ERR('call sendLevelWelfareInfo: no welfareType', welfareType)
            return
        
        if not self.client:
            LOG_INFO('call sendLevelWelfareInfo: no client')
            return

        welfareLevelInfo = self.welfareLevelInfos[welfareType]
        self.client.onGetLevelWelfareInfo(welfareLevelInfo, welfareType)
        LOG_INFO('call sendLevelWelfareInfo done', welfareLevelInfo)

    def checkUnlock(self, welfareID):
        uid = WWCONFIG.datas.get(welfareID, {}).get('unlockID', None)
        isUnlock = self._isUIVisibleStr(uid)
        LOG_INFO('call checkUnlock', isUnlock)
        return isUnlock

    def updateWelfareSignIn(self, curTimestamp, welfareType):
        welfareSignInInfo = self.welfareSignInInfos.get(welfareType, None)
        if not welfareSignInInfo:
            LOG_ERR('call updateWelfareSignIn: no welfareType', welfareType)
            return

        if welfareType == "TenSign":
            if welfareType not in WSLCONFIG.maxDayData:
                return
            maxSignInDay = WSLCONFIG.maxDayData[welfareType]
            welfareSignInDay = min(utils.getSvrOpenDays(), maxSignInDay)
            if welfareSignInDay < 0:
                welfareSignInDay = 0
            LOG_INFO('call updateWelfareSignIn: TenSign', welfareSignInDay)
            welfareSignInInfo.welfareSignInDay = welfareSignInDay
        else:
            welfareSignInInfo.welfareSignInDay += 1
        welfareSignInInfo.welfareLastSignInTimestamp = curTimestamp

    def gmUpdateWelfareSignIn(self, flag, welfareType):
        LOG_INFO('call gmUpdateWelfareSignIn', flag, welfareType)
        welfareSignInInfo = self.welfareSignInInfos.get(welfareType, None)
        if not welfareSignInInfo:
            LOG_ERR('call gmUpdateWelfareSignIn: no welfareType', welfareType)
            return False, '未解锁福利签到'


        if not welfareSignInInfo.welfareSignInDay:
            LOG_INFO('call gmUpdateWelfareSignIn, not lock', welfareSignInInfo.welfareSignInDay)
            return False, '未解锁福利签到'

        success = True
        msg = ''
        if not flag:
            welfareSignInInfo.welfareSignInDay = 1
            welfareSignInInfo.welfareLastSignInTimestamp = utils.curTS()
            welfareSignInInfo.welfareSignInData = 0
            LOG_INFO('call gmUpdateWelfareSignIn: reset all', welfareSignInInfo.welfareSignInDay)
            msg = '重置签到天数成功'
        else:
            maxSignInDay = WSLCONFIG.maxKey
            if welfareSignInInfo.welfareSignInDay >= maxSignInDay:
                LOG_INFO('call gmUpdateWelfareSignIn: all signed in', welfareSignInInfo.welfareSignInDay)
                msg ='已经达到最大签到天数'
                success = False
            else:
                self.updateWelfareSignIn(utils.curTS(), welfareType)
                LOG_INFO('call gmUpdateWelfareSignIn: add signin day', welfareSignInInfo.welfareSignInDay)
                msg ='已累增1天'

        self.sendWelfareSignInInfo(welfareType)
        return success, msg
