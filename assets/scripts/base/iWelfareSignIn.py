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
import welfare_serverLogin   as WSLCONFIG
import antiAddictCategory_antiAddictCategory_def as AAC_AACDD

class IWelfareSignIn(object):
    @gamedecorator.checkGameconfigEnable('welfare')
    def reqWelfareSignIn(self, exposed, signInDayNo):
        INFO_MSG('call reqWelfareSignIn')
        if not self.welfareSignInInfo.welfareSignInDay:
            ERROR_MSG('call reqWelfareSignIn: not lock')
            return

        if signInDayNo > self.welfareSignInInfo.welfareSignInDay or signInDayNo <= 0:
            ERROR_MSG('call reqWelfareSignIn: day err', signInDayNo, self.welfareSignInInfo.welfareSignInDay)
            return

        if self.welfareSignInInfo.hasSignIn(signInDayNo):
            ERROR_MSG('call reqWelfareSignIn: alerady sign in', signInDayNo)
            return

        self.welfareSignInInfo.doSignIn(signInDayNo)

        self.sendWelfareSignInInfo()

        if not self.addSignInAward(signInDayNo):
            ERROR_MSG('call reqWelfareSignIn: add award err', signInDayNo)
            return

    def addSignInAward(self, signInDayNo):
        INFO_MSG('call addSignInAward')
        rewardId = WSLCONFIG.datas.get(signInDayNo, {}).get('rewardID', 0)
        if not rewardId:
            ERROR_MSG('call addSignInAward: no reward')
            return False

        awardCtx = self._getAvatarAwardCtx(rewardId, None)
        detail = gameclass.AwardDetail(signInDayNo=signInDayNo)
        opUUID = KBEngine.genUUID64()
        self.addAwards(AAC_AACDD.datas.BONUS_SRC_WELFARE_SIGN_IN, rewardId, 1, opUUID, detail, awardCtx)
        return True

    def welfareSignInOnLogin(self):
        INFO_MSG('call welfareSignInOnLogin')
        self.checkAndUnlockWelfareSignIn(updateFlag = True)
        self.checkAndUpdateWelfareSignIn(updateFlag = False)

    def checkAndUnlockWelfareSignIn(self, updateFlag = True, offsetSeconds = gameconst.COMMON_CYCLE_TIME):
        INFO_MSG('call checkAndUnlockWelfareSignIn')
        if self.welfareSignInInfo.welfareSignInDay:
            INFO_MSG('call checkAndUnlockWelfareSignIn, already lock', self.welfareSignInInfo.welfareSignInDay)
            return
        if not self.checkUnlock():
            INFO_MSG('call checkAndUnlockWelfareSignIn: can not lock')
            return
        self.onWelfareSignInUpdate(updateFlag, offsetSeconds)

    def checkAndUpdateWelfareSignIn(self, updateFlag = True, offsetSeconds = gameconst.COMMON_CYCLE_TIME):
        INFO_MSG('call checkAndUpdateWelfareSignIn')
        if not self.welfareSignInInfo.welfareSignInDay:
            INFO_MSG('call checkAndUpdateWelfareSignIn, not lock', self.welfareSignInInfo.welfareSignInDay)
            return
        self.onWelfareSignInUpdate(updateFlag, offsetSeconds)

    def onWelfareSignInUpdate(self, updateFlag, offsetSeconds):
        INFO_MSG('call onWelfareSignInUpdate',updateFlag, offsetSeconds)
        maxSignInDay = WSLCONFIG.maxKey
        if self.welfareSignInInfo.welfareSignInDay >= maxSignInDay:
            INFO_MSG('call onWelfareSignInUpdate: all signed in', self.welfareSignInInfo.welfareSignInDay)
            return

        newDaySignIn = updateFlag
        curTimestamp = utils.getNow()
        if not updateFlag:
            newDaySignIn = utils.isDiffDay(curTimestamp, self.welfareSignInInfo.welfareLastSignInTimestamp, offsetSeconds)

        if not newDaySignIn:
            INFO_MSG('call onWelfareSignInUpdate: alerady signed in today', self.welfareSignInInfo.welfareLastSignInTimestamp)
            return

        self.updateWelfareSignIn(curTimestamp)

        self.sendWelfareSignInInfo()

    def sendWelfareSignInInfo(self):
        INFO_MSG('call sendWelfareSignInInfo')
        if not self.welfareSignInInfo.welfareSignInDay:
            INFO_MSG('call sendWelfareSignInInfo: not lock')
            return

        if not self.client:
            INFO_MSG('call sendWelfareSignInInfo: no client')
            return

        self.client.onGetWelfareSignInInfo(self.welfareSignInInfo)
        INFO_MSG('call sendWelfareSignInInfo done', self.welfareSignInInfo)

    def checkUnlock(self):
        uid = WWCONFIG.datas.get(1, {}).get('unlockID', None)
        isUnlock = self._isUIVisibleStr(uid)
        INFO_MSG('call checkUnlock', isUnlock)
        return isUnlock

    def updateWelfareSignIn(self, curTimestamp):
        self.welfareSignInInfo.welfareSignInDay += 1
        self.welfareSignInInfo.welfareLastSignInTimestamp = curTimestamp

    def gmUpdateWelfareSignIn(self, flag):
        DEBUG_MSG('call gmUpdateWelfareSignIn', flag)

        if not self.welfareSignInInfo.welfareSignInDay:
            DEBUG_MSG('call gmUpdateWelfareSignIn, not lock', self.welfareSignInInfo.welfareSignInDay)
            return False, '未解锁福利签到'

        success = True
        msg = ''
        if not flag:
            self.welfareSignInInfo.welfareSignInDay = 1
            self.welfareSignInInfo.welfareLastSignInTimestamp = utils.getNow()
            self.welfareSignInInfo.welfareSignInData = 0
            DEBUG_MSG('call gmUpdateWelfareSignIn: reset all', self.welfareSignInInfo.welfareSignInDay)
            msg = '重置签到天数成功'
        else:
            maxSignInDay = WSLCONFIG.maxKey
            if self.welfareSignInInfo.welfareSignInDay >= maxSignInDay:
                DEBUG_MSG('call gmUpdateWelfareSignIn: all signed in', self.welfareSignInInfo.welfareSignInDay)
                msg ='已经达到最大签到天数'
                success = False
            else:
                self.updateWelfareSignIn(utils.getNow())
                DEBUG_MSG('call gmUpdateWelfareSignIn: add signin day', self.welfareSignInInfo.welfareSignInDay)
                msg ='已累增1天'

        self.sendWelfareSignInInfo()
        return success, msg
